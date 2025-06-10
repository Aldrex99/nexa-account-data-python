from dataclasses import dataclass, field
import pandas as pd
from typing import Any, Dict

@dataclass
class ResultatEpargne:
    """
    Represents the result of a savings suggestion for a product.

    Attributes:
        nom_client (str): Name of the client.
        nom_produit (str): Name of the savings product.
        effort_mensuel (float): Monthly contribution effort.
        montant_net_final (float): Final net amount after taxes.
        atteint_objectif (bool): Whether the savings goal was reached.
        indicateurs (Dict[str, Any]): Additional metrics for extensibility.
    """
    nom_client: str
    scenarios: str
    nom_produit: str
    effort_mensuel: float
    montant_net_final: float
    atteint_objectif: bool
    indicateurs: Dict[str, Any] = field(default_factory=dict)

    def afficher(self) -> None:
        """
        Prints a formatted summary of the result to the console.
        """
        status = '✅ Objective reached' if self.atteint_objectif else '❌ Objective not reached'
        print(f"Product: {self.nom_produit}")
        print(f"  - Monthly effort: {self.effort_mensuel:.2f} €")
        print(f"  - Final net amount: {self.montant_net_final:.2f} €")
        print(f"  - Status: {status}")
        if self.indicateurs:
            print("  - Additional indicators:")
            for key, value in self.indicateurs.items():
                print(f"      * {key}: {value}")

    def to_dataframe(self) -> pd.DataFrame:
        """
        Exports the result to a pandas DataFrame (single-row).

        Returns:
            pd.DataFrame: DataFrame with columns for each attribute and any extra indicators.
        """
        # Base data
        data = {
            'nom_client': self.nom_client,
            'scenarios': self.scenarios,
            'nom_produit': self.nom_produit,
            'effort_mensuel': round(self.effort_mensuel, 2),
            'montant_net_final': round(self.montant_net_final, 2),
            'atteint_objectif': self.atteint_objectif,
        }
        # Merge additional indicators
        data.update(self.indicateurs)
        # Create DataFrame
        df = pd.DataFrame([data])
        return df
