from Xadrez.tabuleiro import Xadrez

xadrez = Xadrez()
xadrez.printarTabuleiro()

print("\n")

xadrez.moverPedra("a2","a3")
xadrez.printarTabuleiro()

fen = xadrez.matriz_para_fen(xadrez.tabAtual)
print(fen)

score = xadrez.avaliar_posicao(depth=20)
print("Avaliação:", score)
