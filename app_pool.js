const express = require('express');
const betterSqlite3 = require('better-sqlite3');// optimize the database usage, not really pool
const path = require('path');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Connect to the SQLite database using better-sqlite3
const db = betterSqlite3('./users.db', { verbose: console.log });

// Middleware for parsing the request body
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve the HTML login page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// Handle authentication requests
app.post('/auth', (req, res) => {
  const { username, password } = req.body;

  console.log(`Received data: username=${username}, password=${password}`);

  try {
    // Use parameterized queries to securely query the database
    const query = `SELECT * FROM users WHERE username = ? AND password = ?`;
    const stmt = db.prepare(query);
    const user = stmt.get(username, password); // Execute the query

    if (user) {
      res.status(200).send('Authentication successful!');
    } else {
      res.status(401).send('Invalid credentials');
    }
  } catch (err) {
    console.error('Database query error:', err.message);
    res.status(500).send('Server error');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
