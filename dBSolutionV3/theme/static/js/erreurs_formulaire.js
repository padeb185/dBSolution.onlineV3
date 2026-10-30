/*
 * Formulaires : champs en erreur.
 * - entoure en rouge les champs en erreur (aria-invalid="true" posé par Django, ou .input-error) ;
 * - après un envoi refusé, va au premier champ en erreur (défilement + focus) ;
 * - affiche en haut du formulaire la liste des champs à corriger : un clic renvoie vers le champ ;
 * - quand le champ est modifié, le rouge disparaît ;
 * - les champs refusés par le navigateur (required, min, max…) passent aussi en rouge.
 * Messages : window.ERREURS_FORM_MESSAGES (base.html).
 */
(function () {
    "use strict";

    var M = window.ERREURS_FORM_MESSAGES || {
        titre: "Veuillez corriger les champs suivants :",
        champ: "Champ"
    };
    var SELECTEUR = '[aria-invalid="true"], .input-error';

    function champsEnErreur(racine) {
        return Array.prototype.filter.call(
            (racine || document).querySelectorAll(SELECTEUR),
            function (el) {
                return /^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName) && el.type !== "hidden";
            }
        );
    }

    function estVisible(el) {
        return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
            && window.getComputedStyle(el).visibility !== "hidden";
    }

    /* Ouvre les <details> fermés et les onglets qui cachent le champ */
    function rendreVisible(el) {
        var n = el.parentElement;
        while (n && n !== document.body) {
            if (n.tagName === "DETAILS" && !n.open) { n.open = true; }
            if (n.id && !estVisible(n)) {
                var id = n.id;
                var bouton = document.querySelector(
                    '[aria-controls="' + id + '"], [data-target="#' + id + '"], [data-tab="' + id + '"], ' +
                    '[data-bs-target="#' + id + '"], a[href="#' + id + '"]'
                );
                if (bouton) { bouton.click(); }
            }
            n = n.parentElement;
        }
    }

    /* Élément à montrer : le champ, ou un élément visible qui le remplace (select personnalisé…) */
    function cible(el) {
        if (estVisible(el)) { return el; }
        var parent = el.parentElement;
        while (parent && parent !== document.body) {
            if (estVisible(parent)) {
                var remplacant = parent.querySelector("button, input:not([type=hidden]), select, textarea");
                return remplacant && estVisible(remplacant) ? remplacant : parent;
            }
            parent = parent.parentElement;
        }
        return el;
    }

    function allerAuChamp(el) {
        rendreVisible(el);
        var c = cible(el);
        c.scrollIntoView({behavior: "smooth", block: "center"});
        setTimeout(function () {
            try { c.focus({preventScroll: true}); } catch (e) { c.focus(); }
            c.classList.remove("champ-erreur-flash");
            void c.offsetWidth;
            c.classList.add("champ-erreur-flash");
        }, 350);
    }

    function libelle(el) {
        var lab = el.id ? document.querySelector('label[for="' + el.id + '"]') : null;
        if (!lab) { lab = el.closest("label"); }
        if (!lab) {
            var bloc = el.parentElement;
            for (var i = 0; i < 3 && bloc && !lab; i++) {
                lab = bloc.querySelector("label");
                bloc = bloc.parentElement;
            }
        }
        var texte = lab ? lab.textContent : (el.getAttribute("placeholder") || el.name || M.champ);
        texte = texte.replace(/\s+/g, " ").replace(/[*:]\s*$/, "").trim();
        return texte.length > 80 ? texte.slice(0, 77) + "…" : texte;
    }

    function corrige(el) {
        el.removeAttribute("aria-invalid");
        el.classList.remove("input-error", "champ-erreur-flash");
        var lien = document.querySelector('[data-erreur-pour="' + (el.id || el.name) + '"]');
        if (lien && lien.parentElement) { lien.parentElement.classList.add("corrige"); }
    }

    function resume(form, champs) {
        if (form.querySelector(".erreurs-resume")) { return; }
        var vus = {};
        var boite = document.createElement("div");
        boite.className = "erreurs-resume";
        boite.setAttribute("role", "alert");
        var titre = document.createElement("strong");
        titre.textContent = M.titre;
        boite.appendChild(titre);
        var liste = document.createElement("ul");
        champs.forEach(function (el) {
            var cle = el.id || el.name;
            if (vus[cle]) { return; }
            vus[cle] = true;
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = "#" + (el.id || "");
            a.setAttribute("data-erreur-pour", cle);
            a.textContent = libelle(el);
            a.addEventListener("click", function (e) {
                e.preventDefault();
                allerAuChamp(el);
            });
            li.appendChild(a);
            liste.appendChild(li);
        });
        boite.appendChild(liste);
        form.insertBefore(boite, form.firstChild);
    }

    function initialiser() {
        var champs = champsEnErreur();
        if (!champs.length) { return; }

        // Le rouge disparaît dès que le champ est corrigé
        champs.forEach(function (el) {
            el.addEventListener("input", function () { corrige(el); }, {once: true});
            el.addEventListener("change", function () { corrige(el); }, {once: true});
        });

        // Liste des champs à corriger en haut de chaque formulaire concerné
        var parForm = new Map();
        champs.forEach(function (el) {
            var f = el.form || el.closest("form");
            if (!f) { return; }
            if (!parForm.has(f)) { parForm.set(f, []); }
            parForm.get(f).push(el);
        });
        parForm.forEach(function (liste, f) {
            if (liste.length > 1) { resume(f, liste); }
        });

        // Va au premier champ en erreur
        allerAuChamp(champs[0]);
    }

    // Champs refusés par le navigateur (required, min, max, pattern…) : rouge aussi
    document.addEventListener("invalid", function (e) {
        var el = e.target;
        if (!el || !el.classList) { return; }
        el.setAttribute("aria-invalid", "true");
        el.addEventListener("input", function () { corrige(el); }, {once: true});
        el.addEventListener("change", function () { corrige(el); }, {once: true});
        if (!estVisible(el)) {
            // Champ caché (onglet, <details>, select personnalisé) : le navigateur ne peut pas y aller seul
            rendreVisible(el);
        }
    }, true);

    // Après le loader de la page (base.html) pour que le défilement soit correct
    if (document.readyState === "complete") {
        setTimeout(initialiser, 400);
    } else {
        window.addEventListener("load", function () { setTimeout(initialiser, 400); });
    }

    window.allerAuChampEnErreur = allerAuChamp;
})();
