# init_mongo_servers_noauth.py
import pymongo
import yaml
import sys
import time

CONFIG_FILE = 'mongo_servers.yml'

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def test_connection_noauth(host, port):
    uri = f"mongodb://{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"Connected to {host}:{port} successfully (no auth).")
        client.close()
        return True
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {e}")
        return False

def init_replica_set(host, port):
    uri = f"mongodb://{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        rs_config = {
            '_id': 'rs0',
            'members': [
                {'_id': 0, 'host': '127.0.0.1:27030'},
                {'_id': 1, 'host': '127.0.0.1:27031'},
                {'_id': 2, 'host': '127.0.0.1:27032'},
            ]
        }
        try:
            result = client.admin.command('replSetInitiate', rs_config)
            print(f"Replica set initiated successfully: {result}")
            
            # Wait for replica set to stabilize
            print("Waiting for replica set to stabilize...")
            time.sleep(10)
            
            # Create admin users after replica set is initialized
            print("Creating admin users...")
            create_admin_users(client)
            
        except Exception as e:
            if 'already initialized' in str(e):
                print("Replica set already initialized.")
            else:
                print(f"Replica set initiation error: {e}")
                raise
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {e}")
        exit(1)
    finally:
        client.close()

def create_admin_users(client):
    config = load_config(CONFIG_FILE)
    for idx, server in enumerate(config['servers']):
        user = server['user']
        password = server['password']
        try:
            client.admin.command(
                'createUser',
                user,
                pwd=password,
                roles=['root']
            )
            print(f"Created admin user: {user}")
        except Exception as e:
            if 'already exists' in str(e):
                print(f"User {user} already exists")
            else:
                print(f"Error creating user {user}: {e}")

def main():
    config = load_config(CONFIG_FILE)
    
    # Test connections without auth
    print("Testing connections...")
    for server in config['servers']:
        test_connection_noauth(server['host'], server['port'])
    
    # Initialize replica set on first server
    print("\nInitializing replica set...")
    init_replica_set(config['servers'][0]['host'], config['servers'][0]['port'])

if __name__ == '__main__':
    main()