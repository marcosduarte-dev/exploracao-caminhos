# Exploração de Caminhos: Comparação entre Algoritmos de Busca em Labirintos

## Autores

*   Marcos Pedroso Duarte
*   Camila de Figueiredo Jardim
*   Wesley Amorim dos Santos

## Descrição

Este projeto é uma ferramenta visual para gerar, resolver e comparar diferentes algoritmos de busca em labirintos. A aplicação permite ao usuário visualizar o processo de resolução de cada algoritmo passo a passo, além de apresentar estatísticas de desempenho como tempo de execução, consumo de memória e tamanho do caminho encontrado.

## Funcionalidades

*   **Geração de Labirintos:** Criação de labirintos com diferentes tamanhos (Pequeno, Médio, Grande).
*   **Algoritmos de Resolução:** Implementação de múltiplos algoritmos de busca, incluindo:
    *   Busca em Largura (BFS)
    *   Busca em Profundidade (DFS)
    *   Busca Gulosa (Greedy BFS)
    *   A* (com heurística de Manhattan)
    *   Busca Bidirecional
    *   Busca Bidirecional A*
*   **Interface Interativa:**
    *   Visualização gráfica do labirinto e do processo de resolução.
    *   Zoom para explorar o labirinto.
    *   Controle passo a passo da execução do algoritmo.
*   **Análise de Desempenho:**
    *   Exibição de estatísticas detalhadas para cada algoritmo (tempo, memória, etc.).
    *   Conexão com banco de dados Supabase para armazenamento e análise de resultados.

## Tecnologias Utilizadas

*   **Python:** Linguagem principal do projeto.
*   **Pygame:** Biblioteca para a criação da interface gráfica e visualização.
*   **Supabase:** Plataforma de backend para armazenamento de dados e estatísticas.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd TCC-Labirinto
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    python -m pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto.
    *   Adicione as suas credenciais do Supabase neste arquivo:
        ```
        SUPABASE_URL="SUA_URL_DO_SUPABASE"
        SUPABASE_KEY="SUA_CHAVE_DO_SUPABASE"
        ```

## Uso

Para executar a aplicação, rode o seguinte comando na raiz do projeto:

```bash
python src/main.py
```

## Estrutura do Projeto

```
TCC-Labirinto/
├── src/
│   ├── enums/         # Enumerações para algoritmos, cores e tamanhos
│   ├── maze/          # Lógica do labirinto (geração e resolução)
│   ├── ui/            # Componentes da interface gráfica
│   └── utils/         # Utilitários (configuração, banco de dados)
├── .gitignore
├── requirements.txt   # Dependências do projeto
└── README.md          # Este arquivo
```
