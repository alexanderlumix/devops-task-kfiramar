// Switch to admin database
db = db.getSiblingDB('admin');

// Create admin user using localhost exception
db.createUser({
  user: 'admin',
  pwd: 'adminpassword',
  roles: ['root']
});

print('Admin user created successfully');

// Create server-specific users
db.createUser({user: 'mongo-0', pwd: 'mongo-0', roles: ['root']});
db.createUser({user: 'mongo-1', pwd: 'mongo-1', roles: ['root']});
db.createUser({user: 'mongo-2', pwd: 'mongo-2', roles: ['root']});

print('All users created successfully');