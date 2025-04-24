Enhanced Product Requirements Document (PRD) for Scalable Video/Photo-Sharing Platform
1. Project Overview
This project entails designing and deploying a scalable, cloud-native web application for sharing videos and photos, inspired by platforms like Instagram. Developed using Django and hosted on Microsoft Azure, the platform supports two user roles: creators, who upload content with metadata, and consumers, who browse, search, view, comment, and rate content. The focus is on robust functionality and scalability, utilizing Azure’s free-tier services, with minimal emphasis on elaborate UI/UX design.

1.1 Goals
Build a Django-based web application with a REST API for seamless frontend-backend communication.
Implement secure, role-based user authentication and authorization using Django’s authentication system.
Leverage Azure services: PostgreSQL for relational data, Blob Storage for media files, and Cache for Redis for performance optimization.
Deploy the application on Azure App Service (free tier) to ensure scalability and cost-efficiency.
Produce a 13-slide presentation and a 5-minute demonstration video highlighting the application’s functionality, scalability, and cloud integration.
1.2 Non-Goals
Elaborate UI/UX design; functional HTML templates with basic CSS suffice.
Public creator signup; creators are managed exclusively via the Django admin interface.
Advanced features such as content editing, real-time notifications, or social media sharing.
1.3 User Experience Expectations
Creators: Expect a simple, intuitive form to upload videos/photos and enter metadata (e.g., title, caption, location, people present), with immediate feedback on upload success.
Consumers: Expect an easy-to-navigate interface for browsing paginated content, searching by keywords, viewing media details, and submitting comments/ratings, with smooth performance under load.
Scalability: The platform must maintain responsiveness with at least 100 concurrent users, ensuring no noticeable latency in content loading or interactions.
2. Functional Requirements
2.1 User Authentication and Roles
Custom User Model:
Extend Django’s AbstractUser with a role field (choices: ‘creator’, ‘consumer’).
Include fields: username, email, password, role, date_joined.
Signup and Login:
Consumers: Self-register via a form requiring username, email, and password; login with username and password.
Creators: Added manually by an admin through the Django admin panel; no public signup.
Role-Based Permissions:
Creators: Upload and view their own content.
Consumers: Browse, search, view all content, and add comments/ratings.
Interface: Basic HTML forms with Bootstrap for minimal styling (e.g., buttons, input fields).
2.2 Core Data Models
MediaContent:
Fields:
creator (ForeignKey to User, limit to ‘creator’ role),
file (FileField, max upload size 50MB, formats: .jpg, .png, .mp4),
title (CharField, max_length=100),
caption (TextField, max_length=500, optional),
location (CharField, max_length=100, optional),
people_present (TextField, max_length=200, optional),
upload_date (DateTimeField, auto_now_add=True),
is_active (BooleanField, default=True).
Comment:
Fields:
user (ForeignKey to User, limit to ‘consumer’ role),
media (ForeignKey to MediaContent),
text (TextField, max_length=300),
created_at (DateTimeField, auto_now_add=True).
Rating:
Fields:
user (ForeignKey to User, limit to ‘consumer’ role),
media (ForeignKey to MediaContent),
score (IntegerField, range 1-5, validated),
created_at (DateTimeField, auto_now_add=True).
Database: Use SQLite locally for development; migrate to Azure PostgreSQL for production.
2.3 Creator Features
Upload Interface:
Form fields: File upload, title (required), caption, location, people present (all optional).
Validation: Ensure file type and size constraints; display error messages on failure.
View Uploads:
Paginated list (10 items/page) of the creator’s content, showing title, upload date, and a thumbnail/link.
Access Control: Restricted to ‘creator’ role via Django decorators.
2.4 Consumer Features
Browse Content:
Paginated list (10 items/page) of all active MediaContent, ordered by upload_date (newest first).
Display: Thumbnail, title, creator username, upload date.
Search:
Search by keywords in title, caption, or location; case-insensitive, partial matches supported.
Results paginated, with “No results” message if empty.
View Details:
Full media display (image/video player), metadata, average rating, and all comments.
Interact:
Comment form: Text input (max 300 chars), submit button.
Rating form: Dropdown (1-5), submit button; one rating per user per media item.
Access Control: Restricted to ‘consumer’ role for interactions.
2.5 REST API
Endpoints:
/api/media/:
GET: List all MediaContent (paginated, 10/page).
POST: Create MediaContent (creators only, requires file and title).
/api/media/<id>/: GET: Retrieve single MediaContent with metadata, comments, ratings.
/api/comments/: POST: Add comment (consumers only, requires text and media ID).
/api/ratings/: POST: Add rating (consumers only, requires score and media ID).
Authentication: Use Django REST Framework’s TokenAuthentication; tokens generated post-login.
Response Format: JSON, with status codes (200, 201, 400, 403, 404).
Testing Interface: Simple HTML page with JavaScript (fetch API) to test endpoints.
2.6 Scalability and Cloud Integration
Database: Azure PostgreSQL (free tier, 1GB storage, 10 connections).
Storage: Azure Blob Storage (free tier, 5GB) for media files, with public read access for serving content.
Caching: Azure Cache for Redis (free tier, 250MB) to cache media lists and detail pages.
Deployment: Azure App Service (free tier, 1GB memory, 60 minutes compute/day).
3. Technical Requirements
Framework: Django 4.2.x (latest stable version at development start).
Apps:
core: Handles models, views, and API logic.
users: Manages authentication and user models.
Database:
Development: SQLite 3.x.
Production: Azure PostgreSQL 15.x.
Dependencies:
djangorestframework (3.14.x) for API.
psycopg2-binary (2.9.x) for PostgreSQL.
django-storages (1.13.x) and azure-storage-blob (12.19.x) for Blob Storage.
django-redis (5.4.x) for caching.
gunicorn (22.0.x) for production server.
API: Built with Django REST Framework, supporting token-based authentication.
Deployment: Azure App Service with Gunicorn, configured via Azure CLI.
Testing: Use Django’s TestCase and DRF’s APITestCase for unit/integration tests.
4. Non-Functional Requirements
Performance:
Page load time < 2 seconds for up to 100 concurrent users.
API response time < 500ms under normal load.
Security:
Passwords hashed with Django’s PBKDF2 (SHA256).
HTTPS enforced on Azure deployment.
Role-based access control enforced at view and API levels.
Scalability:
Handle 100 concurrent users with no downtime.
Scale media storage seamlessly via Blob Storage.
Usability:
Forms include inline validation and error messages.
Navigation via a top bar with links (e.g., Home, Upload, Login).
Maintainability:
Code follows PEP 8 style guidelines.
Include docstrings for all models, views, and serializers.
Unit tests cover 80% of core functionality.
5. Constraints and Assumptions
Constraints:
Azure free-tier limits: 5GB Blob Storage, 1GB PostgreSQL, 250MB Redis, 60 minutes App Service compute/day.
Development on Windows; all commands must be Windows-compatible.
Assumptions:
Users have modern browsers (Chrome, Firefox, Edge) supporting HTML5 video.
No need for mobile responsiveness; desktop focus only.
Internet speed of at least 5Mbps for smooth media uploads/views.