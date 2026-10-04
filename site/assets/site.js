(function () {
  /* ---------- menu, tabs, enquiry form ---------- */
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

  /* ---------- tracking ----------
     Sends events to Google Analytics when the tag is on the page; does nothing otherwise.
     No names, emails or phone numbers typed by visitors are ever sent. */
  function track(name, data) {
    if (typeof window.gtag === 'function') window.gtag('event', name, data || {});
  }
  function where(el) {
    var map = [['.actionbar', 'mobile_bar'], ['.utility', 'top_bar'], ['.site-head', 'header'], ['.hero', 'hero'], ['.page-head', 'page_heading'],
               ['.aside-card', 'sidebar'], ['.quote-side', 'enquiry_section'], ['.offices', 'contact_details'], ['.region', 'locations'], ['.foot', 'footer']];
    for (var i = 0; i < map.length; i++) if (el.closest(map[i][0])) return map[i][1];
    return 'page_content';
  }

  // First touch: where this visitor originally came from. Kept in the browser and
  // attached to the enquiry form so each lead carries its source into the CRM.
  var first = null;
  try {
    first = JSON.parse(localStorage.getItem('sd_first_touch') || 'null');
    if (!first) {
      var ref = document.referrer && document.referrer.indexOf(location.hostname) === -1 ? document.referrer.split('/')[2] : '';
      first = {
        source: params.get('utm_source') || ref || 'direct',
        medium: params.get('utm_medium') || (ref ? 'referral' : 'none'),
        campaign: params.get('utm_campaign') || '',
        landing_page: location.pathname
      };
      localStorage.setItem('sd_first_touch', JSON.stringify(first));
    }
  } catch (e) { first = null; }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) {
      track('phone_call_click', { link_location: where(a), phone_number: href.slice(4) });
    } else if (href.indexOf('mailto:') === 0) {
      track('email_click', { link_location: where(a) });
    } else if (href.indexOf('rms.mysoutherndesign.com') !== -1) {
      track('portal_click', { link_location: where(a) });
    } else if (/contact\/(index\.html)?(\?|$)/.test(href) || href === '#quote') {
      track('quote_cta_click', { link_location: where(a), link_text: (a.textContent || '').trim().slice(0, 60) });
    }
  });

  var form = document.getElementById('quote-form'), msg = document.getElementById('form-msg');
  if (form) {
    if (first) {
      ['source', 'medium', 'campaign', 'landing_page'].forEach(function (k) {
        var h = document.createElement('input');
        h.type = 'hidden'; h.name = 'first_' + k; h.value = first[k] || '';
        form.appendChild(h);
      });
    }
    var started = false;
    form.addEventListener('focusin', function () {
      if (!started) { started = true; track('form_start', { form_name: 'enquiry' }); }
    });
    // Concept build: the form does not send anywhere yet, so a submit here is not counted as a lead.
    // The live form redirects to contact/thanks/, and that page records the lead.
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (msg) msg.hidden = false;
      track('form_demo_submit', { form_name: 'enquiry', need: need ? need.value : '' });
    });
  }

  // A lead is counted once, when the thank-you page loads after a real submission.
  if (/\/contact\/thanks\/(index\.html)?$/.test(location.pathname)) {
    var lead = { lead_type: 'enquiry_form', need: params.get('need') || '', state: params.get('state') || '' };
    if (first) { lead.first_source = first.source; lead.first_medium = first.medium; lead.first_landing_page = first.landing_page; }
    track('generate_lead', lead);
  }
})();
