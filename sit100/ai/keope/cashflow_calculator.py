"""
cashflow_calculator.py
Classe che si occupa di lanciare la pipeline Cashflow.
Ritorna il dizionario dei modelli.
"""

import matplotlib.pyplot as plt
import os.path
import matplotlib
from ..ecofin.financial_pipeline import FinancialPipeline
# Usa il backend non-GUI per evitare problemi con i thread
matplotlib.use('Agg')


class CashflowCalculator:

    def __init__(self, data):
        self.data = data
        self.project_complete_path = self.data['project_complete_path']

    def process_pipeline(self):
        """Lancia le pipelines di cashflow."""

        # ---------------- USER + MODELS INPUT
        with_storage = True if self.data.get('storage') == '1' else False

        energy_first_year = self.data.get('ao1', {}).get('total_energy_production', 0)
        private_house = True if self.data.get('private_house') == 'si' else False
        with_autoconsumption = True if self.data.get('self_consumption') == '1' else False
        with_cer = True if self.data.get('plant_scope') == 'cer' else False
        with_rid = True if self.data.get('rid') == '1' else False
        with_autoconsumption_and_rid = True if self.data.get('plant_scope') == 'produzione-vendita-industriale' else False
        autoconsumption_level = self.data.get('auto_consumption')

        data = {
            'generator_power': self.data.get('generator_power'),
            'with_storage': with_storage,
            'energy_first_year': energy_first_year,
            'private_house': private_house,
            'with_autoconsumption': with_autoconsumption,
            'with_cer': with_cer,
            'with_rid': with_rid,
            'with_autoconsumption_and_rid': with_autoconsumption_and_rid,
            'autoconsumption_level': autoconsumption_level,
        }

        pipeline = FinancialPipeline(data)

        try:
            result = pipeline.run()
        except RuntimeError as e:
            print("❌ Errore nella pipeline:", e)
            return {}
        else:
            return {"ecofin": result}
