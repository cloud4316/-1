/* ============================================================
   CircuitBuilder — самостоятельный редактор схем для Arduino
   ============================================================ */

'use strict';

// ── Компоненты ───────────────────────────────────────────────────────────────

const CT = {  // Component Types
  arduino_uno: {
    name: 'Arduino Uno', category: 'mcu', icon: '🟦',
    w: 200, h: 260,
    color: '#1a659e',
    props: {},
    pins: [
      // Цифровые пины — правая сторона
      {id:'d13',x:200,y:28,lbl:'~13'}, {id:'d12',x:200,y:48,lbl:'12'},
      {id:'d11',x:200,y:68,lbl:'~11'}, {id:'d10',x:200,y:88,lbl:'~10'},
      {id:'d9', x:200,y:108,lbl:'~9'},  {id:'d8', x:200,y:128,lbl:'8'},
      {id:'d7', x:200,y:148,lbl:'7'},   {id:'d6', x:200,y:168,lbl:'~6'},
      {id:'d5', x:200,y:188,lbl:'~5'},  {id:'d4', x:200,y:208,lbl:'4'},
      {id:'d3', x:200,y:228,lbl:'~3'},  {id:'d2', x:200,y:248,lbl:'2'},
      // Аналоговые пины — левая сторона
      {id:'a0',x:0,y:148,lbl:'A0'}, {id:'a1',x:0,y:168,lbl:'A1'},
      {id:'a2',x:0,y:188,lbl:'A2'}, {id:'a3',x:0,y:208,lbl:'A3'},
      {id:'a4',x:0,y:228,lbl:'A4 SDA'}, {id:'a5',x:0,y:248,lbl:'A5 SCL'},
      // Питание
      {id:'5v', x:0,y:28,lbl:'5V',  type:'vcc'},
      {id:'33v',x:0,y:48,lbl:'3.3V',type:'vcc'},
      {id:'gnd1',x:0,y:68,lbl:'GND',type:'gnd'},
      {id:'gnd2',x:0,y:88,lbl:'GND',type:'gnd'},
      {id:'rst', x:0,y:108,lbl:'RST'},
      {id:'vin', x:0,y:128,lbl:'VIN'},
    ],
    render(c) {
      return `<rect x="0" y="0" width="${c.w}" height="${c.h}" rx="6"
              fill="#1a659e" stroke="#0d4a7a" stroke-width="2"/>
        <rect x="4" y="4" width="${c.w-8}" height="${c.h-8}" rx="4"
              fill="none" stroke="#4a9cd0" stroke-width="1" opacity="0.4"/>
        <text x="${c.w/2}" y="14" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">Arduino</text>
        <text x="${c.w/2}" y="26" text-anchor="middle" fill="#93c5fd" font-size="8">UNO</text>
        ${c.type.pins.filter(p=>p.x===200).map(p=>`
          <line x1="${c.w-12}" y1="${p.y}" x2="${c.w}" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="${c.w-12}" y="${p.y-5}" width="10" height="10" rx="2" fill="#1e3a5f"/>
          <text x="${c.w-14}" y="${p.y+3}" text-anchor="end" fill="#93c5fd" font-size="7">${p.lbl}</text>
        `).join('')}
        ${c.type.pins.filter(p=>p.x===0).map(p=>`
          <line x1="0" y1="${p.y}" x2="12" y2="${p.y}" stroke="#93c5fd" stroke-width="1.5"/>
          <rect x="2" y="${p.y-5}" width="10" height="10" rx="2" fill="#1e3a5f"/>
          <text x="14" y="${p.y+3}" fill="#93c5fd" font-size="7">${p.lbl}</text>
        `).join('')}`;
    }
  },

  resistor: {
    name: 'Резистор', category: 'passive', icon: '⊓',
    w: 80, h: 30,
    color: '#78350f',
    props: {value: '220 Ω'},
    pins: [{id:'a',x:0,y:15,lbl:''},{id:'b',x:80,y:15,lbl:''}],
    render(c) {
      const v = c.props.value || '?Ω';
      return `<line x1="0" y1="15" x2="20" y2="15" stroke="#d97706" stroke-width="2"/>
        <line x1="60" y1="15" x2="80" y2="15" stroke="#d97706" stroke-width="2"/>
        <rect x="20" y="6" width="40" height="18" rx="3" fill="#92400e" stroke="#d97706" stroke-width="1.5"/>
        <line x1="26" y1="6" x2="26" y2="24" stroke="#fbbf24" stroke-width="3" opacity="0.8"/>
        <line x1="32" y1="6" x2="32" y2="24" stroke="#ef4444" stroke-width="3" opacity="0.8"/>
        <line x1="40" y1="6" x2="40" y2="24" stroke="#fbbf24" stroke-width="3" opacity="0.8"/>
        <line x1="48" y1="6" x2="48" y2="24" stroke="#a3a3a3" stroke-width="3" opacity="0.8"/>
        <text x="40" y="38" text-anchor="middle" fill="#d97706" font-size="9">${v}</text>`;
    }
  },

  led: {
    name: 'Светодиод', category: 'passive', icon: '💡',
    w: 60, h: 30,
    color: '#ef4444',
    props: {color: 'red'},
    pins: [{id:'anode',x:0,y:15,lbl:'+'},{id:'cathode',x:60,y:15,lbl:'-'}],
    colorMap: {red:'#ef4444',green:'#22c55e',yellow:'#eab308',blue:'#3b82f6',white:'#e5e7eb'},
    render(c) {
      const col = this.colorMap[c.props.color||'red'] || '#ef4444';
      const lit  = c._lit;
      return `<line x1="0" y1="15" x2="18" y2="15" stroke="${col}" stroke-width="2"/>
        <line x1="42" y1="15" x2="60" y2="15" stroke="${col}" stroke-width="2"/>
        <polygon points="18,5 18,25 38,15" fill="${lit?col:'none'}" stroke="${col}" stroke-width="1.5"/>
        <line x1="38" y1="5" x2="38" y2="25" stroke="${col}" stroke-width="2"/>
        ${lit?`<circle cx="28" cy="15" r="14" fill="${col}" opacity="0.2"/>
          <line x1="40" y1="4" x2="45" y2="0" stroke="${col}" stroke-width="1.5" opacity="0.7"/>
          <line x1="43" y1="7" x2="49" y2="4" stroke="${col}" stroke-width="1.5" opacity="0.7"/>`:''}
        <text x="30" y="38" text-anchor="middle" fill="${col}" font-size="8">${c.props.color||'red'}</text>`;
    }
  },

  button: {
    name: 'Кнопка', category: 'passive', icon: '⏺',
    w: 60, h: 50,
    color: '#6b7280',
    props: {pressed: false},
    pins: [
      {id:'p1',x:0,y:15,lbl:'1'},{id:'p2',x:60,y:15,lbl:'2'},
      {id:'p3',x:0,y:35,lbl:'3'},{id:'p4',x:60,y:35,lbl:'4'},
    ],
    render(c) {
      const pr = c._pressed;
      return `<line x1="0" y1="15" x2="22" y2="15" stroke="#9ca3af" stroke-width="2"/>
        <line x1="38" y1="15" x2="60" y2="15" stroke="#9ca3af" stroke-width="2"/>
        <line x1="0" y1="35" x2="22" y2="35" stroke="#9ca3af" stroke-width="2"/>
        <line x1="38" y1="35" x2="60" y2="35" stroke="#9ca3af" stroke-width="2"/>
        <line x1="22" y1="10" x2="22" y2="40" stroke="#9ca3af" stroke-width="1.5"/>
        <line x1="38" y1="10" x2="38" y2="40" stroke="#9ca3af" stroke-width="1.5"/>
        ${pr
          ? `<line x1="22" y1="15" x2="38" y2="15" stroke="#60a5fa" stroke-width="2"/>
             <line x1="22" y1="35" x2="38" y2="35" stroke="#60a5fa" stroke-width="2"/>`
          : `<line x1="25" y1="20" x2="35" y2="20" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2"/>
             <line x1="25" y1="30" x2="35" y2="30" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2"/>`}
        <rect x="24" y="18" width="12" height="14" rx="2" fill="${pr?'#3b82f6':'#374151'}" stroke="#6b7280" stroke-width="1"/>
        <text x="30" y="58" text-anchor="middle" fill="#9ca3af" font-size="8">BTN</text>`;
    }
  },

  vcc: {
    name: '+5V / VCC', category: 'power', icon: '⚡',
    w: 30, h: 40,
    color: '#ef4444',
    props: {},
    pins: [{id:'out',x:15,y:40,lbl:''}],
    render() {
      return `<line x1="15" y1="20" x2="15" y2="40" stroke="#ef4444" stroke-width="2"/>
        <line x1="5" y1="20" x2="25" y2="20" stroke="#ef4444" stroke-width="2"/>
        <line x1="8" y1="14" x2="22" y2="14" stroke="#ef4444" stroke-width="2"/>
        <line x1="11" y1="8" x2="19" y2="8" stroke="#ef4444" stroke-width="2"/>
        <text x="15" y="5" text-anchor="middle" fill="#ef4444" font-size="8" font-weight="bold">+5V</text>`;
    }
  },

  gnd: {
    name: 'GND', category: 'power', icon: '⏚',
    w: 30, h: 40,
    color: '#6b7280',
    props: {},
    pins: [{id:'in',x:15,y:0,lbl:''}],
    render() {
      return `<line x1="15" y1="0" x2="15" y2="20" stroke="#6b7280" stroke-width="2"/>
        <line x1="5" y1="20" x2="25" y2="20" stroke="#6b7280" stroke-width="2"/>
        <line x1="8" y1="26" x2="22" y2="26" stroke="#6b7280" stroke-width="2"/>
        <line x1="11" y1="32" x2="19" y2="32" stroke="#6b7280" stroke-width="2"/>
        <text x="15" y="44" text-anchor="middle" fill="#6b7280" font-size="8">GND</text>`;
    }
  },

  buzzer: {
    name: 'Зуммер', category: 'passive', icon: '🔔',
    w: 50, h: 50,
    color: '#8b5cf6',
    props: {},
    pins: [{id:'p',x:0,y:25,lbl:'+'},{id:'n',x:50,y:25,lbl:'-'}],
    render(c) {
      const on = c._lit;
      return `<line x1="0" y1="25" x2="12" y2="25" stroke="#8b5cf6" stroke-width="2"/>
        <line x1="38" y1="25" x2="50" y2="25" stroke="#8b5cf6" stroke-width="2"/>
        <circle cx="25" cy="25" r="14" fill="${on?'#4c1d95':'#1e1b4b'}" stroke="#8b5cf6" stroke-width="2"/>
        ${on?`<text x="25" y="30" text-anchor="middle" fill="#a78bfa" font-size="14">♪</text>`
            :`<text x="25" y="29" text-anchor="middle" fill="#7c3aed" font-size="11">BZZ</text>`}
        <text x="25" y="48" text-anchor="middle" fill="#8b5cf6" font-size="8">Зуммер</text>`;
    }
  },

  wire_node: {
    name: 'Узел', category: 'passive', icon: '●',
    w: 10, h: 10,
    color: '#374151',
    props: {},
    pins: [{id:'c',x:5,y:5,lbl:''}],
    render() {
      return `<circle cx="5" cy="5" r="4" fill="#374151" stroke="#6b7280" stroke-width="1"/>`;
    }
  },
};

// Порядок в палитре
const PALETTE_ORDER = [
  ['mcu',     'Микроконтроллеры'],
  ['power',   'Питание'],
  ['passive', 'Компоненты'],
];


// ── Утилиты ──────────────────────────────────────────────────────────────────

let _idSeq = 0;
const uid = () => `c${++_idSeq}_${Date.now().toString(36)}`;
const snap = (v, g) => Math.round(v / g) * g;
const dist2 = (x1,y1,x2,y2) => (x2-x1)**2+(y2-y1)**2;

function absPin(comp, pin) {
  return {x: comp.x + pin.x, y: comp.y + pin.y};
}


// ── Состояние схемы ───────────────────────────────────────────────────────────

class CircuitState {
  constructor() {
    this.components = [];  // {id, type(key), x, y, props, _lit, _pressed}
    this.wires = [];       // {id, from:{compId,pinId}, to:{compId,pinId}, pts:[{x,y},...]}
  }

  addComponent(typeKey, x, y) {
    const t = CT[typeKey];
    if (!t) return null;
    const c = {
      id: uid(), typeKey,
      type: t,           // reference to type definition
      x, y,
      w: t.w, h: t.h,
      props: {...(t.props||{})},
      _lit: false, _pressed: false,
    };
    this.components.push(c);
    this.simulate();
    return c;
  }

  removeComponent(id) {
    this.components = this.components.filter(c => c.id !== id);
    this.wires = this.wires.filter(w => w.from.compId !== id && w.to.compId !== id);
    this.simulate();
  }

  addWire(fromCompId, fromPinId, toCompId, toPinId) {
    if (fromCompId === toCompId) return null;
    const dup = this.wires.find(w =>
      (w.from.compId===fromCompId && w.from.pinId===fromPinId &&
       w.to.compId===toCompId   && w.to.pinId===toPinId) ||
      (w.to.compId===fromCompId && w.to.pinId===fromPinId &&
       w.from.compId===toCompId && w.from.pinId===toPinId)
    );
    if (dup) return null;
    const wire = {
      id: uid(),
      from: {compId: fromCompId, pinId: fromPinId},
      to:   {compId: toCompId,   pinId: toPinId},
    };
    this.wires.push(wire);
    this.simulate();
    return wire;
  }

  removeWire(id) {
    this.wires = this.wires.filter(w => w.id !== id);
    this.simulate();
  }

  getComp(id) { return this.components.find(c => c.id === id); }

  getPin(comp, pinId) {
    if (!comp) return null;
    return comp.type.pins.find(p => p.id === pinId);
  }

  // Строим граф смежности для симуляции
  simulate() {
    // Сброс состояния
    this.components.forEach(c => { c._lit = false; });

    // Граф: каждый пин — вершина; рёбра — провода
    // Ищем VCC-источники и GND
    const nodes = new Map(); // "${compId}:${pinId}" → Set(соседей)
    const key = (cid,pid) => `${cid}:${pid}`;

    for (const c of this.components) {
      for (const p of c.type.pins) {
        nodes.set(key(c.id,p.id), new Set());
      }
    }
    for (const w of this.wires) {
      const k1 = key(w.from.compId, w.from.pinId);
      const k2 = key(w.to.compId, w.to.pinId);
      if (nodes.has(k1)) nodes.get(k1).add(k2);
      if (nodes.has(k2)) nodes.get(k2).add(k1);
    }

    // BFS от всех VCC-источников
    const vccNodes = new Set();
    for (const c of this.components) {
      for (const p of c.type.pins) {
        if (p.type === 'vcc' || c.typeKey === 'vcc') {
          vccNodes.add(key(c.id, p.id));
        }
      }
    }
    const gndNodes = new Set();
    for (const c of this.components) {
      for (const p of c.type.pins) {
        if (p.type === 'gnd' || c.typeKey === 'gnd') {
          gndNodes.add(key(c.id, p.id));
        }
      }
    }

    // Обходим связные компоненты графа
    // Узел «заряжен» если достижим из VCC
    const charged = new Set([...vccNodes]);
    let changed = true;
    while (changed) {
      changed = false;
      for (const [node, nbrs] of nodes) {
        if (charged.has(node)) {
          for (const nb of nbrs) {
            if (!charged.has(nb)) { charged.add(nb); changed = true; }
          }
        }
      }
    }

    // LED светится если anode заряжен И cathode на GND
    // Buzzer аналогично
    for (const c of this.components) {
      if (c.typeKey === 'led') {
        const aKey = key(c.id, 'anode');
        const kKey = key(c.id, 'cathode');
        // cathode должен быть соединён с GND-цепью
        const cathodeGnd = [...(nodes.get(kKey)||[])].some(n => gndNodes.has(n))
          || gndNodes.has(kKey);
        c._lit = charged.has(aKey) && cathodeGnd;
      }
      if (c.typeKey === 'buzzer') {
        const pKey = key(c.id, 'p');
        const nKey = key(c.id, 'n');
        const nGnd = [...(nodes.get(nKey)||[])].some(n => gndNodes.has(n))
          || gndNodes.has(nKey);
        c._lit = charged.has(pKey) && nGnd;
      }
    }
  }

  toJSON() {
    return JSON.stringify({
      components: this.components.map(c => ({
        id: c.id, typeKey: c.typeKey,
        x: c.x, y: c.y, props: c.props
      })),
      wires: this.wires.map(w => ({
        id: w.id,
        from: w.from, to: w.to
      }))
    }, null, 2);
  }

  fromJSON(json) {
    const data = typeof json === 'string' ? JSON.parse(json) : json;
    this.components = [];
    this.wires = [];
    for (const cd of (data.components||[])) {
      const t = CT[cd.typeKey];
      if (!t) continue;
      this.components.push({
        id: cd.id, typeKey: cd.typeKey, type: t,
        x: cd.x, y: cd.y,
        w: t.w, h: t.h,
        props: {...(t.props||{}), ...cd.props},
        _lit: false, _pressed: false,
      });
    }
    for (const wd of (data.wires||[])) {
      this.wires.push({id: wd.id, from: wd.from, to: wd.to});
    }
    this.simulate();
  }
}


// ── Редактор (UI) ─────────────────────────────────────────────────────────────

class CircuitEditor {
  constructor(svgEl, state, opts={}) {
    this.svg   = svgEl;
    this.state = state;
    this.opts  = opts; // {onSave, onSubmit, readonly}
    this.GRID  = 20;
    this.selected = null;  // {type:'comp'|'wire', id}
    this.mode  = 'select'; // 'select' | 'add:<typeKey>' | 'wire'
    this.wire  = null;     // {fromCompId, fromPinId, x1, y1, curX, curY}
    this.drag  = null;     // {compId, ox, oy, mx, my}
    this.vb    = {x:0, y:0, w:1400, h:900}; // viewBox
    this.history = [];   // undo stack (JSON strings)
    this.redoStack = [];

    this._setupSVG();
    this._setupEvents();
    this.render();
  }

  // ── SVG setup ────────────────────────────────────────────────────────────

  _setupSVG() {
    this.svg.setAttribute('width',  '100%');
    this.svg.setAttribute('height', '100%');
    this._applyVB();

    // Слои
    this._layerGrid  = this._mkLayer('layer-grid');
    this._layerWires = this._mkLayer('layer-wires');
    this._layerComps = this._mkLayer('layer-comps');
    this._layerUI    = this._mkLayer('layer-ui');

    this._drawGrid();
  }

  _mkLayer(id) {
    let g = document.getElementById(id);
    if (!g) {
      g = document.createElementNS('http://www.w3.org/2000/svg','g');
      g.id = id;
      this.svg.appendChild(g);
    }
    return g;
  }

  _applyVB() {
    this.svg.setAttribute('viewBox',
      `${this.vb.x} ${this.vb.y} ${this.vb.w} ${this.vb.h}`);
  }

  _drawGrid() {
    const g = this.GRID;
    const W = 4000, H = 4000;
    let html = `<defs>
      <pattern id="smallGrid" width="${g}" height="${g}" patternUnits="userSpaceOnUse">
        <path d="M ${g} 0 L 0 0 0 ${g}" fill="none" stroke="var(--grid-color,#e5e7eb)" stroke-width="0.5"/>
      </pattern>
      <pattern id="bigGrid" width="${g*5}" height="${g*5}" patternUnits="userSpaceOnUse">
        <rect width="${g*5}" height="${g*5}" fill="url(#smallGrid)"/>
        <path d="M ${g*5} 0 L 0 0 0 ${g*5}" fill="none" stroke="var(--grid-color2,#d1d5db)" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="${W}" height="${H}" fill="url(#bigGrid)"/>`;
    this._layerGrid.innerHTML = html;
  }


  // ── Рендер ───────────────────────────────────────────────────────────────

  render() {
    this._renderWires();
    this._renderComps();
    this._renderUI();
    this._notifyChange();
  }

  _renderWires() {
    const html = this.state.wires.map(w => {
      const fc = this.state.getComp(w.from.compId);
      const tc = this.state.getComp(w.to.compId);
      if (!fc||!tc) return '';
      const fp = this.state.getPin(fc, w.from.pinId);
      const tp = this.state.getPin(tc, w.to.pinId);
      if (!fp||!tp) return '';
      const {x:x1,y:y1} = absPin(fc,fp);
      const {x:x2,y:y2} = absPin(tc,tp);
      const sel = this.selected?.type==='wire'&&this.selected.id===w.id;
      // Manhattan routing
      const mx = x1 + (x2-x1)/2;
      const path = `M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}`;
      return `<path id="wire-${w.id}" d="${path}"
        fill="none" stroke="${sel?'#f59e0b':'#374151'}" stroke-width="${sel?3:2}"
        stroke-linecap="round" cursor="pointer"
        data-wire="${w.id}"/>`;
    }).join('');
    this._layerWires.innerHTML = html;
  }

  _renderComps() {
    const html = this.state.components.map(c => {
      const sel = this.selected?.type==='comp'&&this.selected.id===c.id;
      const selRect = sel
        ? `<rect x="-4" y="-4" width="${c.w+8}" height="${c.h+8}" rx="5"
              fill="none" stroke="#667eea" stroke-width="2" stroke-dasharray="5,3" opacity="0.8"/>`
        : '';
      const pins = c.type.pins.map(p => {
        const {x,y} = absPin(c,p);
        const hover = (this.mode.startsWith('wire') && this.wire)
          ? `<circle cx="${p.x}" cy="${p.y}" r="6" fill="#667eea" opacity="0.25" class="pin-hover"/>`
          : '';
        return `<g class="pin" data-comp="${c.id}" data-pin="${p.id}" cursor="crosshair">
          ${hover}
          <circle cx="${p.x}" cy="${p.y}" r="4" fill="#fff" stroke="${sel?'#667eea':'#9ca3af'}"
            stroke-width="1.5" class="pin-dot"/>
        </g>`;
      }).join('');
      return `<g id="comp-${c.id}" class="circuit-comp" transform="translate(${c.x},${c.y})"
              data-comp="${c.id}" cursor="${this.opts.readonly?'default':'move'}">
        ${selRect}
        ${c.type.render(c)}
        ${pins}
      </g>`;
    }).join('');
    this._layerComps.innerHTML = html;
  }

  _renderUI() {
    if (this.wire) {
      const x1=this.wire.x1, y1=this.wire.y1, x2=this.wire.curX||x1, y2=this.wire.curY||y1;
      const mx=x1+(x2-x1)/2;
      this._layerUI.innerHTML =
        `<path d="M${x1},${y1} L${mx},${y1} L${mx},${y2} L${x2},${y2}"
          fill="none" stroke="#667eea" stroke-width="2" stroke-dasharray="6,3"/>`;
    } else {
      this._layerUI.innerHTML = '';
    }
  }


  // ── События ───────────────────────────────────────────────────────────────

  _setupEvents() {
    if (this.opts.readonly) return;

    this.svg.addEventListener('mousedown', e => this._onMouseDown(e));
    this.svg.addEventListener('mousemove', e => this._onMouseMove(e));
    this.svg.addEventListener('mouseup',   e => this._onMouseUp(e));
    this.svg.addEventListener('wheel',     e => this._onWheel(e), {passive:false});
    window.addEventListener('keydown',     e => this._onKey(e));
    this.svg.addEventListener('contextmenu', e => {
      e.preventDefault();
      this._cancelMode();
    });
  }

  _svgCoords(e) {
    const pt = this.svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const m = this.svg.getScreenCTM().inverse();
    const r = pt.matrixTransform(m);
    return {x: r.x, y: r.y};
  }

  _onMouseDown(e) {
    if (e.button !== 0) return;
    const {x,y} = this._svgCoords(e);

    // Клик по пину → начать или закончить провод
    const pinEl = e.target.closest('.pin');
    if (pinEl) {
      e.stopPropagation();
      const compId = pinEl.dataset.comp;
      const pinId  = pinEl.dataset.pin;
      const comp   = this.state.getComp(compId);
      const pin    = this.state.getPin(comp, pinId);
      if (!comp||!pin) return;
      const {x:px,y:py} = absPin(comp,pin);

      if (this.wire) {
        // Завершить провод
        if (compId !== this.wire.fromCompId) {
          this._pushHistory();
          this.state.addWire(this.wire.fromCompId, this.wire.fromPinId, compId, pinId);
        }
        this.wire = null;
        this.mode = 'select';
      } else {
        // Начать провод
        this.wire = {fromCompId:compId, fromPinId:pinId, x1:px, y1:py, curX:px, curY:py};
        this.mode = 'wire';
        this.selected = null;
      }
      this.render();
      return;
    }

    // Клик по проводу → выделить
    const wireEl = e.target.closest('[data-wire]');
    if (wireEl) {
      this.selected = {type:'wire', id: wireEl.dataset.wire};
      this._cancelMode();
      this.render();
      return;
    }

    // Клик по компоненту → выделить + начать перетаскивание
    const compEl = e.target.closest('.circuit-comp');
    if (compEl) {
      const compId = compEl.dataset.comp;
      this.selected = {type:'comp', id:compId};
      const comp = this.state.getComp(compId);
      if (comp) {
        this.drag = {compId, ox:comp.x, oy:comp.y, mx:x, my:y};
      }
      this._cancelMode();
      this.render();
      return;
    }

    // Клик в режиме добавления компонента
    if (this.mode.startsWith('add:')) {
      const typeKey = this.mode.slice(4);
      this._pushHistory();
      const sx = snap(x, this.GRID);
      const sy = snap(y, this.GRID);
      const c = this.state.addComponent(typeKey, sx, sy);
      this.selected = {type:'comp', id:c.id};
      this.render();
      return;
    }

    // Клик на пустом месте — снять выделение
    this.selected = null;
    this._cancelMode();
    this.render();
  }

  _onMouseMove(e) {
    const {x,y} = this._svgCoords(e);

    if (this.drag) {
      const comp = this.state.getComp(this.drag.compId);
      if (comp) {
        comp.x = snap(this.drag.ox + (x - this.drag.mx), this.GRID);
        comp.y = snap(this.drag.oy + (y - this.drag.my), this.GRID);
        this.state.simulate();
        this.render();
      }
      return;
    }

    if (this.wire) {
      this.wire.curX = x;
      this.wire.curY = y;
      this._renderUI();
      return;
    }

    // Pan if space is held
    if (this._panning) {
      this.vb.x -= (x - this._panStart.x);
      this.vb.y -= (y - this._panStart.y);
      this._applyVB();
    }
  }

  _onMouseUp(e) {
    if (this.drag) {
      this._pushHistory();
      this.drag = null;
    }
    this._panning = false;
  }

  _onWheel(e) {
    e.preventDefault();
    const {x,y} = this._svgCoords(e);
    const factor = e.deltaY > 0 ? 1.15 : 0.87;
    this.vb.x = x - (x - this.vb.x) * factor;
    this.vb.y = y - (y - this.vb.y) * factor;
    this.vb.w *= factor;
    this.vb.h *= factor;
    this._applyVB();
  }

  _onKey(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'Escape') { this._cancelMode(); this.render(); }

    if ((e.key === 'Delete' || e.key === 'Backspace') && this.selected) {
      this._pushHistory();
      if (this.selected.type === 'comp') this.state.removeComponent(this.selected.id);
      if (this.selected.type === 'wire') this.state.removeWire(this.selected.id);
      this.selected = null;
      this.render();
    }

    if ((e.ctrlKey||e.metaKey) && e.key === 'z') { e.preventDefault(); this.undo(); }
    if ((e.ctrlKey||e.metaKey) && e.key === 'y') { e.preventDefault(); this.redo(); }
    if ((e.ctrlKey||e.metaKey) && e.key === 's') { e.preventDefault(); this.save(); }
  }


  // ── История (undo/redo) ───────────────────────────────────────────────────

  _pushHistory() {
    this.history.push(this.state.toJSON());
    if (this.history.length > 50) this.history.shift();
    this.redoStack = [];
  }

  undo() {
    if (!this.history.length) return;
    this.redoStack.push(this.state.toJSON());
    this.state.fromJSON(this.history.pop());
    this.selected = null;
    this.render();
  }

  redo() {
    if (!this.redoStack.length) return;
    this.history.push(this.state.toJSON());
    this.state.fromJSON(this.redoStack.pop());
    this.selected = null;
    this.render();
  }


  // ── Режимы ────────────────────────────────────────────────────────────────

  startAdd(typeKey) {
    this._cancelMode();
    this.mode = `add:${typeKey}`;
    this.svg.style.cursor = 'crosshair';
    this._updateStatus(`Кликни на схему чтобы разместить ${CT[typeKey]?.name}`);
  }

  _cancelMode() {
    this.wire = null;
    if (this.mode !== 'select') {
      this.mode = 'select';
      this.svg.style.cursor = '';
      this._updateStatus('');
    }
  }

  startWireMode() {
    this._cancelMode();
    this.mode = 'wire';
    this.svg.style.cursor = 'crosshair';
    this._updateStatus('Кликни на пин компонента чтобы начать провод');
  }


  // ── Сохранение ───────────────────────────────────────────────────────────

  save() {
    if (this.opts.onSave) this.opts.onSave(this.state.toJSON());
  }

  submit() {
    if (this.opts.onSubmit) this.opts.onSubmit(this.state.toJSON());
  }

  clear() {
    this._pushHistory();
    this.state.components = [];
    this.state.wires = [];
    this.selected = null;
    this.render();
  }

  fitView() {
    if (!this.state.components.length) {
      this.vb = {x:0,y:0,w:1400,h:900};
    } else {
      const xs = this.state.components.map(c => c.x);
      const ys = this.state.components.map(c => c.y);
      const x2 = this.state.components.map(c => c.x + c.w);
      const y2 = this.state.components.map(c => c.y + c.h);
      const pad = 60;
      this.vb = {
        x: Math.min(...xs)-pad, y: Math.min(...ys)-pad,
        w: Math.max(...x2)-Math.min(...xs)+pad*2,
        h: Math.max(...y2)-Math.min(...ys)+pad*2,
      };
    }
    this._applyVB();
  }


  // ── Вспомогательные ──────────────────────────────────────────────────────

  _updateStatus(msg) {
    const el = document.getElementById('circuit-status');
    if (el) el.textContent = msg;
  }

  _notifyChange() {
    const el = document.getElementById('circuit-json-hidden');
    if (el) el.value = this.state.toJSON();
  }

  updateProp(propKey, value) {
    if (!this.selected || this.selected.type !== 'comp') return;
    const comp = this.state.getComp(this.selected.id);
    if (!comp) return;
    this._pushHistory();
    comp.props[propKey] = value;
    this.state.simulate();
    this.render();
    this._renderPropsPanel();
  }

  _renderPropsPanel() {
    const panel = document.getElementById('props-panel');
    if (!panel) return;
    if (!this.selected || this.selected.type !== 'comp') {
      panel.innerHTML = '<p class="props-hint">Выбери компонент чтобы изменить свойства</p>';
      return;
    }
    const comp = this.state.getComp(this.selected.id);
    if (!comp) return;
    let html = `<div class="props-title">${comp.type.name}</div>`;

    if (comp.typeKey === 'resistor') {
      const vals = ['100 Ω','220 Ω','470 Ω','1 kΩ','4.7 kΩ','10 kΩ'];
      html += `<label class="prop-label">Номинал</label>
        <select class="prop-input" onchange="EDITOR.updateProp('value',this.value)">
          ${vals.map(v=>`<option${comp.props.value===v?' selected':''}>${v}</option>`).join('')}
        </select>`;
    }
    if (comp.typeKey === 'led') {
      const colors = ['red','green','yellow','blue','white'];
      html += `<label class="prop-label">Цвет</label>
        <select class="prop-input" onchange="EDITOR.updateProp('color',this.value)">
          ${colors.map(c=>`<option${comp.props.color===c?' selected':''}>${c}</option>`).join('')}
        </select>`;
    }
    html += `<button class="prop-delete-btn" onclick="EDITOR._deleteSelected()">
      <i class="fas fa-trash"></i> Удалить
    </button>`;
    panel.innerHTML = html;
  }

  _deleteSelected() {
    if (!this.selected) return;
    this._pushHistory();
    if (this.selected.type === 'comp') this.state.removeComponent(this.selected.id);
    if (this.selected.type === 'wire') this.state.removeWire(this.selected.id);
    this.selected = null;
    this.render();
    this._renderPropsPanel();
  }

  // Обновляем панель свойств при каждом render
  render() {
    this._renderWires();
    this._renderComps();
    this._renderUI();
    this._notifyChange();
    this._renderPropsPanel();
  }
}


// ── Инициализация ─────────────────────────────────────────────────────────────

let EDITOR = null;

function initCircuitEditor(config) {
  const svgEl = document.getElementById('circuit-svg');
  if (!svgEl) return;

  const state = new CircuitState();

  // Загрузить сохранённую схему
  if (config.initialJson && config.initialJson !== 'null') {
    try { state.fromJSON(config.initialJson); } catch(e) { console.warn('Bad JSON', e); }
  }

  EDITOR = new CircuitEditor(svgEl, state, {
    readonly: config.readonly || false,
    onSave(json) {
      fetch(config.saveUrl, {
        method: 'POST',
        headers: {'Content-Type':'application/json','X-CSRFToken': config.csrf},
        body: json
      }).then(r=>r.json()).then(d=>{
        const msg = document.getElementById('save-msg');
        if (msg) { msg.textContent='✓ Сохранено'; msg.style.opacity=1; setTimeout(()=>msg.style.opacity=0, 2000); }
      }).catch(()=>{});
    },
    onSubmit(json) {
      document.getElementById('circuit-json-hidden').value = json;
      document.getElementById('circuit-submit-form').submit();
    }
  });

  // Палитра
  buildPalette();

  // Сохранение каждые 30 секунд автоматически
  if (!config.readonly) {
    setInterval(()=>EDITOR.save(), 30000);
  }
}

function buildPalette() {
  const container = document.getElementById('palette-container');
  if (!container) return;
  for (const [cat, label] of PALETTE_ORDER) {
    const items = Object.entries(CT).filter(([,t])=>t.category===cat);
    if (!items.length) continue;
    let html = `<div class="palette-group-label">${label}</div>`;
    for (const [key, t] of items) {
      html += `<button class="palette-item" onclick="EDITOR.startAdd('${key}')" title="${t.name}">
        <span class="palette-icon">${t.icon}</span>
        <span class="palette-name">${t.name}</span>
      </button>`;
    }
    container.insertAdjacentHTML('beforeend', html);
  }
}
