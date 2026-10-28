from personagem import Personagem  # Importa a classe Personagem

class Vilao(Personagem):
    """
    A classe Vilao representa as características de um vilão no jogo.
    Herda da classe Personagem.
    """
    def __init__(self, nome, idade, vida, ataque, defesa, maldade):
        super().__init__(nome, idade, vida, ataque, defesa)
        niveis_validos = ['Baixa', 'Média', 'Alta']
        if maldade not in niveis_validos:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {niveis_validos}")
        self.maldade = maldade

    def __str__(self):
        return f'Vilão: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa}, Maldade: {self.maldade}'
