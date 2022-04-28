FROM nginx:1.21.6

# Install apache2-utils to get htpasswd command
RUN apt-get update -y && apt-get install -y apache2-utils && rm -rf /var/lib/apt/lists/*

# Basic auth credentials
ENV BASIC_USERNAME=redis
ENV BASIC_PASSWORD=password

# Forward host and foward port as env variables
# google.com is used as a placeholder, to be replaced using environment variables
ENV FORWARD_HOST=redis-insight
ENV FORWARD_PORT=8001

# Nginx config file
WORKDIR /
COPY nginx-basic-auth.conf nginx-basic-auth.conf

# Startup script
COPY run.sh ./
RUN chmod 0755 ./run.sh
CMD [ "./run.sh" ]