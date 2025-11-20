
APP_DIR="/home/ubuntu/my-packing-buddy"
VENV_DIR="$APP_DIR/venv"
SOCK_FILE="$APP_DIR/myproject.sock"
GUNICORN_WORKERS=3
GUNICORN_APP="wsgi:app"
NGINX_SITE_CONF="/etc/nginx/sites-available/my-packing-buddy"

echo "Activating virtual environment"
source "$VENV_DIR/bin/activate"


 Step 2: Kill any old Gunicorn processes

echo "Stopping old Gunicorn processes"
pkill gunicorn || true

echo "Starting Gunicorn"
$VENV_DIR/bin/gunicorn --workers $GUNICORN_WORKERS --bind unix:$SOCK_FILE $GUNICORN_APP &

sleep 3

echo "Fixing permissions"
chmod 777 "$SOCK_FILE"
chmod +x /home/ubuntu
chmod +x "$APP_DIR"


echo "Testing Nginx configuration"
sudo nginx -t


echo "Restarting Nginx..."
sudo systemctl restart nginx
 Step 7: Test local connection
echo "Testing application via localhost"
curl -I http://localhost

echo "Deployment script finished!"

