/* No-Risk live zoekwidget — laad na DOM-ready */
(function () {
  const BASE = '/search-data.json';
  let data = null, idx = -1;

  /* ── DOM refs ── */
  const toggle = document.getElementById('search-toggle');
  const box    = document.getElementById('search-box');
  const input  = document.getElementById('search-input');
  const list   = document.getElementById('search-results');

  if (!toggle || !box || !input || !list) return;

  /* ── Data laden (één keer) ── */
  function load() {
    if (data) return Promise.resolve(data);
    return fetch(BASE)
      .then(r => r.json())
      .then(d => { data = d; return d; });
  }

  /* ── Zoeken ── */
  function search(q) {
    if (!data || q.length < 2) { list.innerHTML = ''; return; }
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = data.filter(e =>
      terms.every(t => e.l.toLowerCase().includes(t))
    ).slice(0, 9);

    if (!hits.length) {
      list.innerHTML = '<li class="sr-empty">Geen resultaten gevonden</li>';
      return;
    }

    list.innerHTML = hits.map((h, i) => {
      const hl = highlight(h.l, terms);
      return `<li>
        <a class="sr-item" href="${h.s}" data-idx="${i}">
          <span class="sr-label">${hl}</span>
          <span class="sr-bj">${h.b}</span>
        </a>
      </li>`;
    }).join('');
    idx = -1;
  }

  /* ── Highlight matching tekst ── */
  function highlight(text, terms) {
    let result = text;
    terms.forEach(t => {
      const re = new RegExp(`(${t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi');
      result = result.replace(re, '<mark>$1</mark>');
    });
    return result;
  }

  /* ── Open / sluit ── */
  function open() {
    box.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    input.focus();
    load().then(() => search(input.value));
  }

  function close() {
    box.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    input.value = '';
    list.innerHTML = '';
    idx = -1;
  }

  /* ── Events ── */
  toggle.addEventListener('click', () => {
    box.classList.contains('open') ? close() : open();
  });

  input.addEventListener('input', () => {
    load().then(() => search(input.value.trim()));
  });

  /* Keyboard: pijltjes + enter + esc */
  input.addEventListener('keydown', e => {
    const items = list.querySelectorAll('.sr-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      idx = Math.min(idx + 1, items.length - 1);
      items[idx]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      idx = Math.max(idx - 1, -1);
      if (idx === -1) input.focus();
      else items[idx]?.focus();
    } else if (e.key === 'Escape') {
      close();
    }
  });

  list.addEventListener('keydown', e => {
    const items = list.querySelectorAll('.sr-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      idx = Math.min(idx + 1, items.length - 1);
      items[idx]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      idx = Math.max(idx - 1, -1);
      if (idx === -1) input.focus();
      else items[idx]?.focus();
    } else if (e.key === 'Escape') {
      close();
    }
  });

  /* Klik buiten → sluit */
  document.addEventListener('click', e => {
    if (!box.contains(e.target) && e.target !== toggle) close();
  });
})();
