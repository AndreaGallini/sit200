"""
photovoltaic_sizing.py
Classe che si occupa di lanciare le pipelines del dimensionamento e delle verifiche tecniche.
Ritorna il dizionario dei modelli.
"""
import json
import os

from .params import STORAGE_CONSTANT_LEVEL
from ..sizing.plant_sizer import PlantSizer


class PhotovoltaicSizing:

    def __init__(self, data):
        self.data = data

    def process_pipelines(self):

        # ---------------- USER INPUT

        # di default: Tetto a Laterizio TL
        fv_type = self.data.get('mounting', 'TL')

        if self.data['storage'] == '1':
            with_storage = True
        else:
            with_storage = False

        # questa deriva dagli scopi
        storage_level = 1
        if self.data['auto_consumption']:
            storage_level = STORAGE_CONSTANT_LEVEL[self.data.get('auto_consumption', 'auto-med')]

        user_subfields = self.data.get('generator', '')
        # facoltativo: potenza totale
        # TODO da spostare in user input processor
        peak_power = self.data.get('peak_power', {})
        peak_power_value = peak_power.get('value')
        peak_power_unit = peak_power.get('unit')
        user_total_power = None
        if peak_power:
            if peak_power_value:
                if peak_power_unit == 'kWp':
                    user_total_power = float(peak_power_value)
                elif peak_power_unit == 'mWp':
                    user_total_power = float(peak_power_value) * 1000
            else:
                user_total_power = None

        # ===============================================================

        sizer = PlantSizer(
            fv_position=fv_type,
            user_subfields=user_subfields,
            user_total_power=user_total_power,
            fv_with_storage=with_storage,
            storage_level=storage_level
        )
        output = sizer.run()

        if output:
            return output
        else:
            print("ERRORE: nel dimensionamento")
            return {}
