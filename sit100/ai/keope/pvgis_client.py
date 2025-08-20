"""
pvgis_client.py
Classe che si occupa di effettuare richieste API a PVGIS, gestire la risposta e ritornare i dati.
"""
# from django.http import JsonResponse
# from django.utils import timezone
from apps.project.models import Counter, Project

import requests


class PVGISClient:
    PVGIS_BASE_URL = 'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc'

    def __init__(self, data):
        self.data = data

    def fetch_solar_data(self, latitude, longitude, peak_power, loss=14, tilt=30, azimuth=0,
                         pvtech_choice="crystSi", fixed=1, output_format="json"):
        """Recupera i dati solari da PVGIS."""

        params = {
            "lat": latitude,
            "lon": longitude,
            "peakpower": peak_power,
            "loss": loss,
            "pvtechchoice": pvtech_choice,
            "fixed": fixed,
            "angle": tilt,
            "aspect": azimuth,
            "outputformat": output_format
        }

        try:
            response = requests.get(
                self.PVGIS_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            # logger.warning(f'pvgis request timeout, {project_code}, {e} ')
            print(e)
            return False
        except requests.exceptions.RequestException as e:
            # logger.warning(f'pvgis request error, {project_code}, {e} ')
            print(e)
            return False
        except ValueError as e:
            print(e)
            # logger.warning(f'pvgis json not valid, {project_code}, {e} ')
            return False
        except Exception as e:
            print(e)
            # logger.warning(f'pvgis json not valid, {project_code}, {e} ')
            return False

    def get_solar_data(self):
        """
        Esegue le richieste PVGIS per ogni sottocampo e restituisce i dati organizzati per sottocampo.
        """
        '''
        pvgis_counter = Counter.objects.get(name='Pvgis_code')
        pvgis_code = pvgis_counter.value
        pvgis_time_at = pvgis_counter.time_at
        time = timezone.now()
        interval = time - pvgis_time_at
        minutes = interval.seconds // 60 % 60
        if (pvgis_code != 200):
            if (minutes > 20):
                pvgis_counter.value = 200
                pvgis_counter.save()
        '''

        project_code = self.data['project_code']
        latitude = self.data['latitude']
        longitude = self.data['longitude']

        # Verifica il tipo di impianto
        plant_type = self.data.get('type', "grid-connected")
        if plant_type == 'off-grid':
            # logger.warning(f'pvgis error, {project_code}, no grid-connected')
            return False

        # Ottieni i dati del generatore
        generator = self.data.get('generator', {})
        if not generator:
            # logger.warning(f'pvgis error, {project_code}, mancano i dati del generatore')
            return False

        # Ottieni le perdite totali
        losses = self.data.get("sizing", {}).get('total_losses', 14)
        loss = losses[0] if isinstance(losses, list) and losses else 14

        pvtech_choice = "crystSi"
        fixed = 1

        # Risultati per ogni sottocampo
        pvgis_subfields = {}
        all_requests_successful = True

        if not self.data['sizing']:
            return {}

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                # Verifica che il sottocampo abbia i dati necessari
                if 'inclination' not in subfield_data or 'azimuth' not in subfield_data:
                    all_requests_successful = False
                    continue

                # Ottieni i parametri specifici del sottocampo
                tilt = subfield_data.get('inclination', 30)
                azimuth = subfield_data.get('azimuth', 0)
                subfield_peak_power = self.data['sizing'][field_name][subfield_name].get(
                    'total_power')

                solar_data = self.fetch_solar_data(
                    latitude=latitude,
                    longitude=longitude,
                    peak_power=subfield_peak_power,
                    loss=loss,
                    tilt=tilt,
                    azimuth=azimuth,
                    pvtech_choice=pvtech_choice,
                    fixed=fixed
                )

                if solar_data:
                    # Salva i dati per questo sottocampo
                    pvgis_subfields[subfield_name] = solar_data
                else:
                    print(
                        f"Errore nella richiesta PVGIS per sottocampo {subfield_name}")
                    all_requests_successful = False

        # Restituisce i risultati
        if pvgis_subfields:
            result = {"pvgis_subfields": pvgis_subfields}

            # Per compatibilità con il codice esistente, aggiungi anche un risultato aggregato
            # usando il primo sottocampo come riferimento
            if pvgis_subfields:
                first_subfield_data = list(pvgis_subfields.values())[0]
                result["pvgis"] = first_subfield_data

            return result
        else:
            # pvgis_counter.value = 405
            # pvgis_counter.save()
            return {}
