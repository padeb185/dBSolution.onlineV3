/* Casse moteur : pistes de diagnostic, écarts de compression, fuites, total des pièces, ajout de lignes. */
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
    const prefixes = (classe) => Array.from(form.querySelectorAll(`tr.${classe}`)).map((r) => r.dataset.prefix);
    const supprime = (p) => { const d = champ(`${p}-DELETE`); return !!(d && d.checked); };

    /* ---------- Pistes de diagnostic ---------- */
    let pistes = [];
    try { pistes = JSON.parse(document.getElementById("pistes-data").textContent); } catch (e) { pistes = []; }

    function majPistes() {
        const msgs = pistes.filter(([champs]) => champs.every((c) => champ(c) && champ(c).checked)).map(([, m]) => m);
        const essais = prefixes("ligne-essai").filter((p) => !supprime(p));
        const coche = (suffixe) => essais.some((p) => champ(`${p}-${suffixe}`) && champ(`${p}-${suffixe}`).checked);
        if (coche("fuite_refroidissement")) msgs.push(form.dataset.pisteRefroidissement || "Fuite vers le refroidissement : joint de culasse ou fissure.");
        if (coche("fuite_admission") || coche("fuite_echappement")) msgs.push(form.dataset.pisteSoupapes || "Fuite par l'admission / l'échappement : soupape tordue, brûlée ou mal assise.");
        if (coche("fuite_carter")) msgs.push(form.dataset.pisteCarter || "Fuite au carter : segments, piston fissuré ou percé, cylindre rayé.");
        const box = document.getElementById("pistes"), ul = document.getElementById("pistes-liste");
        ul.innerHTML = "";
        msgs.forEach((m) => { const li = document.createElement("li"); li.textContent = m; ul.appendChild(li); });
        box.classList.toggle("hidden", msgs.length === 0);
    }

    /* ---------- Compression / étanchéité ---------- */
    function majEssais() {
        const essais = prefixes("ligne-essai").filter((p) => !supprime(p));
        const comps = essais.map((p) => val(`${p}-compression_bar`)).filter((v) => v !== null);
        const best = comps.length ? Math.max(...comps) : null;
        const nominale = val("compression_nominale_bar");
        const ecartMax = val("ecart_compression_max_pct");
        const fuiteMax = val("fuite_max_pct");
        prefixes("ligne-essai").forEach((p) => {
            const row = form.querySelector(`tr[data-prefix="${p}"]`);
            const cell = row.querySelector('[data-calc="ecart"]');
            const c = val(`${p}-compression_bar`), f = val(`${p}-fuite_pct`);
            cell.classList.remove("ok", "hors");
            if (c !== null && best) {
                const e = (best - c) / best * 100;
                cell.textContent = e.toFixed(1).replace(".", ",") + " %";
                const bad = (ecartMax !== null && e > ecartMax) || (nominale && c < nominale * 0.8);
                cell.classList.add(bad ? "hors" : "ok");
            } else cell.textContent = "—";
            const fe = champ(`${p}-fuite_pct`);
            if (fe) fe.classList.toggle("hors", f !== null && fuiteMax !== null && f > fuiteMax);
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
            const dec = (champ(`${p}-decision`) || {}).value || "";
            const facture = ["A_REMPLACER", "REMPLACE", "A_REPARER", "REPARE"].includes(dec) && !supprime(p) && (champ(`${p}-piece`) || {}).value;
            const t = q * pr;
            row.querySelector(".total-ligne").textContent = facture ? fmtEuro(t) : "—";
            if (facture) total += t;
            const grav = (champ(`${p}-gravite`) || {}).value;
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
        let m = 0;
        prefixes("ligne-essai").forEach((p) => { const x = val(`${p}-numero`); if (x) m = Math.max(m, x); });
        const i = ajouter("essai", "tpl-essai", "table-essais");
        const n = champ(`essai-${i}-numero`); if (n) n.value = m + 1;
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
