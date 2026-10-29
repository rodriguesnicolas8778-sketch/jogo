from personagem import Personagem  # Importa a classe Personagem

class Heroi(Personagem):
    """
    A classe Heroi representa as características de um herói no jogo.
    Herda da classe Personagem.
    """
    def __init__(self, nome, idade, vida, ataque, defesa):
        super().__init__(nome, idade, vida, ataque, defesa)
        self.itens = {'Poção': 2}   # dicionário de itens

    def usar_pocao(self):
        """Usa uma poção para recuperar 30 de vida."""
        if self.itens['Poção'] > 0:
            self.itens['Poção'] -= 1
            print(f'{self.nome} bebeu uma poção! Restam {self.itens["Poção"]}.')
            self.upgrade_vida(30)
        else:
            print('Acabaram as poções!')

    def salvar_refem(self, refem):
        """Salva um refém."""
        print(f'{self.nome} salvou {refem.nome}!')

    def __str__(self):
        return f'Herói: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa}'
