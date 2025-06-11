from src.account_module.models.epargne import Epargne

def test_repr_with_all_fields():
  epargne = Epargne(nom="Livret A", taux_interet=3.0, fiscalite=0.0, duree_min=1, versement_max=22950.0)
  expected = ("Epargne(nom=Livret A, taux_interet=3.0, "
        "fiscalite=0.0, duree_min=1, versement_max=22950.0)")
  assert repr(epargne) == expected

def test_repr_with_default_versement_max():
  epargne = Epargne(nom="PEL", taux_interet=2.0, fiscalite=17.2, duree_min=4)
  expected = ("Epargne(nom=PEL, taux_interet=2.0, "
        "fiscalite=17.2, duree_min=4, versement_max=inf)")
  assert repr(epargne) == expected

def test_repr_with_zero_values():
  epargne = Epargne(nom="Test", taux_interet=0.0, fiscalite=0.0, duree_min=0, versement_max=0.0)
  expected = ("Epargne(nom=Test, taux_interet=0.0, "
        "fiscalite=0.0, duree_min=0, versement_max=0.0)")
  assert repr(epargne) == expected