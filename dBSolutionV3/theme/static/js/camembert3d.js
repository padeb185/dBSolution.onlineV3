/*
 * Camembert 3D en SVG, sans dépendance.
 *   Camembert3D.dessiner(element, parts, {devise: "€", locale: "fr-BE"})
 *   parts = [{label: "Pièces", valeur: 1234.5}, ...]
 * Ellipse inclinée + paroi avant extrudée ; info-bulle au survol ; légende avec montants et pourcentages.
 */
(function () {
    "use strict";
    var COULEURS = ["#2563eb", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899", "#84cc16", "#64748b"];
    var NS = "http://www.w3.org/2000/svg";
    var TAU = Math.PI * 2;

    function assombrir(hex, f) {
        var n = parseInt(hex.slice(1), 16);
        var r = Math.round(((n >> 16) & 255) * f), g = Math.round(((n >> 8) & 255) * f), b = Math.round((n & 255) * f);
        return "rgb(" + r + "," + g + "," + b + ")";
    }
    function el(nom, attrs) {
        var e = document.createElementNS(NS, nom);
        for (var k in attrs) e.setAttribute(k, attrs[k]);
        return e;
    }

    function dessiner(conteneur, parts, options) {
        options = options || {};
        var locale = options.locale || document.documentElement.lang || "fr-BE";
        var devise = options.devise || "€";
        var fmt = function (v) {
            return v.toLocaleString(locale, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + " " + devise;
        };
        conteneur.innerHTML = "";
        parts = (parts || []).filter(function (p) { return p.valeur > 0; });
        var total = parts.reduce(function (s, p) { return s + p.valeur; }, 0);
        if (!total) {
            conteneur.innerHTML = '<p class="text-gray-500 text-sm py-8 text-center">' + (options.vide || "—") + "</p>";
            return;
        }

        var L = 360, H = 250, cx = L / 2, cy = 105, rx = 160, ry = 82, prof = 34;
        var svg = el("svg", {viewBox: "0 0 " + L + " " + H, width: "100%", role: "img",
                             "aria-label": options.titre || ""});
        svg.style.maxWidth = "420px";
        svg.style.overflow = "visible";
        var pt = function (a, dy) { return [cx + rx * Math.cos(a), cy + ry * Math.sin(a) + (dy || 0)]; };

        // ombre portée
        svg.appendChild(el("ellipse", {cx: cx, cy: cy + prof + 10, rx: rx * 0.95, ry: ry * 0.55,
                                       fill: "rgba(0,0,0,0.12)"}));

        // angles (départ en haut, sens horaire à l'écran)
        var a = -Math.PI / 2, tranches = [];
        parts.forEach(function (p, i) {
            var balayage = p.valeur / total * TAU;
            tranches.push({p: p, i: i, a0: a, a1: a + balayage, couleur: COULEURS[i % COULEURS.length],
                           pct: p.valeur / total * 100});
            a += balayage;
        });

        var gParois = el("g", {}), gDessus = el("g", {}), gTextes = el("g", {"pointer-events": "none"});
        var bulle = document.createElement("div");
        bulle.className = "camembert3d-bulle";
        bulle.style.cssText = "position:absolute;pointer-events:none;background:#111827;color:#fff;font-size:12px;" +
            "padding:6px 9px;border-radius:6px;white-space:nowrap;display:none;z-index:20;box-shadow:0 2px 6px rgba(0,0,0,.25)";

        function survol(t, elements) {
            elements.forEach(function (e) {
                e.addEventListener("mousemove", function (ev) {
                    var r = conteneur.getBoundingClientRect();
                    bulle.innerHTML = "<b>" + t.p.label + "</b><br>" + fmt(t.p.valeur) + " · " +
                        t.pct.toLocaleString(locale, {maximumFractionDigits: 1}) + " %";
                    bulle.style.left = (ev.clientX - r.left + 12) + "px";
                    bulle.style.top = (ev.clientY - r.top + 12) + "px";
                    bulle.style.display = "block";
                    elements.forEach(function (x) { x.style.filter = "brightness(1.12)"; });
                });
                e.addEventListener("mouseleave", function () {
                    bulle.style.display = "none";
                    elements.forEach(function (x) { x.style.filter = ""; });
                });
            });
        }

        tranches.forEach(function (t) {
            var elems = [];
            // paroi avant : partie de l'arc dont l'angle est dans [0, π] (moitié basse de l'ellipse)
            for (var k = -1; k <= 1; k++) {
                var s = Math.max(t.a0, k * TAU), e = Math.min(t.a1, k * TAU + Math.PI);
                if (e - s > 1e-6) {
                    var p0 = pt(s), p1 = pt(e), p1b = pt(e, prof), p0b = pt(s, prof);
                    var paroi = el("path", {
                        d: "M" + p0 + " A" + rx + "," + ry + " 0 0 1 " + p1 + " L" + p1b +
                           " A" + rx + "," + ry + " 0 0 0 " + p0b + " Z",
                        fill: assombrir(t.couleur, 0.72), stroke: assombrir(t.couleur, 0.6), "stroke-width": 0.5});
                    gParois.appendChild(paroi);
                    elems.push(paroi);
                }
            }
            // dessus
            var dessus;
            if (t.a1 - t.a0 >= TAU - 1e-6) {
                dessus = el("ellipse", {cx: cx, cy: cy, rx: rx, ry: ry, fill: t.couleur});
            } else {
                var grand = (t.a1 - t.a0) > Math.PI ? 1 : 0;
                dessus = el("path", {d: "M" + cx + "," + cy + " L" + pt(t.a0) + " A" + rx + "," + ry + " 0 " + grand +
                                       " 1 " + pt(t.a1) + " Z",
                                    fill: t.couleur, stroke: "#fff", "stroke-width": 1.2, "stroke-linejoin": "round"});
            }
            dessus.style.cursor = "pointer";
            gDessus.appendChild(dessus);
            elems.push(dessus);
            survol(t, elems);

            // pourcentage sur la tranche
            if (t.pct >= 5) {
                var m = (t.a0 + t.a1) / 2, q = [cx + rx * 0.62 * Math.cos(m), cy + ry * 0.62 * Math.sin(m)];
                var txt = el("text", {x: q[0], y: q[1] + 4, "text-anchor": "middle", "font-size": 13,
                                      "font-weight": "700", fill: "#fff"});
                txt.style.textShadow = "0 1px 2px rgba(0,0,0,.45)";
                txt.textContent = Math.round(t.pct) + " %";
                gTextes.appendChild(txt);
            }
        });
        // reflet léger sur le dessus
        var defs = el("defs", {});
        var grad = el("radialGradient", {id: "cam3d-reflet-" + Math.random().toString(36).slice(2), cx: "35%", cy: "25%", r: "75%"});
        grad.appendChild(el("stop", {offset: "0%", "stop-color": "#fff", "stop-opacity": 0.28}));
        grad.appendChild(el("stop", {offset: "100%", "stop-color": "#fff", "stop-opacity": 0}));
        defs.appendChild(grad);
        svg.appendChild(defs);
        svg.appendChild(gParois);
        svg.appendChild(gDessus);
        svg.appendChild(el("ellipse", {cx: cx, cy: cy, rx: rx, ry: ry, fill: "url(#" + grad.id + ")",
                                       "pointer-events": "none"}));
        svg.appendChild(gTextes);

        // légende
        var legende = document.createElement("ul");
        legende.className = "mt-3 space-y-1 text-sm";
        tranches.forEach(function (t) {
            var li = document.createElement("li");
            li.className = "flex items-center gap-2";
            li.innerHTML = '<span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:' +
                t.couleur + '"></span><span class="flex-1">' + t.p.label + '</span><span class="font-semibold tabular-nums">' +
                fmt(t.p.valeur) + '</span><span class="text-gray-500 w-14 text-right tabular-nums">' +
                t.pct.toLocaleString(locale, {maximumFractionDigits: 1}) + " %</span>";
            legende.appendChild(li);
        });

        conteneur.style.position = "relative";
        var boite = document.createElement("div");
        boite.className = "flex justify-center";
        boite.appendChild(svg);
        conteneur.appendChild(boite);
        conteneur.appendChild(legende);
        conteneur.appendChild(bulle);
    }

    window.Camembert3D = {dessiner: dessiner};
})();
