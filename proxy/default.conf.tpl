server{
  listen ${LISTEN_PORT};
  add_header 'Access-Control-Allow-Origin' '*';

  location /static {
    alias /vol/static;
  }

  location / {
    uwsgi_pass               ${APP_HOST}:${APP_PORT};
    include                  /etc/nginx/uwsgi_params;
    client_max_body_size     100M;
  }
}
