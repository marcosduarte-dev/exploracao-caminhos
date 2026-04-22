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
        if isinstance(maze_obj, Maze):
            tamanho = maze_obj.width
            id = gerar_id_labirinto(maze_obj.grid)
            _ = (
                database.table("labirinto")
                .insert({"id": id, "tamanho": tamanho, "representacao": maze_obj.grid})
                .execute()
            )

def inserir_estatistica(database, maze, algoritmo, tempo_execucao, celulas_visitadas, tamanho_caminho, memory):
    if(database):
        id = gerar_id_labirinto(maze.grid)
        _ = (
            database.table("estatisticas")
            .insert({
                    "id_labirinto": id,
                    "algoritmo": algoritmo.value,
                    "tamanho_labirinto": maze.width,
                    "tempo_execucao": tempo_execucao,
                    "celulas_visitadas": celulas_visitadas,
                    "tamanho_caminho": tamanho_caminho,
                    "memoria": memory
                    })
            .execute()
        )

def gerar_id_labirinto(grid):
    maze_str = json.dumps(grid, sort_keys=True)
    return hashlib.md5(maze_str.encode()).hexdigest()

def buscar_estatisticas(database, filtro_tamanho=None):
    """
    Busca estatísticas do banco de dados com filtro opcional por tamanho.
    
    Args:
        database: Conexão com o banco de dados
        filtro_tamanho (int, opcional): Tamanho do labirinto para filtrar (10, 50, 100)
    
    Returns:
        list: Lista de estatísticas encontradas
    """
    if not database:
        return []
    
    try:
        query = database.table("estatisticas").select("*")
        
        if filtro_tamanho is not None:
            query = query.eq("tamanho_labirinto", filtro_tamanho)
        
        response = query.execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao buscar estatísticas: {e}")
        return []

def buscar_estatisticas_por_algoritmo(database, algoritmo=None):
    """
    Busca estatísticas agrupadas por algoritmo.
    
    Args:
        database: Conexão com o banco de dados
        algoritmo (int, opcional): ID do algoritmo para filtrar
    
    Returns:
        dict: Dicionário com estatísticas agrupadas por algoritmo
    """
    if not database:
        return {}
    
    try:
        query = database.table("estatisticas").select("*")
        
        if algoritmo is not None:
            query = query.eq("algoritmo", algoritmo)
        
        response = query.execute()
        data = response.data if response.data else []
        
        # Agrupa por algoritmo
        stats_por_algoritmo = {}
        for stat in data:
            algo_id = stat['algoritmo']
            if algo_id not in stats_por_algoritmo:
                stats_por_algoritmo[algo_id] = []
            stats_por_algoritmo[algo_id].append(stat)
        
        return stats_por_algoritmo
    except Exception as e:
        print(f"Erro ao buscar estatísticas por algoritmo: {e}")
        return {}

def calcular_estatisticas_gerais(database):
    """
    Calcula estatísticas gerais de todos os dados.
    
    Args:
        database: Conexão com o banco de dados
    
    Returns:
        dict: Dicionário com estatísticas gerais
    """
    if not database:
        return {}
    
    try:
        response = database.table("estatisticas").select("*").execute()
        data = response.data if response.data else []
        
        if not data:
            return {}
        
        # Calcula estatísticas gerais
        total_execucoes = len(data)
        tempo_medio = sum(stat['tempo_execucao'] for stat in data) / total_execucoes
        celulas_visitadas_medio = sum(stat['celulas_visitadas'] for stat in data) / total_execucoes
        caminho_medio = sum(stat['tamanho_caminho'] for stat in data) / total_execucoes
        memoria_media = sum(stat['memoria'] for stat in data) / total_execucoes
        
        return {
            'total_execucoes': total_execucoes,
            'tempo_medio': tempo_medio,
            'celulas_visitadas_medio': celulas_visitadas_medio,
            'caminho_medio': caminho_medio,
            'memoria_media': memoria_media
        }
    except Exception as e:
        print(f"Erro ao calcular estatísticas gerais: {e}")
        return {}

def limpar_estatisticas(database):
    """
    Remove todas as estatísticas do banco de dados.
    
    Args:
        database: Conexão com o banco de dados
    
    Returns:
        bool: True se sucesso, False caso contrário
    """
    if not database:
        return False
    
    try:
        database.table("estatisticas").delete().neq("id", "").execute()
        return True
    except Exception as e:
        print(f"Erro ao limpar estatísticas: {e}")
        return False