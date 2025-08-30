class Regras:
    def emXeque(self, cor, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        
        # Define o rei conforme a cor
        rei = 'R' if cor == 'brancas' else 'r'
        rei_x, rei_y = -1, -1
        for i in range(8):
            for j in range(8):
                if tabuleiro[i][j] == rei:
                    rei_x, rei_y = i, j
                    break
            if rei_x != -1:
                break
        if rei_x == -1:
            return False
        
       
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca == '.':
                    continue
                if (cor == 'brancas' and peca.islower()) or (cor == 'pretas' and peca.isupper()):
                    movimentos = []
                    if peca.lower() == 'p':
                        movimentos = self.movimentoPeao(peca, i, j, tabuleiro)
                    elif peca.lower() == 't':
                        movimentos = self.movimentoTorre(peca, i, j, tabuleiro)
                    elif peca.lower() == 'c':
                        movimentos = self.movimentoCavalo(peca, i, j, tabuleiro)
                    elif peca.lower() == 'b':
                        movimentos = self.movimentoBispo(peca, i, j, tabuleiro)
                    elif peca.lower() == 'd':
                        movimentos = self.movimentoDama(peca, i, j, tabuleiro)
                    elif peca.lower() == 'r':
                        movimentos = self.movimentoRei(peca, i, j, tabuleiro)
                    
                    for mov in movimentos:
                        if mov[2] == rei_x and mov[3] == rei_y:
                            return True
        return False

    def simularMovimento(self, origem, destino):
        tabuleiro_simulado = [linha[:] for linha in self.tabAtual]
        origem_x, origem_y = origem
        destino_x, destino_y = destino
        pedra = tabuleiro_simulado[origem_x][origem_y]
        tabuleiro_simulado[destino_x][destino_y] = pedra
        tabuleiro_simulado[origem_x][origem_y] = "."
        return tabuleiro_simulado

    def buscarTodosLances(self, cor=None):
        lances_possiveis = []
        if cor is None:
            cor = self.turno
        for i in range(8):
            for j in range(8):
                peca = self.tabAtual[i][j]
                if (cor == "brancas" and peca.isupper()) or (cor == "pretas" and peca.islower()):
                    movimentos_validos = []
                    if peca.upper() == 'T':
                        movimentos_validos = self.movimentoTorre(peca, i, j)
                    elif peca.upper() == 'C':
                        movimentos_validos = self.movimentoCavalo(peca, i, j)
                    elif peca.upper() == 'P':
                        movimentos_validos = self.movimentoPeao(peca, i, j)
                    elif peca.upper() == 'B':
                        movimentos_validos = self.movimentoBispo(peca, i, j)
                    elif peca.upper() == 'R':
                        movimentos_validos = self.movimentoRei(peca, i, j)
                      
                        if cor == self.turno:
                            resultado_roque = self.pode_fazer_roque(cor)
                            if resultado_roque == 'roque pequeno':
                                movimentos_validos.append((i, j, i, j + 2))
                            elif resultado_roque == 'roque grande':
                                movimentos_validos.append((i, j, i, j - 2))
                    elif peca.upper() == 'D':
                        movimentos_validos = self.movimentoDama(peca, i, j)
                    else:
                        continue

                    for movimento in movimentos_validos:
                        destino_i, destino_j = movimento[2], movimento[3]
                      
                        if self.tabAtual[destino_i][destino_j] != '.':
                            peca_destino = self.tabAtual[destino_i][destino_j]
                            if (cor == "brancas" and peca_destino.isupper()) or (cor == "pretas" and peca_destino.islower()):
                                continue
                     
                        tabuleiro_simulado = self.simularMovimento((i, j), (destino_i, destino_j))
                        if self.emXeque(cor, tabuleiro_simulado):
                            continue
                        lances_possiveis.append(((i, j), (destino_i, destino_j)))
        return lances_possiveis

    def pode_fazer_roque(self, cor):
        if self.emXeque(cor):
            return False
        if cor == 'brancas':
            rei_pos = (7, 4)
            torre_esq_pos = (7, 0)
            torre_dir_pos = (7, 7)
            adversaria = 'pretas'
        else:
            rei_pos = (0, 4)
            torre_esq_pos = (0, 0)
            torre_dir_pos = (0, 7)
            adversaria = 'brancas'
        
        for jogada in self.jogadas:
            if jogada[0] == rei_pos or jogada[0] == torre_esq_pos or jogada[0] == torre_dir_pos:
                return False
        
        lances_adversarios = self.buscarTodosLances(cor=adversaria)
        casas_proibidas = {lance[1] for lance in lances_adversarios}
        if rei_pos in casas_proibidas:
            return False
    
        if (self.tabAtual[rei_pos[0]][1] == '.' and
            self.tabAtual[rei_pos[0]][2] == '.' and
            self.tabAtual[rei_pos[0]][3] == '.'):
            if ((rei_pos[0], 2) not in casas_proibidas and
                (rei_pos[0], 3) not in casas_proibidas):
                return 'roque grande'
       
        if self.tabAtual[rei_pos[0]][5] == '.' and self.tabAtual[rei_pos[0]][6] == '.':
            if ((rei_pos[0], 5) not in casas_proibidas and
                (rei_pos[0], 6) not in casas_proibidas):
                return 'roque pequeno'
        return False
    
    def matriz_para_fen(self, tabuleiro):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        """
        Converte self.tabAtual para notação FEN, incluindo:
          - posição das peças
          - turno (w/b)
          - direitos de roque (KQkq)
          - en passant (fixo como '-')
          - halfmove clock e fullmove number (0 1)
        """
        # 1) Mapa interno → FEN
        mapa = {
            'P':'P','p':'p',
            'T':'R','t':'r',
            'C':'N','c':'n',
            'B':'B','b':'b',
            'D':'Q','d':'q',
            'R':'K','r':'k',
            '.':'.'
        }

        # 2) Monta a parte das 8 fileiras
        fen_rows = []
        for linha in self.tabAtual:
            row_fen = ""
            empty = 0
            for cell in linha:
                ch = mapa[cell]
                if ch == '.':
                    empty += 1
                else:
                    if empty:
                        row_fen += str(empty)
                        empty = 0
                    row_fen += ch
            if empty:
                row_fen += str(empty)
            fen_rows.append(row_fen)
        fen = "/".join(fen_rows)

        # 3) Turno
        fen += " " + ("w" if self.turno == "brancas" else "b")

        # 4) Direitos de roque
        roque = ""
        # branco
        if self.pode_fazer_roque('brancas') == 'roque pequeno':
            roque += "K"
        if self.pode_fazer_roque('brancas') == 'roque grande':
            roque += "Q"
        # preto
        if self.pode_fazer_roque('pretas') == 'roque pequeno':
            roque += "k"
        if self.pode_fazer_roque('pretas') == 'roque grande':
            roque += "q"
        if not roque:
            roque = "-"
        fen += " " + roque

        # 5) En passant (aqui simplificado como "-")
        fen += " -"

        # 6) Halfmove clock e fullmove number (padrão)
        fen += " 0 1"

        return fen
    
    def verificarFimDeJogo(self):
       
        lances = self.buscarTodosLances(self.turno)
        if not lances:
           
            if self.emXeque(self.turno):
                vencedor = "pretas" if self.turno == "brancas" else "brancas"
                print(f"Xeque mate! Vitória das {vencedor}.")
                return "xeque mate", vencedor
            else:
                
                print("Empate por afogamento!")
                return "empate", None
        return None, None
    
    

    def validarLance(self, pedra, origem, destino, checkTurn=True):
        origem_x, origem_y = origem
        destino_x, destino_y = destino

        if (origem_x > 7 or origem_y > 7 or destino_x > 7 or destino_y > 7 or
            origem_x < 0 or origem_y < 0 or destino_x < 0 or destino_y < 0):
            print("Lance inválido: Posições fora do tabuleiro")
            return None

        if checkTurn and not self.verificarTurno(pedra):
            print("Lance inválido: Não é a vez dessa cor")
            return None

        if pedra.upper() == 'T':
            movimentos_validos = self.movimentoTorre(pedra, origem_x, origem_y)
        elif pedra.upper() == 'C':
            movimentos_validos = self.movimentoCavalo(pedra, origem_x, origem_y)
        elif pedra.upper() == 'P':
            movimentos_validos = self.movimentoPeao(pedra, origem_x, origem_y)
        elif pedra.upper() == 'B':
            movimentos_validos = self.movimentoBispo(pedra, origem_x, origem_y)
        elif pedra.upper() == 'R':
            movimentos_validos = self.movimentoRei(pedra, origem_x, origem_y)
            resultado_roque = self.pode_fazer_roque(self.turno)
            if resultado_roque == 'roque pequeno':
                movimentos_validos.append((origem_x, origem_y, origem_x, origem_y + 2))
            elif resultado_roque == 'roque grande':
                movimentos_validos.append((origem_x, origem_y, origem_x, origem_y - 2))
        elif pedra.upper() == 'D':
            movimentos_validos = self.movimentoDama(pedra, origem_x, origem_y)
        else:
            return None

        if (origem_x, origem_y, destino_x, destino_y) not in movimentos_validos:
            return None

        tabuleiro_simulado = self.simularMovimento((origem_x, origem_y), (destino_x, destino_y))
        if self.emXeque(self.turno, tabuleiro_simulado):
            print("Lance inválido: o rei ficará em xeque após o movimento")
            return None

        return movimentos_validos
            


    def moverPedra(self, origem, destino):
        origem_x, origem_y = origem
        destino_x, destino_y = destino
        pedra = self.tabAtual[origem_x][origem_y]

        if not self.verificarTurno(pedra):
            print("Lance inválido: Não é a vez dessa cor")
            return

       
        if (destino_x, destino_y) == (origem_x, origem_y + 2) or (destino_x, destino_y) == (origem_x, origem_y - 2):
            resultado_roque = self.pode_fazer_roque(self.turno)
            if resultado_roque:
                if resultado_roque == "roque grande":
                    self.tabAtual[origem_x][origem_y] = "."
                    self.tabAtual[origem_x][origem_y - 2] = "R" if self.turno == 'brancas' else "r"
                    self.tabAtual[origem_x][0] = "."
                    self.tabAtual[origem_x][3] = "T" if self.turno == 'brancas' else "t"
                    print("Roque grande realizado!")
                elif resultado_roque == "roque pequeno":
                    self.tabAtual[origem_x][origem_y] = "."
                    self.tabAtual[origem_x][origem_y + 2] = "R" if self.turno == 'brancas' else "r"
                    self.tabAtual[origem_x][7] = "."
                    self.tabAtual[origem_x][5] = "T" if self.turno == 'brancas' else "t"
                    print("Roque pequeno realizado!")
                self.jogadas.append((origem, destino))
                self.mudarTurno()
                return
            else:
                print("Roque inválido!")
                return

        if self.validarLance(pedra, origem, destino) is None:
            print("Lance inválido: Movimento não permitido para essa peça")
            return

      
        if pedra.upper() == 'P' and origem_y != destino_y and self.tabAtual[destino_x][destino_y] == '.':
            self.tabAtual[origem_x][destino_y] = "."

        self.tabAtual[destino_x][destino_y] = pedra
        self.tabAtual[origem_x][origem_y] = "."
        self.jogadas.append((origem, destino))
        self.mudarTurno()

        
        fim, vencedor = self.verificarFimDeJogo()
        if fim == "xeque mate":
            print(f"Fim de jogo: Xeque mate! Vitória das {vencedor}.")
        elif fim == "empate":
            print("Fim de jogo: Empate por afogamento.")
            
    pass
