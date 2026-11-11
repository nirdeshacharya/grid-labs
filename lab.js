/* Shared helpers for Grid Labs entries. Entries fetch SSEN's open data in the reader's
   browser and compute their figures on load, so nothing here is a stored result. */
const CKAN = 'https://data-api.ssen.co.uk/api/3/action/';
const PAGE = 32000; // CKAN's maximum rows per request

async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${new URL(url).hostname} returned ${r.status}`);
  return r.json();
}
// Newest datastore CSV in a dataset whose name matches; SSEN republishes some files under month-stamped names.
async function latestResource(dataset, nameRe) {
  const res = (await getJSON(`${CKAN}package_show?id=${dataset}`)).result.resources
    .filter(r => r.datastore_active && /csv/i.test(r.format) && nameRe.test(r.name))
    .sort((a, b) => String(b.last_modified || b.created).localeCompare(String(a.last_modified || a.created)));
  if (!res[0]) throw new Error(`no matching file in SSEN's ${dataset} dataset`);
  return { id: res[0].id, name: res[0].name, modified: res[0].last_modified };
}
async function fetchAll(resource, fields) {
  let out = [], offset = 0, total = Infinity;
  while (offset < total) {
    const u = new URL(CKAN + 'datastore_search');
    u.searchParams.set('resource_id', resource);
    u.searchParams.set('limit', PAGE);
    u.searchParams.set('offset', offset);
    if (fields) u.searchParams.set('fields', fields.join(','));
    const j = (await getJSON(u)).result;
    out = out.concat(j.records);
    total = j.total;
    offset += PAGE;
    if (!j.records.length) break;
  }
  return out;
}
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = v => { const n = parseFloat(v); return Number.isFinite(n) ? n : null; };
const fmt = (n, d = 0) => n == null ? 'n/a' : n.toLocaleString('en-GB', { maximumFractionDigits: d, minimumFractionDigits: d });
const day = s => s ? new Date(s).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) : '';
const norm = s => String(s || '').toUpperCase().replace(/\b(PRIMARY|BSP|GSP|GRID)\b/g, '').replace(/[^A-Z0-9]/g, '');

document.addEventListener('mousemove', e => { // one tooltip for anything carrying data-tip
  let tip = $('#tip');
  if (!tip) { tip = document.createElement('div'); tip.id = 'tip'; tip.hidden = true; document.body.appendChild(tip); }
  const t = e.target.closest?.('[data-tip]');
  if (!t) { tip.hidden = true; return; }
  tip.textContent = t.dataset.tip; tip.hidden = false;
  tip.style.left = Math.min(e.clientX + 12, innerWidth - tip.offsetWidth - 8) + 'px';
  tip.style.top = (e.clientY + 14) + 'px';
});
