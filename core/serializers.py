from rest_framework import serializers
from .models import MediaContent, Comment, Rating
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model (simplified)"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        read_only_fields = ['id', 'username', 'role']

class RatingSerializer(serializers.ModelSerializer):
    """Serializer for the Rating model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'user', 'score', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """Create and return a new rating"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        # Check if the user already rated this media
        try:
            rating = Rating.objects.get(user=user, media_id=media_id)
            rating.score = validated_data['score']
            rating.save()
            return rating
        except Rating.DoesNotExist:
            return Rating.objects.create(
                user=user,
                media_id=media_id,
                **validated_data
            )

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """Create and return a new comment"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        return Comment.objects.create(
            user=user,
            media_id=media_id,
            **validated_data
        )

class MediaContentSerializer(serializers.ModelSerializer):
    """Serializer for the MediaContent model"""
    creator = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaContent
        fields = [
            'id', 'creator', 'file', 'title', 'caption', 'location', 
            'people_present', 'upload_date', 'is_active', 
            'comments', 'ratings', 'average_rating'
        ]
        read_only_fields = ['id', 'creator', 'upload_date', 'comments', 'ratings']
    
    def get_average_rating(self, obj):
        """Calculate the average rating for a media item"""
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return sum(rating.score for rating in ratings) / len(ratings)
    
    def create(self, validated_data):
        """Create and return a new media content item"""
        user = self.context['request'].user
        return MediaContent.objects.create(creator=user, **validated_data)

class MediaContentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing media content"""
    creator = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaContent
        fields = [
            'id', 'creator', 'file', 'title', 'upload_date', 
            'is_active', 'average_rating', 'comment_count'
        ]
        read_only_fields = ['id', 'creator', 'upload_date']
    
    def get_average_rating(self, obj):
        """Calculate the average rating for a media item"""
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return sum(rating.score for rating in ratings) / len(ratings)
    
    def get_comment_count(self, obj):
        """Get the comment count for a media item"""
        return obj.comments.count() 