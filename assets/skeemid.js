/* Skeemid: voog, puu, tasandid, vordlus, kaalud. Sisu tuleb teemafailist. */
(function () {
  "use strict";
  const A = window.APP;
  const md = (s) => A.md(s);

  function kast(o) {
    if (!o) return "";
    return `<div class="skeem-kast"><b>${md(o.pealkiri)}</b>${o.tekst ? `<span>${md(o.tekst)}</span>` : ""}${o.viide ? A.refNupp(o.viide) : ""}</div>`;
  }

  const R = {
    voog(s) {
      return `<ol class="s-voog">${s.sammud.map((x) => `<li>${kast(x)}</li>`).join("")}</ol>`;
    },
    puu(s) {
      const harud = s.harud.map((h) => `<div class="haru" data-toon="${h.toon || "a"}"><h4>${md(h.pealkiri)}</h4>${h.lapsed.map(kast).join("")}</div>`).join("");
      return `<div class="s-puu"><div class="juur">${kast(s.juur)}</div><div class="harud">${harud}</div></div>`;
    },
    tasandid(s) {
      return `<div class="s-tasandid">${s.tasandid.map((t) => `<div class="s-tase" data-toon="${t.toon || "a"}"><h4>${md(t.pealkiri)}</h4><div class="kastid">${t.kastid.map(kast).join("")}</div></div>`).join("")}</div>`;
    },
    vordlus(s) {
      const pais = `<thead><tr><th scope="col"><span class="peidetud">Rida</span></th>${s.veerud.map((v) => `<th scope="col">${md(v)}</th>`).join("")}</tr></thead>`;
      const read = s.read.map((r) => `<tr><th scope="row">${md(r.silt)}</th>${r.lahtrid.map((l, i) => `<td data-veerg="${A.esc(s.veerud[i] || "")}">${md(l)}</td>`).join("")}</tr>`).join("");
      return `<table class="s-vordlus">${pais}<tbody>${read}</tbody></table>`;
    },
    kaalud(s) {
      const vaagen = (o) => `<div class="vaagen">${kast(o)}<span class="silt-k">${md(o.silt)}</span></div>`;
      return `<div class="s-kaalud">${vaagen(s.vasak)}${vaagen(s.parem)}</div>
        ${s.all ? `<div class="s-kaalud-all"><ul>${s.all.map((x) => `<li>${md(x)}</li>`).join("")}</ul></div>` : ""}`;
    }
  };

  A.skeem = function (s) {
    if (!s) return "";
    if (Array.isArray(s)) return s.map(A.skeem).join("");
    const f = R[s.tyyp];
    if (!f) return "";
    return `<figure class="skeem" style="margin-inline:0"><h3>${md(s.pealkiri || "")}</h3>${f(s)}</figure>`;
  };
})();
