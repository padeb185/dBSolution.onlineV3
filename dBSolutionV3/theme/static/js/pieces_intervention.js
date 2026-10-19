/*
 * Formulaires d'intervention : pour chaque ligne de pièce (<p>_fabricant, <p>_quantite, <p>_prix),
 * ajoute un champ « OEM / EAN » entre le fabricant et la quantité.
 * Ordre : intitulé → fabricant → OEM / EAN → quantité → prix.
 * Le code est cherché au catalogue : fabricant et prix de vente sont repris de la fiche pièce.
 * À l'enregistrement, chaque ligne codée devient une pièce utilisée de la maintenance (stock).
 */
(function () {
    var cfg = window.PIECES_INTERVENTION;
    if (!cfg || !cfg.api) return;
    var M = cfg.messages;

    function norm(s) { return (s || '').toString().trim().toLowerCase(); }

    function choisirFabricant(sel, nom) {
        if (!nom) return true;
        if (sel.tagName !== 'SELECT') { sel.value = nom; return true; }
        var cible = norm(nom);
        for (var i = 0; i < sel.options.length; i++) {
            var o = sel.options[i];
            if (norm(o.value) === cible || norm(o.text) === cible) { sel.value = o.value; return true; }
        }
        for (var j = 0; j < sel.options.length; j++) {   // correspondance partielle (« Bosch » / « Robert Bosch »)
            var t = norm(sel.options[j].text);
            if (t.length > 2 && (t.indexOf(cible) !== -1 || cible.indexOf(t) !== -1)) { sel.value = sel.options[j].value; return true; }
        }
        return false;
    }

    function ligne(form, fab) {
        var prefixe = fab.name.slice(0, -'_fabricant'.length);
        var qte = form.querySelector('[name="' + prefixe + '_quantite"]');
        var prix = form.querySelector('[name="' + prefixe + '_prix"]');
        if (!qte || !prix || form.querySelector('[name="' + prefixe + '_code_piece"]')) return null;

        // bloc du fabricant = plus grand ancêtre qui ne contient pas la quantité
        var bloc = fab;
        while (bloc.parentElement && !bloc.parentElement.contains(qte) && bloc.parentElement !== form) bloc = bloc.parentElement;

        var div = document.createElement(bloc.tagName === 'TD' ? 'td' : 'div');
        div.className = bloc.className || 'mb-4';
        div.innerHTML =
            '<label class="block font-semibold mb-1">' + M.label + '</label>' +
            '<div class="flex gap-2"><input type="text" name="' + prefixe + '_code_piece" autocomplete="off" ' +
            'class="input border rounded px-3 py-2 w-full font-mono uppercase" placeholder="' + M.placeholder + '">' +
            '<button type="button" class="bg-gray-200 hover:bg-gray-300 px-3 rounded font-semibold">' + M.chercher + '</button></div>' +
            '<p class="text-sm mt-1"></p>';
        bloc.parentNode.insertBefore(div, bloc.nextSibling);

        var input = div.querySelector('input'), etat = div.querySelector('p');
        function message(txt, couleur) { etat.className = 'text-sm mt-1 ' + couleur; etat.textContent = txt; }

        function chercher() {
            var v = input.value.trim();
            if (!v) { etat.textContent = ''; return; }
            fetch(cfg.api + '?code=' + encodeURIComponent(v), {credentials: 'same-origin'})
                .then(function (r) { return r.json(); })
                .then(function (d) {
                    if (!d.found) { message(M.inconnue, 'text-orange-600'); return; }
                    var p = d.piece, txt = M.trouvee + ' ' + p.designation + ' · ' + M.stock + ' ' + p.stock;
                    if (!choisirFabricant(fab, p.fabricant)) txt += ' · ' + M.fabricantAbsent.replace('%s', p.fabricant);
                    prix.value = p.prix_vente_effectif;
                    if (!parseFloat(qte.value)) qte.value = 1;
                    // pièce posée : l'état « OK » passe à « Fait » (sinon absente du rapport, du PDF et de la facture)
                    var etatSel = form.querySelector('select[name="' + prefixe + '"], select[name="' + prefixe + '_etat"]');
                    if (etatSel && etatSel.value === 'OK' && etatSel.querySelector('option[value="REMPLACE"]')) {
                        etatSel.value = 'REMPLACE';
                        etatSel.dispatchEvent(new Event('change', {bubbles: true}));
                    }
                    [fab, prix, qte].forEach(function (el) { el.dispatchEvent(new Event('change', {bubbles: true})); });
                    message(txt, 'text-green-700');
                    qte.focus(); if (qte.select) qte.select();
                });
        }
        input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); chercher(); } });
        input.addEventListener('change', chercher);
        div.querySelector('button').addEventListener('click', chercher);
        return {prefixe: prefixe, input: input, message: message};
    }

    document.querySelectorAll('form').forEach(function (form) {
        var lignes = {};
        form.querySelectorAll('[name$="_fabricant"]').forEach(function (fab) {
            var l = ligne(form, fab);
            if (l) lignes[l.prefixe] = l;
        });
        if (!Object.keys(lignes).length) return;

        // Formulaire renvoyé avec des erreurs : les codes saisis sont restaurés (mémoire de l'onglet)
        var cle = 'pieces_codes:' + window.location.pathname;
        try {
            var memo = JSON.parse(sessionStorage.getItem(cle) || 'null');
            sessionStorage.removeItem(cle);
            // uniquement si la page est le formulaire renvoyé avec des erreurs (pas un nouveau formulaire)
            var erreurs = document.querySelector('.errorlist, form .text-red-600');
            if (memo && erreurs && Date.now() - memo.t < 15 * 60 * 1000) {
                Object.keys(memo.codes).forEach(function (p) {
                    if (lignes[p] && memo.codes[p] && !lignes[p].input.value) lignes[p].input.value = memo.codes[p];
                });
            }
        } catch (e) {}
        form.addEventListener('submit', function () {
            var codes = {};
            Object.keys(lignes).forEach(function (p) { if (lignes[p].input.value) codes[p] = lignes[p].input.value; });
            try { sessionStorage.setItem(cle, JSON.stringify({t: Date.now(), codes: codes})); } catch (e) {}
        });

        // Modification : reprise des codes déjà enregistrés (maintenance retrouvée via l'URL de la page)
        if (!cfg.apiCodes) return;
        fetch(cfg.apiCodes + '?chemin=' + encodeURIComponent(window.location.pathname), {credentials: 'same-origin'})
            .then(function (r) { return r.ok ? r.json() : {lignes: {}}; })
            .then(function (d) {
                Object.keys(d.lignes || {}).forEach(function (prefixe) {
                    var l = lignes[prefixe], info = d.lignes[prefixe];
                    if (!l) return;
                    if (!l.input.value) l.input.value = info.code;
                    if (info.debitee) {
                        l.input.readOnly = true;
                        l.input.classList.add('bg-gray-100');
                        l.message(info.designation + ' · ' + M.debitee, 'text-green-700');
                    } else {
                        l.message(info.designation + ' · ' + M.stock + ' ' + info.stock, 'text-gray-600');
                    }
                });
            });
    });
})();
