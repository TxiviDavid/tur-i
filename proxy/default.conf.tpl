server{
  listen ${LISTEN_PORT};

  location /static {
    alias /vol/static;
  }

  location / {
    uwsgi_pass               ${APP_HOST}:${APP_PORT};
    include                  /etc/nginx/uwsgi_params;
    client_max_body_size     10M;
    add_header "Access-Control-Allow-Origin" $http_origin;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
    add_header 'Access-Control-Max-Age' 1728000;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    return 200 '{"status": "OK"}';
  }
}
