
1. Copy project to server

(Local machine)

scp -r /path/to/my-packing-buddy ubuntu@your_droplet_ip:/home/ubuntu/

2. SSH into server
ssh ubuntu@your_droplet_ip
cd ~/my-packing-buddy

3. Set up virtual environment

This is correct:

sudo apt update
sudo apt install python3.12-venv -y

python3 -m venv venv
source venv/bin/activate


Install MySQL build tools:

sudo apt install pkg-config default-libmysqlclient-dev build-essential -y
pip install -r requirements.txt

4. Test Gunicorn

Good:

gunicorn --bind 0.0.0.0:5000 wsgi:app

5. Create systemd service

Your service is correct.

sudo nano /etc/systemd/system/my-packing-buddy.service


Paste:

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


Enable:

sudo systemctl daemon-reload
sudo systemctl start my-packing-buddy
sudo systemctl enable my-packing-buddy
sudo systemctl status my-packing-buddy

6. Nginx Configuration
sudo apt update
sudo apt install nginx -y


Create:

sudo nano /etc/nginx/sites-available/my-packing-buddy


Paste:

server {
    listen 80;
    server_name YOUR_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/my-packing-buddy/myproject.sock;
    }
}


Enable:

sudo ln -s /etc/nginx/sites-available/my-packing-buddy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

7. Permissions

Here you made small mistakes. Let me correct it.

You wrote:

sudo chmod 750 /home/ubuntu/my-packing-buddy
sudo chmod 660 myproject.sock


These are NOT correct for Gunicorn + Nginx.

Use this instead:
sudo chown -R ubuntu:www-data /home/ubuntu/my-packing-buddy
sudo chmod 755 /home/ubuntu/my-packing-buddy
sudo chmod 766 /home/ubuntu/my-packing-buddy/myproject.sock


Why?

Nginx (www-data) must enter the folder → needs execute bit (x).

The socket must be readable/writable.

8. If 502 Bad Gateway error comes

Yes, parent directory permissions often cause it:

sudo chmod o+x /home
sudo chmod o+x /home/ubuntu
sudo chmod o+x /home/ubuntu/my-packing-buddy


This solves:

connect() to unix:/home/...myproject.sock failed (13: Permission denied)

9. Firewall

Correct:

sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
