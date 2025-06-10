from src.account_module.models.epargne import Epargne
from src.account_module.models.personne import Personne
from src.account_module.utils import calcul_interets_composes

def main():
    # Création d'un objet Epargne
    epargne = Epargne(
        nom="Livret A",
        taux_interet=3.0,
        fiscalite=0.0,
        duree_min=12,
        versement_max=15000.0,
    )

    # Affichage de l'objet Epargne
    print(epargne)

    # Création d'un objet Personne
    personne = Personne(
        nom="Alice",
        age=30,
        revenu_annuel=30000.0,
        loyer=800.0,
        depenses_mensuelles=500.0,
        objectif=20000.0,
        duree_epargne=5,
        versement_mensuel_utilisateur=200.0
    )

    # Affichage de l'objet Personne
    print(personne)

    # Calcul des intérêts composés
    versement_annuel = personne.versement_mensuel_utilisateur * 12
    taux_annuel = epargne.taux_interet
    duree_annees = personne.duree_epargne

    montant_final = calcul_interets_composes(versement_annuel, taux_annuel, duree_annees)

    print(f"Montant final après {duree_annees} ans: {montant_final:.2f} €")

if __name__ == "__main__":
    main()
