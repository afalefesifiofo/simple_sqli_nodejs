const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Crea una connessione al database SQLite
const db = new sqlite3.Database('./users.db');

// Middleware per il parsing dei dati del corpo della richiesta
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve la pagina HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// Endpoint per la gestione del login
app.post('/auth', (req, res) => {
  const { username, password } = req.body;

  // La query è costruita in modo pericoloso, concatenando i valori direttamente
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

  // Esegui la query
  db.get(query, (err, row) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Errore del server');
    }

    if (row) {
      return res.status(200).send('Autenticazione riuscita!');
    } else {
      return res.status(401).send('Credenziali errate');
    }
  });
});

// Avvia il server
app.listen(port, () => {
  console.log(`Server in ascolto su http://localhost:${port}`);
});
