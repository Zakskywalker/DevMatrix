/* DevMatrix UI layer.
   Turns each <section> table into a collapsible data section with a Table /
   Display (carousel + tiles) switch, adds a global Multi / Single view, search,
   a TOC tree with per-entity jump lists, and footer dialogs. */
(() => {
    'use strict';

    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
    const el = (tag, attrs = {}, ...kids) => {
        const n = document.createElement(tag);
        for (const [k, v] of Object.entries(attrs)) {
            if (v == null || v === false) continue;
            if (k === 'class') n.className = v;
            else if (k === 'text') n.textContent = v;
            else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
            else n.setAttribute(k, v === true ? '' : v);
        }
        kids.flat().forEach(k => k != null && n.append(k));
        return n;
    };
    const mobile = window.matchMedia('(max-width: 760px)');
    const norm = s => s.replace(/\s+/g, ' ').trim();
    const clip = (s, n) => (s.length > n ? s.slice(0, n - 1) + '…' : s);

    const hue = s => { let h = 0; for (const c of s) h = (h * 31 + c.codePointAt(0)) >>> 0; return h % 360; };
    const initials = name => {
        const w = name.replace(/[^\p{L}\p{N}\s]/gu, ' ').trim().split(/\s+/).filter(Boolean);
        if (!w.length) return name.slice(0, 2) || '?';
        return (w.length > 1 ? w[0][0] + w[1][0] : w[0].slice(0, 2)).toUpperCase();
    };
    const glyph = (name, large) =>
        el('span', { class: 'glyph' + (large ? ' lg' : ''), style: `--h:${hue(name)}`, 'aria-hidden': 'true', text: initials(name) });

    function cloneCell(cell) {
        const frag = document.createDocumentFragment();
        cell.childNodes.forEach(n => frag.append(n.cloneNode(true)));
        const t = $('.product-detail-trigger', frag);
        if (t) t.replaceWith(document.createTextNode(t.textContent));
        return frag;
    }

    /* ------------------------------------------------------------------ *
     * Models: one per table section
     * ------------------------------------------------------------------ */
    const models = [];
    const byId = {};

    $$('main > section').forEach(sec => {
        const table = $('table', sec);
        const h2 = $('h2', sec);
        if (!table || !h2) return;

        const heads = $$('thead th', table).map(th => norm(th.textContent));
        const rows = $$('tbody tr', table).filter(r => r.cells.length > 1);
        const model = {
            id: sec.id, sec, title: norm(h2.textContent), view: 'table', query: '',
            displays: new Set(), inputs: new Set(), entities: [],
        };
        model.shortTitle = model.title.replace(/^\d+\.\s*/, '');

        model.entities = rows.map((row, i) => {
            const trigger = $('.product-detail-trigger', row);
            const name = norm(trigger ? trigger.textContent : row.cells[0].textContent);
            const sub = norm(row.cells[0].textContent.replace(name, ''));
            const pop = $('.pop', row);
            const note = $('.pop-note', row);
            const e = {
                i, row, trigger, name, sub, model,
                popLabel: pop ? norm(pop.textContent) : '',
                popClass: pop ? pop.className : '',
                fields: Array.from(row.cells).map((cell, c) => ({ label: heads[c] || '', cell, text: norm(cell.textContent) })),
                text: norm(row.textContent).toLowerCase(),
            };
            e.blurb = note ? norm(note.textContent) : clip((e.fields[1] || {}).text || '', 110);
            e.match = true;
            return e;
        });

        buildSection(model, h2);
        models.push(model);
        byId[model.id] = model;
    });

    /* ------------------------------------------------------------------ *
     * Section construction
     * ------------------------------------------------------------------ */
    function buildSection(model, h2) {
        const { sec, id } = model;
        const wrapper = $('.table-wrapper', sec);
        const intro = $$(':scope > p', sec);

        const details = el('details', { class: 'data-section', 'data-view': 'table', 'data-testid': `section-${id}` });
        const summary = el('summary', { 'data-testid': `section-header-${id}` }, h2, el('span', { class: 'section-count', text: String(model.entities.length) }));
        const body = el('div', { class: 'section-body' });

        // Toolbar: view switch + search
        const btnTable = el('button', { type: 'button', 'aria-pressed': 'true', 'data-testid': `view-table-${id}`, text: 'Table' });
        const btnDisplay = el('button', { type: 'button', 'aria-pressed': 'false', 'data-testid': `view-display-${id}`, text: 'Display' });
        const seg = el('div', { class: 'seg', role: 'group', 'aria-label': `${model.shortTitle} layout` }, btnTable, btnDisplay);
        const search = el('input', { type: 'search', class: 'search-input', placeholder: `Search ${model.shortTitle}…`, 'aria-label': `Search ${model.shortTitle}`, 'data-testid': `search-${id}` });
        const count = el('span', { class: 'match-count', 'aria-live': 'polite', 'data-testid': `count-${id}` });
        const toolbar = el('div', { class: 'section-toolbar' }, seg, search, count);

        // Table view (desktop table / mobile square cells)
        const cellGrid = el('div', { class: 'cell-grid', 'data-testid': `cells-${id}` });
        model.entities.forEach(e => {
            e.cell = el('button', { type: 'button', class: 'cell-tile', 'data-testid': `cell-${id}`, 'aria-label': `Show details for ${e.name}` },
                el('span', { class: 'glyph', style: `--h:${hue(e.name)}`, 'aria-hidden': 'true', text: initials(e.name) }),
                el('span', { class: 'tile-name', text: e.name }),
                e.popLabel ? el('span', { class: e.popClass, text: e.popLabel }) : el('span', { class: 'tile-sub', text: e.sub }));
            e.cell.addEventListener('click', () => e.trigger && e.trigger.click());
            cellGrid.append(e.cell);
        });
        const viewTable = el('div', { class: 'view-table' }, wrapper, cellGrid);
        const viewDisplay = el('div', { class: 'view-display' });

        body.append(...intro, toolbar, viewTable, viewDisplay);
        details.append(summary, body);
        sec.replaceChildren(details);
        model.details = details;
        model.viewDisplay = viewDisplay;
        model.count = count;

        model.setView = v => {
            model.view = v;
            details.dataset.view = v;
            btnTable.setAttribute('aria-pressed', String(v === 'table'));
            btnDisplay.setAttribute('aria-pressed', String(v === 'display'));
            if (v === 'display' && !model.mainDisplay) {
                model.mainDisplay = createDisplay(model, 'display-' + id);
                viewDisplay.append(model.mainDisplay.el);
            }
            if (model.mainDisplay) model.mainDisplay.render();
        };
        btnTable.addEventListener('click', () => model.setView('table'));
        btnDisplay.addEventListener('click', () => model.setView('display'));

        model.inputs.add(search);
        search.addEventListener('input', () => setQuery(model, search.value));
        refresh(model);
    }

    function setQuery(model, q) {
        model.query = q;
        model.inputs.forEach(i => { if (i.value !== q) i.value = q; });
        refresh(model);
    }

    function refresh(model) {
        const q = model.query.trim().toLowerCase();
        let n = 0;
        model.entities.forEach(e => {
            e.match = !q || e.text.includes(q);
            e.row.hidden = !e.match;
            if (e.cell) e.cell.hidden = !e.match;
            if (e.match) n++;
        });
        model.count.textContent = q ? `${n} of ${model.entities.length} match` : `${model.entities.length} entries`;
        model.displays.forEach(d => d.render());
    }

    /* ------------------------------------------------------------------ *
     * Display component: search + carousel + dropdown + featured card + tiles
     * ------------------------------------------------------------------ */
    function createDisplay(model, tid) {
        const inst = { model, idx: model.entities.length ? 0 : -1 };

        const search = el('input', { type: 'search', class: 'search-input', value: model.query, placeholder: `Search ${model.shortTitle}…`, 'aria-label': `Search ${model.shortTitle} display`, 'data-testid': `${tid}-search` });
        const prev = el('button', { type: 'button', class: 'car-btn', 'aria-label': 'Previous entry', 'data-testid': `${tid}-prev`, text: '‹' });
        const next = el('button', { type: 'button', class: 'car-btn', 'aria-label': 'Next entry', 'data-testid': `${tid}-next`, text: '›' });
        const sidePrev = el('button', { type: 'button', class: 'car-side', tabindex: '-1', 'aria-hidden': 'true' });
        const sideNext = el('button', { type: 'button', class: 'car-side', tabindex: '-1', 'aria-hidden': 'true' });
        const current = el('span', { class: 'car-current', 'aria-live': 'polite', 'data-testid': `${tid}-current` });
        const track = el('div', { class: 'car-track' }, sidePrev, current, sideNext);
        const carousel = el('div', { class: 'carousel', role: 'group', 'aria-label': `${model.shortTitle} carousel` }, prev, track, next);
        const select = el('select', { class: 'fancy-select', 'aria-label': `Choose entry in ${model.shortTitle}`, 'data-testid': `${tid}-select` });
        const bar = el('div', { class: 'display-bar' }, search, carousel, select);
        const featured = el('article', { class: 'featured', 'data-testid': `${tid}-featured` });
        const grid = el('div', { class: 'tile-grid' });
        const root = el('div', { class: 'display' }, bar, featured, grid);

        model.entities.forEach(e => {
            const t = el('button', { type: 'button', class: 'tile', 'data-testid': `${tid}-tile`, 'aria-label': `Select ${e.name}` },
                el('span', { class: 'glyph lg', style: `--h:${hue(e.name)}`, 'aria-hidden': 'true', text: initials(e.name) }),
                el('span', {}, el('span', { class: 'tile-name', text: e.name }), el('br'), el('span', { class: 'tile-sub', text: e.sub })),
                e.popLabel ? el('span', { class: e.popClass, text: e.popLabel }) : el('span', { class: 'tile-blurb', text: e.blurb }));
            t.addEventListener('click', () => { inst.select(e.i); featured.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); });
            e.tiles = e.tiles || new Map();
            e.tiles.set(inst, t);
            grid.append(t);
        });

        const visible = () => model.entities.filter(e => e.match);
        const step = d => {
            const vis = visible();
            if (!vis.length) return;
            const pos = Math.max(0, vis.findIndex(e => e.i === inst.idx));
            inst.select(vis[(pos + d + vis.length) % vis.length].i);
        };

        inst.select = i => { inst.idx = i; inst.render(); };

        inst.render = () => {
            const vis = visible();
            if (!vis.length) {
                current.textContent = 'No matches';
                sidePrev.textContent = sideNext.textContent = '';
                select.replaceChildren();
                featured.replaceChildren(el('p', { class: 'empty-note', text: 'No entries match your search.' }));
                model.entities.forEach(e => e.tiles.get(inst).hidden = true);
                return;
            }
            let pos = vis.findIndex(e => e.i === inst.idx);
            if (pos < 0) { pos = 0; inst.idx = vis[0].i; }
            const cur = vis[pos];
            const n = vis.length;

            current.replaceChildren(glyph(cur.name), document.createTextNode(cur.name));
            sidePrev.textContent = n > 1 ? vis[(pos - 1 + n) % n].name : '';
            sideNext.textContent = n > 1 ? vis[(pos + 1) % n].name : '';
            prev.disabled = next.disabled = n < 2;

            select.replaceChildren(...vis.map(e => el('option', { value: String(e.i), text: e.name })));
            select.value = String(cur.i);

            const dl = el('dl', { class: 'featured-fields' });
            cur.fields.slice(1).forEach(f => {
                if (!f.label || !f.text) return;
                dl.append(el('div', {}, el('dt', { text: f.label }), el('dd', {}, cloneCell(f.cell))));
            });
            featured.replaceChildren(
                el('div', { class: 'featured-head' }, glyph(cur.name, true),
                    el('div', {}, el('h3', { text: cur.name }), el('span', { class: 'featured-sub', text: cur.sub })),
                    cur.popLabel ? el('span', { class: cur.popClass, text: cur.popLabel }) : null),
                dl,
                el('div', { class: 'featured-actions' },
                    el('button', { type: 'button', class: 'chip-btn', 'data-testid': `${tid}-details`, text: 'Open full details', onclick: () => cur.trigger && cur.trigger.click() }),
                    el('button', { type: 'button', class: 'chip-btn', 'data-testid': `${tid}-in-table`, text: 'Show in table', onclick: () => goTo(model.id, { entity: cur.i, view: 'table' }) })));

            model.entities.forEach(e => {
                const t = e.tiles.get(inst);
                t.hidden = !e.match;
                t.classList.toggle('active', e === cur);
                t.setAttribute('aria-pressed', String(e === cur));
            });
        };

        prev.addEventListener('click', () => step(-1));
        next.addEventListener('click', () => step(1));
        sidePrev.addEventListener('click', () => step(-1));
        sideNext.addEventListener('click', () => step(1));
        select.addEventListener('change', () => inst.select(Number(select.value)));
        model.inputs.add(search);
        search.addEventListener('input', () => setQuery(model, search.value));

        inst.el = root;
        inst.destroy = () => { model.displays.delete(inst); model.inputs.delete(search); model.entities.forEach(e => e.tiles.delete(inst)); };
        model.displays.add(inst);
        inst.render();
        return inst;
    }

    /* ------------------------------------------------------------------ *
     * Global bar, single-view panel, results
     * ------------------------------------------------------------------ */
    const main = $('main');
    main.dataset.mode = 'multi';

    const btnMulti = el('button', { type: 'button', 'aria-pressed': 'true', 'data-testid': 'mode-multi', text: 'Multi view' });
    const btnSingle = el('button', { type: 'button', 'aria-pressed': 'false', 'data-testid': 'mode-single', text: 'Single view' });
    const modeSeg = el('div', { class: 'seg', role: 'group', 'aria-label': 'Data layout' }, btnMulti, btnSingle);
    const gSearch = el('input', { type: 'search', class: 'search-input', placeholder: 'Search every table…', 'aria-label': 'Search all data', 'data-testid': 'global-search' });
    const expandAll = el('button', { type: 'button', class: 'chip-btn multi-only', 'data-testid': 'expand-all', text: 'Expand all' });
    const collapseAll = el('button', { type: 'button', class: 'chip-btn multi-only', 'data-testid': 'collapse-all', text: 'Collapse all' });
    const bar = el('div', { class: 'global-bar', id: 'data' }, el('span', { class: 'bar-title', text: 'Data' }), modeSeg, el('div', { class: 'global-search' }, gSearch), expandAll, collapseAll);
    const results = el('div', { class: 'global-results', hidden: true, 'data-testid': 'global-results', 'aria-live': 'polite' });

    const sectionSelect = el('select', { class: 'fancy-select', id: 'single-section-select', 'data-testid': 'single-section-select', 'aria-label': 'Choose table' },
        models.map(m => el('option', { value: m.id, text: m.title })));
    const singleHost = el('div', { 'data-testid': 'single-host' });
    const singlePanel = el('div', { class: 'single-panel', hidden: true, 'data-testid': 'single-panel' },
        el('div', { class: 'single-head' }, el('label', { for: 'single-section-select', text: 'Table' }), sectionSelect), singleHost);

    const firstIntro = $(':scope > p', main);
    (firstIntro || main.firstChild).after(bar, results, singlePanel);

    let single = { inst: null, id: null };

    function showSingle(id, entityIdx) {
        const model = byId[id];
        if (!model) return;
        if (single.inst) single.inst.destroy();
        single.id = id;
        sectionSelect.value = id;
        single.inst = createDisplay(model, 'single');
        singleHost.replaceChildren(single.inst.el);
        if (entityIdx != null) single.inst.select(entityIdx);
    }

    function setMode(mode) {
        main.dataset.mode = mode;
        btnMulti.setAttribute('aria-pressed', String(mode === 'multi'));
        btnSingle.setAttribute('aria-pressed', String(mode === 'single'));
        singlePanel.hidden = mode !== 'single';
        if (mode === 'single') showSingle(single.id || models[0].id);
        else if (single.inst) { single.inst.destroy(); single.inst = null; singleHost.replaceChildren(); }
    }

    btnMulti.addEventListener('click', () => setMode('multi'));
    btnSingle.addEventListener('click', () => setMode('single'));
    sectionSelect.addEventListener('change', () => showSingle(sectionSelect.value));
    expandAll.addEventListener('click', () => models.forEach(m => { m.details.open = true; }));
    collapseAll.addEventListener('click', () => models.forEach(m => { m.details.open = false; }));

    function renderResults() {
        const q = gSearch.value.trim().toLowerCase();
        results.replaceChildren();
        if (!q) { results.hidden = true; return; }
        const hits = [];
        models.forEach(m => m.entities.forEach(e => { if (e.text.includes(q)) hits.push(e); }));
        results.hidden = false;
        results.append(el('p', { class: 'results-summary', text: hits.length ? `${hits.length} result${hits.length === 1 ? '' : 's'} across ${new Set(hits.map(h => h.model.id)).size} table(s) — click one to open it.` : 'No results.' }));
        hits.slice(0, 60).forEach(e => {
            const mini = el('dl', { class: 'result-fields' });
            e.fields.slice(1).filter(f => f.label && f.text && f.label !== 'Download Link' && f.label !== 'FAQ / KB').slice(0, 3)
                .forEach(f => mini.append(el('div', {}, el('b', { text: f.label + ': ' }), clip(f.text, 70))));
            const card = el('button', { type: 'button', class: 'result-card', 'data-testid': 'result-card', 'aria-label': `Open ${e.name} in ${e.model.shortTitle}` },
                el('span', { class: 'result-section', text: e.model.shortTitle }),
                el('span', { class: 'result-head' }, glyph(e.name), el('span', { class: 'result-name', text: e.name }), e.popLabel ? el('span', { class: e.popClass, text: e.popLabel }) : null),
                mini, el('span', { class: 'result-go', text: 'Go to page →' }));
            card.addEventListener('click', () => {
                gSearch.value = '';
                renderResults();
                goTo(e.model.id, { entity: e.i });
            });
            results.append(card);
        });
    }
    gSearch.addEventListener('input', renderResults);
    gSearch.addEventListener('keydown', ev => { if (ev.key === 'Escape') { gSearch.value = ''; renderResults(); } });

    /* ------------------------------------------------------------------ *
     * Navigation
     * ------------------------------------------------------------------ */
    function goTo(id, opts = {}) {
        const model = byId[id];
        if (!model) return;
        const { entity, view } = opts;
        if (view) model.setView(view);
        if (view === 'table' && main.dataset.mode === 'single') setMode('multi');

        if (main.dataset.mode === 'single') {
            if (single.id !== id || !single.inst) showSingle(id);
            if (entity != null) single.inst.select(entity);
            singlePanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
            return;
        }

        model.details.open = true;
        if (model.view === 'display' && model.mainDisplay && entity != null) model.mainDisplay.select(entity);
        const e = entity != null ? model.entities[entity] : null;
        let target = model.details;
        if (e && model.view === 'table') target = mobile.matches ? e.cell : e.row;
        if (e && model.view === 'display') target = model.viewDisplay;
        if (e && model.query && !e.match) setQuery(model, '');
        requestAnimationFrame(() => {
            target.scrollIntoView({ behavior: 'smooth', block: e && model.view === 'table' ? 'center' : 'start' });
            if (e && model.view === 'table') {
                target.classList.remove('flash');
                void target.offsetWidth;
                target.classList.add('flash');
            }
        });
    }

    /* ------------------------------------------------------------------ *
     * Table of contents tree
     * ------------------------------------------------------------------ */
    const dataHeader = $('.toc-node-header');
    const tocList = $('#toc-data-list');
    dataHeader.addEventListener('click', () => {
        const open = dataHeader.getAttribute('aria-expanded') === 'true';
        dataHeader.setAttribute('aria-expanded', String(!open));
        tocList.hidden = open;
    });

    $$('li', tocList).forEach(li => {
        const a = $('a', li);
        const id = (a.getAttribute('href') || '').slice(1);
        const model = byId[id];
        if (!model) return;

        const toggle = el('button', { type: 'button', class: 'toc-expand', 'aria-expanded': 'false', 'aria-label': `Show entries in ${model.shortTitle}`, 'data-testid': `toc-expand-${id}`, text: '▸' });
        const box = el('div', { class: 'toc-entities', hidden: true, 'data-testid': `toc-entities-${id}` });
        li.prepend(el('div', { class: 'toc-row' }, a, toggle));
        li.append(box);

        a.addEventListener('click', ev => {
            ev.preventDefault();
            history.replaceState(null, '', '#' + id);
            goTo(id);
        });
        toggle.addEventListener('click', () => {
            const open = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!open));
            box.hidden = open;
            if (!open && !box.childElementCount) {
                model.entities.forEach(e => {
                    const name = el('button', { type: 'button', class: 'toc-entity-name', title: e.name, 'data-testid': `toc-entity-${id}`, text: e.name });
                    name.addEventListener('click', () => goTo(id, { entity: e.i }));
                    const t = el('button', { type: 'button', class: 'toc-mini', title: `${e.name} in table`, 'aria-label': `Show ${e.name} in table`, text: '▤' });
                    t.addEventListener('click', () => goTo(id, { entity: e.i, view: 'table' }));
                    const g = el('button', { type: 'button', class: 'toc-mini', title: `${e.name} in display`, 'aria-label': `Show ${e.name} in display`, text: '◧' });
                    g.addEventListener('click', () => goTo(id, { entity: e.i, view: 'display' }));
                    box.append(el('div', { class: 'toc-entity' }, name, t, g));
                });
            }
        });
    });

    /* ------------------------------------------------------------------ *
     * Footer dialogs, hash routing
     * ------------------------------------------------------------------ */
    $$('[data-dialog]').forEach(b => b.addEventListener('click', () => $('#' + b.dataset.dialog).showModal()));
    $$('.info-dialog').forEach(d => {
        $('[data-close]', d).addEventListener('click', () => d.close());
        d.addEventListener('click', ev => { if (ev.target === d) d.close(); });
    });
    const year = $('#copyright-year');
    if (year) year.textContent = String(new Date().getFullYear());

    function routeHash() {
        const id = decodeURIComponent(location.hash.slice(1));
        if (byId[id]) goTo(id);
    }
    window.addEventListener('hashchange', routeHash);
    routeHash();

    // Expose a small API for tests / debugging.
    window.DevMatrix = { models, goTo, setMode };
})();
