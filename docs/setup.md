# Production Setup

The following document describes how to set up the application for production.

Assumed is a Debian-based system, but the instructions should be similar for other systems. The application is set up in /var/www/mls. The Python version has to be installed in version 3.12. If not otherwise stated commands have to be executed by root-User.

## Install the Application

```bash
cd to the git directory of mls checkout
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
