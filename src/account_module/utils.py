def calcul_interets_composes(versement_annuel: float, taux_annuel: float, duree_annees: int) -> float:
    montant_final = 0.0
    for _ in range(duree_annees):
        montant_final = (montant_final + versement_annuel) * (1 + taux_annuel / 100)
    return montant_final
