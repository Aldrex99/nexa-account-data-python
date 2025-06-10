class Epargne:
    def __init__(self, nom: str, taux_interet: float, fiscalite: float, duree_min: int, versement_max: float= None):
        self.nom: str = nom
        self.taux_interet: float = taux_interet
        self.fiscalite: float = fiscalite
        self.duree_min: int = duree_min
        self.versement_max: float = versement_max if versement_max is not None else float('inf')

    def __repr__(self):
        return (f"Epargne(nom={self.nom}, taux_interet={self.taux_interet}, "
                f"fiscalite={self.fiscalite}, duree_min={self.duree_min}, "
                f"versement_max={self.versement_max})")

    def __str__(self):
        return (f"Epargne: {self.nom}, Taux d'Intérêt: {self.taux_interet}%, "
                f"Fiscalité: {self.fiscalite}%, Durée Minimum: {self.duree_min} années, "
                f"Versement Maximum: {'Aucune limite' if self.versement_max == float('inf') else self.versement_max}")