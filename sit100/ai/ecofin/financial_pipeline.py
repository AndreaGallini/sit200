from typing import Any

from .constants_ecofin import PRODUCTION_DECREASE_COEFFICIENT, SYSTEM_LIFETIME, MAINTENANCE_PERCENTAGE, \
    INSURANCE_PERCENTAGE, INCENTIVE_PERCENTAGE, INCENTIVE_MAX, INCENTIVE_YEARS, ENERGY_COST_PER_KWH, \
    AUTOCONSUMPTION_LEVEL, CER_REVENUE_PER_KW, RID_REVENUE_PER_KW, INCENTIVE_POWER_LIMIT


class FinancialPipeline:
    def __init__(self, data):
        self.data = data.copy()
        self.result: dict[str, Any] = {'success': True}

    def _calculate_energy_allocation(self):
        """Calcolo del riparto dell'energia prodotta annualmente in base all'uso e agli scopi."""
        self.result['autoconsumption_percentage'] = 0
        self.result['rid_percentage'] = 0
        self.result['cer_percentage'] = 0

        # è una cer: va tutto in cer
        if self.data.get('with_cer'):
            self.result['cer_percentage'] = 100
        # c'è autoconsumo
        elif self.data.get('with_autoconsumption'):
            # se c'è l'autoconsumo e vendita
            if self.data['with_autoconsumption_and_rid'] and self.data['autoconsumption_level']:
                self.result['autoconsumption_percentage'] = AUTOCONSUMPTION_LEVEL.get(
                    self.data['autoconsumption_level'], 50)
                self.result['rid_percentage'] = int(
                    100 - self.result['autoconsumption_percentage'])
            # se c'è l'autoconsumo e nessuna vendita
            else:
                self.result['autoconsumption_percentage'] = 100
        # c'è RID: tutto venduto
        elif self.data.get('with_rid'):
            self.result['rid_percentage'] = 100
        # caso non previsto: tutto autoconsumato
        else:
            self.result['autoconsumption_percentage'] = 100

    def _calculate_energy_production_decrease(self):
        """Calcolo della produzione di energia elettrica annuale considerando il normale decremento."""
        self.result['yearly_energy_produced'] = [
            int(self.data['energy_first_year'] * PRODUCTION_DECREASE_COEFFICIENT[i]) for i in
            range(SYSTEM_LIFETIME)
        ]

    def _calculate_total_energy_produced(self):
        """Calcola l'energia totale prodotta nel ciclo di vita dell'impianto."""
        self.result['lifetime_total_energy_produced'] = sum(
            self.result['yearly_energy_produced'])

    def _calculate_plant_cost(self):
        """Calcolo del costo dell'impianto."""
        self.result['plant_with_storage_cost'] = int(
            (1238.7 * self.data['generator_power'] + 49158))
        self.result['plant_without_storage_cost'] = int(
            (802.12 * self.data['generator_power'] + 27252))

    def _calculate_maintenance_costs(self):
        """Calcolo del costo annuale della manutenzione dal secondo anno in poi."""
        annual_maintenance_with = int(
            self.result['plant_with_storage_cost'] * MAINTENANCE_PERCENTAGE / 100)
        annual_maintenance_without = int(
            self.result['plant_without_storage_cost'] * MAINTENANCE_PERCENTAGE / 100)

        self.result['yearly_maintenance_with_storage'] = [0] + \
            [annual_maintenance_with] * (SYSTEM_LIFETIME - 1)
        self.result['yearly_maintenance_without_storage'] = [0] + \
            [annual_maintenance_without] * (SYSTEM_LIFETIME - 1)

    def _calculate_insurance_costs(self):
        """Calcolo del costo annuale dell'assicurazione."""
        self.result['yearly_insurance_with_storage'] = [
            int(self.result['plant_with_storage_cost'] * INSURANCE_PERCENTAGE / 100) for _ in
            range(SYSTEM_LIFETIME)
        ]
        self.result['yearly_insurance_without_storage'] = [
            int(self.result['plant_without_storage_cost'] * INSURANCE_PERCENTAGE / 100) for _ in
            range(SYSTEM_LIFETIME)
        ]

    def _calculate_yearly_total_costs(self):
        """Calcolo della somma di tutti i costi annuali (eccetto costo dell'impianto)."""
        self.result['yearly_total_costs_with_storage'] = [
            int(m + i)
            for m, i in zip(
                self.result['yearly_maintenance_with_storage'],
                self.result['yearly_insurance_with_storage']
            )
        ]
        self.result['yearly_total_costs_without_storage'] = [
            int(m + i)
            for m, i in zip(
                self.result['yearly_maintenance_without_storage'],
                self.result['yearly_insurance_without_storage']
            )
        ]

    def _calculate_tax_incentive_revenues(self):
        """Ricavi da incentivo fiscale previsto in caso di abitazione privata e fino a 20 kW,
        che inizia il secondo anno e dura 10 anni."""
        if self.data['private_house'] and self.data['generator_power'] <= INCENTIVE_POWER_LIMIT:
            incentive_with_storage = int(
                self.result['plant_with_storage_cost'] * INCENTIVE_PERCENTAGE / 100)
            incentive_without_storage = int(
                self.result['plant_without_storage_cost'] * INCENTIVE_PERCENTAGE / 100)
            incentive_with_storage = min(incentive_with_storage, INCENTIVE_MAX)
            incentive_without_storage = min(
                incentive_without_storage, INCENTIVE_MAX)
            self.result['yearly_incentive_with_storage'] = [0]
            self.result['yearly_incentive_without_storage'] = [0]
            for _ in range(1, INCENTIVE_YEARS + 1):
                self.result['yearly_incentive_with_storage'].append(
                    incentive_with_storage)
                self.result['yearly_incentive_without_storage'].append(
                    incentive_without_storage)
            self.result['incentive_with_storage'] = incentive_with_storage
            self.result['incentive_without_storage'] = incentive_without_storage
        else:
            self.result['yearly_incentive_with_storage'] = []
            self.result['yearly_incentive_without_storage'] = []
            self.result['incentive_with_storage'] = 0
            self.result['incentive_without_storage'] = 0

    def _calculate_savings_revenues(self):
        """Ricavi annuali da risparmio in bolletta."""
        energy = self.result.get('yearly_energy_produced', [])
        self.result['yearly_savings_revenues'] = [
            int(e * self.result['autoconsumption_percentage'] / 100 * ENERGY_COST_PER_KWH) for e in energy]

    def _calculate_cer_revenues(self):
        """Ricavi annuali da CER."""
        energy = self.result.get('yearly_energy_produced', [])
        self.result['yearly_cer_revenues'] = [int(e * self.result['cer_percentage'] / 100 * CER_REVENUE_PER_KW) for e in
                                              energy]

    def _calculate_rid_revenues(self):
        """Ricavi annuali da DIR (vendita)."""
        energy = self.result.get('yearly_energy_produced', [])
        self.result['yearly_rid_revenues'] = [int(e * self.result['rid_percentage'] / 100 * RID_REVENUE_PER_KW) for e in
                                              energy]

    def _calculate_total_revenue_components(self):
        """Calcola i ricavi totali su tutto il ciclo di vita da autoconsumo, CER e RID."""
        self.result['lifetime_savings_revenues'] = sum(
            self.result.get('yearly_savings_revenues', []))
        self.result['lifetime_cer_revenues'] = sum(
            self.result.get('yearly_cer_revenues', []))
        self.result['lifetime_rid_revenues'] = sum(
            self.result.get('yearly_rid_revenues', []))
        self.result['lifetime_incentive_with_storage'] = sum(
            self.result['yearly_incentive_with_storage'])
        self.result['lifetime_incentive_without_storage'] = sum(
            self.result['yearly_incentive_without_storage'])

    def _calculate_yearly_total_revenues(self):
        """Totale dei ricavi o risparmi annuali."""
        savings = self.result.get('yearly_savings_revenues', [])
        rid = self.result.get('yearly_rid_revenues', [])
        cer = self.result.get('yearly_cer_revenues', [])
        inc_with = self.result.get(
            'yearly_incentive_with_storage', [0] * SYSTEM_LIFETIME)
        inc_without = self.result.get(
            'yearly_incentive_without_storage', [0] * SYSTEM_LIFETIME)

        # Uniforma tutte le liste alla stessa lunghezza
        length = max(len(savings), len(rid), len(
            cer), len(inc_with), len(inc_without))
        savings += [0] * (length - len(savings))
        rid += [0] * (length - len(rid))
        cer += [0] * (length - len(cer))
        inc_with += [0] * (length - len(inc_with))
        inc_without += [0] * (length - len(inc_without))

        self.result['yearly_total_revenues_with_storage'] = [
            s + r + c + i for s, r, c, i in zip(savings, rid, cer, inc_with)
        ]
        self.result['yearly_total_revenues_without_storage'] = [
            s + r + c + i for s, r, c, i in zip(savings, rid, cer, inc_without)
        ]

    def _calculate_netcashflow(self):
        """Calcolo del cashflow netto annuale, escluso costo impianto."""
        revenues_with = self.result.get(
            'yearly_total_revenues_with_storage', [])
        revenues_without = self.result.get(
            'yearly_total_revenues_without_storage', [])
        costs_with = self.result.get('yearly_total_costs_with_storage', [])
        costs_without = self.result.get(
            'yearly_total_costs_without_storage', [])

        # Uniforma tutte le liste alla lunghezza del ciclo di vita
        length = SYSTEM_LIFETIME
        revenues_with += [0] * (length - len(revenues_with))
        revenues_without += [0] * (length - len(revenues_without))
        costs_with += [0] * (length - len(costs_with))
        costs_without += [0] * (length - len(costs_without))

        self.result['yearly_net_cashflow_with_storage'] = [
            r - c for r, c in zip(revenues_with, costs_with)
        ]
        self.result['yearly_net_cashflow_without_storage'] = [
            r - c for r, c in zip(revenues_without, costs_without)
        ]

    def _calculate_cumulative_cashflow(self):
        """Calcolo del cashflow cumulativo sulla lista dell'impainto, considerando anche cost impianto"""
        net_with = self.result.get('yearly_net_cashflow_with_storage', [])
        net_without = self.result.get(
            'yearly_net_cashflow_without_storage', [])
        length = SYSTEM_LIFETIME

        # Assicurati che le liste abbiano la lunghezza giusta
        net_with += [0] * (length - len(net_with))
        net_without += [0] * (length - len(net_without))

        initial_cost_with = self.result.get('plant_with_storage_cost', 0)
        initial_cost_without = self.result.get('plant_without_storage_cost', 0)

        cumulative_with = []
        cumulative_without = []

        # CON STORAGE
        total = net_with[0] - initial_cost_with
        cumulative_with.append(total)
        for i in range(1, length):
            total += net_with[i]
            cumulative_with.append(total)

        # SENZA STORAGE
        total = net_without[0] - initial_cost_without
        cumulative_without.append(total)
        for i in range(1, length):
            total += net_without[i]
            cumulative_without.append(total)

        self.result['cumulative_cashflow_with_storage'] = cumulative_with
        self.result['cumulative_cashflow_without_storage'] = cumulative_without

    def _total_costs_lifetime(self):
        """Calcolo dei costi totali (escluso impianto) sull'intero lifetime."""
        maintenance_with = self.result.get(
            'yearly_maintenance_with_storage', [])
        maintenance_without = self.result.get(
            'yearly_maintenance_without_storage', [])
        insurance_with = self.result.get('yearly_insurance_with_storage', [])
        insurance_without = self.result.get(
            'yearly_insurance_without_storage', [])

        total_with = sum(maintenance_with) + sum(insurance_with)
        total_without = sum(maintenance_without) + sum(insurance_without)

        self.result['total_cost_lifetime_with_storage'] = total_with
        self.result['total_cost_lifetime_without_storage'] = total_without

    def _total_revenues_lifetime(self):
        """Calcolo dei ricavi totali sull'intero lifetime."""
        savings = self.result.get('yearly_savings_revenues', [])
        cer = self.result.get('yearly_cer_revenues', [])
        rid = self.result.get('yearly_rid_revenues', [])
        incentive_with = self.result.get('yearly_incentive_with_storage', [])
        incentive_without = self.result.get(
            'yearly_incentive_without_storage', [])

        total_revenues_base = sum(savings) + sum(cer) + sum(rid)
        total_with = total_revenues_base + sum(incentive_with)
        total_without = total_revenues_base + sum(incentive_without)

        self.result['total_revenue_lifetime_with_storage'] = total_with
        self.result['total_revenue_lifetime_without_storage'] = total_without

    def _calculate_payback_period(self):
        """Calcolo dell'indice payback period."""
        cumulative_with = self.result.get(
            'cumulative_cashflow_with_storage', [])
        cumulative_without = self.result.get(
            'cumulative_cashflow_without_storage', [])

        def find_payback(cumulative_list):
            for i, value in enumerate(cumulative_list):
                if value >= 0:
                    return i + 1  # Anno 1-based
            return None

        self.result['payback_period_with_storage'] = find_payback(
            cumulative_with)
        self.result['payback_period_without_storage'] = find_payback(
            cumulative_without)

    def _evaluate_payback_period_comment(self):
        """Valutazione qualitativa del Payback Period (con e senza accumulo)."""

        def get_comment_text(payback_period):
            if payback_period is None:
                return "Il progetto in esame non raggiunge il Payback Period."

            comments = [
                (-1,
                 "Il valore di Payback Period è negativo. Questo valore è tipico di progetti con un alto livello di investimento iniziale e un basso livello di costi operativi."),
                (0,
                 "Si tratta di un tempo di recupero dell'investimento particolarmente rapido con una elevata convenienza finanziaria."),
                (5,
                 "Il valore di Payback Period evidenzia una buona sostenibilità finanziaria, ma con un periodo di rientro più lungo rispetto alle soluzioni più efficienti."),
                (10,
                 "Un tempo di recupero dell'investimento superiore ai 10 anni indica una redditività finanziaria dilazionata nel lungo periodo."),
            ]

            for threshold, comment in comments:
                if payback_period <= threshold:
                    return comment
            return comments[-1][1]  # Se > 10

        storage_payback = self.result.get('payback_period_with_storage')
        nostorage_payback = self.result.get('payback_period_without_storage')

        self.result['payback_comment_with_storage'] = get_comment_text(
            storage_payback)
        self.result['payback_comment_without_storage'] = get_comment_text(
            nostorage_payback)

    def _calculate_roi(self):
        """Calcolo dell'indice ROI (Return On Investment)."""
        total_revenue_with = self.result.get(
            'total_revenue_lifetime_with_storage', 0)
        total_revenue_without = self.result.get(
            'total_revenue_lifetime_without_storage', 0)
        total_cost_with = self.result.get(
            'total_cost_lifetime_with_storage', 0)
        total_cost_without = self.result.get(
            'total_cost_lifetime_without_storage', 0)
        initial_cost_with = self.result.get('plant_with_storage_cost', 0)
        initial_cost_without = self.result.get('plant_without_storage_cost', 0)

        roi_with = ((total_revenue_with - total_cost_with) / initial_cost_with * 100) \
            if initial_cost_with else None
        roi_without = ((total_revenue_without - total_cost_without) / initial_cost_without * 100) \
            if initial_cost_without else None

        self.result['roi_with_storage'] = round(
            roi_with, 2) if roi_with is not None else None
        self.result['roi_without_storage'] = round(
            roi_without, 2) if roi_without is not None else None

    def _evaluate_roi_comment(self):
        """Valutazione qualitativa del ROI (Return On Investment)."""

        def get_roi_comment_text(roi_value):
            if roi_value is None:
                return "Non è possibile calcolare il ROI per questo progetto."

            roi_comments = [
                (-1, "Questo valore di ROI indica un mancato ritorno economico rispetto alla spesa sostenuta."),
                (0, "Questo valore di ROI indica un ritorno economico limitato rispetto alla spesa sostenuta."),
                (150,
                 "Questo valore di ROI cumulativo indica un ritorno economico bilanciato e in linea con i parametri standard del settore fotovoltaico."),
                (300,
                 "Questo valore di ROI cumulativo rappresenta un ritorno economico eccellente con elevata redditività, tipica di progetti ben ottimizzati e in contesti particolarmente favorevoli."),
            ]

            comment = roi_comments[0][1]
            for threshold, text in roi_comments:
                if roi_value <= threshold:
                    break
                else:
                    comment = text
            return comment

        storage_roi = self.result.get('roi_with_storage')
        nostorage_roi = self.result.get('roi_without_storage')

        self.result['roi_comment_with_storage'] = (
            f"Nel caso in esame si ottiene un ROI pari al {storage_roi:.2f}%: {get_roi_comment_text(storage_roi)}"
            if storage_roi is not None else "Non è possibile calcolare il ROI per il caso con accumulo."
        )
        self.result['roi_comment_without_storage'] = (
            f"Nel caso in esame si ottiene un ROI pari al {nostorage_roi:.2f}%: {get_roi_comment_text(nostorage_roi)}"
            if nostorage_roi is not None else "Non è possibile calcolare il ROI per il caso senza accumulo."
        )

    def _compile_strings(self):
        self.result['str_system_lifetime'] = f"{SYSTEM_LIFETIME} anni"
        self.result['str_energy_cost_per_kwh'] = f"{ENERGY_COST_PER_KWH} €/kWh"
        self.result['str_maintenance_percentage'] = f"{MAINTENANCE_PERCENTAGE}% del costo dell'impianto"
        self.result['str_insurance_percentage'] = f"{INSURANCE_PERCENTAGE}% del costo dell'impianto"
        self.result['str_cer_revenue_per_kwh'] = f"{CER_REVENUE_PER_KW} €/kWh"
        self.result['str_rid_revenue_per_kwh'] = f"{RID_REVENUE_PER_KW} €/kWh"

        if self.result['lifetime_incentive_with_storage'] > 0:
            self.result['str_incentive_with_storage_comment'] = (f"Detrazioni fiscali per abitazione privata: "
                                                                 f"detrazione fiscale del {INCENTIVE_PERCENTAGE}% del "
                                                                 f"costo dell'impianto in un arco di 10 anni, "
                                                                 f"con un limite massimo di spesa di {INCENTIVE_MAX} euro. "
                                                                 f"Durata della detrazione fiscale è di {INCENTIVE_YEARS} anni "
                                                                 f"a partire dal secondo anno fino al {INCENTIVE_YEARS + 1}° anno."
                                                                 f" Il bonus fiscale annuale per l’impianto è pari a "
                                                                 f"{self.result['yearly_incentive_with_storage'][1]} €.")
        if self.result['lifetime_incentive_without_storage'] > 0:
            self.result['str_incentive_without_storage_comment'] = (f"Detrazioni fiscali per abitazione privata: "
                                                                    f"detrazione fiscale del {INCENTIVE_PERCENTAGE}% del "
                                                                    f"costo dell'impianto in un arco di 10 anni, "
                                                                    f"con un limite massimo di spesa di {INCENTIVE_MAX} euro. "
                                                                    f"Durata della detrazione fiscale è di {INCENTIVE_YEARS} anni "
                                                                    f"a partire dal secondo anno fino al {INCENTIVE_YEARS + 1}° anno."
                                                                    f" Il bonus fiscale annuale per l’impianto è pari a "
                                                                    f"{self.result['yearly_incentive_without_storage'][1]} €.")
        self.result['str_incentive_with_storage'] = f"{self.result['incentive_with_storage']} €/anno"
        self.result['str_incentive_without_storage'] = f"{self.result['incentive_without_storage']} €/anno"

        self.result['str_energy_produced_first_year'] = f"{self.data['energy_first_year']} kWh/year"
        self.result['str_lifetime_total_energy_produced'] = f"{self.result['lifetime_total_energy_produced']} kWh"

        self.result['str_lifetime_savings_revenues'] = f"{self.result['lifetime_savings_revenues']} €"
        self.result['str_lifetime_cer_revenues'] = f"{self.result['lifetime_cer_revenues']} €"
        self.result['str_lifetime_rid_revenues'] = f"{self.result['lifetime_rid_revenues']} €"

        self.result[
            'str_plant_with_storage_cost'] = f"Il costo dell'impianto con accumulo è {self.result['plant_with_storage_cost']} €."
        self.result[
            'str_plant_without_storage_cost'] = f"Il costo dell'impianto senza accumulo è {self.result['plant_without_storage_cost']} €."

        self.result[
            'str_total_revenues_first_year_with_storage'] = f"{self.result['yearly_total_revenues_with_storage'][0]} €/primo anno"
        self.result[
            'str_total_revenues_first_year_without_storage'] = f"{self.result['yearly_total_revenues_without_storage'][0]} €/primo anno"

    def run(self):
        def safe_call(method, name):
            try:
                method()
            except Exception as e:
                self.result['success'] = False
                self.result['failed_step'] = name
                self.result['error'] = str(e)
                raise RuntimeError(
                    f"Errore nella pipeline ({name}): {e}") from e

        try:
            safe_call(self._calculate_energy_allocation, "energy_allocation")
            safe_call(self._calculate_energy_production_decrease,
                      "energy_production_decrease")
            safe_call(self._calculate_total_energy_produced,
                      "total_energy_produced")

            safe_call(self._calculate_plant_cost, "plant_cost")
            safe_call(self._calculate_maintenance_costs, "maintenance_costs")
            safe_call(self._calculate_insurance_costs, "insurance_costs")
            safe_call(self._calculate_yearly_total_costs, "total_costs")

            safe_call(self._calculate_tax_incentive_revenues,
                      "tax_incentive_revenues")
            safe_call(self._calculate_savings_revenues, "savings_revenues")
            safe_call(self._calculate_cer_revenues, "cer_revenues")
            safe_call(self._calculate_rid_revenues, "rid_revenues")
            safe_call(self._calculate_total_revenue_components,
                      "total_revenue_components")
            safe_call(self._calculate_yearly_total_revenues, "total_revenues")

            safe_call(self._total_costs_lifetime, "costs_lifetime")
            safe_call(self._total_revenues_lifetime, "revenues_lifetime")

            safe_call(self._calculate_netcashflow, "netcashflow")
            safe_call(self._calculate_cumulative_cashflow,
                      "cumulative_cashflow")

            safe_call(self._calculate_payback_period, "payback_period")
            safe_call(self._evaluate_payback_period_comment,
                      "comment_payback_period")
            safe_call(self._calculate_roi, "roi")
            safe_call(self._evaluate_roi_comment, "comment_roi")

            safe_call(self._compile_strings, "compile_strings")

            return self.result

        except RuntimeError:
            # L'errore è già stato tracciato e rilanciato da safe_call
            raise
