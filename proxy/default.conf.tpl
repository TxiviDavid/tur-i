server{
  listen ${LISTEN_PORT};

  location /static {
    alias /vol/static;
  }

  location / {
    uwsgi_pass               ${APP_HOST}:${APP_PORT};
    include                  /etc/nginx/uwsgi_params;
    client_max_body_size     10M;
    if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, PUT, OPTIONS, POST, DELETE';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-Amz-Date';
            add_header 'Access-Control-Max-Age' 86400;
            add_header 'Content-Type' 'text/html; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    if ($request_method = 'PUT') {
        add_header 'Access-Control-Allow-Methods' 'GET, PUT, OPTIONS, POST, DELETE';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-Amz-Date';
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
    }
    if ($request_method = 'GET') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, PUT, OPTIONS, POST, DELETE';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-Amz-Date';
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
    }
  }
}
