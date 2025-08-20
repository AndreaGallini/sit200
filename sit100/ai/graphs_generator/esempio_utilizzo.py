#!/usr/bin/env python3
"""
Esempio di utilizzo della classe Chart_Generator
Mostra come creare grafici personalizzati con dati vari
"""

import matplotlib.pyplot as plt
from chart_generator import Chart_Generator
import matplotlib
# Usa il backend non-GUI per evitare problemi con i thread
matplotlib.use('Agg')


def main():
    # Inizializza il generatore di grafici
    generatore = Chart_Generator()

    # Mostra gli stili disponibili
    print("Stili disponibili:")
    for stile in generatore.ottieni_stili_disponibili():
        print(f"- {stile}")
    print()

    # Dati di esempio - potenza mensile in kW
    dati_potenza_2023 = {
        1: 450,   # Gennaio
        2: 380,   # Febbraio
        3: 520,   # Marzo
        4: 490,   # Aprile
        5: 610,   # Maggio
        6: 780,   # Giugno
        7: 850,   # Luglio
        8: 820,   # Agosto
        9: 670,   # Settembre
        10: 540,  # Ottobre
        11: 420,  # Novembre
        12: 390   # Dicembre
    }

    dati_potenza_2023_ori = {
        'Gen': 450,   # Gennaio
        'Feb': 380,   # Febbraio
        'Mar': 520,   # Marzo
        'Apr': 490,   # Aprile
        'Mag': 610,   # Maggio
        'Giu': 780,   # Giugno
        'Lug': 850,   # Luglio
        'Ago': 820,   # Agosto
        'Sett': 670,   # Settembre
        'Ott': 540,  # Ottobre
        'Nov': 420,  # Novembre
        'Dic': 390   # Dicembre
    }
    dati_potenza_2024 = {
        1: 400,   # Gennaio
        2: 383,   # Febbraio
        3: 400,   # Marzo
        4: 690,   # Aprile
        5: 660,   # Maggio
        6: 580,   # Giugno
        7: 350,   # Luglio
        8: 220,   # Agosto
        9: 970,   # Settembre
        10: 340,  # Ottobre
        11: 220,  # Novembre
        12: 190   # Dicembre
    }

    dati_campo_2023 = {
        'campo 1': '14%',
        'campo 2': '86%'
    }

    dati_su_anni = {
        1: -1000000,
        2: -50000,
        3: -20000,
        4: -10000,
        5: -5000,
        6: 0,
        7: 1000,
        8: 100000,
        9: 200000,
        10: 300000,
        11: 1000000
    }

    print("\n=== ESEMPIO 1: Salvataggio del grafico ===")
    fig1 = generatore.crea_grafico(
        dati=dati_potenza_2023,
        titolo="Grafico Salvato - Produzione 2023",
        label_x="Mese",
        label_y="Potenza (kW)",
        stile="moderno",
        tipo_grafico="barre",
        unita_misura_tempo='mesi',
        salva_file="output_chart/grafico_potenza_2023.png"
    )

    print("\n=== ESEMPIO 2: Grafico a linee con stile moderno ===")
    fig2 = generatore.crea_grafico(
        dati=dati_potenza_2023,
        titolo="Trend Energetico Mensile",
        label_x="Periodo",
        label_y="Energia Prodotta (kW)",
        stile="moderno",
        tipo_grafico="linee",
        unita_misura_tempo='mesi',
        dimensioni=(14, 7),
        salva_file="output_chart/grafico_potenza_2023_linee.png"
    )

    print("\n=== ESEMPIO 3: Grafico a torta con stile colorato ===")
    fig3 = generatore.crea_grafico(
        dati=dati_campo_2023,
        titolo="Distribuzione Percentuale Potenza 2023",
        label_x="Mese",
        label_y="Potenza (%)",
        stile="colorato",
        tipo_grafico="torta",
        dimensioni=(10, 8),
        salva_file="output_chart/grafico_potenza_2023_torta.png"
    )

    print("\n=== ESEMPIO 4: Valore su anni (senza mesi) ===")
    fig4 = generatore.crea_grafico(
        dati=dati_su_anni,
        titolo="Valore del progetto",
        label_x="Anni",
        label_y="Euro",
        stile="moderno",
        tipo_grafico="barre",
        salva_file="output_chart/valore_progetto.png"
    )

    # Esempio con dati di confronto
    print("\n=== ESEMPIO 5: Confronto tra anni ===")
    dati_confronto = {
        '2022': {1: 400, 2: 350, 3: 480, 4: 450, 5: 580, 6: 720},
        '2023': {1: 450, 2: 380, 3: 520, 4: 490, 5: 610, 6: 780}
    }

    fig5 = generatore.crea_grafico_confronto(
        dati_multipli=dati_confronto,
        titolo="Confronto Produzione 2022 vs 2023",
        label_x="Mese",
        label_y="Potenza (kW)",
        stile="elegante",
        unita_misura_tempo='mesi',
        salva_file="output_chart/confronto_produzione.png"
    )

    print("\n=== ESEMPIO 6: Barre orizzontali ===")
    fig6 = generatore.crea_grafico(
        dati=dati_potenza_2023_ori,
        titolo="Produzione Energetica 2023 - Barre Orizzontali",
        label_x="Potenza (kW)",
        label_y="Mese",
        stile="elegante",
        tipo_grafico="barre_orizzontali",
        # Nessuna conversione (chiavi già in forma testuale)
        unita_misura_tempo='',
        dimensioni=(12, 8),
        salva_file="output_chart/grafico_barre_orizzontali.png"
    )

    print("\n=== Tutti i grafici creati con successo! ===")


if __name__ == "__main__":
    main()
