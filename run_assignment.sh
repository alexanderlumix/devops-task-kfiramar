#!/bin/bash

# DevOps Assignment Runner Script
# This script runs all the steps needed to complete the assignment

set -e  # Exit on error

echo "=== DevOps Assignment Execution ==="
echo

# Step 1: Launch MongoDB servers
echo "Step 1: Launching MongoDB servers..."
cd mongo
docker compose up -d
echo "Waiting for MongoDB containers to be healthy..."
sleep 20  # Give MongoDB time to start

# Step 2: Initialize replica set
echo
echo "Step 2: Initializing MongoDB replica set..."
cd ../scripts
python3 init_mongo_servers.py

# Step 3: Check replica set status
echo
echo "Step 3: Checking replica set status..."
python3 check_replicaset_status.py

# Step 4: Create application user
echo
echo "Step 4: Creating application user..."
python3 create_app_user.py

# Step 5: Create products with Node.js app
echo
echo "Step 5: Creating products with Node.js app..."
cd ../app-node
npm install
echo "Creating first product..."
node create_product.js
echo "Creating second product..."
node create_product.js

# Step 6: Run Go application to read products
echo
echo "Step 6: Running Go application to read products..."
cd ../app-go
docker compose up -d
echo "Go application is now running and displaying products every 3 seconds."
echo "To see the output, run: docker logs -f product-reader-go"
echo
echo "=== Assignment completed successfully! ==="