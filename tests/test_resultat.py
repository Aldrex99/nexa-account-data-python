import pandas as pd
from src.account_module.models.resultat import ResultatEpargne

def test_to_dataframe_basic():
  resultat = ResultatEpargne(
    nom_client="Alice",
    scenarios="Base",
    nom_produit="Livret A",
    effort_mensuel=100.123,
    total_versement=1200.567,
    montant_net_final=1250.891,
    atteint_objectif=True,
    indicateurs={}
  )
  df = resultat.to_dataframe()
  assert isinstance(df, pd.DataFrame)
  assert df.shape == (1, 7)
  row = df.iloc[0]
  assert row['nom_client'] == "Alice"
  assert row['scenarios'] == "Base"
  assert row['nom_produit'] == "Livret A"
  assert row['effort_mensuel'] == round(100.123, 2)
  assert row['total_versement'] == round(1200.567, 2)
  assert row['montant_net_final'] == round(1250.891, 2)
  assert row['atteint_objectif'] == True

def test_to_dataframe_with_indicateurs():
  indicateurs = {"taux_interet": 0.025, "bonus": "Oui"}
  resultat = ResultatEpargne(
    nom_client="Bob",
    scenarios="Optimiste",
    nom_produit="PEL",
    effort_mensuel=200.0,
    total_versement=2400.0,
    montant_net_final=2500.0,
    atteint_objectif=False,
    indicateurs=indicateurs
  )
  df = resultat.to_dataframe()
  assert isinstance(df, pd.DataFrame)
  assert df.shape == (1, 9)
  row = df.iloc[0]
  assert row['nom_client'] == "Bob"
  assert row['scenarios'] == "Optimiste"
  assert row['nom_produit'] == "PEL"
  assert row['effort_mensuel'] == 200.0
  assert row['total_versement'] == 2400.0
  assert row['montant_net_final'] == 2500.0
  assert row['atteint_objectif'] == False
  assert row['taux_interet'] == 0.025
  assert row['bonus'] == "Oui"

def test_to_dataframe_rounding():
  resultat = ResultatEpargne(
    nom_client="Charlie",
    scenarios="Pessimiste",
    nom_produit="Assurance Vie",
    effort_mensuel=99.999,
    total_versement=1999.999,
    montant_net_final=2999.999,
    atteint_objectif=True,
    indicateurs={}
  )
  df = resultat.to_dataframe()
  row = df.iloc[0]
  assert row['effort_mensuel'] == 100.00
  assert row['total_versement'] == 2000.00
  assert row['montant_net_final'] == 3000.00