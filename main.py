from Xadrez.tabuleiro import Xadrez

xadrez = Xadrez()
xadrez.printarTabuleiro()

score = xadrez.avaliar_posicao(depth=20)
print("Avaliação:", score)