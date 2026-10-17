/* DevMatrix analytics base: consent banner, interaction log, visit counter.
   Static hosting (GitHub Pages) has no server logs, so everything is collected
   client-side and only after the visitor accepts. Configure via
   window.DEVMATRIX_ANALYTICS = { endpoint, counter: { base, namespace, key } }.
   - endpoint: optional URL (your own Worker / Supabase / Firebase function) that
     receives batches of events via navigator.sendBeacon. Null = keep local only. */
(() => {
    'use strict';

    const CFG = Object.assign({ endpoint: null, counter: null, maxLog: 500, flushMs: 15000 }, window.DEVMATRIX_ANALYTICS || {});
    const LOG_KEY = 'dm_event_log';
    const COOKIE = 'dm_consent';

    const getCookie = n => (document.cookie.split('; ').find(c => c.startsWith(n + '=')) || '').split('=')[1] || '';
    const setCookie = (n, v) => { document.cookie = `${n}=${v}; max-age=${60 * 60 * 24 * 180}; path=/; SameSite=Lax`; };
    const consent = () => getCookie(COOKIE) || (localStorage.getItem(COOKIE) || '');
    const granted = () => consent() === 'granted';
    const storeConsent = v => { setCookie(COOKIE, v); try { localStorage.setItem(COOKIE, v); } catch (_) { /* ignore */ } };

    const sid = () => {
        let s = sessionStorage.getItem('dm_sid');
        if (!s) { s = (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2)); sessionStorage.setItem('dm_sid', s); }
        return s;
    };

    /* ---------------- Log ---------------- */
    let memory = [];
    let queue = [];
    try { memory = JSON.parse(localStorage.getItem(LOG_KEY) || '[]'); } catch (_) { memory = []; }

    function log(type, data = {}) {
        if (!granted()) return;
        const ev = { t: new Date().toISOString(), session: sid(), type, page: location.pathname + location.hash, ...data };
        memory.push(ev);
        if (memory.length > CFG.maxLog) memory = memory.slice(-CFG.maxLog);
        try { localStorage.setItem(LOG_KEY, JSON.stringify(memory)); } catch (_) { /* quota */ }
        if (CFG.endpoint) queue.push(ev);
        refreshLogView();
    }

    function flush() {
        if (!CFG.endpoint || !queue.length || !granted()) return;
        const body = JSON.stringify(queue);
        queue = [];
        if (!(navigator.sendBeacon && navigator.sendBeacon(CFG.endpoint, body))) {
            fetch(CFG.endpoint, { method: 'POST', body, keepalive: true, headers: { 'Content-Type': 'text/plain' } }).catch(() => {});
        }
    }
    setInterval(flush, CFG.flushMs);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); });

    const idOf = el => {
        const c = el.closest('[data-automation-id]');
        return c ? c.getAttribute('data-automation-id') : (el.tagName || '').toLowerCase();
    };

    document.addEventListener('click', ev => {
        const c = ev.target.closest('button, a, summary, input, select, [data-automation-id]');
        if (!c || c.closest('.cookie-banner')) return;
        if (c.matches('input, select')) return; // logged via input/change
        if (c.classList.contains('skull-key')) return log('easter_egg', { id: idOf(c) });
        log('click', { id: idOf(c) });
    }, true);

    const timers = new WeakMap();
    document.addEventListener('input', ev => {
        const t = ev.target;
        if (!t.matches || !t.matches('input[type="search"]')) return;
        clearTimeout(timers.get(t));
        timers.set(t, setTimeout(() => { if (t.value.trim()) log('search', { id: idOf(t), query: t.value.trim().slice(0, 80) }); }, 700));
    }, true);

    document.addEventListener('change', ev => {
        const t = ev.target;
        if (t.matches && t.matches('select')) log('select', { id: idOf(t), value: t.value });
    }, true);

    document.addEventListener('toggle', ev => {
        const d = ev.target;
        if (d.tagName === 'DETAILS' && d.classList.contains('data-section')) {
            log('toggle', { id: idOf(d.querySelector(':scope > summary')), open: d.open });
        }
    }, true);

    /* ---------------- Visit counter ---------------- */
    async function counter() {
        const out = document.getElementById('site-counter-value');
        const c = CFG.counter;
        if (!out || !c) { if (out) out.textContent = '—'; return; }
        const hit = granted() && !sessionStorage.getItem('dm_counted');
        const url = `${c.base}/${hit ? 'hit' : 'get'}/${encodeURIComponent(c.namespace)}/${encodeURIComponent(c.key)}`;
        const ctl = new AbortController();
        const timer = setTimeout(() => ctl.abort(), 5000);
        try {
            const res = await fetch(url, { signal: ctl.signal });
            if (!res.ok) throw new Error(res.status);
            const data = await res.json();
            if (hit) sessionStorage.setItem('dm_counted', '1');
            out.textContent = Number(data.value ?? data.count).toLocaleString();
        } catch (_) {
            out.textContent = '—';
        } finally { clearTimeout(timer); }
    }

    /* ---------------- Banner ---------------- */
    function el(tag, attrs = {}, text) {
        const n = document.createElement(tag);
        Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
        if (text) n.textContent = text;
        return n;
    }

    let banner;
    function showBanner() {
        banner = el('div', { class: 'cookie-banner', role: 'region', 'aria-label': 'Cookie consent', 'data-testid': 'cookie-banner' });
        const msg = el('p', {}, 'This site uses a first-party cookie and local storage to remember your choice and record anonymous interactions (clicks, searches, layout changes) for statistics, plus a third-party visit counter. ');
        const more = el('button', { type: 'button', class: 'footer-link', 'data-dialog': 'privacy-dialog', 'data-testid': 'cookie-details' }, 'Details');
        msg.append(more);
        const accept = el('button', { type: 'button', class: 'chip-btn cookie-accept', 'data-testid': 'cookie-accept' }, 'Accept');
        const decline = el('button', { type: 'button', class: 'chip-btn', 'data-testid': 'cookie-decline' }, 'Decline');
        const actions = el('div', { class: 'cookie-actions' });
        actions.append(accept, decline);
        banner.append(msg, actions);
        document.body.append(banner);
        more.addEventListener('click', openPrivacy);
        accept.addEventListener('click', () => setConsent('granted'));
        decline.addEventListener('click', () => setConsent('denied'));
    }

    function setConsent(v) {
        storeConsent(v);
        if (banner) { banner.remove(); banner = null; }
        if (v === 'granted') { log('consent', { value: v }); log('page_view'); counter(); }
        else { memory = []; localStorage.removeItem(LOG_KEY); queue = []; }
        refreshLogView();
    }

    /* ---------------- Privacy & Log dialog ---------------- */
    let dlg, status, tbody;
    function ensureDialog() {
        if (dlg) return;
        dlg = el('dialog', { id: 'privacy-dialog', class: 'info-dialog map-dialog', 'aria-labelledby': 'privacy-title' });
        dlg.innerHTML = `
            <div class="product-dialog-header"><h2 id="privacy-title">Privacy &amp; Interaction Log</h2>
                <button class="product-dialog-close" type="button" aria-label="Close privacy dialog" data-testid="privacy-close">&times;</button></div>
            <div class="info-body">
                <p>Consent status: <strong data-testid="consent-status"></strong></p>
                <p>With consent, this page logs interaction type, the control's automation ID, search terms and a random session ID. No names or e-mail addresses. The log is stored in your browser${CFG.endpoint ? ' and sent to the site owner' : ' only'}.</p>
                <div class="map-meta">
                    <button type="button" class="chip-btn" data-testid="privacy-accept">Accept</button>
                    <button type="button" class="chip-btn" data-testid="privacy-decline">Decline &amp; erase log</button>
                    <button type="button" class="chip-btn" data-testid="log-download">Download log</button>
                    <button type="button" class="chip-btn" data-testid="log-clear">Clear log</button>
                </div>
                <div class="map-scroll"><table class="map-table compact"><thead><tr><th>Time</th><th>Event</th><th>Control / Detail</th></tr></thead><tbody data-testid="log-rows"></tbody></table></div>
            </div>`;
        document.body.append(dlg);
        status = dlg.querySelector('[data-testid="consent-status"]');
        tbody = dlg.querySelector('tbody');
        dlg.querySelector('.product-dialog-close').addEventListener('click', () => dlg.close());
        dlg.addEventListener('click', ev => { if (ev.target === dlg) dlg.close(); });
        dlg.querySelector('[data-testid="privacy-accept"]').addEventListener('click', () => setConsent('granted'));
        dlg.querySelector('[data-testid="privacy-decline"]').addEventListener('click', () => setConsent('denied'));
        dlg.querySelector('[data-testid="log-clear"]').addEventListener('click', () => { memory = []; localStorage.removeItem(LOG_KEY); refreshLogView(); });
        dlg.querySelector('[data-testid="log-download"]').addEventListener('click', () => {
            const blob = new Blob([JSON.stringify(memory, null, 2)], { type: 'application/json' });
            const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: 'interaction-log.json' });
            a.click();
            URL.revokeObjectURL(a.href);
        });
    }

    function refreshLogView() {
        if (!dlg) return;
        status.textContent = { granted: 'Accepted', denied: 'Declined' }[consent()] || 'Not chosen yet';
        tbody.replaceChildren(...memory.slice(-100).reverse().map(ev => {
            const tr = document.createElement('tr');
            [ev.t.replace('T', ' ').slice(0, 19), ev.type, ev.id ? (ev.query ? `${ev.id} — "${ev.query}"` : ev.id) : (ev.value || ev.page)].forEach(v => {
                const td = document.createElement('td'); td.textContent = v; tr.append(td);
            });
            return tr;
        }));
    }

    function openPrivacy() {
        ensureDialog();
        refreshLogView();
        if (!dlg.open) dlg.showModal();
    }
    // Footer button is wired by the UI script; this guarantees the dialog exists first.
    document.addEventListener('click', ev => {
        if (ev.target.closest('[data-dialog="privacy-dialog"]')) { ensureDialog(); refreshLogView(); }
    }, true);

    /* ---------------- Start ---------------- */
    if (!consent()) showBanner();
    if (granted()) log('page_view');
    counter();

    window.DevMatrixAnalytics = { log, flush, getLog: () => memory.slice(), consent };
})();
