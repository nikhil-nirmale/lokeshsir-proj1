# # FROM node:20-alpine

# # WORKDIR /app

# # COPY package*.json .

# # RUN npm install

# # COPY . .

# # EXPOSE 5173

# # CMD ["npm","run","dev"]

# # frontend/Dockerfile

# FROM node:18-alpine

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY package*.json ./
# RUN npm install

# # Copy source
# COPY . .

# # Expose port
# EXPOSE 5173

# # Start Vite
# CMD ["npm", "run", "dev", "--", "--host"]


# Use full Node (not Alpine!)
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install
COPY package*.json ./
RUN npm install

# Copy the entire app
COPY . .

# Expose Vite dev port
EXPOSE 5173

# Start Vite dev server with host binding
CMD ["npm", "run", "dev", "--", "--host"]
