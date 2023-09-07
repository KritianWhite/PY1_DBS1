const express = require('express');
const app = express();

// Configuración del servidor
app.set('port', 3000);

app.listen(app.get('port'), () => {
  console.log('Server listening on port ' + app.get('port') + '...');
});
