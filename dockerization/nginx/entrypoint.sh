#!/bin/sh

# Get certs
certbot certonly -n -d alfahackathon.hopto.org,www.alfahackathon.hopto.org \
  --standalone --preferred-challenges http --email alex.strunskiy@ya.ru --agree-tos --expand

# Kick off cron
/usr/sbin/crond -f -d 8 &

# Start nginx
/usr/sbin/nginx -g "daemon off;"