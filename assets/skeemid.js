/* Skeemid: voog, puu, tasandid, vordlus, kaalud, kontroll, kaardid, otsus, kolmnurk, pyramiid, sambad, lahka, subsumeeri. Sisu tuleb teemafailist. */
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
    kontroll(s) {
      const sammud = s.sammud.map((x, i) => `<li class="${i ? "lukus" : ""}">
        <div class="kontroll-kys"><span class="kontroll-silt">${md(x.silt || "")}</span><b>${md(x.kysimus)}</b></div>
        <button type="button" class="nupp teine kontroll-ava"${i ? " disabled" : ""}>Mõtle ise, siis näita</button>
        <div class="kontroll-vastus" hidden>${md(x.vastus)}${x.viited ? `<div class="kontroll-viited">${x.viited.map((v) => A.refNupp(v)).join("")}</div>` : ""}</div></li>`).join("");
      return `<div class="s-kontroll">${s.olukord ? `<div class="kontroll-olukord">${md(s.olukord)}</div>` : ""}
        <div class="kontroll-pea"><div class="kontroll-riba" aria-hidden="true"><i></i></div><span class="kontroll-seis" role="status" aria-live="polite">Samm 0 / ${s.sammud.length}</span>
          <button type="button" class="kontroll-koik">Näita kõik</button></div>
        <ol class="kontroll-sammud">${sammud}</ol>
        ${s.jareldus ? `<div class="kontroll-jareldus" hidden><b>Järeldus</b>${md(s.jareldus)}</div>` : ""}
        ${s.markus ? `<p class="kontroll-markus">${md(s.markus)}</p>` : ""}</div>`;
    },
    /* Kaardid: ruudustik; silt (suur märk/number), pealkiri, tekst, viide, toon a/b/c/d. */
    kaardid(s) {
      return `<ul class="s-kaardid${s.kitsad ? " kitsad" : ""}">${s.kaardid.map((k) => `<li data-toon="${k.toon || "a"}">
        ${k.silt ? `<span class="k-silt">${md(k.silt)}</span>` : ""}<b class="k-pea">${md(k.pealkiri)}</b>
        ${k.tekst ? `<span class="k-tekst">${md(k.tekst)}</span>` : ""}${k.viide ? `<span class="k-viide">${A.refNupp(k.viide)}</span>` : ""}</li>`).join("")}</ul>`;
    },
    /* Otsustusrada: iga samm on küsimus; "ei" viib kõrvale väljapääsu; lõpus tulemus. */
    otsus(s) {
      const sammud = s.sammud.map((x, i) => `<li class="o-samm">
        <div class="o-kys"><span class="o-nr">${i + 1}</span><div><b>${md(x.kysimus)}</b>${x.tekst ? `<span>${md(x.tekst)}</span>` : ""}${x.viide ? A.refNupp(x.viide) : ""}</div></div>
        ${x.ei ? `<div class="o-ei"><span class="o-silt">${md(x.ei_silt || "Ei")}</span><div><b>${md(x.ei.tulemus)}</b>${x.ei.tekst ? `<span>${md(x.ei.tekst)}</span>` : ""}</div></div>` : ""}
        ${i < s.sammud.length - 1 ? `<span class="o-jah" aria-hidden="true">${md(x.jah_silt || "Jah")}</span>` : ""}</li>`).join("");
      return `<div class="s-otsus">${s.algus ? `<div class="o-algus">${md(s.algus)}</div>` : ""}<ol>${sammud}</ol>
        ${s.lopp ? `<div class="o-lopp"><span class="o-silt">${md(s.lopp.silt || "Jah")}</span><div><b>${md(s.lopp.tulemus)}</b>${s.lopp.tekst ? `<span>${md(s.lopp.tekst)}</span>` : ""}</div></div>` : ""}</div>`;
    },
    /* Kolmnurk: kolm osalist ja nende vahelised seosed. */
    kolmnurk(s) {
      const nurk = (o, kl) => `<div class="kn-nurk ${kl}">${kast(o)}</div>`;
      const n = s.nooled || {};
      return `<div class="s-kolmnurk">
        <svg class="kn-jooned" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
          <line x1="50" y1="16" x2="17" y2="78"/><line x1="50" y1="16" x2="83" y2="78"/><line x1="24" y1="86" x2="76" y2="86" class="katk"/></svg>
        ${nurk(s.yla, "kn-yla")}${nurk(s.vasak, "kn-vasak")}${nurk(s.parem, "kn-parem")}
        ${n.vasak ? `<span class="kn-noole kn-nv">${md(n.vasak)}</span>` : ""}${n.parem ? `<span class="kn-noole kn-np">${md(n.parem)}</span>` : ""}${n.all ? `<span class="kn-noole kn-na">${md(n.all)}</span>` : ""}
      </div>${s.all ? `<p class="kn-all">${md(s.all)}</p>` : ""}`;
    },
    /* Püramiid: astmed ülevalt alla (kitsast laiaks); "vahel" = silt kahe astme vahel. */
    pyramiid(s) {
      const k = s.astmed.length;
      return `<ol class="s-pyramiid">${s.astmed.map((x, i) => `<li style="--l:${Math.round(52 + 48 * i / Math.max(1, k - 1))}%" data-toon="${x.toon || "a"}">
          <div class="p-aste"><b>${md(x.pealkiri)}</b>${x.tekst ? `<span>${md(x.tekst)}</span>` : ""}${x.viide ? A.refNupp(x.viide) : ""}</div>
          ${x.vahel ? `<div class="p-vahel"><span>${md(x.vahel)}</span></div>` : ""}</li>`).join("")}</ol>`;
    },
    /* Sambad: katus (ühine alus), sambad (harud) ja vundament; tasakaal = seosed sammaste vahel. */
    sambad(s) {
      return `<div class="s-sambad">${s.katus ? `<div class="sb-katus"><b>${md(s.katus.pealkiri)}</b>${s.katus.tekst ? `<span>${md(s.katus.tekst)}</span>` : ""}${s.katus.viide ? A.refNupp(s.katus.viide) : ""}</div>` : ""}
        <div class="sb-read">${s.sambad.map((x) => `<div class="sb-sammas" data-toon="${x.toon || "a"}"><h4>${md(x.pealkiri)}</h4>${x.viide ? A.refNupp(x.viide) : ""}
          <ul>${(x.read || []).map((r) => `<li>${md(r)}</li>`).join("")}</ul></div>`).join("")}</div>
        ${s.alus ? `<div class="sb-alus"><b>${md(s.alus.pealkiri)}</b>${s.alus.tekst ? `<span>${md(s.alus.tekst)}</span>` : ""}${s.alus.viide ? A.refNupp(s.alus.viide) : ""}</div>` : ""}
        ${s.tasakaal ? `<div class="sb-tasakaal"><h4>${md(s.tasakaal_pealkiri || "Kuidas harud üksteist kontrollivad")}</h4><ul>${s.tasakaal.map((r) => `<li>${md(r)}</li>`).join("")}</ul></div>` : ""}</div>`;
    },
    /* Normi lahkamine: sätte tekst tuleb seadused.json-ist SÕNA-SÕNALT; osad = tekstilõigud, mis märgitakse.
       roll: k = koosseisu tunnus (hüpotees), t = õiguslik tagajärg (dispositsioon), s = sanktsioon, m = seos (ja/või/võib/peab). */
    lahka(s) {
      const r = A.parseRef(s.viide), satt = r && A.seadused && A.seadused.satted[r.voti];
      if (!satt) return `<p class="teade viga">Sätet ${A.esc(s.viide)} ei leitud.</p>`;
      const SILT = { k: "K", t: "T", s: "S", m: "" };
      const lugur = { k: 0, t: 0, s: 0 };
      const osad = s.osad.map((o) => Object.assign({}, o, { nr: o.roll === "m" ? "" : SILT[o.roll] + (++lugur[o.roll]) }));
      // ainult viidatud lõige (kuni järgmise lõike alguseni), muidu terve paragrahv
      let read = satt.read.filter((x) => !/^\[(RT|Kehtetu)/.test(x));
      if (r.lg) {
        const algus = read.findIndex((x) => x.startsWith(`(${r.lg})`));
        if (algus >= 0) { let lopp = read.findIndex((x, i) => i > algus && /^\(\d/.test(x)); read = read.slice(algus, lopp < 0 ? undefined : lopp); }
      }
      read = read.filter((x) => osad.some((o) => x.includes(o.tekst)) || /^\d+(\^\d+)?\)/.test(x));
      const tehtud = new Set();
      const rida = (x) => {
        let h = A.esc(x);
        osad.forEach((o, i) => {
          if (tehtud.has(i)) return;
          const e = A.esc(o.tekst);
          if (!h.includes(e)) return;
          tehtud.add(i);
          h = h.replace(e, `<mark class="lk lk-${o.roll}" data-nr="${o.nr}">${e}${o.nr ? `<sup>${o.nr}</sup>` : ""}</mark>`);
        });
        return `<p>${A.ylaindeks(h)}</p>`;
      };
      const legend = [["k", "koosseis ehk hüpotees – „kui …”"], ["t", s.t_silt || "õiguslik tagajärg – „siis …”"], ["s", "sanktsioon – „vastasel juhul …”"], ["m", "seos: ja / või / võib / peab"]]
        .filter(([k]) => osad.some((o) => o.roll === k)).map(([k, t]) => `<li><span class="lk lk-${k}">${k === "m" ? "ja/või" : SILT[k]}</span> ${t}</li>`).join("");
      const tabel = osad.filter((o) => o.roll !== "m").map((o) => `<li><b class="lk lk-${o.roll}">${o.nr}</b> ${A.esc(o.tekst)}${o.selgitus ? ` <span class="lk-selg">– ${md(o.selgitus)}</span>` : ""}</li>`).join("");
      return `<div class="s-lahka">
        <div class="lk-pea">${A.refNupp(s.viide)}<span class="lk-juhis">${md(s.juhis || "Leia ise: mis on tingimus (kui …) ja mis on tagajärg (siis …)?")}</span></div>
        <div class="lk-tekst">${read.map(rida).join("")}</div>
        <button type="button" class="nupp teine lk-nupp" aria-expanded="false">Näita lahkamist</button>
        <div class="lk-tulem" hidden><ul class="lk-legend">${legend}</ul><ol class="lk-tabel">${tabel}</ol>
          ${s.valem ? `<p class="lk-valem">${md(s.valem)}</p>` : ""}</div></div>`;
    },
    /* Subsumeerimine: normi tunnused ↔ elulised asjaolud (↔ tõend); kasutaja otsustab iga rea, siis järeldus. */
    subsumeeri(s) {
      const read = s.read.map((x, i) => `<li class="sb-rida" data-oige="${x.taidetud ? 1 : 0}">
        <div class="sb-tunnus"><span class="sb-nr">${s.seos === "või" ? "V" : "K"}${i + 1}</span>${md(x.tunnus)}</div>
        <div class="sb-asjaolu">${md(x.asjaolu)}${x.toend ? `<span class="sb-toend">Tõend: ${md(x.toend)}</span>` : ""}</div>
        <div class="sb-otsus" role="group" aria-label="Kas tunnus on täidetud?"><button type="button" class="sb-v" data-v="1">✓ täidetud</button><button type="button" class="sb-v" data-v="0">✗ ei ole</button></div>
        ${x.selgitus ? `<div class="sb-selg" hidden>${md(x.selgitus)}</div>` : ""}</li>`).join("");
      return `<div class="s-subsumeeri" data-seos="${s.seos || "ja"}">
        <div class="sb-pea">${s.kysimus ? `<p class="sb-kys"><b>Õiguslik küsimus:</b> ${md(s.kysimus)}</p>` : ""}
          <p class="sb-norm">${A.refNupp(s.viide)} <span>Tunnused peavad olema täidetud <b>${s.seos === "või" ? "vähemalt üks (alternatiivne koosseis)" : "kõik korraga (kumulatiivne koosseis)"}</b>.</span></p></div>
        <div class="sb-veerud" aria-hidden="true"><span>Normi tunnus (kui …)</span><span>Mis elus juhtus</span><span>Kas klapib?</span></div>
        <ol class="sb-read">${read}</ol>
        <div class="sb-jareldus" hidden><b>Järeldus</b>${md(s.jareldus)}${s.tagajarg ? `<p class="sb-tagajarg">Tagajärg normis: ${md(s.tagajarg)}</p>` : ""}</div></div>`;
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
    return `<figure class="skeem" style="margin-inline:0">${s.pealkiri ? `<h3>${md(s.pealkiri)}</h3>` : ""}${s.sissejuhatus ? `<p class="skeem-sissejuhatus">${md(s.sissejuhatus)}</p>` : ""}${f(s)}${s.allkiri ? `<figcaption>${md(s.allkiri)}</figcaption>` : ""}</figure>`;
  };
})();
