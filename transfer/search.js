/* No-Risk live zoekwidget — altijd zichtbaar invoerveld */
(function () {
  const BASE = '/search-data.json';
  let data = null;

  /* ── DOM refs ── */
  const input = document.getElementById('search-input');
  const box   = document.getElementById('search-box');

  if (!input || !box) return;

  /* ── Type-iconen ── */
  const ICONS = { locatie:'📍', dienst:'🔧', info:'ℹ️', merk:'🚗', model:'🚗', pagina:'📄', volmacht:'🛡️', maatschappij:'🏢' };

  /* ── Data laden (één keer) ── */
  function load() {
    if (data) return Promise.resolve(data);
    return fetch(BASE)
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(d => { data = d; return d; })
      .catch(() => { data = []; return []; });
  }

  /* ── Zoeken ── */
  function search(q) {
    if (!data || q.length < 2) { close(); return; }
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = data.filter(e => {
      const hay = (e.l + ' ' + (e.b || '') + ' ' + (e.t || '')).toLowerCase();
      return terms.every(t => hay.includes(t));
    }).slice(0, 10);

    if (!hits.length) {
      box.innerHTML = '<li class="sr-empty">Geen resultaten gevonden</li>';
      box.classList.add('open');
      return;
    }

    box.innerHTML = hits.map((h, i) => {
      const hl   = highlight(h.l, terms);
      const icon = ICONS[h.t] ? '<span class="sr-icon">' + ICONS[h.t] + '</span>' : '';
      const badge = h.t && h.t !== 'model'
        ? '<span class="sr-badge sr-badge--' + h.t + '">' + h.b + '</span>'
        : '<span class="sr-bj">' + h.b + '</span>';
      const url = h.s || ('/' + h.u);
      return '<li><a class="sr-item" href="' + url + '" data-idx="' + i + '"><span class="sr-label">' + icon + hl + '</span>' + badge + '</a></li>';
    }).join('');
    box.classList.add('open');
  }

  /* ── Highlight matching tekst ── */
  function highlight(text, terms) {
    let result = text;
    terms.forEach(t => {
      const re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&') + ')', 'gi');
      result = result.replace(re, '<mark>$1</mark>');
    });
    return result;
  }

  /* ── Sluit dropdown ── */
  function close() {
    box.classList.remove('open');
    box.innerHTML = '';
  }

  /* ── Events ── */
  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (q.length < 2) { close(); return; }
    load().then(() => search(q));
  });

  input.addEventListener('focus', () => {
    const q = input.value.trim();
    if (q.length >= 2 && data) search(q);
  });

  /* Keyboard: pijltjes + esc */
  input.addEventListener('keydown', e => {
    const items = box.querySelectorAll('.sr-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      items[0]?.focus();
    } else if (e.key === 'Escape') {
      close(); input.blur();
    }
  });

  box.addEventListener('keydown', e => {
    const items = [...box.querySelectorAll('.sr-item')];
    const cur = document.activeElement;
    const idx = items.indexOf(cur);
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      items[idx + 1]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (idx <= 0) input.focus();
      else items[idx - 1]?.focus();
    } else if (e.key === 'Escape') {
      close(); input.focus();
    }
  });

  /* Klik buiten sluit */
  document.addEventListener('click', e => {
    const wrapper = input.closest('.nav-search');
    if (wrapper && !wrapper.contains(e.target)) close();
  });
})();
