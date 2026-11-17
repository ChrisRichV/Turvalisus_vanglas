/* Joonised: Excalidraw' elementide käsitsijoonistuse stiilis renderdaja ja Mermaid.
   - tyyp "excalidraw": { elemendid: [...Excalidraw elemendid...], alt }  – joonistatakse SVG-na siin (ilma välise teegita),
     värvid kohanduvad tumeda/heleda vaatega. Joonised on kavandatud Excalidraw' connectoriga.
   - tyyp "mermaid": { kood, alt } – Mermaid laetakse ainult siis, kui lehel on Mermaidi joonis (jsdelivr).
   Mõlemal on "alt" (lühike tekstiline kirjeldus): ekraanilugejale ja varuks, kui joonis ei lae. */
(function () {
  "use strict";
  const A = window.APP;
  const esc = (s) => A.esc(s == null ? "" : String(s));
  const tume = () => document.documentElement.dataset.theme !== "light";

  /* ---------- värvid: Excalidraw' palett → lehe teema ---------- */
  const TAIDE = { // pastell (hele) → tume variant
    "#a5d8ff": "#1e3a5f", "#b2f2bb": "#1a4d2e", "#ffd8a8": "#5c3d1a", "#d0bfff": "#2d1b69",
    "#ffc9c9": "#5c1a1a", "#fff3bf": "#4d4415", "#c3fae8": "#1a4d4d", "#eebefa": "#4d1a4d",
    "#dbe4ff": "#1b2540", "#e5dbff": "#241b40", "#d3f9d8": "#16301d", "#ffffff": "#151c25"
  };
  const JOON = { // joonevärv tumedas vaates
    "#1e1e1e": "#e6eaee", "#757575": "#a0a8b4", "#15803d": "#4ade80", "#2563eb": "#7fb0ff"
  };
  const vTaide = (c) => !c || c === "transparent" ? "none" : tume() ? (TAIDE[c.toLowerCase()] || c) : c;
  const vJoon = (c) => { c = c || "#1e1e1e"; return tume() ? (JOON[c.toLowerCase()] || c) : (c.toLowerCase() === "#1e1e1e" ? "#1c2733" : c); };
  const tekstiVarv = (el) => vJoon(el.strokeColor && el.type === "text" ? el.strokeColor : "#1e1e1e");

  /* ---------- deterministlik juhus (sama joonis näeb alati ühtmoodi välja) ---------- */
  function rng(seemne) {
    let h = 2166136261;
    for (const c of String(seemne)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); }
    return () => { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) % 1000) / 1000 - 0.5; };
  }

  /* käsitsi tõmmatud joon: kaks veidi erinevat kõverat */
  function kriips(x1, y1, x2, y2, r, karedus) {
    const k = karedus == null ? 1 : karedus;
    const pikk = Math.hypot(x2 - x1, y2 - y1) || 1;
    const nihe = Math.min(2.2, pikk / 60) * k;
    let d = "";
    for (let i = 0; i < 2; i++) {
      const mx = (x1 + x2) / 2 + r() * nihe * 3, my = (y1 + y2) / 2 + r() * nihe * 3;
      d += `M${(x1 + r() * nihe).toFixed(1)} ${(y1 + r() * nihe).toFixed(1)} Q${mx.toFixed(1)} ${my.toFixed(1)} ${(x2 + r() * nihe).toFixed(1)} ${(y2 + r() * nihe).toFixed(1)} `;
    }
    return d;
  }

  /* ---------- tekst ja murdmine ---------- */
  const LAIUS = 0.53; // keskmine tähelaius fondisuuruse suhtes (Archivo)
  function murra(tekst, maxL, fs) {
    const read = [];
    String(tekst).split("\n").forEach((loik) => {
      let rida = "";
      loik.split(/\s+/).forEach((s) => {
        const uus = rida ? rida + " " + s : s;
        if (rida && uus.length * fs * LAIUS > maxL) { read.push(rida); rida = s; } else rida = uus;
      });
      read.push(rida);
    });
    return read;
  }
  function tekstSvg(read, cx, cy, fs, varv, ank, paks) {
    const lh = fs * 1.22, y0 = cy - ((read.length - 1) * lh) / 2;
    return `<text x="${cx}" y="${y0}" font-size="${fs}" fill="${varv}" text-anchor="${ank || "middle"}" dominant-baseline="central"${paks ? ' font-weight="600"' : ""}>` +
      read.map((t, i) => `<tspan x="${cx}" y="${(y0 + i * lh).toFixed(1)}">${esc(t)}</tspan>`).join("") + `</text>`;
  }

  /* ---------- Excalidraw → SVG ---------- */
  function excalidrawSvg(elemendid) {
    const els = elemendid.filter((e) => e && e.type && !["cameraUpdate", "delete", "restoreCheckpoint"].includes(e.type));
    // konteineri kõrgus kasvab, kui silt ei mahu (nagu Excalidraw's)
    els.forEach((e) => {
      if (e.label && ["rectangle", "ellipse", "diamond"].includes(e.type)) {
        const fs = e.label.fontSize || 18, sisemine = e.type === "rectangle" ? e.width - 20 : e.width * 0.72;
        const read = murra(e.label.text, sisemine, fs), th = read.length * fs * 1.22;
        const vaja = e.type === "rectangle" ? th + 20 : th / 0.66 + 10;
        e._read = read; e._fs = fs;
        if (vaja > e.height) { e.y -= (vaja - e.height) / 2; e.height = vaja; }
      }
    });
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    const laienda = (a, b, c, d) => { x0 = Math.min(x0, a); y0 = Math.min(y0, b); x1 = Math.max(x1, c); y1 = Math.max(y1, d); };
    els.forEach((e) => {
      if (e.type === "text") {
        const fs = e.fontSize || 20, read = String(e.text).split("\n");
        const w = Math.max(...read.map((t) => t.length)) * fs * LAIUS, h = read.length * fs * 1.22;
        e._w = w; e._h = h; laienda(e.x, e.y, e.x + w, e.y + h);
      } else if (e.points) {
        e.points.forEach(([dx, dy]) => laienda(e.x + dx - 6, e.y + dy - 6, e.x + dx + 6, e.y + dy + 6));
      } else laienda(e.x, e.y, e.x + e.width, e.y + e.height);
    });
    const P = 14; x0 -= P; y0 -= P; x1 += P; y1 += P;
    const W = x1 - x0, H = y1 - y0;
    let s = "";
    els.forEach((e) => {
      const r = rng(e.id || JSON.stringify([e.x, e.y]));
      const joon = vJoon(e.strokeColor), taide = vTaide(e.backgroundColor);
      const sw = e.strokeWidth == null ? 2 : e.strokeWidth, kr = e.roughness == null ? 1 : e.roughness;
      const op = e.opacity != null && e.opacity < 100 ? ` opacity="${(e.opacity / 100).toFixed(2)}"` : "";
      const dash = e.strokeStyle === "dashed" ? ' stroke-dasharray="7 6"' : e.strokeStyle === "dotted" ? ' stroke-dasharray="2 5"' : "";
      const piir = joon === "transparent" || sw === 0 ? "" : `stroke="${joon}" stroke-width="${sw}"${dash} fill="none" stroke-linecap="round"`;
      if (e.type === "rectangle") {
        const { x, y, width: w, height: h } = e, rr = e.roundness ? Math.min(14, w / 6, h / 4) : 0;
        s += `<g${op}><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rr}" fill="${taide}"/>`;
        if (piir) s += `<path d="${kriips(x + rr, y, x + w - rr, y, r, kr)}${kriips(x + w, y + rr, x + w, y + h - rr, r, kr)}${kriips(x + w - rr, y + h, x + rr, y + h, r, kr)}${kriips(x, y + h - rr, x, y + rr, r, kr)}${rr ? `M${x + w - rr} ${y} Q${x + w} ${y} ${x + w} ${y + rr} M${x + w} ${y + h - rr} Q${x + w} ${y + h} ${x + w - rr} ${y + h} M${x + rr} ${y + h} Q${x} ${y + h} ${x} ${y + h - rr} M${x} ${y + rr} Q${x} ${y} ${x + rr} ${y}` : ""}" ${piir}/>`;
        s += "</g>";
      } else if (e.type === "ellipse") {
        const cx = e.x + e.width / 2, cy = e.y + e.height / 2;
        s += `<g${op}><ellipse cx="${cx}" cy="${cy}" rx="${e.width / 2}" ry="${e.height / 2}" fill="${taide}"/>`;
        if (piir) for (let i = 0; i < 2; i++) s += `<ellipse cx="${(cx + r() * 2 * kr).toFixed(1)}" cy="${(cy + r() * 2 * kr).toFixed(1)}" rx="${(e.width / 2 + r() * 3 * kr).toFixed(1)}" ry="${(e.height / 2 + r() * 3 * kr).toFixed(1)}" ${piir}/>`;
        s += "</g>";
      } else if (e.type === "diamond") {
        const { x, y, width: w, height: h } = e, p = [[x + w / 2, y], [x + w, y + h / 2], [x + w / 2, y + h], [x, y + h / 2]];
        s += `<g${op}><polygon points="${p.map((q) => q.join(",")).join(" ")}" fill="${taide}"/>`;
        if (piir) s += `<path d="${p.map((q, i) => kriips(q[0], q[1], p[(i + 1) % 4][0], p[(i + 1) % 4][1], r, kr)).join("")}" ${piir}/>`;
        s += "</g>";
      } else if (e.type === "arrow" || e.type === "line") {
        const pts = e.points.map(([dx, dy]) => [e.x + dx, e.y + dy]);
        let d = "";
        for (let i = 0; i < pts.length - 1; i++) d += kriips(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], r, kr * 0.6);
        const ots = (a, b, tyyp) => {
          if (!tyyp) return "";
          const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = 13;
          if (tyyp === "dot") return `<circle cx="${b[0]}" cy="${b[1]}" r="4" fill="${joon}"/>`;
          if (tyyp === "bar") { const px = Math.sin(ang) * 8, py = -Math.cos(ang) * 8; return `<path d="M${b[0] - px} ${b[1] - py} L${b[0] + px} ${b[1] + py}" stroke="${joon}" stroke-width="${sw}"/>`; }
          const p1 = [b[0] - L * Math.cos(ang - 0.45), b[1] - L * Math.sin(ang - 0.45)], p2 = [b[0] - L * Math.cos(ang + 0.45), b[1] - L * Math.sin(ang + 0.45)];
          return tyyp === "triangle"
            ? `<polygon points="${b.join(",")} ${p1.join(",")} ${p2.join(",")}" fill="${joon}"/>`
            : `<path d="M${p1[0].toFixed(1)} ${p1[1].toFixed(1)} L${b[0]} ${b[1]} L${p2[0].toFixed(1)} ${p2[1].toFixed(1)}" stroke="${joon}" stroke-width="${sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
        };
        const lopp = e.type === "arrow" ? (e.endArrowhead === undefined ? "arrow" : e.endArrowhead) : null;
        s += `<g${op}><path d="${d}" ${piir}/>${ots(pts[pts.length - 2], pts[pts.length - 1], lopp)}${ots(pts[1], pts[0], e.startArrowhead)}</g>`;
        if (e.label && e.label.text) {
          const m = Math.floor((pts.length - 1) / 2), a = pts[m], b = pts[m + 1] || a;
          const cx = (a[0] + b[0]) / 2, cy = (a[1] + b[1]) / 2, fs = e.label.fontSize || 16;
          const read = String(e.label.text).split("\n"), w = Math.max(...read.map((t) => t.length)) * fs * LAIUS + 10, h = read.length * fs * 1.22 + 4;
          s += `<rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="4" fill="${tume() ? "#0d1117" : "#f7f8f5"}"/>` + tekstSvg(read, cx, cy, fs, vJoon("#1e1e1e"));
        }
      } else if (e.type === "text") {
        const fs = e.fontSize || 20, read = String(e.text).split("\n");
        s += tekstSvg(read, e.x, e.y + e._h / 2, fs, tekstiVarv(e), "start", fs >= 20);
      }
      if (e._read) {
        const cx = e.x + e.width / 2, cy = e.y + e.height / 2;
        s += tekstSvg(e._read, cx, cy, e._fs, vJoon(e.label.strokeColor || "#1e1e1e"), "middle", e._fs >= 20);
      }
    });
    return { svg: `<svg viewBox="${x0} ${y0} ${W} ${H}" width="${W}" role="img" aria-hidden="true" font-family="Archivo, Arial, sans-serif">${s}</svg>`, W };
  }

  function joonistaExcalidraw(juur) {
    juur.querySelectorAll(".s-excalidraw[data-el]").forEach((div) => {
      try {
        const els = JSON.parse(div.dataset.el);
        const { svg, W } = excalidrawSvg(els);
        const koht = div.querySelector(".joonis");
        koht.innerHTML = svg;
        koht.style.maxWidth = Math.min(W, 680) + "px";
        div.classList.add("valmis");
      } catch (e) { div.classList.add("viga"); }
    });
  }

  /* ---------- Mermaid ---------- */
  let mermaidP = null, loendur = 0;
  function mermaidTeema() {
    const t = tume();
    return {
      startOnLoad: false, securityLevel: "strict", theme: "base",
      fontFamily: "Archivo, Arial, sans-serif",
      flowchart: { htmlLabels: false, curve: "basis", useMaxWidth: true },
      mindmap: { useMaxWidth: true },
      themeVariables: t ? {
        darkMode: true, background: "transparent", fontFamily: "Archivo, Arial, sans-serif", fontSize: "16px",
        primaryColor: "#1e3a5f", primaryTextColor: "#e6eaee", primaryBorderColor: "#2ef5d6",
        secondaryColor: "#2d1b69", secondaryTextColor: "#e6eaee", secondaryBorderColor: "#b388ff",
        tertiaryColor: "#1a4d2e", tertiaryTextColor: "#e6eaee", tertiaryBorderColor: "#4ade80",
        lineColor: "#8f9bab", textColor: "#e6eaee", mainBkg: "#1e3a5f", nodeBorder: "#2ef5d6",
        clusterBkg: "#151c25", clusterBorder: "#253141", edgeLabelBackground: "#0d1117", titleColor: "#e6eaee",
        cScale0: "#1e3a5f", cScale1: "#2d1b69", cScale2: "#1a4d2e", cScale3: "#5c3d1a", cScale4: "#5c1a1a", cScale5: "#1a4d4d",
        cScaleLabel0: "#e6eaee", cScaleLabel1: "#e6eaee", cScaleLabel2: "#e6eaee", cScaleLabel3: "#e6eaee", cScaleLabel4: "#e6eaee", cScaleLabel5: "#e6eaee",
        pie1: "#2ef5d6", pie2: "#253141", pie3: "#b388ff", pieTitleTextColor: "#e6eaee", pieSectionTextColor: "#0d1117", pieLegendTextColor: "#e6eaee", pieStrokeColor: "#0d1117",
        xyChart: { backgroundColor: "transparent", titleColor: "#e6eaee", xAxisLabelColor: "#e6eaee", yAxisLabelColor: "#e6eaee", xAxisLineColor: "#8f9bab", yAxisLineColor: "#8f9bab", xAxisTitleColor: "#e6eaee", yAxisTitleColor: "#e6eaee", plotColorPalette: "#2ef5d6, #b388ff, #ffe14a" }
      } : {
        background: "transparent", fontFamily: "Archivo, Arial, sans-serif", fontSize: "16px",
        primaryColor: "#a5d8ff", primaryTextColor: "#1c2733", primaryBorderColor: "#1c2733",
        secondaryColor: "#d0bfff", tertiaryColor: "#b2f2bb", lineColor: "#56616e", textColor: "#1c2733",
        mainBkg: "#e7f3ff", nodeBorder: "#1c2733", clusterBkg: "#f7f8f5", clusterBorder: "#cdd2cc", edgeLabelBackground: "#f7f8f5",
        cScale0: "#a5d8ff", cScale1: "#d0bfff", cScale2: "#b2f2bb", cScale3: "#ffd8a8", cScale4: "#ffc9c9", cScale5: "#c3fae8",
        pie1: "#2f6f6a", pie2: "#cdd2cc", pie3: "#8b5cf6", pieSectionTextColor: "#ffffff", pieStrokeColor: "#f7f8f5",
        xyChart: { backgroundColor: "transparent", plotColorPalette: "#2f6f6a, #8b5cf6, #f2c230" }
      }
    };
  }
  function joonistaMermaid(juur) {
    const kohad = [...juur.querySelectorAll(".s-mermaid[data-kood]")];
    if (!kohad.length) return;
    if (!mermaidP) mermaidP = import("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs").then((m) => m.default);
    mermaidP.then(async (mermaid) => {
      mermaid.initialize(mermaidTeema());
      for (const div of kohad) {
        try {
          const { svg } = await mermaid.render("mm" + (++loendur), div.dataset.kood);
          div.querySelector(".joonis").innerHTML = svg;
          div.classList.add("valmis");
        } catch (e) { div.classList.add("viga"); }
      }
    }).catch(() => kohad.forEach((d) => d.classList.add("viga")));
  }

  A.joonista = function (juur) {
    juur = juur || document;
    joonistaExcalidraw(juur);
    joonistaMermaid(juur);
  };
  // teema vahetus → joonista uuesti õigete värvidega
  new MutationObserver(() => A.joonista(document)).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

  /* skeemitüübid (registreeritakse skeemid.js-i) */
  A.lisaSkeemid({
    excalidraw(s) {
      return `<div class="s-excalidraw s-joonis" data-el="${esc(JSON.stringify(s.elemendid))}"><div class="joonis" role="img" aria-label="${esc(s.alt || "")}"></div>
        <p class="joonis-alt">${A.md(s.alt || "")}</p></div>`;
    },
    mermaid(s) {
      return `<div class="s-mermaid s-joonis" data-kood="${esc(s.kood)}"><div class="joonis" role="img" aria-label="${esc(s.alt || "")}"></div>
        <p class="joonis-alt">${A.md(s.alt || "")}</p></div>`;
    }
  });
})();
