/* Casse boîte manuelle : pistes de diagnostic, lubrification, contrôle par rapport, total des pièces, ajout de lignes. */
(function () {
    "use strict";
    const form = document.getElementById("casse-form");
    if (!form) return;

    const champ = (n) => form.querySelector(`[name="${n}"]`);
    function num(el) {
        if (!el) return null;
        const v = String(el.value || "").trim().replace(",", ".");
        if (v === "") return null;
        const n = Number(v);
        return Number.isFinite(n) ? n : null;
    }
    const val = (n) => num(champ(n));
    const valeur = (n) => (champ(n) || {}).value || "";
    const prefixes = (classe) => Array.from(form.querySelectorAll(`tr.${classe}`)).map((r) => r.dataset.prefix);
    const supprime = (p) => { const d = champ(`${p}-DELETE`); return !!(d && d.checked); };
    const coche = (n) => { const c = champ(n); return !!(c && c.checked); };
    const libelleRapport = (p) => { const s = champ(`${p}-rapport`); return s && s.selectedIndex >= 0 ? s.options[s.selectedIndex].text : ""; };

    /* ---------- Lubrification ---------- */
    function manqueHuile() {
        const cap = val("capacite_huile_l"), q = val("quantite_vidangee_l");
        const niveau = valeur("niveau_huile");
        const parQuantite = cap && q !== null && q < cap * 0.8;
        const p = document.getElementById("manque-huile");
        if (p) {
            p.classList.toggle("hidden", !parQuantite);
            if (parQuantite) p.textContent = `⚠ ${q.toString().replace(".", ",")} L / ${cap.toString().replace(".", ",")} L`;
        }
        ["capacite_huile_l", "quantite_vidangee_l"].forEach((n) => { const c = champ(n); if (c) c.classList.toggle("hors", !!parQuantite); });
        return parQuantite || niveau === "BAS" || niveau === "VIDE";
    }

    /* ---------- Pistes de diagnostic ---------- */
    let pistes = [];
    try { pistes = JSON.parse(document.getElementById("pistes-data").textContent); } catch (e) { pistes = []; }

    function majPistes() {
        const msgs = pistes.filter(([champs]) => champs.every((c) => coche(c))).map(([, m]) => m);
        const d = form.dataset;
        if (manqueHuile()) msgs.push(d.pisteManqueHuile);
        if (valeur("etat_huile") === "EMULSION") msgs.push(d.pisteEau);
        if (valeur("bouchon_magnetique") === "ECLATS" || valeur("etat_huile") === "ECLATS") msgs.push(d.pisteEclats);

        const essais = prefixes("ligne-essai").filter((p) => !supprime(p));
        const craque = essais.filter((p) => coche(`${p}-craquement`)).map(libelleRapport);
        const saute = essais.filter((p) => coche(`${p}-saute`)).map(libelleRapport);
        if (craque.length) msgs.push(`${d.pisteCraque} (${craque.join(", ")})`);
        if (saute.length) msgs.push(`${d.pisteSaute} (${saute.join(", ")})`);
        if (craque.length >= 3) msgs.push(d.pistePlusieurs);

        const box = document.getElementById("pistes"), ul = document.getElementById("pistes-liste");
        ul.innerHTML = "";
        msgs.filter(Boolean).forEach((m) => { const li = document.createElement("li"); li.textContent = m; ul.appendChild(li); });
        box.classList.toggle("hidden", msgs.length === 0);
    }

    /* ---------- Contrôle par rapport ---------- */
    function majEssais() {
        prefixes("ligne-essai").forEach((p) => {
            const row = form.querySelector(`tr[data-prefix="${p}"]`);
            const anomalie = ["craquement", "saute", "passage_dur", "impossible", "bruit"].some((s) => coche(`${p}-${s}`));
            row.classList.toggle("bg-red-50", anomalie && !supprime(p));
            row.classList.toggle("opacity-40", supprime(p));
        });
    }

    /* ---------- Pièces ---------- */
    const fmtEuro = (n) => n.toFixed(2).replace(".", ",") + " €";
    function majPieces() {
        let total = 0;
        prefixes("ligne-piece").forEach((p) => {
            const row = form.querySelector(`tr[data-prefix="${p}"]`);
            const q = val(`${p}-quantite`) || 0, pr = val(`${p}-prix`) || 0;
            const dec = valeur(`${p}-decision`);
            const facture = ["A_REMPLACER", "REMPLACE", "A_REPARER", "REPARE"].includes(dec) && !supprime(p) && valeur(`${p}-piece`);
            const t = q * pr;
            row.querySelector(".total-ligne").textContent = facture ? fmtEuro(t) : "—";
            if (facture) total += t;
            const grav = valeur(`${p}-gravite`);
            row.classList.toggle("bg-red-50", grav === "GRAVE" || grav === "DETRUITE");
            row.classList.toggle("opacity-40", supprime(p));
        });
        document.getElementById("total-pieces").textContent = fmtEuro(total);
    }

    function tout() { majPistes(); majEssais(); majPieces(); }

    /* ---------- Ajout / retrait de lignes ---------- */
    function ajouter(prefix, tpl, table) {
        const total = form.querySelector(`#id_${prefix}-TOTAL_FORMS`);
        const i = Number(total.value);
        const html = document.getElementById(tpl).innerHTML.replace(/__prefix__/g, String(i));
        document.querySelector(`#${table} tbody`).insertAdjacentHTML("beforeend", html);
        total.value = i + 1;
        return i;
    }
    document.getElementById("ajouter-piece").addEventListener("click", () => { ajouter("piece", "tpl-piece", "table-pieces"); tout(); });
    document.getElementById("ajouter-essai").addEventListener("click", () => {
        const pris = new Set(prefixes("ligne-essai").map((p) => valeur(`${p}-rapport`)));
        const i = ajouter("essai", "tpl-essai", "table-essais");
        const s = champ(`essai-${i}-rapport`);
        if (s) {
            const libre = Array.from(s.options).find((o) => o.value && !pris.has(o.value));
            if (libre) s.value = libre.value;
        }
        tout();
    });
    form.addEventListener("click", (e) => {
        const b = e.target.closest(".retirer-ligne");
        if (!b) return;
        b.closest("tr").remove();
        tout();
    });
    form.addEventListener("input", tout);
    form.addEventListener("change", tout);

    /* ---------- Kilométrage ---------- */
    const kmAvant = champ("kilometres_chassis"), kmInter = champ("kilometrage_casse"), kmVar = champ("kilometrage_variation");
    const popup = document.getElementById("kilometrage-popup");
    let confirme = false;
    function variation() {
        const a = num(kmAvant), b = num(kmInter);
        if (kmVar) kmVar.value = a !== null && b !== null ? b - a : "";
        confirme = false;
    }
    if (kmAvant && kmInter && kmVar && popup) {
        kmInter.addEventListener("input", variation);
        form.addEventListener("submit", (e) => {
            const v = Number(kmVar.value);
            if (v > 2000 && !confirme) {
                e.preventDefault();
                document.getElementById("popup-variation").textContent = v.toLocaleString();
                popup.classList.add("popup-visible");
            }
        });
        document.getElementById("popup-annuler").addEventListener("click", () => { popup.classList.remove("popup-visible"); kmInter.focus(); });
        document.getElementById("popup-confirmer").addEventListener("click", () => { confirme = true; popup.classList.remove("popup-visible"); form.requestSubmit(); });
        variation();
    }

    tout();
})();
