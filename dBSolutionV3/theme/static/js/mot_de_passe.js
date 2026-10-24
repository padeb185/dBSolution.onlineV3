/*
 * Mots de passe : contrôle en direct des règles (12 caractères, majuscule, minuscule, chiffre,
 * caractère spécial) sous le champ data-mdp="nouveau", et comparaison avec le champ data-mdp="confirmation".
 * Bouton « afficher / masquer » sur chaque champ. Messages traduits : window.MDP_MESSAGES (base.html).
 */
(function () {
    "use strict";
    var M = window.MDP_MESSAGES || {
        longueur: "Au moins 12 caractères", majuscule: "Une majuscule", minuscule: "Une minuscule",
        chiffre: "Un chiffre", special: "Un caractère spécial (! ? @ # $ % & * …)",
        identiques: "Les mots de passe sont identiques", differents: "Les mots de passe ne sont pas identiques",
        afficher: "Afficher", masquer: "Masquer"
    };
    var REGLES = [
        ["longueur", function (v) { return v.length >= 12; }],
        ["majuscule", function (v) { return /[A-Z]/.test(v); }],
        ["minuscule", function (v) { return /[a-z]/.test(v); }],
        ["chiffre", function (v) { return /\d/.test(v); }],
        ["special", function (v) { return /[^A-Za-z0-9\s]|_/.test(v); }]
    ];

    function boutonAfficher(champ) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "mt-1 text-xs text-blue-700 hover:underline";
        b.textContent = M.afficher;
        b.addEventListener("click", function () {
            var cache = champ.type === "password";
            champ.type = cache ? "text" : "password";
            b.textContent = cache ? M.masquer : M.afficher;
        });
        champ.insertAdjacentElement("afterend", b);
        return b;
    }

    function init() {
        document.querySelectorAll('input[data-mdp="nouveau"]').forEach(function (champ) {
            var apres = boutonAfficher(champ);
            var liste = document.createElement("ul");
            liste.className = "mt-2 text-sm space-y-0.5";
            REGLES.forEach(function (r) {
                var li = document.createElement("li");
                li.dataset.regle = r[0];
                li.textContent = "○ " + M[r[0]];
                liste.appendChild(li);
            });
            apres.insertAdjacentElement("afterend", liste);

            var form = champ.form;
            var confirmation = form ? form.querySelector('input[data-mdp="confirmation"]') : null;
            var etat = null;
            if (confirmation) {
                var b2 = boutonAfficher(confirmation);
                etat = document.createElement("p");
                etat.className = "mt-1 text-sm";
                b2.insertAdjacentElement("afterend", etat);
            }

            function maj() {
                var v = champ.value || "";
                REGLES.forEach(function (r) {
                    var li = liste.querySelector('[data-regle="' + r[0] + '"]');
                    var ok = r[1](v);
                    li.textContent = (ok ? "✔ " : "○ ") + M[r[0]];
                    li.className = ok ? "text-green-700" : (v ? "text-red-700" : "text-gray-500");
                });
                if (confirmation && etat) {
                    var c = confirmation.value || "";
                    if (!c) { etat.textContent = ""; confirmation.setCustomValidity(""); return; }
                    var identiques = c === v;
                    etat.textContent = (identiques ? "✔ " : "✖ ") + (identiques ? M.identiques : M.differents);
                    etat.className = "mt-1 text-sm " + (identiques ? "text-green-700" : "text-red-700");
                    confirmation.setCustomValidity(identiques ? "" : M.differents);
                }
            }
            champ.addEventListener("input", maj);
            if (confirmation) confirmation.addEventListener("input", maj);
            maj();
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
