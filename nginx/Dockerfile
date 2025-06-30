FROM nginx:1.25.4-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN rm -rf /usr/share/nginx/html/*

# Создаем символические ссылки для правильных путей
RUN mkdir -p /app/static && \
    mkdir -p /app/media && \
    ln -s /usr/share/nginx/html /frontend_static && \
    chown -R nginx:nginx /app && \
    chmod -R 755 /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
