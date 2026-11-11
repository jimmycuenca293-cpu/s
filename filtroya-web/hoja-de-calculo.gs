// Google Apps Script: anota en tu hoja cada pedido y cada pago de la tienda.
// 1) Crea una hoja de cálculo en Google Sheets. 2) Extensiones > Apps Script > pega este código.
// 3) Cambia CLAVE por una palabra secreta (la misma que pones en config.php: 'hoja' => ['clave' => ...]).
// Puedes usar LA MISMA hoja y el mismo correo en todas tus tiendas: en cada config.php pones la misma URL y la misma clave; la columna TIENDA/SITIO dice de cuál es cada pedido.
// 4) Implementar > Nueva implementación > Aplicación web > Ejecutar como: yo · Quién tiene acceso: cualquiera. Copia la URL en config.php ('hoja' => ['url' => ...]).
const CLAVE = 'cambia-esta-clave';
const CORREO = 'tucorreo@gmail.com';   // aquí te llega cada pedido con todos los datos del cliente (además del correo de la tienda)
const COLS = ['fecha', 'tienda', 'sitio', 'pedido', 'estado', 'productos', 'total', 'entrega', 'ciudad', 'nombre', 'celular', 'correo', 'barrio', 'direccion', 'indicaciones', 'modelo', 'recordatorio', 'pago'];

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  if (d.clave !== CLAVE) return ContentService.createTextOutput('clave incorrecta');
  const h = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (h.getLastRow() === 0) h.appendRow(COLS.map(c => c.toUpperCase()));
  const fila = COLS.map(c => d[c] === undefined ? '' : d[c]);
  // Una sola hoja para varias tiendas: la fila se identifica por pedido + sitio, así dos tiendas nunca se pisan
  const colP = COLS.indexOf('pedido') + 1, colS = COLS.indexOf('sitio') + 1;
  let fila_n = 0;
  if (h.getLastRow() > 1) {
    const datos = h.getRange(2, 1, h.getLastRow() - 1, COLS.length).getValues();
    for (let i = datos.length - 1; i >= 0; i--) if (String(datos[i][colP - 1]) === String(d.pedido) && String(datos[i][colS - 1]) === String(d.sitio)) { fila_n = i + 2; break; }
  }
  if (fila_n) h.getRange(fila_n, 1, 1, COLS.length).setValues([fila]);   // el pago actualiza la fila del pedido
  else h.appendRow(fila);
  try {
    const cuerpo = COLS.map(c => c.toUpperCase() + ': ' + (d[c] === undefined ? '' : d[c])).join('\n');
    MailApp.sendEmail(CORREO, '[' + d.tienda + '] ' + (d.tipo === 'pagado' ? 'Nuevo pedido PAGADO ' : 'Nuevo pedido (esperando pago) ') + d.pedido + ' — $' + d.total, cuerpo);
  } catch (e) {}
  return ContentService.createTextOutput('ok');
}
