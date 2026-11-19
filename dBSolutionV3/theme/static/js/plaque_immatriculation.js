/*
 * Plaque d'immatriculation mise en forme dans les formulaires carburant / recharge.
 * Une fois le véhicule choisi, le champ texte est remplacé par la plaque (pays, couleurs) ;
 * elle reste affichée (rechargement de la page, erreurs de formulaire, modification).
 * « Changer » rend le champ pour choisir un autre véhicule.
 *
 * <script src="plaque_immatriculation.js" data-url="URL autocomplete" data-changer="Changer"></script>
 * L'autocomplete renvoie [{immatriculation, plaque_html, plaque_html_selection, …}].
 */
(function () {
    "use strict";
    const script = document.currentScript;
    const url = script && script.dataset.url;
    const libelleChanger = (script && script.dataset.changer) || "Changer";

    function init() {
        const input = document.getElementById("id_immatriculation");
        if (!input) return;
        const exemplaire = document.getElementById("id_voiture_exemplaire");

        const bloc = document.createElement("div");
        bloc.className = "plaque-choisie";
        bloc.style.cssText = "display:none;align-items:center;gap:12px;flex-wrap:wrap;margin-top:4px;";
        bloc.innerHTML = '<span class="plaque-rendu" style="display:inline-flex;"></span>' +
            '<button type="button" class="plaque-changer" style="background:#e5e7eb;padding:6px 12px;' +
            'border-radius:6px;font-weight:600;font-size:14px;"></button>';
        bloc.querySelector(".plaque-changer").textContent = libelleChanger;
        input.insertAdjacentElement("afterend", bloc);

        let plaqueAffichee = "";

        function afficher(html, immat) {
            if (!html) return;
            bloc.querySelector(".plaque-rendu").innerHTML = html;
            bloc.style.display = "flex";
            input.style.display = "none";
            plaqueAffichee = (immat || input.value || "").toUpperCase();
        }

        function masquer() {
            bloc.style.display = "none";
            input.style.display = "";
            plaqueAffichee = "";
        }

        /* Cherche la plaque exacte saisie dans le champ et l'affiche mise en forme */
        function chercher() {
            const valeur = input.value.trim();
            if (!valeur || !url || valeur.toUpperCase() === plaqueAffichee) return;
            fetch(url + (url.includes("?") ? "&" : "?") + "term=" + encodeURIComponent(valeur))
                .then(function (r) { return r.ok ? r.json() : []; })
                .then(function (liste) {
                    const v = (liste || []).find(function (x) {
                        return (x.immatriculation || "").toUpperCase() === valeur.toUpperCase();
                    });
                    if (v) afficher(v.plaque_html_selection || v.plaque_html, v.immatriculation);
                })
                .catch(function () {});
        }

        bloc.querySelector(".plaque-changer").addEventListener("click", function () {
            masquer();
            input.value = "";
            if (exemplaire) exemplaire.value = "";
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.focus();
        });

        // Véhicule choisi dans la liste de suggestions (appelé par le formulaire)
        window.afficherPlaqueChoisie = function (voiture) {
            if (!voiture) return;
            afficher(voiture.plaque_html_selection || voiture.plaque_html, voiture.immatriculation);
        };

        // Saisie complète au clavier puis sortie du champ
        input.addEventListener("change", chercher);

        // Page affichée avec un véhicule déjà choisi (modification, erreurs, véhicule de l'URL)
        chercher();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
