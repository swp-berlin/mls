# Production Setup

The following document describes how to set up the application for production.

Assumed is a Debian-based system, but the instructions should be similar for other systems. The application is set up in /var/www/mls. The Python version has to be installed in version 3.12. If not otherwise stated commands have to be executed by root-User.

## Install the Application

```bash
cd /var/www/mls
git submodule update --init
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chown -R www-data:www-data .
```

## Set up the Application
1. Reconfigure systemd service:
   - ExecStart: adjust path to python environment and uwsgi.ini

3. Reconfigure the following uWSGI parameters:
   - chdir: git directory of mls checkout
   - http-socket: ip address and port to bind to

# Restrict access to mls service port
You should restrict access to the service to certain internal ip addresses, for example by installing a reverse proxy in front of the application.

- sample nginx_site_config.conf:
  ```
  server {
    server_name mls.swp.cosmoco.de;
    listen 443 ssl;
    listen [::]:443 ssl;
    client_max_body_size 500M;

    location / {
        allow 10.1.0.0/24;
        deny all;
        proxy_pass http://INTERNAL_IP_ADDRESS:8080;
        proxy_set_header Host $server_name;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
  }
  ```

## Set up and start the services
1. Link and activate MLS service
  ```bash
  ln -s conf/mls.service /etc/systemd/system/
  systemctl enable mls.service
  systemctl edit mls.service
  ```
2. Override/Adjust environment for mls.service
  ```
  [Service]
  Environment=ALLOWED_HOST="mls.swp.cosmoco.de"
  Environment=ENVIRONMENT="production"
  Environment=SECRET_KEY="YOUR_SECRET_KEY"
  ```
3. Start MLS Service
  ```bash
  systemctl start mls.service
  ```
