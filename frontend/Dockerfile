# Use official Node.js image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project files into the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8000

# Command to run the development server
CMD ["npm", "run", "serve", "--", "--port", "8000"]
