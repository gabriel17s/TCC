import chess.pgn
import os
import glob

out_dir = os.path.join("xadrez", "partidas")
os.makedirs(out_dir, exist_ok=True)

arquivos_pgn = glob.glob(r"C:\Users\gabri\Downloads\master_games*.pgn")

out_path = os.path.join(out_dir, "partidas.txt")

with open(out_path, "w") as out:
    for arquivo in arquivos_pgn:
        with open(arquivo) as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break

                board = game.board()
                for move in game.mainline_moves():
                    board.push(move)
                    out.write(board.fen() + "\n")

                out.write("\n")
