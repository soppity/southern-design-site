(function () {
  var menuBtn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.textContent = open ? 'Close' : 'Menu';
    });
  }
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  function selectTab(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { selectTab(tab); });
    tab.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      selectTab(next); next.focus();
    });
  });
  var need = document.getElementById('need'), equip = document.getElementById('equip');
  document.querySelectorAll('[data-need]').forEach(function (link) {
    link.addEventListener('click', function () { if (need) need.value = link.getAttribute('data-need'); });
  });
  var params = new URLSearchParams(location.search);
  if (need && params.get('need')) need.value = params.get('need');
  if (equip && params.get('about')) equip.value = params.get('about');
  var form = document.getElementById('quote-form'), msg = document.getElementById('form-msg');
  if (form && msg) form.addEventListener('submit', function (e) { e.preventDefault(); msg.hidden = false; });
})();
