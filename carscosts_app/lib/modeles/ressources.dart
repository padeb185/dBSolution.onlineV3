import 'package:flutter/material.dart';

import '../widgets/format.dart';

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
    required this.titreSingulier,
    required this.icone,
    required this.champs,
    required this.titreLigne,
    required this.sousTitreLigne,
    this.montantLigne,
  });

  final String chemin; // ex. "pleins"
  final String titre; // ex. "Pleins"
  final String titreSingulier; // ex. "plein"
  final IconData icone;
  final List<Champ> champs;
  final String Function(Map<String, dynamic>) titreLigne;
  final String Function(Map<String, dynamic>) sousTitreLigne;
  final String Function(Map<String, dynamic>)? montantLigne;
}

const typesEntretien = {
  'revision': 'Révision / entretien périodique',
  'vidange': 'Vidange',
  'pneus': 'Pneus',
  'freins': 'Freins',
  'distribution': 'Distribution',
  'batterie': 'Batterie',
  'climatisation': 'Climatisation',
  'controle_technique': 'Contrôle technique',
  'carrosserie': 'Carrosserie',
  'reparation': 'Réparation',
  'autre': 'Autre',
};

const typesDocument = {
  'assurance': 'Assurance',
  'controle_technique': 'Contrôle technique',
  'carte_grise': 'Certificat d\'immatriculation (carte grise)',
  'coc': 'Certificat de conformité (COC)',
  'facture_achat': 'Facture d\'achat',
  'autre': 'Autre',
};

const categoriesDepense = {
  'taxe': 'Taxe de circulation / vignette',
  'assurance': 'Assurance',
  'parking': 'Parking / péage',
  'lavage': 'Lavage',
  'accessoire': 'Accessoires / équipements',
  'amende': 'Amende',
  'financement': 'Crédit / leasing',
  'autre': 'Autre',
};

const energies = {
  'essence': 'Essence',
  'diesel': 'Diesel',
  'hybride': 'Hybride',
  'phev': 'Hybride rechargeable',
  'electrique': 'Électrique',
  'gpl': 'GPL',
  'gnc': 'GNC',
};

final pleins = Ressource(
  chemin: 'pleins',
  titre: 'Pleins',
  titreSingulier: 'plein',
  icone: Icons.local_gas_station,
  champs: const [
    Champ('date', 'Date', TypeChamp.date, obligatoire: true),
    Champ('kilometrage', 'Kilométrage', TypeChamp.entier, obligatoire: true, suffixe: 'km'),
    Champ('quantite', 'Quantité', TypeChamp.decimal, obligatoire: true, suffixe: 'L / kWh'),
    Champ('montant', 'Montant payé', TypeChamp.decimal, obligatoire: true, suffixe: '€'),
    Champ('plein_complet', 'Plein complet', TypeChamp.booleen,
        parDefaut: true, aide: 'Nécessaire pour calculer la consommation.'),
    Champ('electrique', 'Recharge électrique', TypeChamp.booleen, parDefaut: false),
    Champ('station', 'Station', TypeChamp.texte),
    Champ('ticket', 'Photo du ticket', TypeChamp.image),
    Champ('remarques', 'Remarques', TypeChamp.texte),
  ],
  titreLigne: (p) => '${nombre(p['quantite'])} ${p['electrique'] == true ? 'kWh' : 'L'} – ${euros(p['montant'])}',
  sousTitreLigne: (p) => '${dateFr(p['date'])} · ${km(p['kilometrage'])}'
      '${p['prix_unitaire'] != null ? ' · ${nombre(p['prix_unitaire'], decimales: 3)} €/u' : ''}',
);

final entretiens = Ressource(
  chemin: 'entretiens',
  titre: 'Entretiens',
  titreSingulier: 'entretien',
  icone: Icons.build,
  champs: const [
    Champ('date', 'Date', TypeChamp.date, obligatoire: true),
    Champ('type', 'Type', TypeChamp.choix, obligatoire: true, choix: typesEntretien, parDefaut: 'revision'),
    Champ('kilometrage', 'Kilométrage', TypeChamp.entier, suffixe: 'km'),
    Champ('description', 'Description', TypeChamp.texte),
    Champ('garage', 'Garage', TypeChamp.texte),
    Champ('montant', 'Montant', TypeChamp.decimal, suffixe: '€', parDefaut: '0'),
    Champ('facture', 'Facture (PDF ou photo)', TypeChamp.fichier),
  ],
  titreLigne: (e) => typesEntretien[e['type']] ?? e['type'].toString(),
  sousTitreLigne: (e) => [
    dateFr(e['date']),
    if (e['kilometrage'] != null) km(e['kilometrage']),
    if ((e['garage'] ?? '').toString().isNotEmpty) e['garage'],
  ].join(' · '),
  montantLigne: (e) => euros(e['montant']),
);

final rappels = Ressource(
  chemin: 'rappels',
  titre: 'Rappels',
  titreSingulier: 'rappel',
  icone: Icons.notifications_active,
  champs: const [
    Champ('libelle', 'Libellé', TypeChamp.texte, obligatoire: true),
    Champ('type_entretien', 'Type d\'entretien', TypeChamp.choix,
        choix: typesEntretien, aide: 'Un entretien de ce type encodé ensuite relance automatiquement le rappel.'),
    Champ('echeance_date', 'Échéance (date)', TypeChamp.date),
    Champ('echeance_km', 'Échéance (kilométrage)', TypeChamp.entier, suffixe: 'km'),
    Champ('intervalle_mois', 'Répéter tous les', TypeChamp.entier, suffixe: 'mois'),
    Champ('intervalle_km', 'Répéter tous les', TypeChamp.entier, suffixe: 'km'),
    Champ('actif', 'Actif', TypeChamp.booleen, parDefaut: true),
  ],
  titreLigne: (r) => r['libelle'].toString(),
  sousTitreLigne: (r) => [
    if (r['echeance_date'] != null) dateFr(r['echeance_date']),
    if (r['echeance_km'] != null) km(r['echeance_km']),
  ].join(' ou '),
);

final documents = Ressource(
  chemin: 'documents',
  titre: 'Documents',
  titreSingulier: 'document',
  icone: Icons.description,
  champs: const [
    Champ('type', 'Type', TypeChamp.choix, obligatoire: true, choix: typesDocument, parDefaut: 'assurance'),
    Champ('titre', 'Titre', TypeChamp.texte),
    Champ('organisme', 'Organisme (assureur, centre…)', TypeChamp.texte),
    Champ('numero', 'Numéro (police, certificat…)', TypeChamp.texte),
    Champ('date_debut', 'Valable du', TypeChamp.date),
    Champ('date_expiration', 'Valable jusqu\'au', TypeChamp.date,
        aide: 'Un rappel est créé automatiquement à l\'échéance.'),
    Champ('montant', 'Montant (prime, redevance…)', TypeChamp.decimal, suffixe: '€'),
    Champ('fichier', 'Fichier (PDF ou photo)', TypeChamp.fichier),
  ],
  titreLigne: (d) => [d['type_libelle'] ?? typesDocument[d['type']], d['titre']]
      .where((x) => x != null && x.toString().isNotEmpty)
      .join(' – '),
  sousTitreLigne: (d) => [
    if ((d['organisme'] ?? '').toString().isNotEmpty) d['organisme'],
    if (d['date_expiration'] != null) 'jusqu\'au ${dateFr(d['date_expiration'])}',
  ].join(' · '),
  montantLigne: (d) => d['montant'] == null ? '' : euros(d['montant']),
);

final depenses = Ressource(
  chemin: 'depenses',
  titre: 'Autres dépenses',
  titreSingulier: 'dépense',
  icone: Icons.receipt_long,
  champs: const [
    Champ('date', 'Date', TypeChamp.date, obligatoire: true),
    Champ('categorie', 'Catégorie', TypeChamp.choix, obligatoire: true, choix: categoriesDepense, parDefaut: 'taxe'),
    Champ('libelle', 'Libellé', TypeChamp.texte),
    Champ('montant', 'Montant', TypeChamp.decimal, obligatoire: true, suffixe: '€'),
  ],
  titreLigne: (d) => categoriesDepense[d['categorie']] ?? d['categorie'].toString(),
  sousTitreLigne: (d) => [dateFr(d['date']), if ((d['libelle'] ?? '').toString().isNotEmpty) d['libelle']].join(' · '),
  montantLigne: (d) => euros(d['montant']),
);

final kilometrages = Ressource(
  chemin: 'kilometrages',
  titre: 'Kilométrages',
  titreSingulier: 'relevé',
  icone: Icons.speed,
  champs: const [
    Champ('date', 'Date', TypeChamp.date, obligatoire: true),
    Champ('kilometrage', 'Kilométrage', TypeChamp.entier, obligatoire: true, suffixe: 'km'),
  ],
  titreLigne: (k) => km(k['kilometrage']),
  sousTitreLigne: (k) => dateFr(k['date']),
);

/// Ressources affichées en onglets dans la fiche d'un véhicule
final ressourcesVehicule = [pleins, entretiens, rappels, documents, depenses, kilometrages];
