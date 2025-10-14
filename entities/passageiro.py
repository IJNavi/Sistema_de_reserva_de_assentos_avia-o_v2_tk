class Passageiro:
    def __init__(self, cpf, nome, data_nascimento, email):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['cpf'], data['nome'], data['data_nascimento'], data['email'])