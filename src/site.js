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
    var map = [['.search', 'search'], ['.actionbar', 'mobile_bar'], ['.utility', 'top_bar'], ['.site-head', 'header'], ['.hero', 'hero'], ['.page-head', 'page_heading'],
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

  /* ---------- search ----------
     The index (assets/search.json) is fetched the first time someone uses a search box, then matched here in the browser.
     Search terms are sent to Analytics, unless they look like an email address or a phone number. */
  var searchForms = Array.prototype.slice.call(document.querySelectorAll('form.search'));
  if (searchForms.length) (function () {
    var index = null, pending = null;
    var STOP = { a: 1, an: 1, the: 1, my: 1, our: 1, is: 1, are: 1, of: 1, 'for': 1, to: 1, 'in': 1, on: 1, and: 1, or: 1, i: 1, it: 1, 'do': 1, does: 1,
                 why: 1, how: 1, what: 1, 'with': 1, need: 1, have: 1, has: 1, we: 1, me: 1, near: 1, keeps: 1, keep: 1 };
    var KIND = { 'Product': 1.15, 'Problem guide': 1.1, 'Manufacturer': 1.1, 'Pump type': 1.1, 'Service': 1.05, 'Call': 1.25, 'Page': 0.9 };  // anything else counts as 1

    function norm(s) { return (s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, ' ').trim(); }
    // "seals" and "seal", "leaking" and "leak" count as the same word
    function stem(w) { return w.length > 4 ? w.replace(/s$/, '').replace(/(ing|ed)$/, '') : w; }
    function words(s) { return norm(s).split(' ').filter(Boolean).map(function (w) { return [w, stem(w)]; }); }
    // true when two words differ by one typo: a wrong, missing, extra or swapped letter
    function near(a, b) {
      var la = a.length, lb = b.length, i = 0;
      if (Math.abs(la - lb) > 1) return false;
      while (i < la && i < lb && a.charAt(i) === b.charAt(i)) i++;
      if (la === lb) return a.slice(i + 1) === b.slice(i + 1) || (a.charAt(i) === b.charAt(i + 1) && a.charAt(i + 1) === b.charAt(i) && a.slice(i + 2) === b.slice(i + 2));
      return la > lb ? a.slice(i + 1) === b.slice(i) : a.slice(i) === b.slice(i + 1);
    }
    // how well a typed word matches a word in the index, from 0 to 1.
    // Two-letter words (state abbreviations) must match exactly, unless they are still being typed.
    function quality(t, ts, w, typing) {
      if (t === w[0]) return 1;
      if (t.length < 3 && !typing) return 0;
      if (ts === w[1]) return 0.95;
      if (w[0].indexOf(t) === 0) return 0.8;
      if (w[1].length > 3 && t.indexOf(w[1]) === 0) return 0.6;
      if (t.length > 4 && near(t, w[0])) return 0.5;
      return 0;
    }
    function best(t, ts, list, typing) {
      var q = 0;
      for (var i = 0; i < list.length && q < 1; i++) q = Math.max(q, quality(t, ts, list[i], typing));
      return q;
    }
    function find(q) {
      var all = norm(q).split(' ').filter(function (t) { return t.length > 1; });
      var toks = all.filter(function (t) { return !STOP[t]; });
      if (!toks.length) toks = all;
      if (!toks.length) return [];
      var out = [], most = 0;
      index.forEach(function (e) {
        var score = 0, hit = 0, strong = 0, inTitle = 0;
        toks.forEach(function (t, n) {
          // the title counts most, then what the page is for, then words from its summary and body
          var ts = stem(t), typing = n === toks.length - 1, title = best(t, ts, e.T, typing);
          var head = title < 1 ? best(t, ts, e.H, typing) : 0;
          var rest = title < 1 && head < 1 ? Math.max(best(t, ts, e.S, typing), best(t, ts, e.W, typing)) : 0;
          var s = Math.max(title * 10, head * 7, rest * 3);
          if (s > 0) hit++;
          if (title > 0 || head > 0) strong++;
          if (title > 0) inTitle++;
          score += s;
        });
        if (!hit) return;
        score += 8 * Math.min(1, inTitle / e.n);                         // how much of the title was typed
        if (inTitle >= e.n && inTitle === toks.length) score += 6;       // the whole title, and nothing else
        if (strong === toks.length) score += 5;                          // every word is something the page is for
        most = Math.max(most, hit);
        out.push({ e: e, hit: hit, score: score * (KIND[e.k] || 1) });
      });
      // pages matching every word typed; failing that, the pages matching the most words
      return out.filter(function (r) { return r.hit === most; }).sort(function (a, b) { return b.score - a.score; });
    }
    function load(src) {
      if (!pending) pending = fetch(src).then(function (r) { return r.json(); }).then(function (rows) {
        index = rows.map(function (r) { return { t: r.t, k: r.k, u: r.u, s: r.s, T: words(r.t),
          n: Math.max(1, norm(r.t).split(' ').filter(function (w) { return w.length > 1 && !STOP[w]; }).length), H: words(r.h), S: words(r.s), W: words(r.w) }; });
      })['catch'](function () { pending = null; });
      return pending;
    }
    function sendable(q) { return q.length > 2 && !/@|\d{3}[\s.\-]?\d{3}[\s.\-]?\d{4}/.test(q); }

    searchForms.forEach(function (form) {
      var input = form.querySelector('input'), pop = form.querySelector('.search-pop'), status = form.querySelector('[role=status]');
      var place = form.getAttribute('data-search'), root = form.getAttribute('data-root'), src = form.getAttribute('data-index');
      var inline = place === 'page', max = inline ? 40 : 8;
      var list = document.createElement('ul'), more = document.createElement('p');
      var shown = [], active = -1, timer = null, nudged = false, lastX = -1, lastY = -1;
      list.className = 'search-list'; list.id = 'results-' + place;
      more.className = 'search-more';
      pop.appendChild(list); pop.appendChild(more);
      if (!inline) {
        // a list of suggestions under the box, worked with the arrow keys
        list.setAttribute('role', 'listbox'); list.setAttribute('aria-label', 'Search results');
        input.setAttribute('role', 'combobox'); input.setAttribute('aria-autocomplete', 'list');
        input.setAttribute('aria-controls', list.id); input.setAttribute('aria-expanded', 'false');
      }
      function term() { return input.value.replace(/\s+/g, ' ').trim(); }
      function report(q, n) {
        clearTimeout(timer);
        if (!sendable(q)) return;
        try { if (sessionStorage.getItem('sd_search') === q.toLowerCase()) return; sessionStorage.setItem('sd_search', q.toLowerCase()); } catch (e) {}
        var data = { search_term: q.toLowerCase().slice(0, 80), link_location: 'search_' + place };
        track('search', data);
        if (!n) track('search_no_results', data);
      }
      function setActive(i) {
        var items = list.querySelectorAll('a');
        if (items[active]) items[active].setAttribute('aria-selected', 'false');
        active = i;
        if (items[i]) { items[i].setAttribute('aria-selected', 'true'); input.setAttribute('aria-activedescendant', items[i].id); items[i].scrollIntoView({ block: 'nearest' }); }
        else input.removeAttribute('aria-activedescendant');
      }
      function close() {
        if (inline) return;
        pop.hidden = true; active = -1;
        input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant');
      }
      function draw() {
        var q = term();
        clearTimeout(timer);
        var found = q.length > 1 && index ? find(q) : [];
        if (!found.length && q.length < 3) { pop.hidden = true; status.textContent = ''; close(); return; }
        shown = found.slice(0, max); active = -1;
        list.textContent = ''; more.textContent = '';
        shown.forEach(function (r, i) {
          var li = document.createElement('li'), a = document.createElement('a'), b = document.createElement('b'), k = document.createElement('em'), s = document.createElement('small');
          a.href = /^(https?|tel):/.test(r.e.u) ? r.e.u : root + r.e.u + 'index.html';
          b.textContent = r.e.t; k.textContent = r.e.k; s.textContent = r.e.s;
          a.appendChild(b); a.appendChild(k); a.appendChild(s); li.appendChild(a); list.appendChild(li);
          // in the suggestion list the link itself is the option, so a screen reader hears one item, not a link inside an item
          if (!inline) { li.setAttribute('role', 'presentation'); a.id = list.id + '-' + i; a.setAttribute('role', 'option'); a.setAttribute('aria-selected', 'false'); a.tabIndex = -1; }
        });
        list.hidden = !shown.length;
        var ask = document.createElement('a'), quoted = '“' + (q.length > 40 ? q.slice(0, 40) + '…' : q) + '”';
        ask.href = root + 'contact/index.html?need=quote&about=' + encodeURIComponent(q.slice(0, 80));
        if (shown.length) { more.appendChild(document.createTextNode('Not what you need? ')); ask.textContent = 'Ask us about ' + quoted; }
        else { more.appendChild(document.createTextNode('Nothing on the site matches ' + quoted + '. ')); ask.textContent = 'Send it to us and a specialist will reply'; }
        more.appendChild(ask);
        pop.hidden = false;
        if (!inline) { input.setAttribute('aria-expanded', shown.length ? 'true' : 'false'); input.removeAttribute('aria-activedescendant'); }
        status.textContent = shown.length ? shown.length + (shown.length === 1 ? ' result' : ' results') + (found.length > shown.length ? ', best matches shown' : '') : 'No results';
        timer = setTimeout(function () { report(q, shown.length); }, 1500);
        fit();
      }
      // Keep the suggestions inside the screen. If there is too little room under the box (a short screen,
      // or a phone with the keyboard up), bring the box up under the header first.
      function fit() {
        if (inline || list.hidden) return;
        var tall = window.visualViewport ? window.visualViewport.height : window.innerHeight, bar = document.querySelector('.actionbar');
        if (bar && bar.offsetHeight) tall -= bar.offsetHeight;  // the call and quote bar fixed to the bottom of a phone screen
        var top = list.getBoundingClientRect().top, room = tall - top - more.offsetHeight - 14;
        if (room < 230 && place === 'hero' && !nudged) {
          var head = document.querySelector('.site-head'), by = form.getBoundingClientRect().top - (head ? head.offsetHeight : 0) - 12;
          nudged = true;
          if (by > 0) { window.scrollBy(0, by); room += by; }
        }
        list.style.maxHeight = Math.max(170, Math.min(440, room)) + 'px';
      }
      function chosen(i) {
        var q = term();
        report(q, shown.length);
        if (sendable(q) && shown[i]) track('search_result_click', { search_term: q.toLowerCase().slice(0, 80), link_text: shown[i].e.t, result_type: shown[i].e.k, position: i + 1, link_location: 'search_' + place });
      }
      input.addEventListener('focus', function () { load(src).then(function () { if (!inline && term().length > 1) draw(); }); });
      input.addEventListener('input', function () { load(src).then(draw); });
      input.addEventListener('blur', function () { nudged = false; });
      input.addEventListener('keydown', function (e) {
        if (inline) return;
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
          if (pop.hidden || !shown.length) return;
          e.preventDefault();
          var n = shown.length;
          setActive(e.key === 'ArrowDown' ? (active + 1) % n : (active <= 0 ? n - 1 : active - 1));
        } else if (e.key === 'Enter' && active > -1) {
          e.preventDefault();
          chosen(active);
          location.href = list.children[active].querySelector('a').href;
        } else if (e.key === 'Escape' && !pop.hidden) {
          e.preventDefault(); e.stopPropagation(); close();  // first Escape closes the list and keeps what was typed
        }
      });
      list.addEventListener('click', function (e) {
        var li = e.target.closest('li');
        if (li) chosen(Array.prototype.indexOf.call(list.children, li));
      });
      // the mouse highlights a suggestion only when it actually moves, not when the page scrolls under it
      list.addEventListener('mousemove', function (e) {
        var li = e.target.closest('li');
        if (inline || !li || (e.screenX === lastX && e.screenY === lastY)) return;
        lastX = e.screenX; lastY = e.screenY;
        var i = Array.prototype.indexOf.call(list.children, li);
        if (i !== active) { var keep = list.scrollTop; setActive(i); list.scrollTop = keep; }
      });
      form.addEventListener('submit', function (e) {
        var q = term();
        if (!q) { e.preventDefault(); input.focus(); return; }
        if (!inline) return;  // the browser opens the search page, which shows and counts the search
        e.preventDefault();
        load(src).then(function () { draw(); report(q, shown.length); });
        try { history.replaceState(null, '', '?q=' + encodeURIComponent(q)); } catch (err) {}
      });
      form.addEventListener('focusout', function (e) { if (e.relatedTarget && !form.contains(e.relatedTarget)) close(); });
      document.addEventListener('click', function (e) { if (!form.contains(e.target)) close(); });
      if (inline) {
        if (params.get('q')) input.value = params.get('q');
        if (term()) load(src).then(draw);
      }
    });

    // the search button in the header opens a panel under it
    var panel = document.getElementById('search-panel'), openers = Array.prototype.slice.call(document.querySelectorAll('.search-btn'));
    if (panel) {
      var panelInput = panel.querySelector('input'), opener = null;
      var setPanel = function (open) {
        panel.hidden = !open;
        openers.forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
        if (open) {
          if (nav && menuBtn && nav.classList.contains('open')) { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.textContent = 'Menu'; }
          panelInput.focus();
        } else if (opener) { opener.focus(); opener = null; }
      };
      openers.forEach(function (b) {
        b.setAttribute('role', 'button'); b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', 'search-panel');
        b.addEventListener('click', function (e) { e.preventDefault(); opener = b; setPanel(panel.hidden); });
        b.addEventListener('keydown', function (e) { if (e.key === ' ') { e.preventDefault(); b.click(); } });
      });
      panel.querySelector('.search-close').addEventListener('click', function () { setPanel(false); });
      panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') setPanel(false); });
      document.addEventListener('click', function (e) { if (!panel.hidden && !e.target.closest('.site-head')) { opener = null; setPanel(false); } });
      if (menuBtn) menuBtn.addEventListener('click', function () { if (!panel.hidden) { opener = null; setPanel(false); } });
    }
  })();

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
    // The form is a Netlify form. Without JavaScript the browser posts it and lands on contact/thanks/.
    // With JavaScript it is posted in the background so the thank-you address can carry the need and state;
    // that page records the lead, once, when it loads.
    var pageField = document.createElement('input');
    pageField.type = 'hidden'; pageField.name = 'page'; pageField.value = location.pathname;
    form.appendChild(pageField);
    form.addEventListener('submit', function (e) {
      if (!form.checkValidity()) return;  // let the browser show what is missing
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]'), label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending\u2026';
      if (msg) msg.hidden = true;
      var done = '/contact/thanks/?need=' + encodeURIComponent(need ? need.value : '') + '&state=' + encodeURIComponent((form.elements.state || {}).value || '');
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) { if (!r.ok) throw new Error(r.status); location.href = done; })
        ['catch'](function () { btn.disabled = false; btn.textContent = label; if (msg) msg.hidden = false; track('form_error', { form_name: 'enquiry' }); });
    });
  }

  // A lead is counted once, when the thank-you page loads after a real submission.
  if (/\/contact\/thanks\/(index\.html)?$/.test(location.pathname)) {
    var lead = { lead_type: 'enquiry_form', need: params.get('need') || '', state: params.get('state') || '' };
    if (first) { lead.first_source = first.source; lead.first_medium = first.medium; lead.first_landing_page = first.landing_page; }
    track('generate_lead', lead);
  }
})();
