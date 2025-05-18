# Use Node base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Expose port (same as in your app)
EXPOSE 3000

# Start the app
CMD ["node", "index.js"]
