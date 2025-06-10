import os
import pandas as pd
import logging
from typing import List

import src.account_module.utils as utils
from src.account_module.models.personne import Personne
from src.account_module.models.epargne import Epargne
from src.account_module.models.resultat import ResultatEpargne

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def import_personnes(fichier: str) -> List[Personne]:
    """
    Import a file of persons and return a list of Personne instances.
    """
    df = utils.read_dataframe(fichier)
    df = utils.clean_dataframe(df, float_cols=['revenu_annuel', 'loyer', 'depenses_mensuelles', 'objectif', 'versement_mensuel_utilisateur'], int_cols=['age', 'duree_epargne'])

    personnes = []
    for idx, row in df.iterrows():
        try:
            p = Personne(
                nom=row['nom'],
                age=int(row['age']),
                revenu_annuel=float(row['revenu_annuel']),
                loyer=float(row['loyer']),
                depenses_mensuelles=float(row['depenses_mensuelles']),
                objectif=float(row['objectif']),
                duree_epargne=int(row['duree_epargne']),
                versement_mensuel_utilisateur=float(row['versement_mensuel_utilisateur']) if 'versement_mensuel_utilisateur' in row else None
            )
            personnes.append(p)
        except Exception as e:
            logging.error(f"Erreur instanciation Personne à la ligne {idx}: {e}")
            raise

    logging.info(f"Import de {len(personnes)} personnes terminé.")
    return personnes


def import_epargnes(fichier: str) -> List[Epargne]:
    """
    Import a file of savings products and return a list of Epargne instances.
    """
    df = utils.read_dataframe(fichier)
    df = utils.clean_dataframe(
        df,
        float_cols=['taux_interet', 'fiscalite', 'versement_max'],
        int_cols=['duree_min']
    )

    epargnes = []
    for idx, row in df.iterrows():
        try:
            e = Epargne(
                nom=row['nom'],
                taux_interet=float(row['taux_interet']),
                fiscalite=float(row['fiscalite']),
                versement_max=float(row['versement_max']),
                duree_min=int(row['duree_min'])
            )
            epargnes.append(e)
        except Exception as e:
            logging.error(f"Erreur instanciation Epargne à la ligne {idx}: {e}")
            raise

    logging.info(f"Import de {len(epargnes)} produits d'épargne terminé.")
    return epargnes

def save_personnes(personnes: List[Personne], fichier: str):
    """
    Save a list of Personne instances to a file.
    """
    # Conversion en DataFrame via dict
    data = [p.__dict__ for p in personnes]
    df = pd.DataFrame(data)
    utils.write_dataframe(df, fichier)


def save_epargnes(epargnes: List[Epargne], fichier: str):
    """
    Save a list of Epargne instances to a file.
    """
    data = [e.__dict__ for e in epargnes]
    df = pd.DataFrame(data)
    utils.write_dataframe(df, fichier)

def suggestion_epargne(personne: Personne,
                        epargnes: List[Epargne]) -> List[ResultatEpargne]:
    """
    Generates savings plan suggestions for each product,
    calculating gross and net amounts over the specified duration.

    Considered scenarios:
    - user-provided monthly deposit (if any)
    - 25%, 50%, 75%, 100% of the monthly savings capacity

    Only products meeting the minimum duration are considered,
    and annual deposits exceeding the product's cap are skipped.
    """
    resultats: List[ResultatEpargne] = []
    capacite_mensuelle = personne.calcul_capacite_epargne()

    # Prepare monthly scenarios
    scenarios = []
    if personne.versement_mensuel_utilisateur and personne.versement_mensuel_utilisateur > 0:
        scenarios.append(personne.versement_mensuel_utilisateur)
    for pct in (0.25, 0.5, 0.75, 1.0):
        scenarios.append(capacite_mensuelle * pct)

    for e in epargnes:
        # Check minimum duration requirement
        if personne.duree_epargne < e.duree_min:
            logging.debug(f"Skipping {e.nom}: minimum duration not met")
            continue
        for vm in scenarios:
            versement_annuel = vm * 12
            # Check annual deposit cap
            if versement_annuel > e.versement_max:
                logging.debug(f"Skipping {vm:.2f}€/mois for {e.nom}: cap exceeded")
                continue
            # Calculate gross amount
            montant_brut = utils.calcul_interets_composes(versement_annuel, e.taux_interet, personne.duree_epargne)
            total_versement = versement_annuel * personne.duree_epargne
            gain = montant_brut - total_versement
            # Apply taxation on the gain
            montant_net = total_versement + gain * (1 - e.fiscalite / 100)
            resultats.append(ResultatEpargne(
                nom_client=personne.nom,
                scenarios= round(vm / capacite_mensuelle * 100, 2) if capacite_mensuelle > 0 else 0,
                nom_produit=e.nom,
                effort_mensuel=vm if vm > 0 else 0,
                montant_net_final=montant_net if montant_net > 0 else 0,
                atteint_objectif=(montant_net >= personne.objectif),
                indicateurs={
                    'taux_interet': e.taux_interet,
                    'fiscalite': e.fiscalite,
                    'duree_min': e.duree_min,
                    'versement_max': e.versement_max
                }
            ))

    logging.info(f"Generated {len(resultats)} savings scenarios successfully.")
    return resultats

