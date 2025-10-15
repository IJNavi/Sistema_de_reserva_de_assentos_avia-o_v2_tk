# Sistema de Reserva de Assentos Aéreos

Sistema de reservas para companhia aérea fictícia desenvolvido em Python com interface gráfica moderna usando Tkinter.

## 🚀 Funcionalidades

- **Cadastro e login de passageiros** com validação de dados
- **Visualização de voos disponíveis** em formato amigável
- **Mapa interativo de assentos** com interface gráfica intuitiva
- **Sistema completo de reservas**: reservar, cancelar e modificar assentos
- **Controle de restrições**: idade mínima para assentos de emergência
- **Sistema de logs** detalhado de todas as operações
- **Persistência de dados** em JSON
- **Controle de concorrência** para múltiplos usuários
- **Interface gráfica** com Tkinter

## 🎨 Interface Gráfica

A nova versão apresenta uma interface gráfica completa com:

- **Tela de login e cadastro** integradas
- **Menu principal** com informações do usuário
- **Mapa visual de assentos** com cores e legendas
- **Popups de confirmação** para todas as operações
- **Scrollbars** para navegação em voos grandes
- **Feedback visual** em tempo real do status dos assentos

## 🛠️ Tecnologias

- Python 3.x
- Tkinter para interface gráfica
- Módulos padrão: json, threading, logging, re, datetime
- Paradigma de orientação a objetos
- Persistência em arquivos JSON

## 📦 Estrutura do Projeto

```
sistema_reservas/
├── main.py
├── entities/
│   ├── __init__.py
│   ├── passageiro.py
│   ├── voo.py
│   └── assento.py
├── database/
│   ├── __init__.py
│   ├── data_manager.py
│   └── dados.json
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── validators.py
└── interface/
    └── tk_interface.py
```

## 🚀 Como Executar

```bash
# Clone o repositório
git clone <https://github.com/IJNavi/Sistema_de_reserva_de_assentos_avia-o.git>

# Execute o programa
python main.py
```

## 🖥️ Como Usar

### 1. **Cadastro e Login**
   - Na tela inicial, preencha os dados para cadastro ou faça login com CPF
   - Validação automática de CPF, e-mail e data de nascimento

### 2. **Navegação no Sistema**
   - **Visualizar Voos**: Veja todos os voos disponíveis
   - **Reserva de Assentos**: Acesse o sistema de reservas

### 3. **Sistema de Reservas**
   - Digite o número do voo e clique em "Carregar Assentos"
   - Visualize o mapa colorido de assentos:
     - 🟦 **Azul**: Disponível
     - 🟥 **Vermelho**: Ocupado  
     - 🟩 **Verde**: Sua reserva

### 4. **Operações Disponíveis**
   - **Reservar**: Clique em assento disponível → Confirmação de pagamento
   - **Cancelar**: Selecione sua reserva → Confirmação de cancelamento
   - **Modificar**: Selecione sua reserva → Escolha novo assento → Confirmação

## 🎯 Legenda dos Assentos

### Status
- `[ ]` - Disponível
- `[X]` - Ocupado  
- `[*]` - Sua reserva
- `[E]` - Emergência

### Classes
- **P** - Primeira Classe
- **X** - Classe Executiva
- **C** - Classe Econômica

### Posições
- **J** - Janela
- **M** - Meio
- **C** - Corredor

## ⚠️ Restrições e Validações

- **Uma reserva por voo**: Cada passageiro pode ter apenas uma reserva por voo
- **Assentos de emergência**: Menores de 18 anos não podem reservar
- **Validação de CPF**: Formato e dígitos verificadores
- **Validação de e-mail**: Formato correto obrigatório
- **Controle de concorrência**: Evita reservas simultâneas no mesmo assento

## 📊 Recursos Técnicos

### Persistência de Dados
- Dados salvos automaticamente em `database/dados.json`
- Backup automático de todas as operações

### Sistema de Logs
- Registro detalhado em `utils/logger.py`
- Logs de login, reservas, cancelamentos e modificações

### Validações
- CPF, e-mail, data de nascimento
- Idade para assentos de emergência
- Concorrência em operações críticas

## 🔧 Arquivos Principais

- `main.py` - Ponto de entrada do sistema
- `interface/tk_interface.py` - Interface gráfica completa
- `entities/` - Classes de Passageiro, Voo e Assento
- `database/data_manager.py` - Gerenciamento de dados
- `utils/` - Validações e sistema de logs

## 📋 Requisitos Atendidos

- [x] Interface gráfica moderna com Tkinter
- [x] Cadastro e login com validação
- [x] Mapa visual interativo de assentos
- [x] Sistema completo de reservas
- [x] Controle de concorrência
- [x] Restrições por idade
- [x] Sistema de logging
- [x] Persistência de dados
- [x] Validações robustas

## 👥 Multiplataforma

O sistema funciona tanto em **Windows** quanto em **Linux**, utilizando bibliotecas padrão do Python e Tkinter.

## 🆕 Melhorias da Versão com Interface Gráfica

- **Experiência visual** intuitiva e amigável
- **Navegação simplificada** com menus claros
- **Feedback imediato** das operações
- **Mapa colorido** de assentos de fácil compreensão
- **Popups de confirmação** para evitar erros
- **Interface responsiva** com scroll para muitos assentos

## 📝 Licença

Este projeto foi desenvolvido por Ivan Barbosa para fins acadêmicos.

---

**Versão**: 2.0 com Interface Gráfica  
**Desenvolvedor**: Ivan Barbosa  
**Tecnologia**: Python + Tkinter