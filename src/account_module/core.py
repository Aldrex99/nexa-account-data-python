import os
import pandas as pd
import logging
from typing import List

from src.account_module.models.personne import Personne
from src.account_module.models.epargne import Epargne

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _read_dataframe(fichier: str) -> pd.DataFrame:
    """
    Read a file into a pandas DataFrame.
    """
    ext = os.path.splitext(fichier)[1].lower()
    try:
        if ext in ['.csv', '.txt']:
            if ext == '.csv':
                df = pd.read_csv(fichier, sep=',')
            else:
                df = pd.read_csv(fichier, sep='\t')
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(fichier)
        else:
            raise ValueError(f"Format de fichier non supporté: {ext}")
    except Exception as e:
        logging.error(f"Erreur lecture fichier {fichier}: {e}")
        raise
    logging.info(f"Fichier {fichier} lu avec succès ({len(df)} lignes)")
    return df


def _clean_dataframe(df: pd.DataFrame,
                     float_cols: List[str],
                     int_cols: List[str]) -> pd.DataFrame:
    """
    Clean a DataFrame by converting specified columns to float or int.
    """
    df = df.copy()
    # Nettoyage float
    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].replace(['None', None], pd.NA)
            try:
                df[col] = df[col].astype(float)
            except Exception as e:
                logging.error(f"Conversion en float impossible pour la colonne '{col}': {e}")
                raise ValueError(f"Format invalide pour {col}")
    # Nettoyage int
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].replace(['None', None], pd.NA)
            try:
                # Utilise Int64 pour permettre les NaN
                df[col] = df[col].astype('Int64')
            except Exception as e:
                logging.error(f"Conversion en int impossible pour la colonne '{col}': {e}")
                raise ValueError(f"Format invalide pour {col}")
    return df


def import_personnes(fichier: str) -> List[Personne]:
    """
    Import a file of persons and return a list of Personne instances.
    """
    df = _read_dataframe(fichier)
    df = _clean_dataframe(df, float_cols=['revenu_annuel', 'loyer', 'depenses_mensuelles', 'objectif', 'versement_mensuel_utilisateur'], int_cols=['age', 'duree_epargne'])

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
    df = _read_dataframe(fichier)
    df = _clean_dataframe(
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


def _write_dataframe(df: pd.DataFrame, fichier: str):
    """
    Write a DataFrame to a file in the appropriate format based on the file extension.
    """
    ext = os.path.splitext(fichier)[1].lower()
    try:
        if ext in ['.csv', '.txt']:
            if ext == '.csv':
                df.to_csv(fichier, index=False)
            else:
                df.to_csv(fichier, sep='\t', index=False)
        elif ext in ['.xlsx', '.xls']:
            df.to_excel(fichier, index=False)
        else:
            raise ValueError(f"Format de fichier non supporté: {ext}")
    except Exception as e:
        logging.error(f"Erreur écriture fichier {fichier}: {e}")
        raise
    logging.info(f"Fichier {fichier} enregistré ({len(df)} lignes)")


def save_personnes(personnes: List[Personne], fichier: str):
    """
    Save a list of Personne instances to a file.
    """
    # Conversion en DataFrame via dict
    data = [p.__dict__ for p in personnes]
    df = pd.DataFrame(data)
    _write_dataframe(df, fichier)


def save_epargnes(epargnes: List[Epargne], fichier: str):
    """
    Save a list of Epargne instances to a file.
    """
    data = [e.__dict__ for e in epargnes]
    df = pd.DataFrame(data)
    _write_dataframe(df, fichier)
