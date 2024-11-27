const fs = require('fs');

fs.access('./users.db', fs.constants.R_OK | fs.constants.W_OK, (err) => {
  if (err) {
    console.error('Non hai i permessi necessari per accedere al database');
  } else {
    console.log('Hai i permessi di lettura e scrittura sul database');
  }
});
