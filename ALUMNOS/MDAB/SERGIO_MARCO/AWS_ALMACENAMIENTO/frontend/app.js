function showTab(name, btn) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  btn.classList.add('active');
  if (name === 'map' && !window._mapInit) initMap();
}

function initMap() {
  window._mapInit = true;
  window._map = L.map('map').setView([40.416775, -3.703790], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(window._map);
  window._markers   = {};
  window._polylines = {};
  updateMap();
  setInterval(updateMap, 3000);
}

async function updateMap() {
  try {
    const routes = await apiFetch('/api/routes/active');
    Object.values(window._markers).forEach(m => m.remove());
    Object.values(window._polylines).forEach(p => p.remove());
    window._markers = {}; window._polylines = {};

    routes.forEach(r => {
      const origin = [r.origen.lat,  r.origen.lng];
      const actual = [r.actual.lat,  r.actual.lng];
      const dest   = [r.destino.lat, r.destino.lng];

      if (actual[0] == null || actual[1] == null) return;

      window._markers[r.id] = L.marker(actual)
        .addTo(window._map)
        .bindPopup('<b>Ruta #' + r.id + '</b><br>Vehículo: ' + r.vehiculo_id);

      window._polylines[r.id] = L.polyline(
        [origin, actual, dest],
        { color: '#1a237e', weight: 2, dashArray: '6,4' }
      ).addTo(window._map);
    });
  } catch (e) { console.error('Map update error:', e); }
}

async function apiFetch(url, opts = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...opts });
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

function formToObj(form) {
  return Object.fromEntries(new FormData(form).entries());
}

async function loadAlerts() {
  const data   = await apiFetch('/api/alerts');
  const total  = data.itv.length + data.sobrecarga.length;
  const badge  = document.getElementById('alert-badge');
  const list   = document.getElementById('alerts-list');

  badge.style.display = total ? 'inline' : 'none';
  document.getElementById('alert-count').textContent = total;

  if (!total) { list.innerHTML = '<em style="color:green">Sin alertas activas</em>'; return; }

  list.innerHTML =
    data.itv.map(a =>
      '<div class="alert-item">&#9888; <b>ITV próxima:</b> ' + a.matricula + ' — vence el ' + a.fecha_itv + '</div>'
    ).join('') +
    data.sobrecarga.map(a =>
      '<div class="alert-item overload">&#128680; <b>Sobrecarga:</b> Ruta #' + a.ruta_id + ' (' + a.matricula + ') — ' + a.total_peso + ' kg / ' + a.capacidad + ' kg cap.</div>'
    ).join('');
}

async function loadConductores() {
  const data = await apiFetch('/api/conductores');
  document.getElementById('tbody-conductores').innerHTML = data.map(c =>
    '<tr><td>' + c.id + '</td><td>' + c.dni + '</td><td>' + c.nombre + '</td><td>' + (c.telefono||'—') + '</td>' +
    '<td><button class="del" onclick="deleteConductor(' + c.id + ')">Eliminar</button></td></tr>'
  ).join('');
}

async function createConductor(e) {
  e.preventDefault();
  await apiFetch('/api/conductores', { method: 'POST', body: JSON.stringify(formToObj(e.target)) });
  e.target.reset(); loadConductores();
}

async function deleteConductor(id) {
  if (!confirm('¿Eliminar conductor?')) return;
  await apiFetch('/api/conductores/' + id, { method: 'DELETE' }); loadConductores();
}

async function loadVehiculos() {
  const data = await apiFetch('/api/vehiculos');
  document.getElementById('tbody-vehiculos').innerHTML = data.map(v =>
    '<tr><td>' + v.id + '</td><td>' + v.matricula + '</td><td>' + v.modelo + '</td>' +
    '<td>' + v.capacidad_carga_kg + ' kg</td><td>' + v.fecha_itv + '</td><td>' + v.estado + '</td>' +
    '<td><button class="del" onclick="deleteVehiculo(' + v.id + ')">Eliminar</button></td></tr>'
  ).join('');
}

async function createVehiculo(e) {
  e.preventDefault();
  const obj = formToObj(e.target);
  obj.capacidad_carga_kg = parseFloat(obj.capacidad_carga_kg);
  await apiFetch('/api/vehiculos', { method: 'POST', body: JSON.stringify(obj) });
  e.target.reset(); loadVehiculos();
}

async function deleteVehiculo(id) {
  if (!confirm('¿Eliminar vehículo?')) return;
  await apiFetch('/api/vehiculos/' + id, { method: 'DELETE' }); loadVehiculos();
}

async function loadRutas() {
  const data = await apiFetch('/api/rutas');
  document.getElementById('tbody-rutas').innerHTML = data.map(r =>
    '<tr><td>' + r.id + '</td><td>' + r.vehiculo_id + '</td><td>' + r.conductor_id + '</td><td>' + r.estado + '</td>' +
    '<td><button class="del" onclick="deleteRuta(' + r.id + ')">Eliminar</button></td></tr>'
  ).join('');
}

async function createRuta(e) {
  e.preventDefault();
  const obj = formToObj(e.target);
  ['vehiculo_id','conductor_id','origen_lat','origen_lng','destino_lat','destino_lng']
    .forEach(k => { obj[k] = parseFloat(obj[k]); });
  await apiFetch('/api/rutas', { method: 'POST', body: JSON.stringify(obj) });
  e.target.reset(); loadRutas();
}

async function deleteRuta(id) {
  if (!confirm('¿Eliminar ruta?')) return;
  await apiFetch('/api/rutas/' + id, { method: 'DELETE' }); loadRutas();
}

loadAlerts(); loadConductores(); loadVehiculos(); loadRutas();
setInterval(loadAlerts, 10000);
