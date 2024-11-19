const sqlite3 = require('sqlite3').verbose();

// Crea una connessione al database
const db = new sqlite3.Database('./users.db');

// Crea la tabella "users"
db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");

  // Inserisce alcuni dati di esempio
  const stmt = db.prepare("INSERT INTO users (username, password) VALUES (?, ?)");
  stmt.run("admin", "adminpass");
  stmt.run("user1", "user1pass");
  stmt.finalize();
});

db.close();
