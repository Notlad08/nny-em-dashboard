FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Install nginx
RUN apk add --no-cache nginx

# Copy nginx config (main config file, removes default)
COPY nginx.conf /etc/nginx/nginx.conf

# Remove any default conf.d files
RUN rm -rf /etc/nginx/conf.d/*

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
