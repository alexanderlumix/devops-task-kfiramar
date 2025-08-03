#!/bin/bash

echo "=== MongoDB Replica Set Assignment Test ==="
echo
echo "This script demonstrates the complete workflow with the new solution:"
echo

echo "1. Start MongoDB cluster with authentication enabled from the beginning:"
echo "   docker compose -f mongo/docker-compose.yml up -d"
echo

echo "2. Wait for containers to be healthy (about 30-60 seconds)"
echo "   docker compose -f mongo/docker-compose.yml ps"
echo

echo "3. Initialize replica set using Python script:"
echo "   cd scripts && python init_mongo_servers.py && cd .."
echo

echo "4. Check replica set status:"
echo "   cd scripts && python check_replicaset_status.py && cd .."
echo

echo "5. Create application user:"
echo "   cd scripts && python create_app_user.py && cd .."
echo

echo "6. Run Node.js app to create products (run twice):"
echo "   docker run --rm --network devops-task-kfiramar_default -v $(pwd)/app-node:/app -w /app node:18-alpine node create_product.js"
echo "   docker run --rm --network devops-task-kfiramar_default -v $(pwd)/app-node:/app -w /app node:18-alpine node create_product.js"
echo

echo "7. Run Go app to read products:"
echo "   docker compose -f mongo/docker-compose.yml run --rm app-go"
echo

echo "=== Key differences from original configuration ==="
echo "- Single root user (root/root) across all nodes"
echo "- Bridge networking with port mapping (works on macOS/Windows/Linux)"
echo "- Service names in HAProxy config and connection strings"
echo "- Keyfile present from first startup allowing MONGO_INITDB_ROOT_* to work"
echo "- Improved health checks that handle 'NotYetInitialized' state"