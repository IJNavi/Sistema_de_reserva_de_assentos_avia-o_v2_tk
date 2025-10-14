from entities.assento import Assento

class Voo:
    def __init__(self, numero, origem, destino, data_hora, aeronave):
        self.numero = numero
        self.origem = origem
        self.destino = destino
        self.data_hora = data_hora
        self.aeronave = aeronave
        self.assentos = self._criar_assentos(aeronave)

    def _criar_assentos(self, aeronave):
        assentos = {}
        fileiras, assentos_por_fileira = aeronave['configuracao']

        classes_config = {
            'primeira': aeronave['classes']['primeira'],
            'executiva': aeronave['classes']['executiva'],
            'economica': aeronave['classes']['economica']
        }

        for fileira in range(1, fileiras + 1):
            for letra in 'ABCDEF'[:assentos_por_fileira]:
                numero_assento = f"{fileira}{letra}"

                # Determinar classe do assento
                if fileira <= classes_config['primeira']:
                    classe = 'primeira'
                    valor = 1000.00
                elif fileira <= classes_config['executiva']:
                    classe = 'executiva'
                    valor = 500.00
                else:
                    classe = 'economica'
                    valor = 200.00

                # Determinar posição
                if letra in ['A', 'F']:
                    posicao = 'janela'
                elif letra in ['B', 'E']:
                    posicao = 'meio'
                else:
                    posicao = 'corredor'

                # Verificar se é saída de emergência
                emergencia = fileira in aeronave['fileiras_emergencia']

                assentos[numero_assento] = Assento(numero_assento, classe, posicao, valor, emergencia)

        return assentos

    def to_dict(self):
        return {
            'numero': self.numero,
            'origem': self.origem,
            'destino': self.destino,
            'data_hora': self.data_hora,
            'aeronave': self.aeronave,
            'assentos': {num: assento.to_dict() for num, assento in self.assentos.items()}
        }

    @classmethod
    def from_dict(cls, data):
        voo = cls(data['numero'], data['origem'], data['destino'],
                  data['data_hora'], data['aeronave'])
        voo.assentos = {num: Assento.from_dict(ass_data)
                        for num, ass_data in data['assentos'].items()}
        return voo