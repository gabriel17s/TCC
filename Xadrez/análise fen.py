import chess
import chess.engine
from pathlib import Path

pasta_fen = Path("Xadrez/partidas")
pasta_saida = Path("Xadrez/análises")
pasta_saida.mkdir(parents=True, exist_ok=True)

caminho_stockfish = "C:/Users/gabri/Downloads/stockfish/stockfish-windows-x86-64-avx2.exe"

arquivo_fen = pasta_fen / "partidas.txt"
arquivo_saida = pasta_saida / "analises.txt"

engine = chess.engine.SimpleEngine.popen_uci(caminho_stockfish)

linhas_saida = []
with arquivo_fen.open() as fen_file:
    for linha in fen_file:
        partes = linha.strip().split()
        if len(partes) < 6:

            linhas_saida.append("")
            continue

        fen = " ".join(partes[:6])

        try:
            tabuleiro = chess.Board(fen)
        except ValueError:
            print(f"FEN inválida: {linha.strip()}")
            continue

        info = engine.analyse(tabuleiro, chess.engine.Limit(depth=15))
        score = info["score"].white().score(mate_score=100000)

        linhas_saida.append(f"{fen} : {score}")

with arquivo_saida.open("w") as f:
    f.write("\n".join(linhas_saida))

engine.quit()
print("Análise concluída em analises.txt.")
