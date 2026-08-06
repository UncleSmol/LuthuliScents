/* LuthuliScents — shared data loader.
   Loads data/products.json once and stores it for the whole session. */
window.LS_DATA = null;
window.LS_MONEY = function (n) { return 'R' + Number(n).toFixed(2); };
window.LS_PRODUCT = function (key) {
  if (!window.LS_DATA) return null;
  return window.LS_DATA.products.find(function (p) { return p.key === key; }) || null;
};
window.LS_READY = fetch('./data/products.json')
  .then(function (r) {
    if (!r.ok) throw new Error('Failed to load products.json: ' + r.status);
    return r.json();
  })
  .then(function (data) {
    window.LS_DATA = data;
    return data;
  });
