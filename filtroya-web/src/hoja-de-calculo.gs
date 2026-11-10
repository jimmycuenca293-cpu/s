// Google Apps Script: anota en tu hoja cada pedido y cada pago de la tienda.
// 1) Crea una hoja de cálculo en Google Sheets. 2) Extensiones > Apps Script > pega este código.
// 3) Cambia CLAVE por una palabra secreta (la misma que pones en config.php: 'hoja' => ['clave' => ...]).
// 4) Implementar > Nueva implementación > Aplicación web > Ejecutar como: yo · Quién tiene acceso: cualquiera. Copia la URL en config.php ('hoja' => ['url' => ...]).
const CLAVE = 'cambia-esta-clave';
const COLS = ['fecha', 'tienda', 'sitio', 'pedido', 'estado', 'productos', 'total', 'entrega', 'ciudad', 'nombre', 'celular', 'correo', 'barrio', 'direccion', 'indicaciones', 'modelo', 'recordatorio', 'pago'];

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  if (d.clave !== CLAVE) return ContentService.createTextOutput('clave incorrecta');
  const h = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (h.getLastRow() === 0) h.appendRow(COLS.map(c => c.toUpperCase()));
  const fila = COLS.map(c => d[c] === undefined ? '' : d[c]);
  const ref = d.pedido, col = COLS.indexOf('pedido') + 1;
  const hallado = h.getLastRow() > 1 ? h.getRange(2, col, h.getLastRow() - 1, 1).createTextFinder(ref).matchEntireCell(true).findNext() : null;
  if (hallado) h.getRange(hallado.getRow(), 1, 1, COLS.length).setValues([fila]);   // el pago actualiza la fila del pedido
  else h.appendRow(fila);
  return ContentService.createTextOutput('ok');
}
