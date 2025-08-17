FROM node:18-alpine

WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm install --legacy-peer-deps || yarn || true

COPY . /app
EXPOSE 3000
ENV PORT=3000
CMD ["npm","run","dev"]
