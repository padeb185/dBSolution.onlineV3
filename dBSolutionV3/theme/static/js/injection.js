/* Injection : nombre de cylindres → nombre d'injecteurs → champs de résistance affichés (1 à n). */
(function () {
    "use strict";
    var form = document.getElementById("injection-form");
    if (!form) return;
    var cyl = form.querySelector('[name="nombre_cylindres"]');
    var inj = form.querySelector('[name="nombre_injecteurs"]');
    if (!inj) return;

    function bloc(el) { return el.closest(".mb-4") || el.parentElement; }

    function afficherResistances() {
        var n = parseInt(inj.value, 10) || 0;
        for (var i = 1; i <= 16; i++) {
            var champ = form.querySelector('[name="injecteur_' + i + '_resistance_ohm"]');
            if (!champ) continue;
            var visible = i <= n;
            bloc(champ).style.display = visible ? "" : "none";
            if (!visible) champ.value = "";
        }
    }

    if (cyl) {
        cyl.addEventListener("change", function () {
            if (cyl.value) { inj.value = cyl.value; afficherResistances(); }
        });
    }
    inj.addEventListener("input", afficherResistances);
    inj.addEventListener("change", afficherResistances);
    afficherResistances();
})();
