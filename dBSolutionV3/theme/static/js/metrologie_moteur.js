/* Métrologie moteur : calculs en direct (ovalisation, conicité, jeux, cylindrée), contrôle des tolérances,
   ajout / retrait de lignes (cylindres, tourillons). Cotes en mm au centième. */
(function () {
    "use strict";

    const form = document.getElementById("metrologie-form");
    if (!form) return;

    const PI = Math.PI;

    function num(el) {
        if (!el) return null;
        const v = String(el.value || "").trim().replace(",", ".");
        if (v === "") return null;
        const n = Number(v);
        return Number.isFinite(n) ? n : null;
    }
    const champ = (name) => form.querySelector(`[name="${name}"]`);
    const val = (name) => num(champ(name));
    const tol = (cle) => val("tol_" + cle);
    const fmt = (n) => (n === null ? "—" : n.toFixed(2).replace(".", ","));
    const ecart = (...v) => { const x = v.filter((a) => a !== null); return x.length >= 2 ? Math.max(...x) - Math.min(...x) : null; };
    const maxi = (...v) => { const x = v.filter((a) => a !== null); return x.length ? Math.max(...x) : null; };
    const mini = (...v) => { const x = v.filter((a) => a !== null); return x.length ? Math.min(...x) : null; };
    const arrondi = (n) => Math.round(n * 100) / 100;

    /* statut : null (non contrôlé), true (OK), false (hors tolérance) */
    function statut(valeurs, tmin, tmax) {
        const v = valeurs.filter((a) => a !== null);
        if (!v.length || (tmin === null && tmax === null)) return null;
        return v.every((x) => (tmin === null || arrondi(x) >= tmin) && (tmax === null || arrondi(x) <= tmax));
    }

    function afficher(ligne, cle, texte, ok) {
        const cell = ligne.querySelector(`[data-calc="${cle}"]`);
        if (!cell) return;
        cell.textContent = texte;
        cell.classList.remove("ok", "hors");
        if (ok === true) cell.classList.add("ok");
        if (ok === false) cell.classList.add("hors");
        return ok === false ? 1 : 0;
    }

    function lignesDe(prefix) {
        return form.querySelectorAll(`tr[data-prefix="${prefix}"]`);
    }

    function calculerCylindre(prefix) {
        const g = (n) => val(`${prefix}-${n}`);
        let hors = 0;
        const rows = lignesDe(prefix);
        const R = (cle, texte, ok) => { rows.forEach((r) => { hors += afficher(r, cle, texte, ok) || 0; }); };

        // Chemise
        const ch = ["chemise_haut_a", "chemise_haut_b", "chemise_milieu_a", "chemise_milieu_b", "chemise_bas_a", "chemise_bas_b"].map(g);
        const [ha, hb, ma, mb, ba, bb] = ch;
        const oval = maxi(ecart(ha, hb), ecart(ma, mb), ecart(ba, bb));
        const coni = maxi(ecart(ha, ma, ba), ecart(hb, mb, bb));
        R("chemise_ovalisation", fmt(oval), statut([oval], null, tol("chemise_ovalisation_max")));
        R("chemise_conicite", fmt(coni), statut([coni], null, tol("chemise_conicite_max")));
        // diamètres de chemise hors tolérance : bordure rouge sur la cellule
        const dmin = tol("chemise_diametre_min"), dmax = tol("chemise_diametre_max");
        ["chemise_haut_a", "chemise_haut_b", "chemise_milieu_a", "chemise_milieu_b", "chemise_bas_a", "chemise_bas_b"].forEach((n, i) => {
            const el = champ(`${prefix}-${n}`);
            const s = statut([ch[i]], dmin, dmax);
            if (el) el.classList.toggle("hors", s === false);
            if (s === false) hors += 1;
        });

        // Piston
        const piston = g("piston_diametre");
        const cmin = mini(...ch), cmax = maxi(...ch);
        if (piston !== null && cmin !== null) {
            const j1 = cmin - piston, j2 = cmax - piston;
            R("jeu_piston", j1 === j2 ? fmt(j1) : `${fmt(j1)} – ${fmt(j2)}`, statut([j1, j2], tol("jeu_piston_min"), tol("jeu_piston_max")));
        } else R("jeu_piston", "—", null);

        // Segments
        [["segment_feu", "segment_feu_jeu"], ["segment_etancheite", "segment_etancheite_jeu"], ["segment_racleur", "segment_racleur_jeu"]].forEach(([cle, n]) => {
            const v = g(n);
            const s = statut([v], tol(cle + "_min"), tol(cle + "_max"));
            R(cle, v === null ? "—" : (s === null ? "" : (s ? "OK" : "✕")), s);
        });

        // Maneton
        const m = ["maneton_1_a", "maneton_1_b", "maneton_2_a", "maneton_2_b"].map(g);
        const mmin = mini(...m), mmax = maxi(...m);
        R("maneton_diametre", mmin === null ? "—" : `${fmt(mmin)} – ${fmt(mmax)}`,
            statut([mmin, mmax], tol("maneton_diametre_min"), tol("maneton_diametre_max")));
        const mo = maxi(ecart(m[0], m[1]), ecart(m[2], m[3]));
        const mc = maxi(ecart(m[0], m[2]), ecart(m[1], m[3]));
        R("maneton_ovalisation", fmt(mo), statut([mo], null, tol("maneton_ovalisation_max")));
        R("maneton_conicite", fmt(mc), statut([mc], null, tol("maneton_conicite_max")));

        // Pied de bielle
        const pa = g("pied_bielle_a"), pb = g("pied_bielle_b"), axe = g("axe_piston_diametre");
        const po = ecart(pa, pb);
        R("pied_bielle_ovalisation", fmt(po), statut([po], null, tol("pied_bielle_ovalisation_max")));
        const pmin = mini(pa, pb), pmax = maxi(pa, pb);
        if (axe !== null && pmin !== null) {
            const j1 = pmin - axe, j2 = pmax - axe;
            R("jeu_pied_bielle", j1 === j2 ? fmt(j1) : `${fmt(j1)} – ${fmt(j2)}`, statut([j1, j2], tol("jeu_pied_bielle_min"), tol("jeu_pied_bielle_max")));
        } else R("jeu_pied_bielle", "—", null);

        // numéro recopié dans les autres tableaux
        const numero = champ(`${prefix}-numero`);
        rows.forEach((r) => { const c = r.querySelector(".numero-cyl"); if (c && numero) c.textContent = numero.value; });

        // ligne marquée supprimée
        const del = champ(`${prefix}-DELETE`);
        rows.forEach((r) => r.classList.toggle("opacity-40", !!(del && del.checked)));
        return del && del.checked ? 0 : hors;
    }

    function calculerTourillon(prefix) {
        const g = (n) => val(`${prefix}-${n}`);
        const rows = lignesDe(prefix);
        let hors = 0;
        const R = (cle, texte, ok) => { rows.forEach((r) => { hors += afficher(r, cle, texte, ok) || 0; }); };
        const t = ["section_1_a", "section_1_b", "section_2_a", "section_2_b"].map(g);
        const tmin = mini(...t), tmax = maxi(...t);
        R("tourillon_diametre", tmin === null ? "—" : `${fmt(tmin)} – ${fmt(tmax)}`,
            statut([tmin, tmax], tol("tourillon_diametre_min"), tol("tourillon_diametre_max")));
        const o = maxi(ecart(t[0], t[1]), ecart(t[2], t[3]));
        const c = maxi(ecart(t[0], t[2]), ecart(t[1], t[3]));
        R("tourillon_ovalisation", fmt(o), statut([o], null, tol("tourillon_ovalisation_max")));
        R("tourillon_conicite", fmt(c), statut([c], null, tol("tourillon_conicite_max")));
        const del = champ(`${prefix}-DELETE`);
        rows.forEach((r) => r.classList.toggle("opacity-40", !!(del && del.checked)));
        return del && del.checked ? 0 : hors;
    }

    function prefixes(classe) {
        return Array.from(form.querySelectorAll(`tr.${classe}`)).map((r) => r.dataset.prefix);
    }

    /* ---------------- Cylindrée ---------------- */
    function nbCyl() { return val("nombre_cylindres") || 0; }

    function moyenneChemises() {
        const v = [];
        prefixes("ligne-cyl").forEach((p) => {
            ["chemise_haut_a", "chemise_haut_b", "chemise_milieu_a", "chemise_milieu_b", "chemise_bas_a", "chemise_bas_b"]
                .forEach((n) => { const x = val(`${p}-${n}`); if (x !== null) v.push(x); });
        });
        return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null;
    }

    function calcul(type) {
        const n = nbCyl();
        const d = val("alesage_mesure"), c = val("course_mesuree"), v = val("cylindree_cm3");
        const k = PI / 4 * n / 1000;
        if (type === "alesage_moyen") {
            const m = moyenneChemises();
            if (m !== null) champ("alesage_mesure").value = m.toFixed(2);
        } else if (!n) {
            return;
        } else if (type === "cylindree" && d && c) {
            champ("cylindree_cm3").value = (k * d * d * c).toFixed(1);
        } else if (type === "course" && v && d) {
            champ("course_mesuree").value = (v / (k * d * d)).toFixed(2);
        } else if (type === "alesage" && v && c) {
            champ("alesage_mesure").value = Math.sqrt(v / (k * c)).toFixed(2);
        }
        tout();
    }

    function resumeCylindree() {
        const n = nbCyl(), d = val("alesage_mesure"), c = val("course_mesuree"), v = val("cylindree_cm3");
        const vc = val("cylindree_constructeur_cm3");
        document.getElementById("res-cyl-unitaire").textContent = v && n ? (v / n).toFixed(1).replace(".", ",") + " cm³" : "—";
        if (d && c) {
            const r = c / d;
            const type = r < 0.98 ? "super-carré" : (r > 1.02 ? "longue course" : "carré");
            document.getElementById("res-rapport").textContent = r.toFixed(2).replace(".", ",") + " (" + type + ")";
        } else document.getElementById("res-rapport").textContent = "—";
        document.getElementById("res-ecart").textContent = v && vc ? ((v - vc) / vc * 100).toFixed(2).replace(".", ",") + " %" : "—";
    }

    function tout() {
        let hors = 0;
        prefixes("ligne-cyl").forEach((p) => { hors += calculerCylindre(p); });
        prefixes("ligne-tour").forEach((p) => { hors += calculerTourillon(p); });
        const h = document.getElementById("res-hors");
        h.textContent = hors;
        h.className = "font-bold " + (hors ? "text-red-700" : "text-green-700");
        resumeCylindree();
    }

    /* ---------------- Lignes ---------------- */
    function ajouter(prefix, gabarits, numero) {
        const total = form.querySelector(`#id_${prefix}-TOTAL_FORMS`);
        const index = Number(total.value);
        gabarits.forEach(([tpl, table]) => {
            const html = document.getElementById(tpl).innerHTML.replace(/__prefix__/g, String(index));
            document.querySelector(`#${table} tbody`).insertAdjacentHTML("beforeend", html);
        });
        total.value = index + 1;
        const n = champ(`${prefix}-${index}-numero`);
        if (n) n.value = numero;
    }

    const GABARITS_CYL = [["tpl-cyl-chemise", "table-chemise"], ["tpl-cyl-segments", "table-segments"],
        ["tpl-cyl-maneton", "table-maneton"], ["tpl-cyl-bielle", "table-bielle"]];
    const GABARITS_TOUR = [["tpl-tour", "table-tourillon"]];

    function prochainNumero(classe) {
        let m = 0;
        prefixes(classe).forEach((p) => { const x = val(`${p}-numero`); if (x) m = Math.max(m, x); });
        return m + 1;
    }

    function ajusterLignes(classe, prefix, gabarits, cible) {
        let presentes = prefixes(classe);
        // retire les lignes nouvelles et vides en trop
        for (let i = presentes.length - 1; i >= 0 && presentes.length > cible; i--) {
            const p = presentes[i];
            if (!champ(`${p}-id`) || champ(`${p}-id`).value) continue;
            const rempli = Array.from(form.querySelectorAll(`tr[data-prefix="${p}"] input.cote`)).some((e) => e.value !== "");
            if (!rempli) { lignesDe(p).forEach((r) => r.remove()); presentes.splice(i, 1); }
        }
        while (presentes.length < cible) {
            ajouter(prefix, gabarits, prochainNumero(classe));
            presentes = prefixes(classe);
        }
    }

    document.getElementById("generer-lignes").addEventListener("click", () => {
        const n = nbCyl();
        if (!n) return;
        ajusterLignes("ligne-cyl", "cyl", GABARITS_CYL, n);
        ajusterLignes("ligne-tour", "tour", GABARITS_TOUR, n + 1);
        tout();
    });
    document.getElementById("ajouter-cylindre").addEventListener("click", () => { ajouter("cyl", GABARITS_CYL, prochainNumero("ligne-cyl")); tout(); });
    document.getElementById("ajouter-tourillon").addEventListener("click", () => { ajouter("tour", GABARITS_TOUR, prochainNumero("ligne-tour")); tout(); });

    form.addEventListener("click", (e) => {
        const b = e.target.closest(".retirer-ligne");
        if (!b) return;
        const p = b.closest("tr").dataset.prefix;
        lignesDe(p).forEach((r) => r.remove());
        tout();
    });
    form.querySelectorAll(".calc-btn").forEach((b) => b.addEventListener("click", () => calcul(b.dataset.calcule)));
    form.addEventListener("input", tout);
    form.addEventListener("change", tout);

    /* ---------------- Kilométrage (variation > 2 000 km à confirmer) ---------------- */
    const kmAvant = champ("kilometres_chassis"), kmInter = champ("kilometrage_metrologie"), kmVar = champ("kilometrage_variation");
    const popup = document.getElementById("kilometrage-popup");
    let variationConfirmee = false;
    function variation() {
        const a = num(kmAvant), b = num(kmInter);
        if (kmVar) kmVar.value = a !== null && b !== null ? b - a : "";
        variationConfirmee = false;
    }
    if (kmAvant && kmInter && kmVar && popup) {
        kmInter.addEventListener("input", variation);
        form.addEventListener("submit", (e) => {
            const v = Number(kmVar.value);
            if (v > 2000 && !variationConfirmee) {
                e.preventDefault();
                document.getElementById("popup-variation").textContent = v.toLocaleString();
                popup.classList.add("popup-visible");
            }
        });
        document.getElementById("popup-annuler").addEventListener("click", () => { popup.classList.remove("popup-visible"); kmInter.focus(); });
        document.getElementById("popup-confirmer").addEventListener("click", () => {
            variationConfirmee = true; popup.classList.remove("popup-visible"); form.requestSubmit();
        });
        variation();
    }

    tout();
})();
