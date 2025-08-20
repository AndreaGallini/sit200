from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
# Usa il backend non-GUI per evitare problemi con i thread
matplotlib.use('Agg')


class Chart_Generator:
    """
    Classe per generare grafici personalizzati con Seaborn
    Supporta diversi stili predefiniti e la visualizzazione di dati con varie unità di misura

    Nota: Utilizza il backend Agg di matplotlib per evitare problemi con i thread
    in applicazioni web Django (NSWindow deve essere creato solo nel thread principale)
    """

    def __init__(self):
        """
        Inizializza il generatore di grafici con stili personalizzati predefiniti
        """
        # Definisce gli stili personalizzati disponibili
        self.stili_disponibili = {
            'cashflow': {
                'style': 'whitegrid',
                'palette': ['#4682B4'],
                'font_scale': 1,
                'rc': {
                    'axes.spines.top': False,
                    'axes.spines.right': False,
                    'axes.spines.left': False,
                    'axes.spines.bottom': True,
                    'axes.grid': True,
                    'axes.grid.axis': 'y',
                    'grid.alpha': 0.3,
                    'axes.labelsize': 9,
                    'xtick.labelsize': 8,
                    'ytick.labelsize': 8,
                    'axes.titlesize': 10
                }
            },
            'elegante': {
                'style': 'whitegrid',
                'palette': ['#2E8B57', '#4682B4', '#DAA520', '#CD853F', '#8B4513', '#556B2F'],
                'font_scale': 1.2,
                'rc': {
                    'axes.spines.top': False,
                    'axes.spines.right': False,
                    'axes.labelsize': 12,
                    'xtick.labelsize': 10,
                    'ytick.labelsize': 10,
                    'axes.titlesize': 14,
                    'legend.fontsize': 10
                }
            },
            'moderno': {
                'style': 'white',
                'palette': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
                'font_scale': 1.1,
                'rc': {
                    'axes.spines.top': False,
                    'axes.spines.right': False,
                    'axes.spines.left': False,
                    'axes.spines.bottom': True,
                    'axes.grid': True,
                    'axes.grid.axis': 'y',
                    'grid.alpha': 0.3,
                    'axes.labelsize': 11,
                    'xtick.labelsize': 9,
                    'ytick.labelsize': 9,
                    'axes.titlesize': 13
                }
            },
            'professionale': {
                'style': 'darkgrid',
                'palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
                'font_scale': 1.0,
                'rc': {
                    'axes.labelsize': 11,
                    'xtick.labelsize': 9,
                    'ytick.labelsize': 9,
                    'axes.titlesize': 12,
                    'legend.fontsize': 9,
                    'grid.color': '.8',
                    'grid.linestyle': '-',
                    'grid.alpha': 0.5
                }
            },
            'minimal': {
                'style': 'ticks',
                'palette': ['#34495e', '#95a5a6', '#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
                'font_scale': 0.9,
                'rc': {
                    'axes.spines.top': False,
                    'axes.spines.right': False,
                    'axes.spines.left': True,
                    'axes.spines.bottom': True,
                    'axes.linewidth': 1.5,
                    'axes.edgecolor': '#333333',
                    'axes.labelsize': 10,
                    'xtick.labelsize': 8,
                    'ytick.labelsize': 8,
                    'axes.titlesize': 12,
                    'axes.titleweight': 'bold'
                }
            },
            'colorato': {
                'style': 'white',
                'palette': ['#9b59b6', '#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#1abc9c'],
                'font_scale': 1.3,
                'rc': {
                    'axes.spines.top': False,
                    'axes.spines.right': False,
                    'axes.spines.left': False,
                    'axes.spines.bottom': False,
                    'axes.grid': True,
                    'grid.alpha': 0.4,
                    'axes.facecolor': '#f8f9fa',
                    'axes.labelsize': 12,
                    'xtick.labelsize': 10,
                    'ytick.labelsize': 10,
                    'axes.titlesize': 15,
                    'axes.titleweight': 'bold'
                }
            }
        }

        # Mesi in italiano per la visualizzazione
        self.mesi_italiano = {
            1: 'Gen', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mag', 6: 'Giu',
            7: 'Lug', 8: 'Ago', 9: 'Set', 10: 'Ott', 11: 'Nov', 12: 'Dic'
        }

    def ottieni_stili_disponibili(self) -> List[str]:
        """
        Restituisce la lista degli stili disponibili
        """
        return list(self.stili_disponibili.keys())

    def applica_stile(self, nome_stile: str) -> bool:
        """
        Applica lo stile specificato al grafico
        """
        if nome_stile not in self.stili_disponibili:
            print(
                f"Stile '{nome_stile}' non disponibile. Stili disponibili: {self.ottieni_stili_disponibili()}")
            return False

        stile = self.stili_disponibili[nome_stile]
        sns.set_theme(
            style=stile['style'],
            palette=stile['palette'],
            font_scale=stile['font_scale'],
            rc=stile['rc']
        )
        return True

    def crea_grafico(self,
                     dati: Dict,
                     titolo: str,
                     label_x: str,
                     label_y: str,
                     stile: str = 'elegante',
                     tipo_grafico: str = 'barre',
                     dimensioni: tuple = (12, 6),
                     unita_misura_tempo: str = '',
                     salva_file: Optional[str] = None) -> plt.Figure:
        """
        Crea un grafico personalizzato

        Args:
            dati: Dizionario con i dati da visualizzare
            titolo: Titolo del grafico
            label_x: Etichetta dell'asse X
            label_y: Etichetta dell'asse Y
            stile: Stile del grafico da applicare
            tipo_grafico: Tipo di grafico ('barre', 'barre_orizzontali', 'linee', 'punti', 'torta')
            dimensioni: Dimensioni del grafico (larghezza, altezza)
            unita_misura_tempo: 'mesi' per conversione a nomi italiani
            salva_file: Nome del file per salvare il grafico (opzionale)

        Returns:
            plt.Figure: Oggetto figura di matplotlib
        """
        # Validazione unificata
        if not self._valida_dati(dati, unita_misura_tempo):
            raise ValueError(
                "Dati non validi per il tipo di grafico specificato")

        # Applica lo stile
        if not self.applica_stile(stile):
            self.applica_stile('elegante')
            print(f"Applicato stile di fallback: 'elegante'")

        # Prepara i dati
        df_dati = self._prepara_dataframe(dati, unita_misura_tempo)

        # Crea il grafico
        fig, ax = plt.subplots(figsize=dimensioni)

        # Genera il grafico in base al tipo richiesto
        metodi_grafici = {
            'barre': self._crea_grafico_barre,
            'barre_orizzontali': self._crea_grafico_barre_orizzontali,
            'linee': self._crea_grafico_linee,
            'punti': self._crea_grafico_punti,
            'torta': lambda df, ax: self._crea_grafico_torta(df, ax, stile)
        }

        if tipo_grafico not in metodi_grafici:
            raise ValueError(
                f"Tipo di grafico '{tipo_grafico}' non supportato. Usa: {list(metodi_grafici.keys())}")

        metodi_grafici[tipo_grafico](df_dati, ax)

        # Personalizza il grafico
        self._personalizza_grafico(ax, titolo, label_x, label_y, tipo_grafico)
        self._applica_finiture(ax, stile, tipo_grafico)

        # Salva il file se richiesto
        if salva_file:
            self._salva_grafico(fig, salva_file)

        plt.tight_layout()
        return fig

    def _valida_dati(self, dati: Dict, unita_misura_tempo: str) -> bool:
        """
        Validazione unificata per tutti i tipi di dati
        """
        if not isinstance(dati, dict) or not dati:
            return False

        for chiave, valore in dati.items():
            # Validazione per mesi
            if unita_misura_tempo == 'mesi':
                if not isinstance(chiave, int) or not (1 <= chiave <= 12):
                    return False

            # Validazione valori (gestisce anche stringhe con %)
            if isinstance(valore, str) and valore.endswith('%'):
                try:
                    float(valore[:-1])
                except ValueError:
                    return False
            elif not isinstance(valore, (int, float)) or not np.isfinite(valore):
                return False

        return True

    def _prepara_dataframe(self, dati: Dict, unita_misura_tempo: str) -> pd.DataFrame:
        """
        Preparazione unificata del DataFrame per tutti i tipi di dati
        """
        chiavi = []
        valori = []
        valori_originali = []

        # Ordina i dati
        if unita_misura_tempo == 'mesi':
            chiavi_ordinate = sorted(dati.keys())
        else:
            try:
                chiavi_ordinate = sorted(dati.keys(), key=lambda x: float(x))
            except (ValueError, TypeError):
                chiavi_ordinate = list(dati.keys())

        # Prepara i dati
        for chiave in chiavi_ordinate:
            valore = dati[chiave]
            valori_originali.append(valore)

            # Converte le chiavi
            if unita_misura_tempo == 'mesi':
                chiavi.append(self.mesi_italiano[chiave])
            else:
                chiavi.append(str(chiave))

            # Converte i valori
            if isinstance(valore, str) and valore.endswith('%'):
                valori.append(float(valore[:-1]))
            else:
                valori.append(float(valore))

        return pd.DataFrame({
            'nome_mese': chiavi,
            'potenza': valori,
            'valore_originale': valori_originali
        })

    def _crea_grafico_barre(self, df_dati: pd.DataFrame, ax: plt.Axes) -> None:
        """
        Crea un grafico a barre verticali utilizzando Seaborn
        """
        sns.barplot(data=df_dati, x='nome_mese',
                    y='potenza', ax=ax)

    def _crea_grafico_barre_orizzontali(self, df_dati: pd.DataFrame, ax: plt.Axes) -> None:
        """
        Crea un grafico a barre orizzontali utilizzando Seaborn
        """
        # Funzione corretta per creare barre orizzontali con larghezza ottimale
        # Converte la colonna nome_mese in categorica per forzare l'ordine
        df_dati = df_dati.copy()
        # Ordine desiderato (mantiene l'ordine originale dei dati)
        ordine_mesi = df_dati['nome_mese'].tolist()

        # Crea il grafico a barre orizzontali con barre più sottili e ordine fisso
        sns.barplot(data=df_dati, x='potenza', y='nome_mese', ax=ax,
                    width=0.4, order=ordine_mesi)

        # Imposta esplicitamente i tick e le etichette per evitare il warning
        ax.set_yticks(range(len(ordine_mesi)))
        ax.set_yticklabels(ordine_mesi, fontweight='normal')

    def _crea_grafico_linee(self, df_dati: pd.DataFrame, ax: plt.Axes) -> None:
        """
        Crea un grafico a linee utilizzando Seaborn
        """
        sns.lineplot(data=df_dati, x='nome_mese', y='potenza', ax=ax,
                     marker='o', markersize=8, linewidth=2.5)

        # Aggiunge valori sui punti
        for i, (mese, potenza) in enumerate(zip(df_dati['nome_mese'], df_dati['potenza'])):
            # Formatta senza decimali se è un intero
            if potenza == int(potenza):
                testo_valore = f'{int(potenza)}'
            else:
                testo_valore = f'{potenza:.1f}'
            ax.annotate(testo_valore, (i, potenza),
                        textcoords="offset points", xytext=(0, 10), ha='center',
                        fontweight='normal', fontsize=9)

    def _crea_grafico_punti(self, df_dati: pd.DataFrame, ax: plt.Axes) -> None:
        """
        Crea un grafico a punti utilizzando Seaborn
        """
        sns.scatterplot(data=df_dati, x='nome_mese', y='potenza', ax=ax,
                        s=120, alpha=0.8, edgecolors='black', linewidth=1.5)

        # Aggiunge valori accanto ai punti
        for i, (mese, potenza) in enumerate(zip(df_dati['nome_mese'], df_dati['potenza'])):
            # Formatta senza decimali se è un intero
            if potenza == int(potenza):
                testo_valore = f'{int(potenza)}'
            else:
                testo_valore = f'{potenza:.1f}'
            ax.annotate(testo_valore, (i, potenza),
                        textcoords="offset points", xytext=(15, 5), ha='left',
                        fontweight='normal', fontsize=9)

    def _crea_grafico_torta(self, df_dati: pd.DataFrame, ax: plt.Axes, stile: str) -> None:
        """
        Crea un grafico a torta utilizzando Matplotlib
        """
        # Ottiene i colori dalla palette dello stile corrente
        colori = self.stili_disponibili[stile]['palette']

        # Crea il grafico a torta
        wedges, texts, autotexts = ax.pie(
            df_dati['potenza'],
            labels=df_dati['nome_mese'],
            autopct='%1.1f%%',
            colors=colori[:len(df_dati)],
            startangle=90,
            # Separa leggermente tutti i settori
            explode=[0.05] * len(df_dati),
            shadow=True,
            textprops={'fontsize': 9, 'fontweight': 'bold'}
        )

        # Personalizza l'aspetto delle etichette percentuali
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)

        # Personalizza l'aspetto delle etichette dei mesi
        for text in texts:
            text.set_fontweight('bold')
            text.set_fontsize(9)

        # Aggiunge una legenda con i valori originali
        legenda_labels = []
        for categoria, valore_orig in zip(df_dati['nome_mese'], df_dati['valore_originale']):
            if isinstance(valore_orig, str) and valore_orig.endswith('%'):
                legenda_labels.append(f'{categoria}: {valore_orig}')
            else:
                # Formatta i numeri senza decimali se sono interi
                if isinstance(valore_orig, (int, float)) and valore_orig == int(valore_orig):
                    legenda_labels.append(f'{categoria}: {int(valore_orig)}')
                else:
                    legenda_labels.append(f'{categoria}: {valore_orig:.1f}')

        ax.legend(wedges, legenda_labels, title="Distribuzione",
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Assicura che il grafico sia circolare
        ax.axis('equal')

    def _personalizza_grafico(self, ax: plt.Axes, titolo: str, label_x: str, label_y: str, tipo_grafico: str = 'barre') -> None:
        """
        Personalizza le etichette e il titolo del grafico
        """
        ax.set_title(titolo, pad=20, fontweight='normal')

        # Per i grafici a torta, non impostiamo etichette per gli assi
        if tipo_grafico != 'torta':
            ax.set_xlabel(label_x, fontweight='normal')
            ax.set_ylabel(label_y, fontweight='normal')
            # Mantieni le etichette dell'asse x orizzontali
            ax.tick_params(axis='x', rotation=0)

            # Evita la notazione scientifica per grandi numeri
            ax.yaxis.set_major_formatter(plt.FuncFormatter(
                lambda x, p: f'{x:,.0f}' if abs(x) >= 1000 else f'{x:g}'))

    def _applica_finiture(self, ax: plt.Axes, stile: str, tipo_grafico: str = 'barre') -> None:
        """
        Applica finiture specifiche in base allo stile
        """
        # Per i grafici a torta, non applichiamo spine o griglie
        if tipo_grafico == 'torta':
            # Rimuove gli assi per i grafici a torta
            ax.axis('off')
            return

        if stile in ['elegante', 'moderno', 'minimal']:
            sns.despine(ax=ax)

        # Migliora la griglia per alcuni stili
        if stile in ['moderno', 'colorato']:
            ax.grid(True, alpha=0.3, axis='y')

        # Aggiunge margini per una migliore visualizzazione
        ax.margins(x=0.05)

    def _salva_grafico(self, fig: plt.Figure, nome_file: str) -> None:
        """
        Salva il grafico in un file
        """
        # Aggiunge estensione se non presente
        if not nome_file.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.svg')):
            nome_file += '.png'

        fig.savefig(nome_file, dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"Grafico salvato come: {nome_file}")

    def crea_grafico_confronto(self,
                               dati_multipli: Dict[str, Dict],
                               titolo: str,
                               label_x: str,
                               label_y: str,
                               stile: str = 'elegante',
                               dimensioni: tuple = (14, 8),
                               unita_misura_tempo: str = 'mesi',
                               salva_file: Optional[str] = None) -> plt.Figure:
        """
        Crea un grafico per confrontare più serie di dati

        Args:
            dati_multipli: Dizionario con chiave il nome della serie e valore i dati
            titolo: Titolo del grafico
            label_x: Etichetta dell'asse X
            label_y: Etichetta dell'asse Y
            stile: Stile del grafico da applicare
            dimensioni: Dimensioni del grafico
            unita_misura_tempo: 'mesi' per conversione a nomi italiani
            salva_file: Nome del file per salvare il grafico (opzionale)

        Returns:
            plt.Figure: Oggetto figura di matplotlib
        """
        # Valida i dati
        for nome_serie, dati in dati_multipli.items():
            if not self._valida_dati(dati, unita_misura_tempo):
                raise ValueError(
                    f"Dati non validi per la serie '{nome_serie}'")

        # Applica lo stile
        self.applica_stile(stile)

        # Prepara i dati combinati
        df_combinato = self._prepara_dataframe_confronto(dati_multipli, unita_misura_tempo)

        # Crea il grafico
        fig, ax = plt.subplots(figsize=dimensioni)

        sns.barplot(data=df_combinato, x='nome_mese', y='potenza', hue='serie', ax=ax)

        # Personalizza
        self._personalizza_grafico(ax, titolo, label_x, label_y, 'barre')
        self._applica_finiture(ax, stile, 'barre')

        # Migliora la legenda
        ax.legend(title='', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Salva il file se richiesto
        if salva_file:
            self._salva_grafico(fig, salva_file)

        plt.tight_layout()
        return fig

    def _prepara_dataframe_confronto(self, dati_multipli: Dict[str, Dict], unita_misura_tempo: str) -> pd.DataFrame:
        """
        Prepara un DataFrame per il confronto di più serie
        """
        righe = []

        for nome_serie, dati in dati_multipli.items():
            # Ordina i dati come nella funzione principale
            if unita_misura_tempo == 'mesi':
                chiavi_ordinate = sorted(dati.keys())
            else:
                try:
                    chiavi_ordinate = sorted(
                        dati.keys(), key=lambda x: float(x))
                except (ValueError, TypeError):
                    chiavi_ordinate = list(dati.keys())

            for chiave in chiavi_ordinate:
                valore = dati[chiave]

                # Converte i valori se necessario
                if isinstance(valore, str) and valore.endswith('%'):
                    valore_numerico = float(valore[:-1])
                else:
                    valore_numerico = float(valore)

                # Converte le chiavi come nella funzione principale
                if unita_misura_tempo == 'mesi':
                    nome_chiave = self.mesi_italiano[chiave]
                else:
                    nome_chiave = str(chiave)

                righe.append({
                    'serie': nome_serie,
                    'potenza': valore_numerico,
                    'nome_mese': nome_chiave
                })

        return pd.DataFrame(righe)
