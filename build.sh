#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Upgrade pip FIRST so it can handle modern packages
python -m pip install --upgrade pip

# 2. Install your project requirements
pip install -r requirements.txt

# 3. Collect static files (Cloudinary needs this)
python manage.py collectstatic --no-input

# 4. Run database migrations
python manage.py migrate