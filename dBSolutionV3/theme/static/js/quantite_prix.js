/*
 * Formulaires d'intervention (création, check, modification) :
 * la quantité et le prix d'une même pièce (<p>_quantite, <p>_prix) sont affichés
 * sur une seule ligne, comme le temps de main-d'œuvre (heures / minutes).
 * Les tableaux (formsets) et les blocs déjà en ligne ne sont pas modifiés.
 */
(function () {
    "use strict";

    function blocDe(champ, ancetre) {
        // enfant direct de « ancetre » qui contient le champ
        var b = champ;
        while (b.parentElement && b.parentElement !== ancetre) b = b.parentElement;
        return b.parentElement === ancetre ? b : null;
    }

    function ancetreCommun(a, b) {
        var p = a.parentElement;
        while (p && !p.contains(b)) p = p.parentElement;
        return p;
    }

    function nbControles(bloc) {
        return bloc.querySelectorAll("input:not([type=hidden]), select, textarea").length;
    }

    function dejaEnLigne(el) {
        var d = window.getComputedStyle(el);
        return d.display === "grid" || d.display === "inline-grid"
            || ((d.display === "flex" || d.display === "inline-flex") && d.flexDirection.indexOf("row") === 0);
    }

    function regrouper(form) {
        form.querySelectorAll('[name$="_quantite"]').forEach(function (qte) {
            var prefixe = qte.name.slice(0, -"_quantite".length);
            var prix = form.querySelector('[name="' + prefixe + '_prix"]');
            if (!prix || qte.closest(".ligne-qte-prix")) return;

            var parent = ancetreCommun(qte, prix);
            if (!parent || /^(TR|TBODY|TABLE|THEAD)$/.test(parent.tagName) || dejaEnLigne(parent)) return;

            var bq = blocDe(qte, parent), bp = blocDe(prix, parent);
            if (!bq || !bp || bq === bp || /^(TD|TH|TR)$/.test(bq.tagName)) return;
            if (nbControles(bq) !== 1 || nbControles(bp) !== 1) return;

            var ligne = document.createElement("div");
            ligne.className = "ligne-qte-prix grid grid-cols-2 gap-4";
            var premier = (bq.compareDocumentPosition(bp) & Node.DOCUMENT_POSITION_FOLLOWING) ? bq : bp;
            parent.insertBefore(ligne, premier);
            ligne.appendChild(bq);   // quantité à gauche
            ligne.appendChild(bp);   // prix à droite
        });
    }

    function init() {
        document.querySelectorAll("form").forEach(regrouper);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () { setTimeout(init, 0); });
    } else {
        setTimeout(init, 0);
    }
})();
