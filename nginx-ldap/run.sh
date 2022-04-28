#!/bin/sh

# nginx config variable injection
envsubst < nginx-ldap.conf > /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"