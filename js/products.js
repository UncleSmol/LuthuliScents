/* LuthuliScents — product catalog rendering (from data/products.json). */

(function () {
  'use strict';

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  window.productCard = function (p) {
    var badge = p.badge ? '<span class="p-badge">' + escapeHtml(p.badge) + '</span>' : '';
    return (
      '<div class="p-card">' +
      '<img src="' + escapeHtml(p.image) + '" alt="' + escapeHtml(p.name) + ' perfume" loading="lazy">' +
      badge +
      '<div class="p-name">' + escapeHtml(p.name) + '</div>' +
      '<div class="p-family">' + escapeHtml(p.family) + ' &middot; ' + escapeHtml(p.size) + '</div>' +
      '<div class="p-notes">' + escapeHtml(p.notes) + '</div>' +
      '<div class="p-price">' + window.LS_MONEY(p.price) + '</div>' +
      '<div class="p-actions">' +
      '<button class="btn add-to-cart" data-key="' + escapeHtml(p.key) + '">Add to cart</button>' +
      '<a class="btn ghost" href="cart.html">View cart</a>' +
      '</div>' +
      '</div>'
    );
  };

  /* Render a grid of products into a container. */
  window.renderProducts = function (containerId, list) {
    var el = document.getElementById(containerId);
    if (!el) return;
    if (!list || list.length === 0) {
      el.innerHTML = '<p class="caption">No scents match that family yet.</p>';
      return;
    }
    el.innerHTML = list.map(window.productCard).join('');
  };

  /* Render the featured scents for the home page. */
  window.renderFeatured = function (containerId) {
    var featured = window.LS_DATA.products.filter(function (p) { return p.featured; });
    window.renderProducts(containerId, featured);
  };

  /* Wire up family filtering on the products page. */
  window.initFamilyFilter = function (gridId, selectId) {
    var select = document.getElementById(selectId);
    var grid = document.getElementById(gridId);
    if (!select || !grid) return;

    function apply() {
      var family = select.value;
      var list = family === 'All'
        ? window.LS_DATA.products
        : window.LS_DATA.products.filter(function (p) { return p.family === family; });
      window.renderProducts(gridId, list);
    }

    select.addEventListener('change', apply);
    apply();
  };

  /* Shared delegated click handler for "Add to cart" buttons. */
  document.addEventListener('click', function (event) {
    var btn = event.target.closest ? event.target.closest('.add-to-cart') : null;
    if (btn && typeof window.addToCart === 'function') {
      window.addToCart(btn.getAttribute('data-key'));
      if (btn.dataset && btn.dataset.doneLabel) {
        var original = btn.textContent;
        btn.textContent = btn.dataset.doneLabel;
        setTimeout(function () { btn.textContent = original; }, 900);
      }
    }
  });
})();