#!/bin/bash

APP_NAME="MyPackingBuddy"
APP_DIR="$HOME/Documents/my-packing-buddy"
VENV_DIR="$APP_DIR/venv"
BRANCH="main"

echo "Starting deployment for $APP_NAME..."

if [ -d "$APP_DIR" ]; then
  echo "Navigating to project directory..."
  cd $APP_DIR
else
  echo "Project directory not found at $APP_DIR"
  exit 1
fi

echo "Pulling latest changes from Git..."
git pull origin $BRANCH

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Restarting Gunicorn service..."
sudo systemctl stop mypackingbuddy.service 2>/dev/null
sudo systemctl start mypackingbuddy.service
sudo systemctl enable mypackingbuddy.service

echo "Deployment complete! App should be live on port 8000."

