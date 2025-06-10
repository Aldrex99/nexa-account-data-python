import logging
import os
from typing import List
import pandas as pd

def calcul_interets_composes(versement_annuel: float, taux_annuel: float, duree_annees: int) -> float:
    montant_final = 0.0
    for _ in range(duree_annees):
        montant_final = (montant_final + versement_annuel) * (1 + taux_annuel / 100)
    return montant_final

def read_dataframe(fichier: str) -> pd.DataFrame:
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


def clean_dataframe(df: pd.DataFrame,
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


def write_dataframe(df: pd.DataFrame, fichier: str):
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