#! /usr/bin/env bash
set -e

USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}

echo "client_max_body_size $USE_NGINX_MAX_UPLOAD;" > /etc/nginx/conf.d/upload.conf


USE_STATIC_URL=${STATIC_URL:-'/static'}
USE_STATIC_PATH=${STATIC_PATH:-'/var/inform/static'}

USE_LISTEN_PORT=${LISTEN_PORT:-80}

echo "server {
    listen ${USE_LISTEN_PORT};
    location / {
        try_files \$uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    location $USE_STATIC_URL {
        alias $USE_STATIC_PATH;
    }" > /etc/nginx/conf.d/nginx.conf

if [[ $STATIC_INDEX == 1 ]] ; then 
echo "    location = / {
        index $USE_STATIC_URL/index.html;
    }" >> /etc/nginx/conf.d/nginx.conf
fi

echo "}" >> /etc/nginx/conf.d/nginx.conf

exec "$@"