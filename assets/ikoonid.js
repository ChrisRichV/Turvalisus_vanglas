/* Teemade ikoonid: ühtne joonstiil (24 × 24, joon 1.7, ümarad otsad), värv = currentColor.
   Ikoonil ei ole värvitähendust – see on ainult äratundmiseks. Uus ikoon: lisa siia ja kirjuta
   teemafaili "ikoon": "<nimi>". */
(function () {
  "use strict";
  const A = (window.APP = window.APP || {});
  const PAR = (x, y, s) => `<text x="${x}" y="${y}" font-size="${s}" text-anchor="middle" fill="currentColor" stroke="none" font-family="Georgia,'Times New Roman',serif">§</text>`;
  const tahed = [[12, 4.5], [17.3, 6.7], [19.5, 12], [17.3, 17.3], [12, 19.5], [6.7, 17.3], [4.5, 12], [6.7, 6.7]]
    .map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.25" fill="currentColor" stroke="none"/>`).join("");

  A.IKOONID = {
    gloobus: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M4.6 7.5h14.8M4.6 16.5h14.8"/>',
    tahering: tahed + '<circle cx="12" cy="12" r="3.2"/>',
    kohtumaja: '<path d="M3 10h18L12 4z"/><path d="M5 10v7M9.7 10v7M14.3 10v7M19 10v7M4 17h16M3 20h18"/>',
    haamer: '<path d="M13.3 4.7l6 6M10.3 7.7l6 6M11.8 6.2l3-3 6 6-3 3"/><path d="M12.2 11.8L4.5 19.5a1.4 1.4 0 0 0 2 2l7.7-7.7"/><path d="M3 21h7"/>',
    kohtutaht: '<path d="M3 11h18L12 5z"/><path d="M5 11v6M9.7 11v6M14.3 11v6M19 11v6M4 17h16M3 20h18"/><circle cx="12" cy="2.6" r="1" fill="currentColor" stroke="none"/>',
    astmed: '<path d="M3 20h18"/><path d="M4 20v-4h5v-4h5V8h6v12"/><path d="M15.5 8V5.5M15.5 5.5h3"/>',
    kilp: '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M12 15.5s-3.6-2.2-3.6-4.6a1.8 1.8 0 0 1 3.6-.6 1.8 1.8 0 0 1 3.6.6c0 2.4-3.6 4.6-3.6 4.6z"/>',
    vaarikus: '<circle cx="12" cy="9" r="3"/><path d="M6.5 20c0-3 2.5-5.5 5.5-5.5s5.5 2.5 5.5 5.5"/><path d="M5 6.5a8.5 8.5 0 0 1 14 0"/>',
    pulss: '<path d="M3 12h4l2-5 3 10 2.5-7 1.5 2H21"/>',
    kompass: '<circle cx="12" cy="12" r="9"/><path d="M15.6 8.4l-2 5.2-5.2 2 2-5.2z"/><circle cx="12" cy="12" r=".6" fill="currentColor"/>',
    varjupaik: '<path d="M3 11l9-7 9 7"/><path d="M6 9.5V20h12V9.5"/><path d="M9.5 20v-3a2.5 2.5 0 0 1 5 0v3"/><circle cx="12" cy="12" r="1.4"/>',
    umbrik: '<rect x="2.5" y="5.5" width="14" height="10" rx="1.5"/><path d="M2.5 6.5l7 5 7-5"/><rect x="14.5" y="13.5" width="7" height="6.5" rx="1"/><path d="M16.2 13.5v-1.6a1.8 1.8 0 0 1 3.6 0v1.6"/>',
    kuunal: '<rect x="9" y="11" width="6" height="9" rx="1"/><path d="M12 11V9.2"/><path d="M12 3.5c1.6 1.8 1.8 3.1 0 4.6-1.8-1.5-1.6-2.8 0-4.6z"/><path d="M6 20h12"/>',
    dokument: '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5"/><path d="M8.5 14.2l2.4 2.4 4.6-5"/>',
    kaalud: '<path d="M12 4v16M8 20h8M5 7h14"/><path d="M5 7l-2.6 6a2.6 2.6 0 0 0 5.2 0z"/><path d="M19 7l-2.6 6a2.6 2.6 0 0 0 5.2 0z"/><circle cx="12" cy="4" r="1"/>',
    raamat: '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3"/>' + PAR(12, 14, 9),
    sambad: '<path d="M3.5 6.5h17M4.5 9h15"/><path d="M6.5 9v9.5M12 9v9.5M17.5 9v9.5"/><path d="M4.5 18.5h15M3 21h18"/><path d="M8 6.5L12 3l4 3.5"/>',
    kolmnurk: '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M10.8 7.2l-4.6 8.6M13.2 7.2l4.6 8.6M7.5 18h9"/>',
    luup: '<circle cx="10" cy="10" r="6.5"/><path d="M14.8 14.8L20.5 20.5"/>' + PAR(10, 13, 8.5),
    liigid: '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><circle cx="17" cy="7" r="3.5"/><path d="M7 13.5l3.8 7H3.2z"/><path d="M13.5 17h7M17 13.5v7"/>',
    kandja: '<circle cx="6" cy="8" r="2.4"/><path d="M2.5 17.5c0-2 1.6-3.7 3.5-3.7s3.5 1.7 3.5 3.7"/><path d="M14.5 20V9.5L18 7l3.5 2.5V20"/><path d="M16.8 12h2.4M16.8 15h2.4M13 20h9.5"/><path d="M10.5 11h2.8M12 9.6l1.4 1.4-1.4 1.4"/>',
    kaitseala: '<circle cx="13.5" cy="13.5" r="7"/><circle cx="13.5" cy="13.5" r="2.2"/><path d="M2.5 2.5l7.4 7.4"/><path d="M9.9 5.6v4.3H5.6"/>',
    trellid: '<rect x="3" y="3.5" width="12" height="17" rx="1.5"/><path d="M7 3.5v17M11 3.5v17"/><circle cx="17.5" cy="16.5" r="4"/><path d="M15.7 16.6l1.3 1.3 2.4-2.6"/>',
    vordsus: '<circle cx="6" cy="7" r="2.4"/><circle cx="18" cy="7" r="2.4"/><path d="M2.5 16c0-2 1.6-3.7 3.5-3.7s3.5 1.7 3.5 3.7M14.5 16c0-2 1.6-3.7 3.5-3.7s3.5 1.7 3.5 3.7"/><path d="M10 18.5h4M10 21h4"/>',
    rongas: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/><path d="M6 6l3.5 3.5M14.5 14.5L18 18M18 6l-3.5 3.5M9.5 14.5L6 18"/>',
    voti: '<circle cx="8" cy="8" r="4.2"/><path d="M11 11l9.5 9.5M16 16l2.2-2.2M18.6 18.6l2.2-2.2"/>',
    kaart: '<circle cx="5" cy="6" r="2.2"/><circle cx="18.5" cy="5" r="2.2"/><circle cx="12" cy="13" r="2.6"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="18.5" r="2.2"/><path d="M6.8 7.4l3.3 3.8M16.7 6.4l-3.2 4.6M10.2 14.9L6.6 17.6M14.4 14.4l2.9 2.7"/>'
  };

  A.ikoon = function (nimi, klass) {
    const s = A.IKOONID[nimi];
    if (!s) return "";
    return `<svg class="ikoon${klass ? " " + klass : ""}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${s}</svg>`;
  };
})();
