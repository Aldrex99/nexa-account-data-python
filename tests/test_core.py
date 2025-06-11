import pytest
from unittest.mock import patch, MagicMock
from src.account_module.core import suggestion_epargne
from src.account_module.models.personne import Personne
from src.account_module.models.epargne import Epargne
from src.account_module.models.resultat import ResultatEpargne

@pytest.fixture
def mock_personne():
  # Mock Personne with calcul_capacite_epargne method
  p = Personne(
    nom="Alice",
    age=30,
    revenu_annuel=36000,
    loyer=6000,
    depenses_mensuelles=1000,
    objectif=10000,
    duree_epargne=5,
    versement_mensuel_utilisateur=200
  )
  p.calcul_capacite_epargne = MagicMock(return_value=500)
  return p

@pytest.fixture
def mock_epargnes():
  # Two products, one with lower min duration, one with higher
  e1 = Epargne(
    nom="Livret A",
    taux_interet=0.01,
    fiscalite=0.0,
    versement_max=22950,
    duree_min=1
  )
  e2 = Epargne(
    nom="PEL",
    taux_interet=0.02,
    fiscalite=0.3,
    versement_max=61000,
    duree_min=4
  )
  return [e1, e2]

@patch("src.account_module.core.utils.calcul_interets_composes")
def test_suggestion_epargne_basic(mock_calc, mock_personne, mock_epargnes):
  # Mock compound interest calculation: just return total deposit + 1000 for test
  def fake_calc(versement_annuel, taux, duree):
    return versement_annuel * duree + 1000
  mock_calc.side_effect = fake_calc

  resultats = suggestion_epargne(mock_personne, mock_epargnes)
  # There should be 2 products * 5 scenarios = 10 results
  assert len(resultats) == 10
  # Check that all results are for the correct client
  for res in resultats:
    assert res.nom_client == "Alice"
    assert res.nom_produit in ["Livret A", "PEL"]
    assert res.effort_mensuel > 0
    assert isinstance(res.atteint_objectif, bool)
    assert "taux_interet" in res.indicateurs

@patch("src.account_module.core.utils.calcul_interets_composes")
def test_suggestion_epargne_min_duration(mock_calc, mock_personne, mock_epargnes):
  # Set personne.duree_epargne lower than one product's min duration
  mock_personne.duree_epargne = 2
  mock_calc.return_value = 10000
  # Only Livret A should be considered (duree_min=1), not PEL (duree_min=4)
  resultats = suggestion_epargne(mock_personne, mock_epargnes)
  assert all(r.nom_produit == "Livret A" for r in resultats)
  assert len(resultats) == 5

@patch("src.account_module.core.utils.calcul_interets_composes")
def test_suggestion_epargne_objectif_exceeds_cap(mock_calc, mock_personne, mock_epargnes):
  # Set objectif higher than both products' versement_max
  mock_personne.objectif = 1000000
  mock_calc.return_value = 10000
  resultats = suggestion_epargne(mock_personne, mock_epargnes)
  # Should skip all products, so resultats is empty
  assert resultats == []

@patch("src.account_module.core.utils.calcul_interets_composes")
def test_suggestion_epargne_no_user_versement(mock_calc, mock_personne, mock_epargnes):
  # Remove user versement, only capacity scenarios should be used
  mock_personne.versement_mensuel_utilisateur = None
  mock_calc.return_value = 10000
  resultats = suggestion_epargne(mock_personne, mock_epargnes)
  # 2 products * 4 scenarios = 8
  assert len(resultats) == 8

@patch("src.account_module.core.utils.calcul_interets_composes")
def test_suggestion_epargne_zero_versement_max(mock_calc, mock_personne, mock_epargnes):
  # Set one product's versement_max to zero
  mock_epargnes[0].versement_max = 0
  mock_calc.return_value = 10000
  resultats = suggestion_epargne(mock_personne, mock_epargnes)
  # Should still return results for the other product
  assert len(resultats) == 5
  assert all(r.nom_produit == "PEL" for r in resultats)
