/* Turvalisus vanglas – ühine loogika: andmed, märgistus, hüpikaknad, tagasiside. */
(function () {
  "use strict";

  const A = (window.APP = {});
  const cache = {};

  A.lae = function (tee) {
    if (!cache[tee]) {
      cache[tee] = fetch(tee, { cache: "no-cache" }).then((r) => {
        if (!r.ok) throw new Error(tee + " – " + r.status);
        return r.json();
      });
    }
    return cache[tee];
  };

  A.andmed = function () {
    return Promise.all([A.lae("data/tunnid.json"), A.lae("data/seadused.json"), A.lae("data/terminid.json")])
      .then(([tunnid, seadused, terminid]) => {
        A.tunnid = tunnid; A.seadused = seadused; A.terminid = terminid;
        return { tunnid, seadused, terminid };
      });
  };

  A.koikTeemad = function () {
    const failid = [];
    A.tunnid.tunnid.forEach((t) => t.teemad.forEach((tm) => failid.push(tm.fail)));
    return Promise.all(failid.map(A.lae));
  };

  /* ---------- tekst ja märgistus ---------- */
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  A.esc = esc;

  const ylaindeks = (s) => s.replace(/\^(\d+)/g, "<sup>$1</sup>");
  A.ylaindeks = ylaindeks;

  const REF = /^(.+?) (§|art|rule) ?(\d+(?:\^\d+)?)(?: lg (\d+(?:\^\d+)?))?(?: p (\S+))?\s*$/;
  A.parseRef = function (r) {
    const m = REF.exec(r.trim());
    if (!m) return null;
    return { akt: m[1], vorm: m[2], nr: m[3], lg: m[4] || null, p: m[5] || null, voti: `${m[1]} ${m[2]} ${m[3]}` };
  };

  A.refNupp = function (ref, naita) {
    const tekst = naita || ref;
    return `<button type="button" class="ref" data-ref="${esc(ref)}" aria-haspopup="dialog" aria-expanded="false">${ylaindeks(esc(tekst))}</button>`;
  };

  A.md = function (s) {
    if (s == null) return "";
    let h = esc(s);
    h = h.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, r, t) => A.refNupp(unesc(r), t ? unesc(t) : null));
    h = h.replace(/\{\{([^}|]+)(?:\|([^}]+))?\}\}/g, (_, id, t) => {
      const term = A.terminid && A.terminid[unesc(id)];
      const naita = t || (term ? esc(term.termin) : id);
      return `<button type="button" class="term" data-term="${id}" aria-haspopup="dialog" aria-expanded="false">${naita}</button>`;
    });
    h = h.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    h = h.replace(/`([^`]+)`/g, "<code>$1</code>");
    return h;
  };
  function unesc(s) {
    return s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
  }

  /* ---------- hüpikaken ---------- */
  let lipik, avaja = null;

  function looLipik() {
    lipik = document.createElement("div");
    lipik.className = "lipik";
    lipik.setAttribute("role", "dialog");
    lipik.setAttribute("aria-modal", "false");
    lipik.hidden = true;
    lipik.tabIndex = -1;
    document.body.appendChild(lipik);
  }

  function lgSobib(rida, lg, idx, akt) {
    if (!lg) return false;
    if (rida.startsWith(`(${lg})`)) return true;
    if (new RegExp("^" + lg.replace("^", "\\^") + "\\.(\\s|$)").test(rida)) return true;
    if (akt === "PS" && idx === parseInt(lg, 10) - 1) return true;
    return false;
  }

  function satteHtml(refStr) {
    const r = A.parseRef(refStr);
    const s = r && A.seadused.satted[r.voti];
    if (!s) {
      return `<div class="l-pais"><div><div class="l-viide">${ylaindeks(esc(refStr))}</div></div>${sulgeNupp()}</div>
        <p class="l-tekst">Sätte teksti ei leitud. Kontrolli Riigi Teatajast.</p>`;
    }
    const m = A.seadused.aktid[s.akt] || {};
    let onPeal = false;
    const read = s.read.map((rida, i) => {
      const muud = rida.match(/^\[(RT|Kehtetu|Sätte sõnastus)[^\]]*\]$/);
      if (muud) return `<span class="muudatus">${esc(rida)}</span>`;
      const klass = [];
      if (lgSobib(rida, r.lg, i, s.akt)) { klass.push("esile"); onPeal = true; }
      if (i === 0 || (s.akt === "harta" && i === 1)) klass.push("pealk");
      let t = esc(rida).replace(/\s*(\[(?:RT|Kehtetu|Sätte sõnastus)[^\]]*\])/g, ' <span class="muudatus">$1</span>');
      return `<p class="${klass.join(" ")}">${ylaindeks(t)}</p>`;
    }).join("");
    const meta = [];
    meta.push(`<div>${esc(m.pealkiri || s.akt)}</div>`);
    if (m.kehtivus) meta.push(`<div>Sõnastus: ${esc(m.kehtivus)}</div>`);
    if (m.avaldamismarge) meta.push(`<div>Avaldamismärge: ${esc(m.avaldamismarge)}</div>`);
    if (m.mitteametlik_tolge) meta.push(`<div><span class="silt">Mitteametlik tõlge</span> – täpne sõnastus võib erineda.</div>`);
    if (m.markus) meta.push(`<div>${esc(m.markus)}</div>`);
    if (m.url) meta.push(`<div><a href="${esc(m.url)}" target="_blank" rel="noopener">Ava ametlik tekst</a></div>`);
    const lgMarkus = r.lg && !onPeal ? `<div>Lõiget ${ylaindeks(esc(r.lg))} ei õnnestunud esile tõsta – loe kogu sätet.</div>` : "";
    return `<div class="l-pais"><div><div class="l-viide" id="lipik-pealk">${ylaindeks(esc(refStr))}</div>
      <div class="l-akt">${esc(m.pealkiri || "")}</div></div>${sulgeNupp()}</div>
      <div class="l-tekst">${read}</div>
      <div class="l-meta">${lgMarkus}${meta.slice(1).join("")}</div>`;
  }

  function terminHtml(id) {
    const t = A.terminid[id];
    if (!t) return `<div class="l-pais"><div class="l-term">${esc(id)}</div>${sulgeNupp()}</div><p>Terminit ei leitud.</p>`;
    const viited = (t.viited || []).map((v) => A.refNupp(v)).join(" ");
    return `<div class="l-pais"><div class="l-term" id="lipik-pealk">${esc(t.termin)}</div>${sulgeNupp()}</div>
      <div class="l-tekst"><p>${A.md(t.selgitus)}</p>${viited ? `<p>${viited}</p>` : ""}</div>
      <div class="l-allikas">Allikas: ${esc(t.allikas || "")}</div>`;
  }

  const sulgeNupp = () => `<button type="button" class="sulge" aria-label="Sulge">×</button>`;

  function paiguta(el) {
    if (window.matchMedia("(max-width: 640px)").matches) { lipik.style.left = ""; lipik.style.top = ""; return; }
    const r = el.getBoundingClientRect();
    const w = lipik.offsetWidth, h = lipik.offsetHeight;
    let left = Math.min(Math.max(16, r.left), window.innerWidth - w - 16);
    let top = r.bottom + 8;
    if (top + h > window.innerHeight - 16) top = Math.max(16, r.top - h - 8);
    lipik.style.left = left + "px";
    lipik.style.top = top + "px";
  }

  function ava(el, html, liik) {
    if (avaja) avaja.setAttribute("aria-expanded", "false");
    avaja = el;
    lipik.className = "lipik" + (liik === "termin" ? " termin" : "");
    lipik.innerHTML = html;
    lipik.setAttribute("aria-labelledby", "lipik-pealk");
    lipik.hidden = false;
    el.setAttribute("aria-expanded", "true");
    paiguta(el);
    lipik.focus({ preventScroll: true });
  }

  A.sulge = function () {
    if (!lipik || lipik.hidden) return;
    lipik.hidden = true;
    if (avaja) { avaja.setAttribute("aria-expanded", "false"); avaja.focus({ preventScroll: true }); }
    avaja = null;
  };

  function klikk(e) {
    const ref = e.target.closest(".ref");
    const term = e.target.closest(".term");
    if (ref) { e.preventDefault(); if (avaja === ref && !lipik.hidden) return A.sulge(); return ava(ref, satteHtml(ref.dataset.ref), "satte"); }
    if (term) { e.preventDefault(); if (avaja === term && !lipik.hidden) return A.sulge(); return ava(term, terminHtml(term.dataset.term), "termin"); }
    if (e.target.closest(".sulge")) return A.sulge();
    if (!lipik.hidden && !lipik.contains(e.target)) A.sulge();
  }

  A.kaivita = function () {
    looLipik();
    document.addEventListener("click", klikk);
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      if (lipik && !lipik.hidden) return A.sulge();
      A.sulgeNaide();
    });
    window.addEventListener("resize", () => { if (avaja && !lipik.hidden) paiguta(avaja); });
    const nupp = document.querySelector(".teemanupp");
    if (nupp) {
      const pane = (v) => {
        document.documentElement.dataset.theme = v;
        nupp.textContent = v === "dark" ? "Hele" : "Tume";
        nupp.setAttribute("aria-label", v === "dark" ? "Lülita hele vaade" : "Lülita tume vaade");
        try { localStorage.setItem("teema", v); } catch (_) { /* ei ole oluline */ }
      };
      let algne = null;
      try { algne = localStorage.getItem("teema"); } catch (_) { /* privaatne aken */ }
      if (!algne) algne = "dark"; // vaikimisi tume neoonteema
      pane(algne);
      nupp.addEventListener("click", () => pane(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
    }
  };

  /* ---------- päris näide (aken) ---------- */
  let naiteTaust = null, naiteAvaja = null, naited = [], naiteI = 0;
  function naiteHtml() {
    const n = naited[naiteI];
    const navi = naited.length > 1 ? `<div class="n-navi"><button type="button" class="nupp teine" data-n="-1">Eelmine näide</button>
      <span class="n-meta">${naiteI + 1} / ${naited.length}</span><button type="button" class="nupp teine" data-n="1">Järgmine näide</button></div>` : "";
    return `<div class="naite-aken" role="dialog" aria-modal="true" aria-labelledby="naide-pealk" tabindex="-1">
      <div class="n-pais"><div><div class="n-silt">Päris juhtum · väljaspool tunnimaterjali</div>
      <h2 id="naide-pealk">${esc(n.pealkiri)}</h2><div class="n-meta">${esc(n.kohus)}, ${esc(n.aeg)}</div></div>
      <button type="button" class="sulge" aria-label="Sulge näide">×</button></div>
      <h3>Mis juhtus</h3><p>${A.md(n.lugu)}</p>
      <h3>Tulemus</h3><p>${A.md(n.tulemus)}</p>
      <div class="n-oppetund"><strong>Mida meelde jätta:</strong> ${A.md(n.oppetund)}</div>
      ${n.seos && n.seos.length ? `<p class="naide-rida">${n.seos.map((x) => A.refNupp(x)).join(" ")}</p>` : ""}
      <div class="n-allikas">Allikas: <a href="${esc(n.allikas.url)}" target="_blank" rel="noopener">${esc(n.allikas.nimi)}</a>. Kokkuvõte on lihtsustatud; täpsus kontrolli allikast.</div>
      ${navi}</div>`;
  }
  A.avaNaide = function (list, i, avaja) {
    naited = list; naiteI = i || 0; naiteAvaja = avaja || null;
    if (!naiteTaust) {
      naiteTaust = document.createElement("div"); naiteTaust.className = "naite-taust"; naiteTaust.hidden = true;
      document.body.appendChild(naiteTaust);
      naiteTaust.addEventListener("click", (e) => {
        if (e.target.closest(".ref") || e.target.closest(".term")) return; // viited avavad lipiku
        if (e.target === naiteTaust || e.target.closest(".sulge")) return A.sulgeNaide();
        const nav = e.target.closest("[data-n]");
        if (nav) { naiteI = (naiteI + (+nav.dataset.n) + naited.length) % naited.length; naiteTaust.innerHTML = naiteHtml(); naiteTaust.querySelector(".naite-aken").focus(); }
      });
    }
    naiteTaust.innerHTML = naiteHtml(); naiteTaust.hidden = false;
    document.body.style.overflow = "hidden";
    naiteTaust.querySelector(".naite-aken").focus();
  };
  A.sulgeNaide = function () {
    if (!naiteTaust || naiteTaust.hidden) return false;
    naiteTaust.hidden = true; document.body.style.overflow = "";
    if (naiteAvaja) naiteAvaja.focus();
    return true;
  };

  /* ---------- harjutuse komponent ---------- */
  A.harjutusHtml = function (h, id, allikas) {
    const liik = h.tyyp === "kaasus" ? "Kaasus" : "Faktiküsimus";
    const all = allikas ? ` – ${esc(allikas)}` : "";
    if (h.tyyp === "tunnikys") {
      return `<div class="harjutus tunnikys" id="${id}">
        <div class="h-liik">Tunni kordamisküsimus ${h.nr}${all}</div><div class="h-kys">${A.md(h.kysimus)}</div>
        <p class="tyhi" style="margin:.2rem 0 .6rem;font-size:.92rem">Vasta enne ise – suuliselt või paberile.</p>
        <button type="button" class="nupp teine ava-vastus">Näita vastust</button>
        <div class="kaasus-vastus tunnikys-vastus" hidden><ul>${h.punktid.map((p) => `<li>${A.md(p)}</li>`).join("")}</ul></div></div>`;
    }
    if (h.tyyp === "fakt") {
      const valikud = h.valikud.map((v, i) => `<button type="button" class="valik" data-i="${i}">${A.md(v)}</button>`).join("");
      return `<div class="harjutus" data-oige="${h.oige}" id="${id}">
        <div class="h-liik">${liik}${all}</div><div class="h-kys">${A.md(h.kysimus)}</div>
        <div class="valikud">${valikud}</div><div class="selgitus" hidden>${A.md(h.selgitus || "")}</div></div>`;
    }
    const vastus = (h.vastus || []).map((v) => `<li>${A.md(v)}</li>`).join("");
    return `<div class="harjutus kaasus" id="${id}">
      <div class="h-liik">${liik}${all}</div><div class="h-kys">${A.md(h.kysimus)}</div>
      <p class="tyhi" style="margin:.2rem 0 .6rem;font-size:.92rem">Lahenda ise: kaitseala → riive → põhiseaduspärasus (formaalne + materiaalne) → järeldus.</p>
      <button type="button" class="nupp teine ava-vastus">Näita lahendust</button>
      <div class="kaasus-vastus" hidden><ol>${vastus}</ol></div></div>`;
  };

  A.seoHarjutused = function (juur, tulemus) {
    juur.addEventListener("click", (e) => {
      const valik = e.target.closest(".valik");
      if (valik) {
        const kast = valik.closest(".harjutus");
        if (kast.dataset.vastatud) return;
        kast.dataset.vastatud = "1";
        const oige = +kast.dataset.oige, i = +valik.dataset.i;
        kast.querySelectorAll(".valik").forEach((b) => {
          b.disabled = true;
          if (+b.dataset.i === oige) b.classList.add("oige");
        });
        if (i !== oige) valik.classList.add("vale");
        const sel = kast.querySelector(".selgitus");
        sel.innerHTML = `<strong>${i === oige ? "Õige." : "Vale."}</strong> ` + sel.innerHTML;
        sel.hidden = false;
        if (tulemus) tulemus(i === oige);
        return;
      }
      const ava = e.target.closest(".ava-vastus");
      if (ava) {
        const v = ava.parentElement.querySelector(".kaasus-vastus");
        v.hidden = !v.hidden;
        const vastus = ava.closest(".tunnikys");
        ava.textContent = v.hidden ? (vastus ? "Näita vastust" : "Näita lahendust") : (vastus ? "Peida vastus" : "Peida lahendus");
      }
    });
  };

  /* ---------- tagasiside (Supabase, ainult INSERT) ---------- */
  A.saadaTagasiside = function (kirje) {
    const S = window.SEADED || {};
    if (!S.supabaseUrl || !S.supabaseVoti) return Promise.reject(new Error("seadistus puudub"));
    return fetch(`${S.supabaseUrl}/rest/v1/${S.tagasisideTabel}`, {
      method: "POST",
      headers: {
        apikey: S.supabaseVoti,
        Authorization: `Bearer ${S.supabaseVoti}`,
        "Content-Type": "application/json",
        Prefer: "return=minimal"
      },
      body: JSON.stringify(kirje)
    }).then((r) => { if (!r.ok) throw new Error("HTTP " + r.status); });
  };

  A.viga = function (kuhu, e) {
    console.error(e);
    kuhu.innerHTML = `<p class="teade viga">Andmeid ei õnnestunud laadida. Ava leht veebiserveri kaudu (nt GitHub Pages või <code>python3 -m http.server</code>), mitte failina.</p>`;
  };
})();
