1. Copy your app to the server

From your local machine:

scp -r /path/to/my-packing-buddy ubuntu@your_droplet_ip:/home/ubuntu/


-r → copies directories recursively

Make sure the venv is on the server, or you’ll create a new one there.

2. SSH into the server
ssh ubuntu@your_droplet_ip
cd /home/ubuntu/my-packing-buddy
----------------------------------
sudo apt update
sudo apt install python3.12-venv -y
--------------------------------------
3. Set up virtual environment (if not copied)
python3 -m venv venv
source venv/bin/activate
sudo apt update
sudo apt install pkg-config default-libmysqlclient-dev build-essential -y

pip install -r requirements.txt

----------------------------------------------------------------------------------------------
1. Gunicorn systemd service
gunicorn --bind 0.0.0.0:5000 wsgi:app
Create a systemd service file:

gunicorn --bind 0.0.0.0:5000 wsgi:app(to test that booting works)

sudo nano /etc/systemd/system/my-packing-buddy.service
 this:

[Unit]
Description=Gunicorn instance to serve my-packing-buddy
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/my-packing-buddy
Environment="PATH=/home/ubuntu/my-packing-buddy/venv/bin"
ExecStart=/home/ubuntu/my-packing-buddy/venv/bin/gunicorn \
          --workers 3 --bind unix:/home/ubuntu/my-packing-buddy/myproject.sock wsgi:app

[Install]
WantedBy=multi-user.target


Enable & start it:

sudo systemctl daemon-reload
sudo systemctl start my-packing-buddy
sudo systemctl enable my-packing-buddy
sudo systemctl status my-packing-buddy

2. Nginx Configuration

Create Nginx site config:

sudo nano /etc/nginx/sites-available/my-packing-buddy


Paste:

server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/my-packing-buddy/myproject.sock;
    }
}


Enable the site:

sudo ln -s /etc/nginx/sites-available/my-packing-buddy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

3. Permissions (safer than 777)
sudo chown -R ubuntu:www-data /home/ubuntu/my-packing-buddy
sudo chmod 750 /home/ubuntu/my-packing-buddy
sudo chmod 660 /home/ubuntu/my-packing-buddy/myproject.sock

4.Firewall
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status

5. Optional: SSL (HTTPS)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com

6. Testing
curl -I http://localhost
curl -I http://your_domain_or_IP
