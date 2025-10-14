class Assento:
    def __init__(self, numero, classe, posicao, valor, emergencia=False):
        self.numero = numero
        self.classe = classe  # 'economica', 'executiva', 'primeira'
        self.posicao = posicao  # 'janela', 'corredor', 'meio'
        self.valor = valor
        self.emergencia = emergencia
        self.disponivel = True
        self.passageiro_cpf = None

    def reservar(self, passageiro_cpf):
        self.passageiro_cpf = passageiro_cpf
        self.disponivel = False

    def liberar(self):
        self.passageiro_cpf = None
        self.disponivel = True

    def to_dict(self):
        return {
            'numero': self.numero,
            'classe': self.classe,
            'posicao': self.posicao,
            'valor': self.valor,
            'emergencia': self.emergencia,
            'disponivel': self.disponivel,
            'passageiro_cpf': self.passageiro_cpf
        }

    @classmethod
    def from_dict(cls, data):
        assento = cls(data['numero'], data['classe'], data['posicao'],
                      data['valor'], data['emergencia'])
        assento.disponivel = data['disponivel']
        assento.passageiro_cpf = data['passageiro_cpf']
        return assento