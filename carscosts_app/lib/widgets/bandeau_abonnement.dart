import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../achats/abonnement.dart';
import '../l10n/langue.dart';
import '../ecrans/formules_ecran.dart';

/// Bandeau d'abonnement envoyé par le serveur : paiement refusé, formule suspendue ou échue, fin proche.
/// Un appui ouvre l'écran des formules.
class BandeauAbonnement extends StatelessWidget {
  const BandeauAbonnement({super.key, this.apresRetour, this.cliquable = true});

  /// false sur l'écran des formules lui-même.
  final bool cliquable;

  /// Appelé au retour de l'écran des formules (rechargement).
  final VoidCallback? apresRetour;

  @override
  Widget build(BuildContext context) {
    final alerte = context.watch<Abonnement>().alerte;
    if (alerte == null) return const SizedBox.shrink();
    final schema = Theme.of(context).colorScheme;
    final (fond, texte, icone) = switch (alerte['niveau']) {
      'erreur' => (schema.errorContainer, schema.onErrorContainer, Icons.lock_outline),
      'avertissement' => (Colors.orange.shade100, Colors.orange.shade900, Icons.credit_card_off),
      _ => (schema.secondaryContainer, schema.onSecondaryContainer, Icons.info_outline),
    };
    return Card(
      color: fond,
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: !cliquable ? null : () async {
          await Navigator.push(context, MaterialPageRoute(builder: (_) => const FormulesEcran()));
          apresRetour?.call();
        },
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(children: [
            Icon(icone, color: texte),
            const SizedBox(width: 12),
            Expanded(child: Text(alerte['message']?.toString() ?? '', style: TextStyle(color: texte))),
            if (cliquable) Icon(Icons.chevron_right, color: texte),
          ]),
        ),
      ),
    );
  }
}

/// Fiche d'un véhicule au-delà de la limite de la formule : consultation seulement.
class BandeauLectureSeule extends StatelessWidget {
  const BandeauLectureSeule({super.key, this.apresRetour});

  final VoidCallback? apresRetour;

  @override
  Widget build(BuildContext context) {
    final ab = context.watch<Abonnement>();
    final schema = Theme.of(context).colorScheme;
    return Card(
      color: schema.errorContainer,
      child: ListTile(
        leading: Icon(Icons.lock_outline, color: schema.onErrorContainer),
        title: Text(t('Véhicule en lecture seule'), style: TextStyle(color: schema.onErrorContainer)),
        subtitle: Text(
            t('Votre formule {formule} permet {n} véhicule(s) modifiable(s). Renouvelez votre formule ou archivez '
                'un véhicule pour le modifier à nouveau.', {'formule': ab.libelle, 'n': ab.limite}),
            style: TextStyle(color: schema.onErrorContainer)),
        trailing: Icon(Icons.chevron_right, color: schema.onErrorContainer),
        onTap: () async {
          await Navigator.push(context, MaterialPageRoute(builder: (_) => const FormulesEcran()));
          apresRetour?.call();
        },
      ),
    );
  }
}
