#docker build -t reverse-proxy .
#docker run --rm --name reverse-proxy-container -p 8000:8000 reverse-proxy
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf