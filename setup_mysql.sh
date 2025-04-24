#!/bin/bash

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Make migrations
echo "Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations to MySQL database..."
python manage.py migrate

# Create superuser (optional)
echo "Would you like to create a superuser? (y/n)"
read create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo "MySQL database setup complete!" 