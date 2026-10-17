/* Automation IDs + hidden Automation Map.
   Every control gets data-automation-id = <area>_<type>_<name>
   (e.g. toc_button_data, footer_link_zmillikin-work-gmail-com).
   The map (searchable) opens from the hidden skull keys (.skull-key). */
(() => {
    'use strict';

    const SEL = 'button, a[href], input, select, textarea, summary';
    const slug = s => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 44);
    const norm = s => (s || '').replace(/\s+/g, ' ').trim();

    function areaOf(el) {
        const dlg = el.closest('dialog');
        if (dlg && dlg.id) return slug(dlg.id.replace(/-dialog$/, ''));
        if (el.closest('.cookie-banner')) return 'cookie';
        if (el.closest('.single-panel')) return 'single';
        if (el.closest('nav')) return 'toc';
        if (el.closest('.global-bar, .global-results')) return 'global';
        if (el.closest('footer')) return 'footer';
        if (el.closest('header')) return 'header';
        const sec = el.closest('section[id]');
        if (sec) {
            if (el.closest('.view-display')) return sec.id + '-display';
            if (el.closest('.view-table')) return sec.id + '-table';
            return sec.id;
        }
        return 'page';
    }

    function typeOf(el) {
        const t = el.tagName.toLowerCase();
        if (t === 'a') return 'link';
        if (t === 'input') return el.type === 'search' ? 'search' : 'input';
        return t;
    }

    function nameOf(el) {
        let label = el.getAttribute('aria-label') || el.getAttribute('title') || norm(el.textContent) || el.getAttribute('placeholder') || el.dataset.testid || el.id || 'unnamed';
        const row = el.closest('tr');
        if (row && row.cells[0] && !row.cells[0].contains(el)) {
            label = norm(row.cells[0].querySelector('.product-detail-trigger, strong')?.textContent) + ' ' + label;
        } else if (row) {
            label = norm(row.cells[0].querySelector('.product-detail-trigger, strong')?.textContent) + ' ' + label;
        }
        return slug(label) || 'unnamed';
    }

    function tag(root) {
        const nodes = root.matches && root.matches(SEL) ? [root] : [];
        nodes.push(...root.querySelectorAll(SEL));
        nodes.forEach(el => {
            if (el.hasAttribute('data-automation-id')) return;
            const base = `${areaOf(el)}_${typeOf(el)}_${nameOf(el)}`;
            let id = base, n = 2;
            while (document.querySelector(`[data-automation-id="${CSS.escape(id)}"]`)) id = `${base}-${n++}`;
            el.setAttribute('data-automation-id', id);
        });
    }

    function buildMap() {
        return Array.from(document.querySelectorAll('[data-automation-id]')).map(el => {
            const id = el.getAttribute('data-automation-id');
            const [area, type] = id.split('_');
            const label = norm(el.getAttribute('aria-label') || el.textContent || el.getAttribute('placeholder') || el.title).slice(0, 80);
            return { id, area, type, label, selector: `[data-automation-id="${id}"]` };
        });
    }

    /* ---------------- Map dialog ---------------- */
    let dialog, listBody, countEl, searchEl;

    function ensureDialog() {
        if (dialog) return;
        dialog = document.createElement('dialog');
        dialog.id = 'automation-map-dialog';
        dialog.className = 'info-dialog map-dialog';
        dialog.setAttribute('aria-labelledby', 'automation-map-title');
        dialog.innerHTML = `
            <div class="product-dialog-header">
                <h2 id="automation-map-title">Automation Map</h2>
                <button class="product-dialog-close" type="button" aria-label="Close automation map" data-testid="map-close">&times;</button>
            </div>
            <div class="info-body">
                <p>Every control exposes <code>data-automation-id</code> as <code>area_type_name</code>. Click a row to copy its selector.</p>
                <div class="skull-search">
                    <span class="skull-icon" aria-hidden="true">&#9760;</span>
                    <input type="search" class="search-input" placeholder="Search the automation map&hellip;" aria-label="Search automation map" data-testid="map-search">
                </div>
                <div class="map-meta"><span data-testid="map-count"></span>
                    <button type="button" class="chip-btn" data-testid="map-download">Download JSON</button></div>
                <div class="map-scroll"><table class="map-table compact"><thead><tr><th>Automation ID</th><th>Type</th><th>Area</th><th>Label</th></tr></thead><tbody data-testid="map-rows"></tbody></table></div>
            </div>`;
        document.body.append(dialog);
        listBody = dialog.querySelector('tbody');
        countEl = dialog.querySelector('[data-testid="map-count"]');
        searchEl = dialog.querySelector('input');
        dialog.querySelector('.product-dialog-close').addEventListener('click', () => dialog.close());
        dialog.addEventListener('click', ev => { if (ev.target === dialog) dialog.close(); });
        searchEl.addEventListener('input', render);
        dialog.querySelector('[data-testid="map-download"]').addEventListener('click', () => {
            const blob = new Blob([JSON.stringify(buildMap(), null, 2)], { type: 'application/json' });
            const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: 'automation-map.json' });
            a.click();
            URL.revokeObjectURL(a.href);
        });
        listBody.addEventListener('click', ev => {
            const tr = ev.target.closest('tr');
            if (tr && navigator.clipboard) navigator.clipboard.writeText(tr.dataset.selector).catch(() => {});
        });
        tag(dialog);
    }

    function render() {
        const q = searchEl.value.trim().toLowerCase();
        const all = buildMap();
        const rows = all.filter(r => !q || `${r.id} ${r.label}`.toLowerCase().includes(q));
        listBody.replaceChildren(...rows.slice(0, 400).map(r => {
            const tr = document.createElement('tr');
            tr.dataset.selector = r.selector;
            [r.id, r.type, r.area, r.label].forEach((v, i) => {
                const td = document.createElement('td');
                if (i === 0) { const c = document.createElement('code'); c.textContent = v; td.append(c); } else td.textContent = v;
                tr.append(td);
            });
            return tr;
        }));
        countEl.textContent = `${rows.length} of ${all.length} controls`;
    }

    function openMap() {
        ensureDialog();
        searchEl.value = '';
        render();
        if (!dialog.open) dialog.showModal();
    }

    // Skull keys: open on click; styling is hover-only (see CSS).
    document.addEventListener('click', ev => {
        if (ev.target.closest('.skull-key')) openMap();
    });

    tag(document.body);
    new MutationObserver(muts => {
        muts.forEach(m => m.addedNodes.forEach(n => { if (n.nodeType === 1) tag(n); }));
    }).observe(document.body, { childList: true, subtree: true });

    window.DevMatrixAutomation = { map: buildMap, open: openMap };
})();
