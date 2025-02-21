db = db.getSiblingDB('honeypot');

db.createUser({
  user: "honeypot_user",
  pwd: "honeypot_password",
  roles: [
    { role: "readWrite", db: "honeypot" },
    { role: "clusterMonitor", db: "admin" }
  ]
});