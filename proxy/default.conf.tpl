server{
  listen ${LISTEN_PORT};
  server_name _;
  location /static {
    alias /vol/static;
    add_header 'Access-Control-Allow-Origin' '*';
  }

  location / {
    uwsgi_pass               ${APP_HOST}:${APP_PORT};
    include                  /etc/nginx/uwsgi_params;
    client_max_body_size     100M;
  }
}

server{
  listen 443 ssl;
  server_name _;
  ssl_certificate /etc/nginx/certs/ser.pem;
  ssl_certificate_key /etc/nginx/certs/ser.key;
  location /static {
    alias /vol/static;
    add_header 'Access-Control-Allow-Origin' '*';
  }

  location / {
    uwsgi_pass               ${APP_HOST}:${APP_PORT};
    include                  /etc/nginx/uwsgi_params;
    client_max_body_size     100M;
  }
}
