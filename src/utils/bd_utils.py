import os
from supabase import create_client, Client
from dotenv import load_dotenv
from maze.maze import Maze
import hashlib
import json

def open_conection():
    load_dotenv()

    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase = False

    if(url and key):
        print("Realizando conexao com o banco de Dados")
        supabase: Client = create_client(url, key)
    else:
        print("Nao foi possivel realizar a conexao com o banco de dados")

    return supabase
       
def inserir_labirintos(mazes, database):
    for _, maze_obj in mazes.items():
        print(maze_obj)
        if isinstance(maze_obj, Maze):
            tamanho = maze_obj.width
            id = gerar_id_labirinto(maze_obj.grid)
            _ = (
                database.table("labirinto")
                .insert({"id": id, "tamanho": tamanho, "representacao": maze_obj.grid})
                .execute()
            )

def gerar_id_labirinto(grid):
    maze_str = json.dumps(grid, sort_keys=True)
    return hashlib.md5(maze_str.encode()).hexdigest()