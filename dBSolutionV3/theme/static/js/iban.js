/*
 * IBAN : mise en forme en direct (groupes de 4, majuscules) et contrôle (longueur du pays + clé mod 97).
 * S'applique à tous les champs IBAN des formulaires : fournisseur, client, société cliente,
 * propriétaire, société… (name = numero_compte / iban / numero_iban / numero_compte_bancaire, ou data-iban).
 * Messages traduits : window.IBAN_MESSAGES (défini dans base.html).
 */
(function () {
    var LONGUEURS = {
        AD: 24, AT: 20, BE: 16, BG: 22, CH: 21, CY: 28, CZ: 24, DE: 22, DK: 18, EE: 20, ES: 24, FI: 18,
        FR: 27, GB: 22, GI: 23, GR: 27, HR: 21, HU: 28, IE: 22, IS: 26, IT: 27, LI: 21, LT: 20, LU: 20,
        LV: 21, MC: 27, MT: 31, NL: 18, NO: 15, PL: 28, PT: 25, RO: 24, SE: 24, SI: 19, SK: 24, SM: 27,
        VA: 22, MA: 28, TN: 24, TR: 26
    };
    var M = window.IBAN_MESSAGES || {
        valide: "IBAN valide", pays: "Code pays + 2 chiffres de contrôle attendus",
        longueur: "Longueur attendue : {n} caractères", cle: "Clé de contrôle incorrecte"
    };

    function compact(v) { return (v || "").toUpperCase().replace(/[^A-Z0-9]/g, ""); }
    function formater(v) { return compact(v).replace(/(.{4})/g, "$1 ").trim(); }

    function mod97(v) {
        var s = v.slice(4) + v.slice(0, 4), reste = 0;
        for (var i = 0; i < s.length; i++) {
            var c = s.charCodeAt(i);
            if (c >= 48 && c <= 57) reste = (reste * 10 + (c - 48)) % 97;
            else reste = (reste * 100 + (c - 55)) % 97;
        }
        return reste === 1;
    }

    function erreur(v) {
        if (!v) return null;
        if (!/^[A-Z]{2}[0-9]{2}[A-Z0-9]+$/.test(v)) return M.pays;
        var attendu = LONGUEURS[v.slice(0, 2)];
        if (attendu && v.length !== attendu) return M.longueur.replace("{n}", attendu);
        if (v.length < 15 || v.length > 34) return M.longueur.replace("{n}", "15-34");
        if (!mod97(v)) return M.cle;
        return "";
    }

    function brancher(input) {
        if (input.dataset.ibanActif) return;
        input.dataset.ibanActif = "1";
        input.setAttribute("autocomplete", "off");
        input.setAttribute("spellcheck", "false");

        var aide = document.createElement("p");
        aide.className = "text-xs mt-1";
        input.insertAdjacentElement("afterend", aide);

        function maj(final) {
            var pos = input.selectionStart, avant = input.value.length;
            input.value = formater(input.value);
            if (!final && pos !== null) {
                var ecart = input.value.length - avant;
                try { input.setSelectionRange(pos + ecart, pos + ecart); } catch (e) {}
            }
            var v = compact(input.value), err = erreur(v);
            input.classList.remove("border-red-500", "border-green-600");
            if (err === null) { aide.textContent = ""; return; }
            // pendant la saisie, on n'affiche l'erreur de longueur qu'une fois la longueur atteinte
            var attendu = LONGUEURS[v.slice(0, 2)];
            if (!final && err && attendu && v.length < attendu) { aide.textContent = ""; return; }
            if (err) {
                input.classList.add("border-red-500");
                aide.className = "text-xs mt-1 text-red-600";
                aide.textContent = "✗ " + err;
            } else {
                input.classList.add("border-green-600");
                aide.className = "text-xs mt-1 text-green-700";
                aide.textContent = "✓ " + M.valide;
            }
        }
        input.addEventListener("input", function () { maj(false); });
        input.addEventListener("blur", function () { maj(true); });
        if (input.value) maj(true);
    }

    function initialiser(racine) {
        (racine || document).querySelectorAll(
            'form input[name="numero_compte"], form input[name="iban"], form input[name="numero_iban"],' +
            ' form input[name="numero_compte_bancaire"], input[data-iban]'
        ).forEach(brancher);
    }
    window.initIban = initialiser;
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { initialiser(); });
    else initialiser();
})();
