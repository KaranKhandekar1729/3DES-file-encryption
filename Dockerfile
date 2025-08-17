# Use official Node.js + Python base
FROM node:18-bullseye

# Install Python + pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy package.json first (for caching npm install)
COPY package*.json ./

# Install Node.js deps
RUN npm install

# Copy Python deps
COPY requirements.txt .

# Install Python deps
RUN pip3 install -r requirements.txt

# Copy rest of app
COPY . .

# Railway requires your app to listen on PORT env variable
ENV PORT=3000

# Expose port
EXPOSE 3000

# Run Node app
CMD ["npm", "start"]
