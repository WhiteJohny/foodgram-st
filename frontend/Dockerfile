FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Копируем результат в общий том
CMD ["sh", "-c", "cp -r /app/build/* /app/build_volume/"]
