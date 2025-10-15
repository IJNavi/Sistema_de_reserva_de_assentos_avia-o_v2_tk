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
        self.assento_selecionado = None
        self.voo_selecionado = None
        self.modo_operacao = None  # 'reservar', 'modificar', 'cancelar'
        self.modo_modificacao = False
        self.reserva_antiga_assento = None

        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Reservas Aéreas")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Inicializar frames
        self.criar_frame_login()
        self.criar_frame_menu()
        self.criar_frame_assentos_centralizado()

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

        # Header com informações do usuário
        header_frame = ttk.Frame(self.frame_menu)
        header_frame.pack(pady=10, fill=tk.X)

        ttk.Label(header_frame, text="Bem-vindo, ",
                  font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        self.label_nome_usuario = ttk.Label(header_frame, text="", font=('Arial', 14, 'bold'))
        self.label_nome_usuario.pack(side=tk.LEFT)

        # Frame de informações do usuário
        info_frame = ttk.LabelFrame(self.frame_menu, text="Seus Dados", padding=10)
        info_frame.pack(fill=tk.X, pady=10)

        self.label_info_cpf = ttk.Label(info_frame, text="CPF: ")
        self.label_info_cpf.pack(anchor=tk.W)

        self.label_info_email = ttk.Label(info_frame, text="E-mail: ")
        self.label_info_email.pack(anchor=tk.W)

        self.label_info_nascimento = ttk.Label(info_frame, text="Data de Nascimento: ")
        self.label_info_nascimento.pack(anchor=tk.W)

        # Botões de ação (APENAS OS ESSENCIAIS)
        botoes_frame = ttk.Frame(self.frame_menu)
        botoes_frame.pack(pady=20)

        botoes = [
            ("Visualizar Voos", self.visualizar_voos),
            ("Reserva de Assentos", self.visualizar_assentos_menu),
            ("Logout", self.logout)
        ]

        for texto, comando in botoes:
            ttk.Button(botoes_frame, text=texto, command=comando, width=20).pack(pady=5)

    def criar_frame_assentos_centralizado(self):
        self.frame_assentos = ttk.Frame(self.frame_principal)

        # Header com controles
        header_frame = ttk.Frame(self.frame_assentos)
        header_frame.pack(fill=tk.X, pady=10)

        ttk.Label(header_frame, text="Selecionar Voo",
                  font=('Arial', 14, 'bold')).pack(side=tk.LEFT)

        # Controles de voo
        controles_frame = ttk.Frame(header_frame)
        controles_frame.pack(side=tk.RIGHT)

        ttk.Label(controles_frame, text="Número do Voo:").pack(side=tk.LEFT)
        self.entry_voo_assentos = ttk.Entry(controles_frame, width=10)
        self.entry_voo_assentos.pack(side=tk.LEFT, padx=5)

        ttk.Button(controles_frame, text="Carregar Assentos",
                   command=self.carregar_assentos).pack(side=tk.LEFT, padx=5)

        # Frame de operações
        self.frame_operacoes = ttk.LabelFrame(self.frame_assentos, text="Operações", padding=10)
        self.frame_operacoes.pack(fill=tk.X, pady=10)

        self.label_operacao = ttk.Label(self.frame_operacoes, text="Selecione um assento para operar",
                                        font=('Arial', 10))
        self.label_operacao.pack()

        botoes_operacao_frame = ttk.Frame(self.frame_operacoes)
        botoes_operacao_frame.pack(pady=5)

        self.btn_reservar = ttk.Button(botoes_operacao_frame, text="Reservar Assento",
                                       command=self.reservar_assento, state='disabled')
        self.btn_reservar.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar = ttk.Button(botoes_operacao_frame, text="Cancelar Reserva",
                                       command=self.cancelar_reserva, state='disabled')
        self.btn_cancelar.pack(side=tk.LEFT, padx=5)

        self.btn_modificar = ttk.Button(botoes_operacao_frame, text="Modificar Reserva",
                                        command=self.modificar_reserva, state='disabled')
        self.btn_modificar.pack(side=tk.LEFT, padx=5)

        # Frame para mapa de assentos
        self.frame_mapa_assentos = ttk.Frame(self.frame_assentos)
        self.frame_mapa_assentos.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Button(self.frame_assentos, text="Voltar ao Menu",
                   command=self.voltar_ao_menu).pack(pady=10)

    def atualizar_info_usuario(self):
        """Atualiza as informações do usuário no menu"""
        if self.usuario_logado:
            self.label_nome_usuario.config(text=self.usuario_logado.nome)
            self.label_info_cpf.config(text=f"CPF: {self.usuario_logado.cpf}")
            self.label_info_email.config(text=f"E-mail: {self.usuario_logado.email}")
            self.label_info_nascimento.config(text=f"Data de Nascimento: {self.usuario_logado.data_nascimento}")

    def mostrar_frame(self, nome_frame):
        frames = {
            "login": self.frame_login,
            "menu": self.frame_menu,
            "assentos": self.frame_assentos
        }

        for frame in frames.values():
            frame.pack_forget()

        frames[nome_frame].pack(fill=tk.BOTH, expand=True)

        if nome_frame == "menu":
            self.atualizar_info_usuario()

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

        self.mostrar_frame("menu")
        self.entry_cpf_login.delete(0, tk.END)

    def logout(self):
        self.logger.log(logging.INFO, "Logout", self.usuario_logado.cpf)
        self.usuario_logado = None
        self.mostrar_frame("login")

    def visualizar_voos(self):
        voos = self.data_manager.data['voos']
        info_voos = "Voos Disponíveis:\n\n"
        for numero, voo_data in voos.items():
            info_voos += f"Voo {numero}: {voo_data['origem']} -> {voo_data['destino']} - {voo_data['data_hora']}\n"

        messagebox.showinfo("Voos Disponíveis", info_voos)

    def visualizar_assentos_menu(self):
        self.mostrar_frame("assentos")
        self.limpar_selecao()

    def carregar_assentos(self):
        numero_voo = self.entry_voo_assentos.get()
        voo_data = self.data_manager.get_voo(numero_voo)

        if not voo_data:
            messagebox.showerror("Erro", "Voo não encontrado!")
            return

        self.voo_selecionado = Voo.from_dict(voo_data)

        # Verificar se usuário tem reserva neste voo e atualizar botões
        reserva_usuario = self.data_manager.get_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)
        if reserva_usuario:
            self.btn_cancelar.config(state='normal')
            self.btn_modificar.config(state='normal')
        else:
            self.btn_cancelar.config(state='disabled')
            self.btn_modificar.config(state='disabled')

        self.mostrar_mapa_assentos_tk(self.voo_selecionado)

    def mostrar_mapa_assentos_tk(self, voo):
        # Limpar frame do mapa
        for widget in self.frame_mapa_assentos.winfo_children():
            widget.destroy()

        ttk.Label(self.frame_mapa_assentos,
                  text=f"Mapa de Assentos - Voo {voo.numero}",
                  font=('Arial', 12, 'bold')).pack(pady=5)

        # Legenda melhorada
        legenda_frame = ttk.Frame(self.frame_mapa_assentos)
        legenda_frame.pack(pady=5)

        # Legenda em grid para melhor organização
        ttk.Label(legenda_frame, text="Legenda:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(legenda_frame, text="[ ] Disponível", font=('Arial', 8)).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(legenda_frame, text="[X] Ocupado", font=('Arial', 8)).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(legenda_frame, text="[*] Sua reserva", font=('Arial', 8)).grid(row=3, column=0, sticky=tk.W)
        ttk.Label(legenda_frame, text="[E] Emergência", font=('Arial', 8)).grid(row=4, column=0, sticky=tk.W)

        ttk.Label(legenda_frame, text="Classe:", font=('Arial', 9, 'bold')).grid(row=0, column=1, sticky=tk.W,
                                                                                 padx=(20, 0))
        ttk.Label(legenda_frame, text="P = Primeira", font=('Arial', 8)).grid(row=1, column=1, sticky=tk.W,
                                                                              padx=(20, 0))
        ttk.Label(legenda_frame, text="X = Executiva", font=('Arial', 8)).grid(row=2, column=1, sticky=tk.W,
                                                                               padx=(20, 0))
        ttk.Label(legenda_frame, text="C = Econômica", font=('Arial', 8)).grid(row=3, column=1, sticky=tk.W,
                                                                               padx=(20, 0))

        ttk.Label(legenda_frame, text="Posição:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W,
                                                                                  padx=(20, 0))
        ttk.Label(legenda_frame, text="J = Janela", font=('Arial', 8)).grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Label(legenda_frame, text="M = Meio", font=('Arial', 8)).grid(row=2, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Label(legenda_frame, text="C = Corredor", font=('Arial', 8)).grid(row=3, column=2, sticky=tk.W,
                                                                              padx=(20, 0))

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

        # Cabeçalho com letras (mais espaço)
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(pady=5)

        ttk.Label(header_frame, text="", width=4).pack(side=tk.LEFT)
        for letra in 'ABCDEF':
            ttk.Label(header_frame, text=letra, width=8, anchor=tk.CENTER).pack(side=tk.LEFT)

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
                btn = tk.Button(fileira_frame, text=texto, width=8, height=2,
                                bg=cor, relief='raised', borderwidth=1,
                                command=lambda num=numero_assento, a=assento: self.selecionar_assento(num, a))
                btn.pack(side=tk.LEFT, padx=1)

            # Linha de informações (MAIS ESPAÇO)
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

                    # Formatação melhorada para evitar corte
                    info_text = f"{classe_char}{posicao_char} R${assento.valor:.0f}"
                    ttk.Label(info_frame, text=info_text, width=10, anchor=tk.CENTER,
                              font=('Arial', 8)).pack(side=tk.LEFT)
                else:
                    ttk.Label(info_frame, text="", width=10).pack(side=tk.LEFT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def selecionar_assento(self, numero_assento, assento):
        """Seleciona um assento e atualiza a interface"""
        self.assento_selecionado = assento
        self.numero_assento_selecionado = numero_assento

        # Verificar se usuário já tem reserva neste voo
        tem_reserva_neste_voo = self.data_manager.get_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)
        minha_reserva_atual = tem_reserva_neste_voo['numero_assento'] if tem_reserva_neste_voo else None

        # Atualizar label de operação
        info_assento = f"Assento {numero_assento} selecionado - "
        info_assento += f"{assento.classe.title()} - {assento.posicao.title()} - R$ {assento.valor:.2f}"

        if tem_reserva_neste_voo:
            info_assento += f" | Sua reserva atual: {minha_reserva_atual}"

        self.label_operacao.config(text=info_assento)

        # LÓGICA CORRIGIDA: Habilitar/desabilitar botões
        if self.modo_modificacao:
            # Modo modificação ativo - só pode clicar em assentos disponíveis
            if assento.disponivel and numero_assento != minha_reserva_atual:
                # Assento disponível e não é a reserva atual - mostrar popup de modificação
                self.mostrar_popup_modificacao(numero_assento, assento, minha_reserva_atual)
            else:
                # Não fazer nada se clicar em assento ocupado ou na própria reserva
                return
        else:
            # Modo normal
            if tem_reserva_neste_voo:
                # Usuário JÁ TEM reserva neste voo
                if numero_assento == minha_reserva_atual:
                    # Selecionou a própria reserva - pode cancelar ou modificar
                    self.btn_reservar.config(state='disabled')
                    self.btn_cancelar.config(state='normal')
                    self.btn_modificar.config(state='normal')
                else:
                    # Selecionou outro assento - nenhuma operação permitida (já tem reserva)
                    self.btn_reservar.config(state='disabled')
                    self.btn_cancelar.config(state='disabled')
                    self.btn_modificar.config(state='disabled')
            else:
                # Usuário NÃO TEM reserva neste voo
                if assento.disponivel:
                    # Assento disponível - pode reservar
                    self.btn_reservar.config(state='normal')
                    self.btn_cancelar.config(state='disabled')
                    self.btn_modificar.config(state='disabled')
                else:
                    # Assento ocupado - nenhuma operação
                    self.btn_reservar.config(state='disabled')
                    self.btn_cancelar.config(state='disabled')
                    self.btn_modificar.config(state='disabled')

    def limpar_selecao(self):
        """Limpa a seleção atual"""
        self.assento_selecionado = None
        self.numero_assento_selecionado = None
        self.voo_selecionado = None
        self.modo_modificacao = False
        self.reserva_antiga_assento = None
        self.label_operacao.config(text="Selecione um assento para operar")
        self.btn_reservar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_modificar.config(state='disabled')
        self.limpar_mapa_assentos()

    def limpar_mapa_assentos(self):
        """Limpa o mapa de assentos da tela"""
        for widget in self.frame_mapa_assentos.winfo_children():
            widget.destroy()

    def reservar_assento(self):
        """Processa a reserva de assento com confirmação de pagamento"""
        if not self.assento_selecionado or not self.voo_selecionado:
            messagebox.showerror("Erro", "Selecione um assento primeiro!")
            return

        # VERIFICAÇÃO CORRIGIDA: Usuário já tem reserva?
        if self.data_manager.get_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero):
            messagebox.showerror("Erro", "Reserva já realizada! Você só pode ter uma reserva por voo.")
            return

        if not self.assento_selecionado.disponivel:
            messagebox.showerror("Erro", "Assento já ocupado!")
            return

        # Verificar restrição de idade para emergência
        if self.assento_selecionado.emergencia:
            idade = calcular_idade(self.usuario_logado.data_nascimento)
            if idade < 18:
                messagebox.showerror("Erro", "Menores de 18 anos não podem reservar assentos de emergência!")
                return

        # Mostrar popup de confirmação de pagamento
        self.mostrar_popup_pagamento()

    def mostrar_popup_pagamento(self):
        """Mostra popup de confirmação de pagamento"""
        popup = tk.Toplevel(self.root)
        popup.title("Confirmação de Pagamento")
        popup.geometry("400x200")
        popup.transient(self.root)
        popup.grab_set()

        # Centralizar popup
        popup.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

        # Conteúdo do popup
        ttk.Label(popup, text="Confirmação de Pagamento",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        info_text = f"Assento: {self.numero_assento_selecionado}\n"
        info_text += f"Tipo: {self.assento_selecionado.classe.title()} - {self.assento_selecionado.posicao.title()}\n"
        info_text += f"Valor: R$ {self.assento_selecionado.valor:.2f}\n\n"
        info_text += "Deseja confirmar o pagamento?"

        ttk.Label(popup, text=info_text, justify=tk.CENTER).pack(pady=10)

        # Frame dos botões
        botoes_frame = ttk.Frame(popup)
        botoes_frame.pack(pady=10)

        ttk.Button(botoes_frame, text="Confirmar Pagamento",
                   command=lambda: self.confirmar_pagamento(popup)).pack(side=tk.LEFT, padx=5)

        ttk.Button(botoes_frame, text="Cancelar",
                   command=popup.destroy).pack(side=tk.LEFT, padx=5)

    def confirmar_pagamento(self, popup):
        """Confirma o pagamento e realiza a reserva"""
        with self.lock:
            # Fazer reserva
            self.assento_selecionado.reservar(self.usuario_logado.cpf)
            self.data_manager.add_reserva(self.usuario_logado.cpf,
                                          self.voo_selecionado.numero,
                                          self.numero_assento_selecionado)
            self.data_manager.add_voo(self.voo_selecionado)

            self.logger.log(logging.INFO,
                            f"Reserva realizada - Voo: {self.voo_selecionado.numero}, "
                            f"Assento: {self.numero_assento_selecionado}",
                            self.usuario_logado.cpf)

        popup.destroy()
        messagebox.showinfo("Sucesso", "Pagamento confirmado e reserva realizada com sucesso!")

        # LIMPAR VISUALIZAÇÃO: Remove o mapa de assentos
        self.limpar_mapa_assentos()
        self.limpar_selecao()

    def cancelar_reserva(self):
        """Cancela uma reserva existente"""
        if not self.assento_selecionado or not self.voo_selecionado:
            messagebox.showerror("Erro", "Selecione sua reserva primeiro!")
            return

        # VERIFICAÇÃO CORRIGIDA: É realmente a reserva do usuário?
        reserva_usuario = self.data_manager.get_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)

        if not reserva_usuario:
            messagebox.showerror("Erro", "Você não possui reserva neste voo!")
            return

        if (self.assento_selecionado.disponivel or
                self.assento_selecionado.passageiro_cpf != self.usuario_logado.cpf or
                self.numero_assento_selecionado != reserva_usuario['numero_assento']):
            messagebox.showerror("Erro", "Este não é o seu assento reservado!")
            return

        # Confirmação
        confirmar = messagebox.askyesno("Confirmar Cancelamento",
                                        f"Deseja cancelar a reserva do assento {self.numero_assento_selecionado}?")
        if not confirmar:
            return

        with self.lock:
            self.assento_selecionado.liberar()
            self.data_manager.remove_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)
            self.data_manager.add_voo(self.voo_selecionado)

            self.logger.log(logging.INFO,
                            f"Reserva cancelada - Voo: {self.voo_selecionado.numero}, "
                            f"Assento: {self.numero_assento_selecionado}",
                            self.usuario_logado.cpf)

        messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")

        # LIMPAR VISUALIZAÇÃO: Remove o mapa de assentos
        self.limpar_mapa_assentos()
        self.limpar_selecao()

    def modificar_reserva(self):
        """Inicia o processo de modificação de reserva"""
        if not self.voo_selecionado:
            messagebox.showerror("Erro", "Primeiro carregue os assentos de um voo!")
            return

        # VERIFICAÇÃO: Usuário tem reserva neste voo?
        reserva_usuario = self.data_manager.get_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)
        if not reserva_usuario:
            messagebox.showerror("Erro", "Você não possui reserva neste voo para modificar!")
            return

        # Entrar em modo modificação
        self.modo_modificacao = True
        self.reserva_antiga_assento = reserva_usuario['numero_assento']

        # Atualizar interface
        self.label_operacao.config(
            text=f"Modo Modificação: Selecione um novo assento disponível (Reserva atual: {self.reserva_antiga_assento})")
        self.btn_reservar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_modificar.config(state='disabled')

        messagebox.showinfo("Modificar Reserva",
                            f"Modo modificação ativado. Sua reserva atual é no assento {self.reserva_antiga_assento}.\n"
                            "Agora selecione um novo assento disponível.")

    def mostrar_popup_modificacao(self, novo_assento_numero, novo_assento, reserva_atual):
        """Mostra popup de confirmação para modificar reserva"""
        popup = tk.Toplevel(self.root)
        popup.title("Confirmar Modificação de Reserva")
        popup.geometry("450x250")
        popup.transient(self.root)
        popup.grab_set()

        # Centralizar popup
        popup.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

        # Conteúdo do popup
        ttk.Label(popup, text="Confirmar Modificação de Reserva",
                  font=('Arial', 14, 'bold')).pack(pady=10)

        info_text = f"Mudar a reserva para o assento {novo_assento_numero}?\n\n"
        info_text += f"De: {reserva_atual}\n"
        info_text += f"Para: {novo_assento_numero}\n"
        info_text += f"Tipo: {novo_assento.classe.title()} - {novo_assento.posicao.title()}\n"
        info_text += f"Valor: R$ {novo_assento.valor:.2f}"

        ttk.Label(popup, text=info_text, justify=tk.CENTER).pack(pady=10)

        # Frame dos botões
        botoes_frame = ttk.Frame(popup)
        botoes_frame.pack(pady=10)

        ttk.Button(botoes_frame, text="Confirmar",
                   command=lambda: self.confirmar_modificacao(popup, novo_assento_numero, novo_assento)).pack(
            side=tk.LEFT, padx=5)

        ttk.Button(botoes_frame, text="Cancelar",
                   command=popup.destroy).pack(side=tk.LEFT, padx=5)

    def confirmar_modificacao(self, popup, novo_assento_numero, novo_assento):
        """Confirma a modificação da reserva"""
        with self.lock:
            try:
                # 1. Encontrar e cancelar reserva anterior
                assento_antigo = self.voo_selecionado.assentos[self.reserva_antiga_assento]
                assento_antigo.liberar()
                self.data_manager.remove_reserva(self.usuario_logado.cpf, self.voo_selecionado.numero)

                # 2. Reservar novo assento
                novo_assento.reservar(self.usuario_logado.cpf)
                self.data_manager.add_reserva(self.usuario_logado.cpf,
                                              self.voo_selecionado.numero,
                                              novo_assento_numero)
                self.data_manager.add_voo(self.voo_selecionado)

                self.logger.log(logging.INFO,
                                f"Reserva modificada - Voo: {self.voo_selecionado.numero}, "
                                f"De: {self.reserva_antiga_assento} Para: {novo_assento_numero}",
                                self.usuario_logado.cpf)

                popup.destroy()
                messagebox.showinfo("Sucesso",
                                    f"Reserva modificada com sucesso!\n"
                                    f"Assento alterado de {self.reserva_antiga_assento} para {novo_assento_numero}")

            except Exception as e:
                popup.destroy()
                messagebox.showerror("Erro", f"Erro ao modificar reserva: {str(e)}")

        # Finalizar modo modificação e limpar interface
        self.finalizar_modificacao()

    def finalizar_modificacao(self):
        """Finaliza o modo de modificação e limpa o estado"""
        self.modo_modificacao = False
        self.reserva_antiga_assento = None

        # LIMPAR VISUALIZAÇÃO: Remove o mapa de assentos e limpa seleção
        self.limpar_mapa_assentos()
        self.limpar_selecao()

    def voltar_ao_menu(self):
        self.mostrar_frame("menu")
        self.limpar_selecao()