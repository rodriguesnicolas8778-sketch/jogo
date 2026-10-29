class Personagem:
    """
    A classe Personagem representa um personagem genérico em um jogo.
    """
    def __init__(self, nome, idade, vida, ataque, defesa):
        self.nome = nome
        self.idade = idade
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa

    def upgrade_vida(self, incremento=10):
        """Aumenta a vida do personagem."""
        self.vida += incremento
        print(f'Vida de {self.nome} após upgrade: {self.vida}')

    def receber_dano(self, dano):
        """Reduz a vida usando a defesa, sem deixar a vida negativa."""
        dano_final = dano - self.defesa
        if dano_final < 1:
            dano_final = 1
        self.vida -= dano_final
        if self.vida < 0:
            self.vida = 0
        print(f'{self.nome} perdeu {dano_final} de vida. Vida: {self.vida}')

    def atacar(self, alvo):
        """Ataca outro personagem."""
        print(f'{self.nome} atacou {alvo.nome}!')
        alvo.receber_dano(self.ataque)

    def dialogar(self, outro, fala):
        """Faz o personagem falar com outro."""
        print(f'{self.nome} para {outro.nome}: "{fala}"')

    def esta_vivo(self):
        return self.vida > 0

    def update_nome(self, nome_editado):
        self.nome = nome_editado

    def __str__(self):
        return f'Personagem: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa}'
