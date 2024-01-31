#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment

# Install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Create folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file
sudo echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' > /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/current /data/web_static/releases/test/

# Give ownership
sudo chown -hR ubuntu:ubuntu /data/

# Update nginx configuration
sudo sed -i '51 i \\n\tlocation /hbnb_static {\n\talias /data/web_static/current;\n\t}' /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
