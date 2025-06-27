FROM nginx:latest

# Copy the Nginx configuration file
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Remove log files to prevent them from being written to the container
RUN rm -f /var/log/nginx/access.log /var/log/nginx/error.log
