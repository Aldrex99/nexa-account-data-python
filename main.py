import pandas as pd

from src.account_module.core import import_personnes, import_epargnes, save_personnes, save_epargnes
from src.account_module.models.epargne import Epargne
from src.account_module.models.personne import Personne
from src.account_module.utils import calcul_interets_composes
from src.account_module.core import suggestion_epargne

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
        personnes_df = import_personnes('./src/account_module/data/personnes.csv')

        epargnes_df = import_epargnes('./src/account_module/data/epargnes.csv')

        save_personnes(personnes_df, 'cleaned_personnes.csv')
        save_epargnes(epargnes_df, 'cleaned_epargnes.csv')

    except Exception as e:
        print(f"An error occurred: {e}")

    # Test suggestion d'épargne
    try:
        cleaned_personnes = import_personnes('cleaned_personnes.csv')
        if not cleaned_personnes:
            raise ValueError("Aucune personne trouvée dans le fichier nettoyé.")

        cleaned_epargnes = import_epargnes('cleaned_epargnes.csv')
        if not cleaned_epargnes:
            raise ValueError("Aucun produit d'épargne trouvé dans le fichier nettoyé.")

        suggestions = []
        for personne in cleaned_personnes:
            print(f"\nSuggestions d'épargne pour {personne.nom}:")
            suggestions.extend(suggestion_epargne(personne, cleaned_epargnes))
            if not suggestions:
                print("Aucune suggestion d'épargne disponible.")
            else:
                for suggestion in suggestions:
                    suggestion.afficher()

        # Export des suggestions en DataFrame
        suggestions_df = pd.concat([s.to_dataframe() for s in suggestions], ignore_index=True)
        suggestions_df.to_csv('suggestions_epargne.csv', index=False)

    except Exception as e:
        print(f"An error occurred during the savings suggestion: {e}")

if __name__ == "__main__":
    main()
