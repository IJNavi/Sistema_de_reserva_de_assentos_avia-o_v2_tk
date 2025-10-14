import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import logging
from database.data_manager import DataManager
from utils.logger import Logger
from utils.validators import validar_cpf, validar_email, calcular_idade
from entities.passageiro import Passageiro
from entities.voo import Voo


class TkInterface:
    def __init__(self):
        self.data_manager = DataManager()
        self.logger = Logger()
        self.usuario_logado = None
        self.lock = threading.Lock()

        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Reservas Aéreas")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Inicializar frames
        self.criar_frame_login()
        self.criar_frame_menu()
        self.criar_frame_voos()
        self.criar_frame_assentos()
        self.criar_frame_reserva()

        # Mostrar frame inicial
        self.mostrar_frame("login")

    def iniciar(self):
        self.root.mainloop()

    def criar_frame_login(self):
        self.frame_login = ttk.Frame(self.frame_principal)

        ttk.Label(self.frame_login, text="Sistema de Reservas Aéreas",
                  font=('Arial', 16, 'bold')).pack(pady=20)

        # Frame de cadastro
        frame_cadastro = ttk.LabelFrame(self.frame_login, text="Cadastro", padding=10)
        frame_cadastro.pack(fill=tk.X, pady=10)

        ttk.Label(frame_cadastro, text="CPF:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_cpf_cadastro = ttk.Entry(frame_cadastro, width=20)
        self.entry_cpf_cadastro.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(frame_cadastro, text="Nome:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_nome = ttk.Entry(frame_cadastro, width=20)
        self.entry_nome.grid(row=1, column=1, pady=2, padx=5)

        ttk.Label(frame_cadastro, text="Data Nasc. (DD/MM/AAAA):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_data_nasc = ttk.Entry(frame_cadastro, width=20)
        self.entry_data_nasc.grid(row=2, column=1, pady=2, padx=5)

        ttk.Label(frame_cadastro, text="E-mail:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.entry_email = ttk.Entry(frame_cadastro, width=20)
        self.entry_email.grid(row=3, column=1, pady=2, padx=5)

        ttk.Button(frame_cadastro, text="Cadastrar",
                   command=self.cadastrar_passageiro).grid(row=4, column=1, pady=10, sticky=tk.E)

        # Frame de login
        frame_login = ttk.LabelFrame(self.frame_login, text="Login", padding=10)
        frame_login.pack(fill=tk.X, pady=10)

        ttk.Label(frame_login, text="CPF:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_cpf_login = ttk.Entry(frame_login, width=20)
        self.entry_cpf_login.grid(row=0, column=1, pady=2, padx=5)

        ttk.Button(frame_login, text="Login",
                   command=self.login).grid(row=1, column=1, pady=10, sticky=tk.E)

    def criar_frame_menu(self):
        self.frame_menu = ttk.Frame(self.frame_principal)

        ttk.Label(self.frame_menu, text="Bem-vindo, ",
                  font=('Arial', 14, 'bold')).pack(pady=10)
        self.label_nome_usuario = ttk.Label(self.frame_menu, text="", font=('Arial', 12))
        self.label_nome_usuario.pack(pady=5)

        botoes = [
            ("Visualizar Voos", self.visualizar_voos),
            ("Visualizar Assentos", self.visualizar_assentos_menu),
            ("Fazer Reserva", self.fazer_reserva_menu),
            ("Cancelar Reserva", self.cancelar_reserva_menu),
            ("Modificar Reserva", self.modificar_reserva_menu),
            ("Logout", self.logout)
        ]

        for texto, comando in botoes:
            ttk.Button(self.frame_menu, text=texto, command=comando, width=20).pack(pady=5)

    def criar_frame_voos(self):
        self.frame_voos = ttk.Frame(self.frame_principal)

        ttk.Label(self.frame_voos, text="Voos Disponíveis",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        # Treeview para voos
        colunas = ('Número', 'Origem', 'Destino', 'Data/Hora')
        self.tree_voos = ttk.Treeview(self.frame_voos, columns=colunas, show='headings', height=10)

        for col in colunas:
            self.tree_voos.heading(col, text=col)
            self.tree_voos.column(col, width=150)

        self.tree_voos.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(self.frame_voos, text="Voltar",
                   command=lambda: self.mostrar_frame("menu")).pack(pady=10)

    def criar_frame_assentos(self):
        self.frame_assentos = ttk.Frame(self.frame_principal)

        ttk.Label(self.frame_assentos, text="Selecionar Voo",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(self.frame_assentos, text="Número do Voo:").pack()
        self.entry_voo_assentos = ttk.Entry(self.frame_assentos, width=10)
        self.entry_voo_assentos.pack(pady=5)

        ttk.Button(self.frame_assentos, text="Visualizar Assentos",
                   command=self.visualizar_assentos).pack(pady=5)

        # Frame para mapa de assentos
        self.frame_mapa_assentos = ttk.Frame(self.frame_assentos)
        self.frame_mapa_assentos.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Button(self.frame_assentos, text="Voltar",
                   command=lambda: self.mostrar_frame("menu")).pack(pady=10)

    def criar_frame_reserva(self):
        self.frame_reserva = ttk.Frame(self.frame_principal)

        ttk.Label(self.frame_reserva, text="Fazer Reserva",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(self.frame_reserva, text="Número do Voo:").pack()
        self.entry_voo_reserva = ttk.Entry(self.frame_reserva, width=10)
        self.entry_voo_reserva.pack(pady=5)

        ttk.Button(self.frame_reserva, text="Selecionar Assento",
                   command=self.selecionar_assento_reserva).pack(pady=5)

        ttk.Button(self.frame_reserva, text="Voltar",
                   command=lambda: self.mostrar_frame("menu")).pack(pady=10)

    def mostrar_frame(self, nome_frame):
        frames = {
            "login": self.frame_login,
            "menu": self.frame_menu,
            "voos": self.frame_voos,
            "assentos": self.frame_assentos,
            "reserva": self.frame_reserva
        }

        for frame in frames.values():
            frame.pack_forget()

        frames[nome_frame].pack(fill=tk.BOTH, expand=True)

    def cadastrar_passageiro(self):
        cpf = self.entry_cpf_cadastro.get()
        nome = self.entry_nome.get()
        data_nascimento = self.entry_data_nasc.get()
        email = self.entry_email.get()

        cpf_validado = validar_cpf(cpf)
        if not cpf_validado:
            messagebox.showerror("Erro", "CPF inválido!")
            return

        if self.data_manager.get_passageiro(cpf_validado):
            messagebox.showerror("Erro", "CPF já cadastrado!")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return

        passageiro = Passageiro(cpf_validado, nome, data_nascimento, email)
        self.data_manager.add_passageiro(passageiro)
        self.logger.log(logging.INFO, f"Novo passageiro cadastrado: {nome}", cpf_validado)

        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

        # Limpar campos
        self.entry_cpf_cadastro.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_data_nasc.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def login(self):
        cpf = self.entry_cpf_login.get()
        cpf_validado = validar_cpf(cpf)

        if not cpf_validado:
            messagebox.showerror("Erro", "CPF inválido!")
            return

        passageiro_data = self.data_manager.get_passageiro(cpf_validado)
        if not passageiro_data:
            messagebox.showerror("Erro", "Passageiro não encontrado!")
            return

        self.usuario_logado = Passageiro.from_dict(passageiro_data)
        self.logger.log(logging.INFO, "Login realizado", self.usuario_logado.cpf)

        # Atualizar nome no menu
        self.label_nome_usuario.config(text=self.usuario_logado.nome)

        self.mostrar_frame("menu")
        self.entry_cpf_login.delete(0, tk.END)

    def logout(self):
        self.logger.log(logging.INFO, "Logout", self.usuario_logado.cpf)
        self.usuario_logado = None
        self.mostrar_frame("login")

    def visualizar_voos(self):
        # Limpar treeview
        for item in self.tree_voos.get_children():
            self.tree_voos.delete(item)

        # Popular com voos
        voos = self.data_manager.data['voos']
        for numero, voo_data in voos.items():
            self.tree_voos.insert('', tk.END, values=(
                numero,
                voo_data['origem'],
                voo_data['destino'],
                voo_data['data_hora']
            ))

        self.mostrar_frame("voos")

    def visualizar_assentos_menu(self):
        self.mostrar_frame("assentos")

    def visualizar_assentos(self):
        numero_voo = self.entry_voo_assentos.get()
        voo_data = self.data_manager.get_voo(numero_voo)

        if not voo_data:
            messagebox.showerror("Erro", "Voo não encontrado!")
            return

        voo = Voo.from_dict(voo_data)
        self.mostrar_mapa_assentos_tk(voo)

    def mostrar_mapa_assentos_tk(self, voo):
        # Limpar frame do mapa
        for widget in self.frame_mapa_assentos.winfo_children():
            widget.destroy()

        ttk.Label(self.frame_mapa_assentos,
                  text=f"Mapa de Assentos - Voo {voo.numero}",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        # Legenda
        legenda_frame = ttk.Frame(self.frame_mapa_assentos)
        legenda_frame.pack(pady=5)

        ttk.Label(legenda_frame, text="Legenda:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(legenda_frame, text="[ ] Disponível  [X] Ocupado  [*] Sua reserva  [E] Emergência").grid(row=0,
                                                                                                           column=1,
                                                                                                           sticky=tk.W)
        ttk.Label(legenda_frame, text="Classe: P=Primeira  X=Executiva  C=Econômica").grid(row=1, column=1, sticky=tk.W)
        ttk.Label(legenda_frame, text="Posição: J=Janela  M=Meio  C=Corredor").grid(row=2, column=1, sticky=tk.W)

        # Container para o mapa com scrollbar
        container = ttk.Frame(self.frame_mapa_assentos)
        container.pack(fill=tk.BOTH, expand=True, pady=10)

        canvas = tk.Canvas(container, bg='white')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cabeçalho com letras
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(pady=5)

        ttk.Label(header_frame, text="", width=4).pack(side=tk.LEFT)
        for letra in 'ABCDEF':
            ttk.Label(header_frame, text=letra, width=6, anchor=tk.CENTER).pack(side=tk.LEFT)

        # Mapa de assentos
        fileiras = sorted(set(int(num[:-1]) for num in voo.assentos.keys()))

        for fileira in fileiras:
            fileira_frame = ttk.Frame(scrollable_frame)
            fileira_frame.pack(pady=2)

            # Número da fileira
            ttk.Label(fileira_frame, text=f"{fileira:2d}", width=4).pack(side=tk.LEFT)

            for letra in 'ABCDEF':
                numero_assento = f"{fileira}{letra}"
                assento = voo.assentos[numero_assento]

                # Determinar cor e texto do botão
                if assento.passageiro_cpf == self.usuario_logado.cpf:
                    texto = "[*]"
                    cor = 'lightgreen'
                elif not assento.disponivel:
                    texto = "[X]"
                    cor = 'lightcoral'
                elif assento.emergencia:
                    texto = "[E]"
                    cor = 'lightyellow'
                else:
                    texto = "[ ]"
                    cor = 'lightblue'

                # Botão do assento
                btn = tk.Button(fileira_frame, text=texto, width=6, height=1,
                                bg=cor, relief='raised', borderwidth=1,
                                command=lambda num=numero_assento: self.mostrar_info_assento(num, voo))
                btn.pack(side=tk.LEFT, padx=1)

            # Linha de informações
            info_frame = ttk.Frame(scrollable_frame)
            info_frame.pack(pady=2)

            ttk.Label(info_frame, text="", width=4).pack(side=tk.LEFT)

            for letra in 'ABCDEF':
                numero_assento = f"{fileira}{letra}"
                assento = voo.assentos[numero_assento]

                if assento.disponivel:
                    # Classe: P=Primeira, X=Executiva, C=Econômica
                    if assento.classe == 'primeira':
                        classe_char = 'P'
                    elif assento.classe == 'executiva':
                        classe_char = 'X'
                    else:
                        classe_char = 'C'

                    # Posição: J=Janela, M=Meio, C=Corredor
                    posicao_char = assento.posicao[0].upper()

                    info_text = f"{classe_char}{posicao_char}${assento.valor:.0f}"
                    ttk.Label(info_frame, text=info_text, width=6, anchor=tk.CENTER,
                              font=('Arial', 7)).pack(side=tk.LEFT)
                else:
                    ttk.Label(info_frame, text="", width=6).pack(side=tk.LEFT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def mostrar_info_assento(self, numero_assento, voo):
        assento = voo.assentos[numero_assento]

        info = f"Assento: {numero_assento}\n"
        info += f"Classe: {assento.classe.title()}\n"
        info += f"Posição: {assento.posicao.title()}\n"
        info += f"Valor: R$ {assento.valor:.2f}\n"
        info += f"Emergência: {'Sim' if assento.emergencia else 'Não'}\n"
        info += f"Disponível: {'Sim' if assento.disponivel else 'Não'}"

        if not assento.disponivel:
            info += f"\nReservado por: {assento.passageiro_cpf}"

        messagebox.showinfo("Informações do Assento", info)

    def fazer_reserva_menu(self):
        self.mostrar_frame("reserva")

    def selecionar_assento_reserva(self):
        numero_voo = self.entry_voo_reserva.get()
        voo_data = self.data_manager.get_voo(numero_voo)

        if not voo_data:
            messagebox.showerror("Erro", "Voo não encontrado!")
            return

        # Verificar se já tem reserva
        if self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo):
            messagebox.showerror("Erro", "Você já possui uma reserva neste voo!")
            return

        voo = Voo.from_dict(voo_data)
        self.abrir_janela_selecao_assento(voo, "reservar")

    def cancelar_reserva_menu(self):
        numero_voo = simpledialog.askstring("Cancelar Reserva", "Número do voo:")
        if not numero_voo:
            return

        reserva = self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo)
        if not reserva:
            messagebox.showerror("Erro", "Reserva não encontrada!")
            return

        voo_data = self.data_manager.get_voo(numero_voo)
        voo = Voo.from_dict(voo_data)
        assento = voo.assentos[reserva['numero_assento']]

        with self.lock:
            assento.liberar()
            self.data_manager.remove_reserva(self.usuario_logado.cpf, numero_voo)
            self.data_manager.add_voo(voo)

            self.logger.log(logging.INFO,
                            f"Reserva cancelada - Voo: {numero_voo}, Assento: {reserva['numero_assento']}",
                            self.usuario_logado.cpf)

            messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")

    def modificar_reserva_menu(self):
        numero_voo = simpledialog.askstring("Modificar Reserva", "Número do voo:")
        if not numero_voo:
            return

        reserva = self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo)
        if not reserva:
            messagebox.showerror("Erro", "Reserva não encontrada!")
            return

        voo_data = self.data_manager.get_voo(numero_voo)
        voo = Voo.from_dict(voo_data)

        # Cancela reserva atual
        assento_antigo = voo.assentos[reserva['numero_assento']]

        with self.lock:
            assento_antigo.liberar()

            # Abre janela para selecionar novo assento
            self.abrir_janela_selecao_assento(voo, "modificar", numero_voo)

    def abrir_janela_selecao_assento(self, voo, operacao, numero_voo=None):
        janela = tk.Toplevel(self.root)
        janela.title(f"Selecionar Assento - Voo {voo.numero}")
        janela.geometry("600x500")

        ttk.Label(janela, text=f"Selecione um assento para {operacao}",
                  font=('Arial', 12, 'bold')).pack(pady=10)

        # Container com scrollbar
        container = ttk.Frame(janela)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg='white')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cabeçalho
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(pady=5)

        ttk.Label(header_frame, text="", width=4).pack(side=tk.LEFT)
        for letra in 'ABCDEF':
            ttk.Label(header_frame, text=letra, width=8, anchor=tk.CENTER).pack(side=tk.LEFT)

        # Assentos
        fileiras = sorted(set(int(num[:-1]) for num in voo.assentos.keys()))

        for fileira in fileiras:
            fileira_frame = ttk.Frame(scrollable_frame)
            fileira_frame.pack(pady=2)

            ttk.Label(fileira_frame, text=f"{fileira:2d}", width=4).pack(side=tk.LEFT)

            for letra in 'ABCDEF':
                numero_assento = f"{fileira}{letra}"
                assento = voo.assentos[numero_assento]

                # Configurar botão baseado na disponibilidade
                if not assento.disponivel:
                    texto = "[X]"
                    cor = 'lightcoral'
                    estado = 'disabled'
                elif assento.emergencia and calcular_idade(self.usuario_logado.data_nascimento) < 18:
                    texto = "[E]"
                    cor = 'lightyellow'
                    estado = 'disabled'
                else:
                    texto = "[ ]"
                    cor = 'lightgreen'
                    estado = 'normal'

                btn = tk.Button(fileira_frame, text=texto, width=8, height=2,
                                bg=cor, state=estado,
                                command=lambda num=numero_assento: self.processar_selecao_assento(
                                    num, voo, operacao, numero_voo, janela))
                btn.pack(side=tk.LEFT, padx=1)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(janela, text="Cancelar", command=janela.destroy).pack(pady=10)

    def processar_selecao_assento(self, numero_assento, voo, operacao, numero_voo, janela):
        assento = voo.assentos[numero_assento]

        # Verificar restrições
        if assento.emergencia:
            idade = calcular_idade(self.usuario_logado.data_nascimento)
            if idade < 18:
                messagebox.showerror("Erro", "Menores de 18 anos não podem reservar assentos de emergência!")
                return

        with self.lock:
            if not assento.disponivel:
                messagebox.showerror("Erro", "Assento já ocupado!")
                return

            # Fazer reserva
            assento.reservar(self.usuario_logado.cpf)
            self.data_manager.add_reserva(self.usuario_logado.cpf, voo.numero, numero_assento)
            self.data_manager.add_voo(voo)

            if operacao == "reservar":
                mensagem = f"Reserva realizada - Voo: {voo.numero}, Assento: {numero_assento}"
                titulo = "Reserva Realizada"
            else:  # modificar
                mensagem = f"Reserva modificada - De: antigo Para: {numero_assento}"
                titulo = "Reserva Modificada"

            self.logger.log(logging.INFO, mensagem, self.usuario_logado.cpf)

            messagebox.showinfo(titulo, "Operação realizada com sucesso!")
            janela.destroy()
            self.mostrar_frame("menu")