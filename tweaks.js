/* Tweaks panel - vanilla JS, no framework. Activated by __activate_edit_mode postMessage. */
(function () {
  const CSS = `
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    transform:scale(var(--dc-inv-zoom,1));transform-origin:bottom right;
    background:rgba(250,249,247,.78);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;
    padding:10px 8px 10px 14px;cursor:move;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);
    width:22px;height:22px;border-radius:6px;cursor:default;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;
    overflow-y:auto;overflow-x:hidden;min-height:0;
    scrollbar-width:thin;scrollbar-color:rgba(0,0,0,.15) transparent}
  .twk-body::-webkit-scrollbar{width:8px}
  .twk-body::-webkit-scrollbar-track{background:transparent;margin:2px}
  .twk-body::-webkit-scrollbar-thumb{background:rgba(0,0,0,.15);border-radius:4px;
    border:2px solid transparent;background-clip:content-box}
  .twk-body::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,.25);
    border:2px solid transparent;background-clip:content-box}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-row-h{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;
    color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}
  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;
    background:rgba(0,0,0,.06);user-select:none}
  .twk-seg-thumb{position:absolute;top:2px;bottom:2px;border-radius:6px;
    background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12);
    transition:left .15s cubic-bezier(.3,.7,.4,1),width .15s}
  .twk-seg.dragging .twk-seg-thumb{transition:none}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;
    background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;
    border-radius:6px;cursor:default;padding:4px 6px;line-height:1.2;
    overflow-wrap:anywhere}
  .twk-toggle{position:relative;width:32px;height:18px;border:0;border-radius:999px;
    background:rgba(0,0,0,.15);transition:background .15s;cursor:default;padding:0}
  .twk-toggle[data-on="1"]{background:#34c759}
  .twk-toggle i{position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
    background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.25);transition:transform .15s}
  .twk-toggle[data-on="1"] i{transform:translateX(14px)}
`;

  const mk = (tag, cls, txt) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt !== undefined) e.textContent = txt;
    return e;
  };

  let panel = null, rObs = null, offR = 16, offB = 16;

  function clamp() {
    if (!panel) return;
    const PAD = 16;
    offR = Math.min(Math.max(PAD, offR), Math.max(PAD, window.innerWidth  - panel.offsetWidth  - PAD));
    offB = Math.min(Math.max(PAD, offB), Math.max(PAD, window.innerHeight - panel.offsetHeight - PAD));
    panel.style.right  = offR + 'px';
    panel.style.bottom = offB + 'px';
  }

  function seg(opts, cur, cb) {
    const n = opts.length;
    const wrap = mk('div', 'twk-seg');
    wrap.setAttribute('role', 'radiogroup');
    const thumb = mk('div', 'twk-seg-thumb');
    wrap.appendChild(thumb);
    const btns = opts.map(o => {
      const b = mk('button', null, o.label); b.type = 'button';
      b.setAttribute('role', 'radio'); wrap.appendChild(b); return b;
    });
    function set(val) {
      const i = Math.max(0, opts.findIndex(o => o.value === val));
      thumb.style.left  = `calc(2px + ${i} * (100% - 4px) / ${n})`;
      thumb.style.width = `calc((100% - 4px) / ${n})`;
      btns.forEach((b, j) => b.setAttribute('aria-checked', String(j === i)));
    }
    set(cur);
    function pick(x) {
      const r = wrap.getBoundingClientRect();
      return opts[Math.max(0, Math.min(n - 1, Math.floor(((x - r.left - 2) / (r.width - 4)) * n)))].value;
    }
    wrap.addEventListener('pointerdown', e => {
      wrap.classList.add('dragging');
      const v0 = pick(e.clientX); if (v0 !== cur) { cur = v0; set(v0); cb(v0); }
      const mv = ev => { const v = pick(ev.clientX); if (v !== cur) { cur = v; set(v); cb(v); } };
      const up = () => { wrap.classList.remove('dragging'); window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); };
      window.addEventListener('pointermove', mv);
      window.addEventListener('pointerup', up);
    });
    return wrap;
  }

  function tog(cur, cb) {
    const btn = mk('button', 'twk-toggle'); btn.type = 'button';
    btn.setAttribute('role', 'switch'); btn.appendChild(mk('i'));
    function set(v) { btn.setAttribute('data-on', v ? '1' : '0'); btn.setAttribute('aria-checked', String(v)); }
    set(cur);
    btn.addEventListener('click', () => { cur = !cur; set(cur); cb(cur); });
    return btn;
  }

  function row(label, ctrl, inline) {
    const d = mk('div', inline ? 'twk-row twk-row-h' : 'twk-row');
    const lbl = mk('div', 'twk-lbl'); lbl.appendChild(mk('span', null, label));
    d.appendChild(lbl); d.appendChild(ctrl); return d;
  }

  function build() {
    const ZM = window.ZM;
    panel = mk('div', 'twk-panel');
    panel.setAttribute('data-noncommentable', '');
    panel.style.right = offR + 'px'; panel.style.bottom = offB + 'px';

    const hd = mk('div', 'twk-hd');
    hd.appendChild(mk('b', null, 'Tweaks'));
    const x = mk('button', 'twk-x', '✕'); x.type = 'button';
    x.setAttribute('aria-label', 'Close tweaks');
    x.addEventListener('mousedown', e => e.stopPropagation());
    x.addEventListener('click', dismiss);
    hd.appendChild(x);

    hd.addEventListener('mousedown', e => {
      const r = panel.getBoundingClientRect();
      const sx = e.clientX, sy = e.clientY;
      const sr = window.innerWidth - r.right, sb = window.innerHeight - r.bottom;
      const mv = ev => { offR = sr - (ev.clientX - sx); offB = sb - (ev.clientY - sy); clamp(); };
      const up = () => { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); };
      window.addEventListener('mousemove', mv);
      window.addEventListener('mouseup', up);
    });

    panel.appendChild(hd);
    const body = mk('div', 'twk-body');

    body.appendChild(mk('div', 'twk-sect', 'Appearance'));
    body.appendChild(row('Theme', seg(
      [{label:'Light',value:'light'},{label:'Dark',value:'dark'},{label:'System',value:'system'}],
      ZM?.getTheme() || 'system', v => ZM?.setTheme(v)
    )));
    body.appendChild(row('Density', seg(
      [{label:'Compact',value:'compact'},{label:'Comfy',value:'comfy'},{label:'Airy',value:'airy'}],
      ZM?.getDensity() || 'comfy', v => ZM?.setDensity(v)
    )));

    body.appendChild(mk('div', 'twk-sect', 'Article list'));
    body.appendChild(row('Style', seg(
      [{label:'List',value:'list'},{label:'Cards',value:'cards'},{label:'Table',value:'table'}],
      ZM?.getListStyle() || 'list', v => ZM?.setListStyle(v)
    )));
    body.appendChild(row('Show reading time', tog(ZM?.getReadtime() ?? true, v => ZM?.setReadtime(v)), true));

    panel.appendChild(body);
  }

  function show() {
    if (panel) return;
    build();
    document.body.appendChild(panel);
    clamp();
    if (typeof ResizeObserver !== 'undefined') {
      rObs = new ResizeObserver(clamp);
      rObs.observe(document.documentElement);
    }
  }

  function hide() {
    if (!panel) return;
    if (rObs) { rObs.disconnect(); rObs = null; }
    panel.remove(); panel = null;
  }

  function dismiss() {
    hide();
    window.parent.postMessage({ type: '__edit_mode_dismissed' }, '*');
  }

  const s = document.createElement('style');
  s.textContent = CSS;
  document.head.appendChild(s);

  window.addEventListener('message', e => {
    const t = e?.data?.type;
    if (t === '__activate_edit_mode') show();
    else if (t === '__deactivate_edit_mode') hide();
  });

  window.parent.postMessage({ type: '__edit_mode_available' }, '*');
})();
