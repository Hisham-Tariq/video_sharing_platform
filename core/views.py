from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from users.views import creator_required
from .models import MediaContent, Comment, Rating
from .forms import MediaContentForm, CommentForm, RatingForm

# Create your views here.

def home(request):
    """
    Home page view to display the landing page of the application.
    """
    # Get the latest 3 active media items to show as featured content
    featured_media = MediaContent.objects.filter(is_active=True).order_by('-upload_date')[:3]
    return render(request, 'core/home.html', {'featured_media': featured_media})

def media_list(request):
    """
    View to display a paginated list of all active media content
    """
    media_list = MediaContent.objects.filter(is_active=True).order_by('-upload_date')
    paginator = Paginator(media_list, 10)  # Show 10 items per page
    
    page_number = request.GET.get('page', 1)
    media = paginator.get_page(page_number)
    
    return render(request, 'core/list.html', {'media': media})

def media_search(request):
    """
    View to search for media content by keywords in title, caption, or location
    """
    query = request.GET.get('query', '')
    results = []
    
    if query:
        results = MediaContent.objects.filter(
            Q(title__icontains=query) | 
            Q(caption__icontains=query) | 
            Q(location__icontains=query),
            is_active=True
        ).order_by('-upload_date')
    
    paginator = Paginator(results, 10)  # Show 10 items per page
    page_number = request.GET.get('page', 1)
    results_page = paginator.get_page(page_number)
    
    return render(request, 'core/search.html', {
        'query': query,
        'results': results_page
    })

def media_detail(request, pk):
    """
    View to display the details of a specific media item, with comments and ratings
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    comments = media.comments.all().order_by('-created_at')
    
    # Calculate average rating
    avg_rating = media.ratings.aggregate(Avg('score'))['score__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    # Show comment and rating forms only to consumers
    comment_form = None
    rating_form = None
    user_rating = None
    
    if request.user.is_authenticated and hasattr(request.user, 'is_consumer') and request.user.is_consumer:
        comment_form = CommentForm()
        rating_form = RatingForm()
        
        # Check if user has already rated this media
        try:
            user_rating = Rating.objects.get(user=request.user, media=media)
            rating_form = RatingForm(instance=user_rating)
        except Rating.DoesNotExist:
            pass
    
    return render(request, 'core/detail.html', {
        'media': media,
        'comments': comments,
        'avg_rating': avg_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating
    })

@login_required
@creator_required
def upload_media(request):
    """
    View for creators to upload new media content
    """
    if request.method == 'POST':
        form = MediaContentForm(request.POST, request.FILES, creator=request.user)
        if form.is_valid():
            media = form.save()
            messages.success(request, f"'{media.title}' was uploaded successfully!")
            return redirect('core:media_detail', pk=media.pk)
    else:
        form = MediaContentForm(creator=request.user)
    
    return render(request, 'core/upload.html', {'form': form})

@login_required
def add_comment(request, pk):
    """
    View for consumers to add comments to media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can comment
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can add comments.")
        return redirect('core:media_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.media = media
            comment.save()
            messages.success(request, "Your comment was added successfully!")
    
    return redirect('core:media_detail', pk=pk)

@login_required
def add_rating(request, pk):
    """
    View for consumers to rate media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can rate
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can rate content.")
        return redirect('core:media_detail', pk=pk)
    
    if request.method == 'POST':
        # Check if user has already rated this media
        try:
            rating = Rating.objects.get(user=request.user, media=media)
            form = RatingForm(request.POST, instance=rating)
        except Rating.DoesNotExist:
            form = RatingForm(request.POST)
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.media = media
            rating.save()
            messages.success(request, "Your rating was saved successfully!")
    
    return redirect('core:media_detail', pk=pk)

def api_test(request):
    """
    View to render the API test page.
    """
    return render(request, 'core/api_test.html')
