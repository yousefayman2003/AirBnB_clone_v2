#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment

# Install Nginx
apt-get -y update
apt-get -y install nginx

# Create folders
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file
echo "Its Working!!" > /data/web_static/releases/test/index.html

# Create symbolic link
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership
chown -hR ubuntu:ubuntu /data/

# Update nginx configuration
NEW="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sed -i "38i $NEW" /etc/nginx/sites-available/default

# Restart nginx
service nginx restart
