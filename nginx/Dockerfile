FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY wait-for-it.sh /wait-for-it.sh
RUN apk add --no-cache curl
ENV INTERNAL_TOKEN=${INTERNAL_TOKEN}