/*
 * Numéro de TVA dans les formulaires : affiché mis en forme (BE 0123.456.789, FR 12 345 678 901…)
 * quand on quitte le champ, puis renvoyé au serveur au format compact (BE0123456789) à l'enregistrement.
 * Champs concernés : name = numero_tva / client_tva, ou attribut data-tva.
 */
(function () {
    "use strict";
    var PAYS = ["AT","BE","BG","CY","CZ","DE","DK","EE","EL","ES","FI","FR","HR","HU","IE","IT","LT","LU",
                "LV","MT","NL","PL","PT","RO","SE","SI","SK","XI","CH","GB","NO"];

    function compact(v) { return (v || "").toUpperCase().replace(/[^A-Z0-9]/g, ""); }
    function grouper(c, tailles, sep) {
        var out = [], i = 0;
        tailles.forEach(function (t) { if (i < c.length) { out.push(c.slice(i, i + t)); i += t; } });
        if (i < c.length) out.push(c.slice(i));
        return out.join(sep || " ");
    }
    function belge(c) {
        if (c.length === 9) c = "0" + c;
        return (c.length === 10 && /^\d+$/.test(c)) ? c.slice(0, 4) + "." + c.slice(4, 7) + "." + c.slice(7) : c;
    }
    function formater(valeur) {
        var v = compact(valeur);
        if (!v) return "";
        var pays = v.slice(0, 2), r = v.slice(2);
        if (PAYS.indexOf(pays) === -1) return (/^\d{9,10}$/.test(v)) ? belge(v) : valeur.trim();
        if (pays === "BE") return "BE " + belge(r);
        if (pays === "FR" && r.length === 11) return "FR " + r.slice(0, 2) + " " + grouper(r.slice(2), [3, 3, 3]);
        if (pays === "NL" && r.length === 12 && r[9] === "B") return "NL " + r.slice(0, 9) + " " + r.slice(9);
        if (pays === "DE" && /^\d{9}$/.test(r)) return "DE " + grouper(r, [3, 3, 3]);
        if (pays === "GB" && /^(\d{9}|\d{12})$/.test(r)) return "GB " + grouper(r, [3, 4, 2, 3]);
        if (pays === "CH" && r[0] === "E" && r.length >= 10)
            return "CHE-" + grouper(r.slice(1, 10), [3, 3, 3], ".") + (r.slice(10) ? " " + r.slice(10) : "");
        return pays + " " + r;
    }

    function init() {
        var champs = document.querySelectorAll('input[name="numero_tva"], input[name="client_tva"], input[data-tva]');
        champs.forEach(function (c) {
            if (c.value) c.value = formater(c.value);
            c.addEventListener("blur", function () { c.value = formater(c.value); });
            if (c.form && !c.form.dataset.tvaCompact) {
                c.form.dataset.tvaCompact = "1";
                c.form.addEventListener("submit", function () {
                    c.form.querySelectorAll('input[name="numero_tva"], input[name="client_tva"], input[data-tva]')
                        .forEach(function (x) { x.value = compact(x.value); });
                });
            }
        });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
    window.formaterTVA = formater;
})();
