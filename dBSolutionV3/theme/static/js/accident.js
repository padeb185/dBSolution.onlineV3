/* Rapport d'accident : total des pièces, ajout de lignes, demi-train complet, tiers, kilométrage. */
(function () {
    "use strict";
    const form = document.getElementById("accident-form");
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
    const prefixes = () => Array.from(form.querySelectorAll("tr.ligne-piece")).map((r) => r.dataset.prefix);
    const supprime = (p) => { const d = champ(`${p}-DELETE`); return !!(d && d.checked); };

    /* ---------- Total des pièces ---------- */
    const fmtEuro = (n) => n.toFixed(2).replace(".", ",") + " €";
    const CHIFFREES = ["A_REMPLACER", "REMPLACE", "A_REPARER", "REPARE", "A_CALIBRER"];
    function majPieces() {
        let total = 0;
        prefixes().forEach((p) => {
            const row = form.querySelector(`tr[data-prefix="${p}"]`);
            const q = val(`${p}-quantite`) || 0, pr = val(`${p}-prix`) || 0;
            const dec = (champ(`${p}-decision`) || {}).value || "";
            const facture = CHIFFREES.includes(dec) && !supprime(p) && (champ(`${p}-piece`) || {}).value;
            const t = q * pr;
            row.querySelector(".total-ligne").textContent = facture ? fmtEuro(t) : "—";
            if (facture) total += t;
            const grav = (champ(`${p}-gravite`) || {}).value;
            row.classList.toggle("bg-red-50", grav === "GRAVE" || grav === "DETRUITE");
            row.classList.toggle("opacity-40", supprime(p));
        });
        document.getElementById("total-pieces").textContent = fmtEuro(total);
    }

    /* ---------- Tiers ---------- */
    function majTiers() {
        const t = champ("tiers_implique");
        const bloc = form.querySelector(".champ-tiers_details");
        if (t && bloc) bloc.style.display = t.checked ? "" : "none";
    }

    function tout() { majPieces(); majTiers(); }

    /* ---------- Ajout / retrait de lignes ---------- */
    function ajouter(valeurs) {
        const total = form.querySelector("#id_piece-TOTAL_FORMS");
        const i = Number(total.value);
        const html = document.getElementById("tpl-piece").innerHTML.replace(/__prefix__/g, String(i));
        document.querySelector("#table-pieces tbody").insertAdjacentHTML("beforeend", html);
        total.value = i + 1;
        Object.entries(valeurs || {}).forEach(([k, v]) => { const c = champ(`piece-${i}-${k}`); if (c) c.value = v; });
        return i;
    }
    document.getElementById("ajouter-piece").addEventListener("click", () => {
        const zone = (document.getElementById("zone-demi-train") || {}).value;
        ajouter(zone ? { zone: zone } : {});
        tout();
    });

    // Demi-train : toutes les pièces à contrôler pour la zone choisie
    const DEMI_TRAIN = ["AMORTISSEUR", "TRIANGLE_INF", "TRIANGLE_SUP", "FUSEE", "ROULEMENT", "CAPTEUR_ABS",
                        "BIELLETTE_DIRECTION", "ROTULE_DIRECTION", "BIELLETTE_STAB", "CARDAN"];
    document.getElementById("ajouter-demi-train").addEventListener("click", () => {
        const zone = document.getElementById("zone-demi-train").value;
        const arriere = zone === "ARG" || zone === "ARD";
        DEMI_TRAIN.forEach((piece) => {
            // Biellette / rotule de direction : uniquement à l'avant (sauf essieu directeur)
            if (arriere && (piece === "BIELLETTE_DIRECTION" || piece === "ROTULE_DIRECTION")) return;
            ajouter({ zone: zone, piece: piece, decision: "A_CONTROLER", gravite: "LEGERE", quantite: "1" });
        });
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
    const kmAvant = champ("kilometres_chassis"), kmInter = champ("kilometrage_accident"), kmVar = champ("kilometrage_variation");
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
