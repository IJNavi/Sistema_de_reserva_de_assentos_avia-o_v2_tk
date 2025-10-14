#!/usr/bin/env python3
import json
from database.data_manager import DataManager
from entities.voo import Voo
from interface.tk_interface import TkInterface

def inicializar_dados():
    data_manager = DataManager()

    # Configuração de aeronave
    aeronave = {
        'configuracao': [30, 6],  # 30 fileiras, 6 assentos por fileira
        'classes': {
            'primeira': 2,  # Fileiras 1-2: primeira classe
            'executiva': 8,  # Fileiras 3-8: executiva
            'economica': 30  # Fileiras 9-30: econômica
        },
        'fileiras_emergencia': [10, 11]
    }

    # Voos
    if not data_manager.data['voos']:
        voos_exemplo = [
            Voo('AA123', 'GRU', 'JFK', '2024-12-01 08:00', aeronave),
            Voo('BB456', 'GRU', 'LHR', '2024-12-02 14:30', aeronave),
            Voo('CC789', 'GRU', 'CDG', '2024-12-03 20:15', aeronave)
        ]

        for voo in voos_exemplo:
            data_manager.add_voo(voo)

    print("Dados inicializados com sucesso!")

if __name__ == "__main__":
    # Inicializar dados de exemplo
    inicializar_dados()

    # Iniciar interface Tkinter
    app = TkInterface()
    app.iniciar()