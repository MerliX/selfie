cd /selfie/src

if [ ! -f /data/base.db ]; then
    python recreate_db.py
fi

cat >/etc/nginx/conf.d/default.conf <<EOL
upstream selfie {
    server 127.0.0.1:8080 fail_timeout=0;
}

server {
    listen       80;
    server_name  ${http_host};

    client_max_body_size  5M;
    keepalive_timeout     5;

    location /static/ {
        root  /selfie/;
    }

    location /selfies/ {
        root  /data/;
    }

    location ~ ^/(favicon|apple-touch-icon|mstile|browserconfig).*\.(png|ico|xml)$ {
        root /selfie/static/favicons/;
    }

    location / {
        proxy_set_header Host       ${http_host};
        proxy_redirect         off;
        proxy_connect_timeout  15;
        proxy_read_timeout     15;
        proxy_pass             http://selfie;
    }
}
EOL

nginx & python selfie.py