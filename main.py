from personagem import Personagem
from heroi import Heroi
from vilao import Vilao

def main():
    # Criando personagens e vilões
    heroi = Heroi('Hercules', 30, 100, 20, 5)
    npc = Personagem('Andarilho Misterioso', 28, 80, 5, 2)
    npc2 = Personagem('Namorada de Hercules', 28, 80, 5, 2)
    vilao = Vilao('Hades', 45, 120, 18, 4, 'Alta')

    # Listas com os personagens
    herois = [heroi]
    viloes = [vilao]
    refens = [npc, npc2]

    # Dicionário com os atributos do herói
    atributos = {'nome': heroi.nome, 'vida': heroi.vida,
                 'ataque': heroi.ataque, 'defesa': heroi.defesa}

    # Lista para registrar o histórico do jogo
    historico = []

    # Mostrando personagens
    print('=== A JORNADA DE HERCULES ===')
    for personagem in herois + viloes + refens:
        print(personagem)
    print('Atributos do herói:', atributos)

    # Diálogo inicial
    vilao.dialogar(heroi, 'Seus amigos estão presos no submundo!')
    heroi.dialogar(vilao, 'Vou libertá-los, Hades!')
    historico.append('Hades desafiou Hercules')

    # Batalha
    rodada = 1
    while heroi.esta_vivo() and vilao.esta_vivo():
        print(f'\n--- Rodada {rodada} ---')
        print(f'Hercules: {heroi.vida} de vida | Hades: {vilao.vida} de vida')
        print('1 - Atacar')
        print('2 - Usar poção')
        escolha = input('O que Hercules vai fazer? ')

        if escolha == '1':
            heroi.atacar(vilao)
            historico.append(f'Rodada {rodada}: Hercules atacou')
        elif escolha == '2':
            heroi.usar_pocao()
            historico.append(f'Rodada {rodada}: Hercules usou poção')
        else:
            print('Opção inválida!')
            continue

        # Vilão ataca se ainda estiver vivo
        if vilao.esta_vivo():
            vilao.atacar(heroi)
            historico.append(f'Rodada {rodada}: Hades atacou')

        rodada += 1

    # Resultado
    if heroi.esta_vivo():
        print('\nHercules venceu Hades!')
        for refem in refens:
            heroi.salvar_refem(refem)
        npc2.dialogar(heroi, 'Você me salvou, Hercules!')
        historico.append('Hercules venceu e salvou os reféns')
    else:
        print('\nHades venceu... Os reféns continuam presos.')
        historico.append('Hades venceu')

    # Mostrando o histórico
    print('\n=== HISTÓRICO ===')
    for evento in historico:
        print(evento)

if __name__ == "__main__":
    # Abre a interface gráfica. Para jogar no terminal, troque por: main()
    from interface import JogoHercules
    JogoHercules().mainloop()
