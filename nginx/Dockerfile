FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#COPY ./certbot/www /var/www/certbot/
#COPY ssl/my-site.crt /etc/ssl/certs/my-site.crt
#COPY ssl/my-site.key /etc/ssl/private/my-site.key


# COPY /etc/letsencrypt/ssl/fullchain.pem /etc/nginx/ssl/fullchain  
# COPY /etc/letsencrypt/ssl/privkey.pem /etc/nginx/ssl/privkey

# COPY /etc/nginx/snippets/self-signed.conf /etc/nginx/snippets/self-signed.conf 
# COPY /etc/nginx/snippets/ssl-params.conf /etc/nginx/snippets/ssl-params.conf 

#  ssh -i C:\Users\Lumberjack\Downloads\lumberjack_key.pem azureuser@20.115.97.168
