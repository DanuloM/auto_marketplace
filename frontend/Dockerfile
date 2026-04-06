FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project
COPY . .

# Expose port
EXPOSE 5174

# Run dev server
CMD ["npx", "vite", "--port", "5174", "--host", "0.0.0.0"]
