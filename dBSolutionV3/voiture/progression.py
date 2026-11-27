"""
Barre de progression texte pour les commandes manage.py (sans dépendance externe).

    barre = Progression(total, "[carscosts] modèles")
    for x in elements:
        ...
        barre.avancer()
    barre.terminer()

Dans un terminal : barre redessinée sur place (« [carscosts] modèles  [██████░░░░]  62 %  8 012/12 806 »).
Hors terminal (journal, redirection) : une ligne tous les 10 %.
Utiliser barre.message(texte) pour afficher une ligne sans casser la barre.
"""
import sys
import time


class Progression:
    def __init__(self, total, libelle="", largeur=30, flux=None):
        self.total = max(int(total), 0)
        self.libelle = libelle
        self.largeur = largeur
        self.flux = flux or sys.stderr
        self.fait = 0
        self.tty = hasattr(self.flux, "isatty") and self.flux.isatty()
        self._dernier_pct = -1
        self._dernier_palier = -10
        self._dernier_temps = 0.0
        self._debut = time.monotonic()
        self._dessiner(force=True)

    def avancer(self, n=1):
        self.fait = min(self.fait + n, self.total) if self.total else self.fait + n
        self._dessiner()

    def message(self, texte):
        """Affiche une ligne au-dessus de la barre, puis redessine la barre."""
        if self.tty:
            self.flux.write("\r\033[K")
        self.flux.write(f"{texte}\n")
        self._dessiner(force=True)

    def terminer(self):
        self.fait = self.total
        self._dessiner(force=True)
        if self.tty:
            self.flux.write("\n")
        self.flux.flush()

    def _pct(self):
        return 100 if not self.total else int(self.fait * 100 / self.total)

    def _dessiner(self, force=False):
        pct = self._pct()
        maintenant = time.monotonic()
        if self.tty:
            if not force and pct == self._dernier_pct and maintenant - self._dernier_temps < 0.2:
                return
            plein = int(self.largeur * pct / 100)
            barre = "█" * plein + "░" * (self.largeur - plein)
            ecoule = maintenant - self._debut
            reste = ""
            if 0 < self.fait < self.total and ecoule > 1:
                secondes = int(ecoule * (self.total - self.fait) / self.fait)
                reste = f"  reste ~{secondes // 60} min {secondes % 60:02d} s"
            total = f"{self.total:,}".replace(",", " ")
            fait = f"{self.fait:,}".replace(",", " ")
            self.flux.write(f"\r\033[K{self.libelle}  [{barre}] {pct:3d} %  {fait}/{total}{reste}")
            self.flux.flush()
        else:
            palier = pct // 10 * 10
            if palier <= self._dernier_palier:
                return
            self._dernier_palier = palier
            self.flux.write(f"{self.libelle} : {pct} % ({self.fait}/{self.total})\n")
            self.flux.flush()
        self._dernier_pct = pct
        self._dernier_temps = maintenant
