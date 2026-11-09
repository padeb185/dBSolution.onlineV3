import 'package:flutter/material.dart';

import '../l10n/langue.dart';
import '../l10n/unites.dart';
import '../widgets/format.dart';
import 'pays.dart';

/// Type de champ d'un formulaire générique.
enum TypeChamp { texte, entier, decimal, date, booleen, choix, image, fichier }

/// Description d'un champ (nom côté API, libellé, type, options).
class Champ {
  const Champ(this.nom, this.libelle, this.type,
      {this.obligatoire = false, this.choix = const {}, this.aide, this.suffixe, this.parDefaut});

  final String nom;
  final String libelle;
  final TypeChamp type;
  final bool obligatoire;

  /// Pour TypeChamp.choix : {code API: libellé}
  final Map<String, String> choix;
  final String? aide;
  final String? suffixe;
  final dynamic parDefaut;

  bool get estFichier => type == TypeChamp.image || type == TypeChamp.fichier;
}

/// Ressource de l'API rattachée à un véhicule (pleins, entretiens…) : liste + formulaire génériques.
class Ressource {
  const Ressource({
    required this.chemin,
    required this.titre,
    required this.titreNouveau,
    required this.titreModifier,
    required this.texteVide,
    required this.texteSupprimer,
    required this.icone,
    required this.champs,
    required this.titreLigne,
    required this.sousTitreLigne,
    this.montantLigne,
    this.params = const {},
    this.iconeLigne,
    this.modifiable,
  });

  final String chemin; // ex. "pleins"
  final String titre; // ex. "Pleins"
  final String titreNouveau; // ex. "Nouveau plein"
  final String titreModifier; // ex. "Modifier le plein"
  final String texteVide; // ex. "Aucun plein pour l'instant."
  final String texteSupprimer; // ex. "Supprimer ce plein ?"
  final IconData icone;
  final List<Champ> champs;
  /// Lignes de la liste (unités du véhicule : km / mi, L / gal)
  final String Function(Map<String, dynamic>, Unites) titreLigne;
  final String Function(Map<String, dynamic>, Unites) sousTitreLigne;
  final String Function(Map<String, dynamic>)? montantLigne;
  /// Paramètres supplémentaires de la liste (ex. historique=1)
  final Map<String, String> params;
  /// Icône propre à une ligne (sinon l'icône de la ressource)
  final IconData Function(Map<String, dynamic>)? iconeLigne;
  /// Une ligne venant d'une autre ressource (plein, entretien…) ne se modifie pas ici
  final bool Function(Map<String, dynamic>)? modifiable;
}

Map<String, String> get typesEntretien => {
  'revision': t('Révision / entretien périodique'),
  'vidange': t('Vidange'),
  'pneus': t('Pneus'),
  'freins': t('Freins'),
  'distribution': t('Distribution'),
  'batterie': t('Batterie'),
  'climatisation': t('Climatisation'),
  'controle_technique': t('Contrôle technique'),
  'carrosserie': t('Carrosserie'),
  'reparation': t('Réparation'),
  'autre': t('Autre'),
};

Map<String, String> get typesDocument => {
  'assurance': t('Assurance'),
  'controle_technique': t('Contrôle technique'),
  'carte_grise': t('Certificat d\'immatriculation (carte grise)'),
  'coc': t('Certificat de conformité (COC)'),
  'facture_achat': t('Facture d\'achat'),
  'autre': t('Autre'),
};

Map<String, String> get categoriesDepense => {
  'taxe': t('Taxe de circulation / vignette'),
  'assurance': t('Assurance'),
  'parking': t('Parking / péage'),
  'lavage': t('Lavage'),
  'accessoire': t('Accessoires / équipements'),
  'amende': t('Amende'),
  'financement': t('Crédit / leasing'),
  'autre': t('Autre'),
};

/// Carburants d'un plein (code API → libellé)
Map<String, String> get carburants => {
  'sp95': t('Essence SP95 (E5)'),
  'sp95_e10': t('Essence SP95-E10'),
  'sp98': t('Essence SP98 (Super Plus)'),
  'sp102': t('Essence 102 (Ultimate 102)'),
  'diesel': t('Diesel (B7)'),
  'diesel_premium': t('Diesel premium (Diesel+)'),
  'hvo': t('HVO (diesel renouvelable, XTL)'),
  'e85': t('Éthanol E85 (superéthanol)'),
  'gpl': t('GPL (LPG)'),
  'gnc': t('GNC (CNG)'),
  'electricite': t('Électricité'),
};


/// Carburant proposé pour un nouveau plein, d'après l'énergie du véhicule.
String carburantParDefaut(String? energie) => switch (energie) {
      'diesel' => 'diesel',
      'gpl' => 'gpl',
      'gnc' => 'gnc',
      // Véhicule électrique : ses recharges sont à part (ressource « recharges »)
      _ => 'sp95',
    };

/// Carburants proposés pour un plein (la recharge électrique est à part)
Map<String, String> get carburantsPlein =>
    {for (final e in carburants.entries) if (e.key != 'electricite') e.key: e.value};

/// Carburant restant dans le réservoir au moment du plein
Map<String, String> get niveauxCarburant => {
  '3/4': '¾',
  '1/2': '½',
  '1/4': '¼',
  'reserve': t('Réserve'),
  'fin_reserve': t('Fin de réserve'),
};

/// Batterie restante au moment de la recharge
Map<String, String> get niveauxBatterie => {
  '3/4': '¾',
  '1/2': '½',
  '1/4': '¼',
  'minimum': t('Au minimum'),
};

Map<String, String> get lieuxRecharge => {
  'domicile': t('Domicile'),
  'travail': t('Travail'),
  'borne': t('Borne publique (AC)'),
  'rapide': t('Borne rapide (DC)'),
};

Map<String, String> get energies => {
  'essence': t('Essence'),
  'diesel': t('Diesel'),
  'hybride': t('Hybride'),
  'phev': t('Hybride rechargeable'),
  'electrique': t('Électrique'),
  'gpl': t('GPL'),
  'gnc': t('GNC'),
};

Ressource get pleins => Ressource(
  chemin: 'pleins',
  titre: t('Pleins'),
  titreNouveau: t('Nouveau plein'),
  titreModifier: t('Modifier le plein'),
  texteVide: t('Aucun plein pour l\'instant.'),
  texteSupprimer: t('Supprimer ce plein ?'),
  icone: Icons.local_gas_station,
  champs: [
    Champ('date', t('Date'), TypeChamp.date, obligatoire: true),
    Champ('carburant', t('Carburant'), TypeChamp.choix, obligatoire: true, choix: carburantsPlein),
    // Pays de la station : taux de TVA proposé (voir FormulaireEcran)
    Champ('pays', t('Pays de la station'), TypeChamp.choix, obligatoire: true, choix: paysImmatriculation),
    Champ('kilometrage', t('Kilométrage'), TypeChamp.entier, obligatoire: true, suffixe: 'km'),
    // Unité affichée selon le carburant choisi (L, kWh, kg) : voir FormulaireEcran
    Champ('quantite', t('Quantité'), TypeChamp.decimal, obligatoire: true, suffixe: 'L'),
    Champ('montant', t('Montant payé TVAC'), TypeChamp.decimal, obligatoire: true, suffixe: '€'),
    Champ('taux_tva', t('Taux de TVA'), TypeChamp.decimal, suffixe: '%',
        aide: t('Taux du pays de la station, modifiable.')),
    Champ('niveau_restant', t('Carburant restant'), TypeChamp.choix, choix: niveauxCarburant,
        aide: t('Niveau dans le réservoir avant le plein.')),
    Champ('plein_complet', t('Plein complet'), TypeChamp.booleen,
        parDefaut: true, aide: t('Nécessaire pour calculer la consommation.')),
    Champ('station', t('Station'), TypeChamp.texte),
    Champ('ticket', t('Photo du ticket'), TypeChamp.image),
    Champ('remarques', t('Remarques'), TypeChamp.texte),
  ],
  titreLigne: (p, u) => '${nombre(u.depuisQuantite(enDouble(p['quantite']) ?? 0, p['carburant'] as String?))} '
      '${u.symboleQuantite(p['carburant'] as String?)} – ${euros(p['montant'])}',
  sousTitreLigne: (p, u) => [
    if (p['carburant'] != null) carburants[p['carburant']] ?? p['carburant'],
    if ((p['niveau_restant'] ?? '').toString().isNotEmpty)
      t('restant : {niveau}', {'niveau': niveauxCarburant[p['niveau_restant']] ?? p['niveau_restant']}),
    dateFr(p['date']),
    km(p['kilometrage'], u),
    if ((p['pays'] ?? '').toString().isNotEmpty) p['pays'],
    if (p['montant_tva'] != null) t('TVA {taux} % : {montant}', {'taux': nombre(p['taux_tva'], decimales: 1), 'montant': euros(p['montant_tva'])}),
    if (p['prix_unitaire'] != null)
      '${nombre(u.prixParQuantite(enDouble(p['prix_unitaire']) ?? 0, p['carburant'] as String?), decimales: 3)} '
          '€/${u.symboleQuantite(p['carburant'] as String?)}',
  ].join(' · '),
);

/// Recharges électriques (à part des pleins) : kWh, lieu, batterie début / fin
Ressource get recharges => Ressource(
  chemin: 'recharges',
  titre: t('Recharges'),
  titreNouveau: t('Nouvelle recharge'),
  titreModifier: t('Modifier la recharge'),
  texteVide: t('Aucune recharge pour l\'instant.'),
  texteSupprimer: t('Supprimer cette recharge ?'),
  icone: Icons.ev_station,
  champs: [
    Champ('date', t('Date'), TypeChamp.date, obligatoire: true),
    Champ('lieu_recharge', t('Lieu de recharge'), TypeChamp.choix, choix: lieuxRecharge),
    Champ('pays', t('Pays de la recharge'), TypeChamp.choix, obligatoire: true, choix: paysImmatriculation),
    Champ('kilometrage', t('Kilométrage'), TypeChamp.entier, obligatoire: true, suffixe: 'km'),
    Champ('quantite', t('Énergie rechargée'), TypeChamp.decimal, obligatoire: true, suffixe: 'kWh'),
    Champ('montant', t('Montant payé TVAC'), TypeChamp.decimal, obligatoire: true, suffixe: '€'),
    Champ('taux_tva', t('Taux de TVA'), TypeChamp.decimal, suffixe: '%',
        aide: t('Taux du pays de la recharge, modifiable.')),
    Champ('niveau_restant', t('Batterie restante'), TypeChamp.choix, choix: niveauxBatterie,
        aide: t('Niveau de la batterie avant la recharge.')),
    Champ('plein_complet', t('Recharge complète'), TypeChamp.booleen,
        parDefaut: true, aide: t('Nécessaire pour calculer la consommation.')),
    Champ('station', t('Borne / opérateur'), TypeChamp.texte),
    Champ('ticket', t('Photo du ticket'), TypeChamp.image),
    Champ('remarques', t('Remarques'), TypeChamp.texte),
  ],
  titreLigne: (p, u) => '${nombre(p['quantite'])} kWh – ${euros(p['montant'])}',
  sousTitreLigne: (p, u) => [
    if ((p['lieu_recharge'] ?? '').toString().isNotEmpty) lieuxRecharge[p['lieu_recharge']] ?? p['lieu_recharge'],
    dateFr(p['date']),
    km(p['kilometrage'], u),
    if ((p['niveau_restant'] ?? '').toString().isNotEmpty)
      t('batterie : {niveau}', {'niveau': niveauxBatterie[p['niveau_restant']] ?? p['niveau_restant']}),
    if (p['prix_unitaire'] != null) '${nombre(p['prix_unitaire'], decimales: 3)} €/kWh',
  ].join(' · '),
);

Ressource get entretiens => Ressource(
  chemin: 'entretiens',
  titre: t('Entretiens'),
  titreNouveau: t('Nouvel entretien'),
  titreModifier: t('Modifier l\'entretien'),
  texteVide: t('Aucun entretien pour l\'instant.'),
  texteSupprimer: t('Supprimer cet entretien ?'),
  icone: Icons.build,
  champs: [
    Champ('date', t('Date'), TypeChamp.date, obligatoire: true),
    Champ('type', t('Type'), TypeChamp.choix, obligatoire: true, choix: typesEntretien, parDefaut: 'revision'),
    Champ('kilometrage', t('Kilométrage'), TypeChamp.entier, suffixe: 'km'),
    Champ('description', t('Description'), TypeChamp.texte),
    Champ('garage', t('Garage'), TypeChamp.texte),
    Champ('montant', t('Montant'), TypeChamp.decimal, suffixe: '€', parDefaut: '0'),
    Champ('facture', t('Facture (PDF ou photo)'), TypeChamp.fichier),
  ],
  titreLigne: (e, u) => typesEntretien[e['type']] ?? e['type'].toString(),
  sousTitreLigne: (e, u) => [
    dateFr(e['date']),
    if (e['kilometrage'] != null) km(e['kilometrage'], u),
    if ((e['garage'] ?? '').toString().isNotEmpty) e['garage'],
  ].join(' · '),
  montantLigne: (e) => euros(e['montant']),
);

Ressource get rappels => Ressource(
  chemin: 'rappels',
  titre: t('Rappels'),
  titreNouveau: t('Nouveau rappel'),
  titreModifier: t('Modifier le rappel'),
  texteVide: t('Aucun rappel pour l\'instant.'),
  texteSupprimer: t('Supprimer ce rappel ?'),
  icone: Icons.notifications_active,
  champs: [
    Champ('libelle', t('Libellé'), TypeChamp.texte, obligatoire: true),
    Champ('type_entretien', t('Type d\'entretien'), TypeChamp.choix,
        choix: typesEntretien, aide: t('Un entretien de ce type encodé ensuite relance automatiquement le rappel.')),
    Champ('echeance_date', t('Échéance (date)'), TypeChamp.date),
    Champ('echeance_km', t('Échéance (kilométrage)'), TypeChamp.entier, suffixe: 'km'),
    Champ('intervalle_mois', t('Répéter tous les'), TypeChamp.entier, suffixe: t('mois')),
    Champ('intervalle_km', t('Répéter tous les'), TypeChamp.entier, suffixe: 'km'),
    Champ('actif', t('Actif'), TypeChamp.booleen, parDefaut: true),
  ],
  titreLigne: (r, u) => r['libelle'].toString(),
  sousTitreLigne: (r, u) => [
    if (r['echeance_date'] != null) dateFr(r['echeance_date']),
    if (r['echeance_km'] != null) km(r['echeance_km'], u),
  ].join(t(' ou ')),
);

Ressource get documents => Ressource(
  chemin: 'documents',
  titre: t('Documents'),
  titreNouveau: t('Nouveau document'),
  titreModifier: t('Modifier le document'),
  texteVide: t('Aucun document pour l\'instant.'),
  texteSupprimer: t('Supprimer ce document ?'),
  icone: Icons.description,
  champs: [
    Champ('type', t('Type'), TypeChamp.choix, obligatoire: true, choix: typesDocument, parDefaut: 'assurance'),
    Champ('titre', t('Titre'), TypeChamp.texte),
    Champ('organisme', t('Organisme (assureur, centre…)'), TypeChamp.texte),
    Champ('numero', t('Numéro (police, certificat…)'), TypeChamp.texte),
    Champ('date_debut', t('Valable du'), TypeChamp.date),
    Champ('date_expiration', t('Valable jusqu\'au'), TypeChamp.date,
        aide: t('Un rappel est créé automatiquement à l\'échéance.')),
    Champ('montant', t('Montant (prime, redevance…)'), TypeChamp.decimal, suffixe: '€'),
    Champ('fichier', t('Fichier (PDF ou photo)'), TypeChamp.fichier),
  ],
  titreLigne: (d, u) => [typesDocument[d['type']] ?? d['type_libelle'], d['titre']]
      .where((x) => x != null && x.toString().isNotEmpty)
      .join(' – '),
  sousTitreLigne: (d, u) => [
    if ((d['organisme'] ?? '').toString().isNotEmpty) d['organisme'],
    if (d['date_expiration'] != null) t('jusqu\'au {date}', {'date': dateFr(d['date_expiration'])}),
  ].join(' · '),
  montantLigne: (d) => d['montant'] == null ? '' : euros(d['montant']),
);

Ressource get depenses => Ressource(
  chemin: 'depenses',
  titre: t('Autres dépenses'),
  titreNouveau: t('Nouvelle dépense'),
  titreModifier: t('Modifier la dépense'),
  texteVide: t('Aucune dépense pour l\'instant.'),
  texteSupprimer: t('Supprimer cette dépense ?'),
  icone: Icons.receipt_long,
  champs: [
    Champ('date', t('Date'), TypeChamp.date, obligatoire: true),
    Champ('categorie', t('Catégorie'), TypeChamp.choix, obligatoire: true, choix: categoriesDepense, parDefaut: 'taxe'),
    Champ('libelle', t('Libellé'), TypeChamp.texte),
    Champ('montant', t('Montant'), TypeChamp.decimal, obligatoire: true, suffixe: '€'),
  ],
  titreLigne: (d, u) => categoriesDepense[d['categorie']] ?? d['categorie'].toString(),
  sousTitreLigne: (d, u) => [dateFr(d['date']), if ((d['libelle'] ?? '').toString().isNotEmpty) d['libelle']].join(' · '),
  montantLigne: (d) => euros(d['montant']),
);

Ressource get kilometrages => Ressource(
  chemin: 'kilometrages',
  titre: t('Kilométrages'),
  titreNouveau: t('Nouveau relevé'),
  titreModifier: t('Modifier le relevé'),
  texteVide: t('Aucun relevé pour l\'instant.'),
  texteSupprimer: t('Supprimer ce relevé ?'),
  icone: Icons.speed,
  champs: [
    Champ('date', t('Date'), TypeChamp.date, obligatoire: true),
    Champ('kilometrage', t('Kilométrage'), TypeChamp.entier, obligatoire: true, suffixe: 'km'),
  ],
  // Historique complet : relevés + kilométrages des pleins, recharges, entretiens et de l'achat
  params: const {'historique': '1'},
  titreLigne: (k, u) => km(k['kilometrage'], u),
  sousTitreLigne: (k, u) => [
    if (k['date'] != null) dateFr(k['date']),
    sourcesKilometrage[k['source']] ?? t('Relevé'),
    if ((k['libelle'] ?? '').toString().isNotEmpty) k['libelle'],
    if (k['ecart'] is num && k['ecart'] > 0) '+${km(k['ecart'], u)}',
  ].join(' · '),
  iconeLigne: (k) => switch (k['source']) {
    'plein' => Icons.local_gas_station,
    'recharge' => Icons.ev_station,
    'entretien' => Icons.build,
    'achat' => Icons.shopping_cart,
    _ => Icons.speed,
  },
  modifiable: (k) => (k['source'] ?? 'releve') == 'releve',
);

/// Origine d'un kilométrage dans l'historique
Map<String, String> get sourcesKilometrage => {
  'releve': t('Relevé'),
  'plein': t('Plein'),
  'recharge': t('Recharge'),
  'entretien': t('Entretien'),
  'achat': t('Achat'),
};

/// Ressources affichées en onglets dans la fiche d'un véhicule
List<Ressource> get ressourcesVehicule =>
    [pleins, recharges, entretiens, rappels, documents, depenses, kilometrages];

/// Onglets d'un véhicule selon son énergie : pas de pleins pour un électrique,
/// recharges seulement pour un électrique ou un hybride rechargeable.
List<Ressource> ressourcesDe(Map? vehicule) {
  final energie = vehicule?['energie'];
  return [
    for (final r in ressourcesVehicule)
      if (!(r.chemin == 'pleins' && energie == 'electrique') &&
          !(r.chemin == 'recharges' && energie != 'electrique' && energie != 'phev'))
        r,
  ];
}
