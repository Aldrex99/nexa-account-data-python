from src.account_module.core import import_personnes, import_epargnes, save_personnes, save_epargnes
from src.account_module.models.epargne import Epargne
from src.account_module.models.personne import Personne
from src.account_module.utils import calcul_interets_composes

def main():
    # Création d'un objet Epargne
    epargne = Epargne(
        nom="Livret A",
        taux_interet=2.4,
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
        duree_epargne=20,
        versement_mensuel_utilisateur=100.0
    )

    # Affichage de l'objet Personne
    print(personne)

    # Calcul des intérêts composés
    versement_annuel = personne.versement_mensuel_utilisateur * 12
    taux_annuel = epargne.taux_interet
    duree_annees = personne.duree_epargne

    montant_final = calcul_interets_composes(versement_annuel, taux_annuel, duree_annees)

    print(f"\nCalcul des intérêts composés pour {personne.nom}:")
    print(f"Versement annuel: {versement_annuel} €")
    print(f"Taux d'intérêt annuel: {taux_annuel}%")
    print(f"Montant final après {duree_annees} ans: {montant_final:.2f} €")

    try:
        personnes_df = import_personnes('./src/account_module/data/personnes.txt')
        print("\nPersonnes importées:")
        print(personnes_df)

        epargnes_df = import_epargnes('./src/account_module/data/epargnes.txt')
        print("\nProduits d'épargne importés:")
        print(epargnes_df)

        save_personnes(personnes_df, 'cleaned_personnes.txt')
        save_epargnes(epargnes_df, 'cleaned_epargnes.txt')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
