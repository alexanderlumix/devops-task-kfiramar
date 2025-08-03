// Switch to appdb
db = db.getSiblingDB('appdb');

// Create application user
db.createUser({
  user: 'appuser',
  pwd: 'appuserpassword',
  roles: [{role: 'readWrite', db: 'appdb'}]
});

print('Application user created successfully');