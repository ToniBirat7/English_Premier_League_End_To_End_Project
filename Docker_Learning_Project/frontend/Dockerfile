FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variable to avoid opening browser
ENV BROWSER=none

# Start the development server
CMD ["npm", "start"]
