class Utils:
    def simularMovimento(self, origem, destino):
        tabuleiro_simulado = [linha[:] for linha in self.tabAtual]
        origem_x, origem_y = origem
        destino_x, destino_y = destino
        pedra = tabuleiro_simulado[origem_x][origem_y]
        tabuleiro_simulado[destino_x][destino_y] = pedra
        tabuleiro_simulado[origem_x][origem_y] = "."
        return tabuleiro_simulado

    def matriz_para_fen(self, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        mapa = {
            'P':'P','p':'p',
            'T':'R','t':'r',
            'C':'N','c':'n',
            'B':'B','b':'b',
            'D':'Q','d':'q',
            'R':'K','r':'k',
            '.':'.'
        }
        fen_rows = []
        for linha in tabuleiro:
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
        fen += " " + ("w" if self.turno == "brancas" else "b")
        fen += " - - 0 1"
        return fen
