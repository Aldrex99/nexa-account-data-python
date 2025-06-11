from src.account_module.models.personne import Personne

def test_repr_with_versement_mensuel_utilisateur():
  personne = Personne(
    nom="Alice",
    age=30,
    revenu_annuel=36000.0,
    loyer=800.0,
    depenses_mensuelles=500.0,
    objectif=10000.0,
    duree_epargne=5,
    versement_mensuel_utilisateur=200.0
  )
  expected = ("Personne(nom=Alice, age=30, revenu_annuel=36000.0, "
        "loyer=800.0, depenses_mensuelles=500.0, "
        "objectif=10000.0, duree_epargne=5, "
        "versement_mensuel_utilisateur=200.0)")
  assert repr(personne) == expected

def test_repr_without_versement_mensuel_utilisateur():
  personne = Personne(
    nom="Bob",
    age=40,
    revenu_annuel=48000.0,
    loyer=1000.0,
    depenses_mensuelles=700.0,
    objectif=20000.0,
    duree_epargne=10
    # versement_mensuel_utilisateur is None by default
  )
  expected = ("Personne(nom=Bob, age=40, revenu_annuel=48000.0, "
        "loyer=1000.0, depenses_mensuelles=700.0, "
        "objectif=20000.0, duree_epargne=10, "
        "versement_mensuel_utilisateur=0)")
  assert repr(personne) == expected

def test_repr_with_zero_values():
  personne = Personne(
    nom="Charlie",
    age=0,
    revenu_annuel=0.0,
    loyer=0.0,
    depenses_mensuelles=0.0,
    objectif=0.0,
    duree_epargne=0,
    versement_mensuel_utilisateur=0.0
  )
  expected = ("Personne(nom=Charlie, age=0, revenu_annuel=0.0, "
        "loyer=0.0, depenses_mensuelles=0.0, "
        "objectif=0.0, duree_epargne=0, "
        "versement_mensuel_utilisateur=0.0)")
  assert repr(personne) == expected