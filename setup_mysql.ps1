# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Green
pip install -r requirements.txt

# Make migrations
Write-Host "Creating database migrations..." -ForegroundColor Green
python manage.py makemigrations

# Apply migrations
Write-Host "Applying migrations to MySQL database..." -ForegroundColor Green
python manage.py migrate

# Create superuser (optional)
$createSuperuser = Read-Host "Would you like to create a superuser? (y/n)"
if ($createSuperuser -eq "y") {
    python manage.py createsuperuser
}

Write-Host "MySQL database setup complete!" -ForegroundColor Green 