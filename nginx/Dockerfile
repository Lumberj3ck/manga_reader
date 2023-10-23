FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#     listen 443 ssl; # managed by Certbot
#     ssl_certificate /etc/letsencrypt/live/mangalove.site/fullchain.pem; # managed by Certbot
#     ssl_certificate_key /etc/letsencrypt/live/mangalove.site/privkey.pem; # managed by Certbot
#     include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
#     ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

# }
# server {
#     if ($host = mangalove.site) {
#         return 301 https://$host$request_uri;
#     } # managed by Certbot


#     server_name mangalove.site;
#     listen 80;
#     return 404; # managed by Certbot


# }
# ssh -i C:\Users\Lumberjack\Downloads\lumberjack_key.pem azureuser@20.115.97.168