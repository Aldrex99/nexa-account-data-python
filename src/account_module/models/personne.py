class Personne:
    def __init__(self, nom: str, age: int, revenu_annuel: float, loyer: float, depenses_mensuelles: float, objectif: float, duree_epargne: int, versement_mensuel_utilisateur: float =None):
        self.nom: str = nom
        self.age: int = age
        self.revenu_annuel: float = revenu_annuel
        self.loyer: float = loyer
        self.depenses_mensuelles: float = depenses_mensuelles
        self.objectif: float = objectif
        self.duree_epargne: int = duree_epargne
        self.versement_mensuel_utilisateur: int = versement_mensuel_utilisateur if versement_mensuel_utilisateur is not None else 0

    def __repr__(self):
        return f"Personne(nom={self.nom}, age={self.age}, revenu_annuel={self.revenu_annuel}, " \
               f"loyer={self.loyer}, depenses_mensuelles={self.depenses_mensuelles}, " \
               f"objectif={self.objectif}, duree_epargne={self.duree_epargne}, " \
               f"versement_mensuel_utilisateur={self.versement_mensuel_utilisateur})"

    def calcul_capacite_epargne(self):
        capacite_mensuelle = (self.revenu_annuel / 12) - self.loyer - self.depenses_mensuelles
        return capacite_mensuelle

    def __str__(self):
        return (f"Personne: {self.nom}, Age: {self.age}, Revenu Annuel: {self.revenu_annuel}, "
                f"Loyer: {self.loyer}, Dépenses Mensuelles: {self.depenses_mensuelles}, "
                f"Objectif: {self.objectif}, Durée d'Épargne: {self.duree_epargne} années, "
                f"Versement Mensuel : {"Pas de versement mensuel prévue" if self.versement_mensuel_utilisateur == 0 else self.versement_mensuel_utilisateur}, "
                f"Capacité d'Épargne Mensuelle: {self.calcul_capacite_epargne():.2f} €")