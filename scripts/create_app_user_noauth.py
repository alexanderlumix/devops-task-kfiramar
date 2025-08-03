import pymongo

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27030  # Connect to primary instead
APP_DB = 'appdb'
APP_USER = 'appuser'
APP_PASS = 'appuserpassword'


def create_app_user():
    # Connect without authentication
    uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/?replicaSet=rs0"
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[APP_DB]
    try:
        db.command("createUser", APP_USER,
                   pwd=APP_PASS,
                   roles=[{"role": "readWrite", "db": APP_DB}])
        print(f"User '{APP_USER}' created with readWrite role on database '{APP_DB}'.")
    except pymongo.errors.OperationFailure as e:
        if 'already exists' in str(e):
            print(f"User '{APP_USER}' already exists.")
        else:
            print(f"Failed to create user: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    create_app_user()