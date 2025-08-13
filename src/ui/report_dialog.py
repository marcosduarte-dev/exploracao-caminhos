from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QRadioButton, QHBoxLayout
from PyQt6.QtCore import Qt
from enums.algorithms import Algorithm
from utils.bd_utils import get_estatisticas

class ReportDialog(QDialog):
    def __init__(self, db_connection, local_stats, parent=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.local_stats = local_stats
        self.stats = []

        self.setWindowTitle("Relatório de Estatísticas")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        # Data source selection
        source_group = QGroupBox("Fonte dos Dados")
        source_layout = QHBoxLayout()
        self.local_rb = QRadioButton("Dados Locais (Sessão Atual)")
        self.db_rb = QRadioButton("Banco de Dados")
        self.local_rb.setChecked(True)
        source_layout.addWidget(self.local_rb)
        source_layout.addWidget(self.db_rb)
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        self.local_rb.toggled.connect(self.fetch_stats)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID Labirinto", "Algoritmo", "Tamanho", "Tempo (ms)", "Células Visitadas", "Caminho", "Memória (MB)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.fetch_stats()

    def fetch_stats(self):
        use_db = self.db_rb.isChecked()
        if use_db and self.db_connection:
            self.stats = get_estatisticas(self.db_connection)
        else:
            self.stats = []
            for size_enum, size_stats in self.local_stats.items():
                if not size_stats: continue
                for alg_enum, stat_values in size_stats.items():
                    if not stat_values: continue
                    self.stats.append({
                        'id_labirinto': stat_values.get('id_labirinto'),
                        'tamanho_labirinto': size_enum.get_dimensions()[0],
                        'algoritmo': alg_enum.value,
                        'tempo_execucao': stat_values['time_taken'],
                        'celulas_visitadas': stat_values['visited_count'],
                        'tamanho_caminho': stat_values['path_length'],
                        'memoria': stat_values['memory_used']
                    })
        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(len(self.stats))
        self.table.setSortingEnabled(False) # Disable sorting during population

        for row, stat in enumerate(self.stats):
            try:
                algorithm_name = Algorithm(stat['algoritmo']).display_name
            except ValueError:
                algorithm_name = f"Unknown ({stat['algoritmo']})"

            maze_id_hex = stat.get('id_labirinto')
            if maze_id_hex:
                maze_id_readable = str(int(maze_id_hex[:8], 16))
            else:
                maze_id_readable = "N/A"

            size = f"{stat['tamanho_labirinto']}x{stat['tamanho_labirinto']}"
            time_val = f"{stat['tempo_execucao']:.2f}"
            visited_val = str(stat['celulas_visitadas'])
            path_val = str(stat['tamanho_caminho'])
            mem_val = f"{stat['memoria']:.2f}"

            self.table.setItem(row, 0, QTableWidgetItem(maze_id_readable))
            self.table.setItem(row, 1, QTableWidgetItem(algorithm_name))
            self.table.setItem(row, 2, QTableWidgetItem(size))
            self.table.setItem(row, 3, QTableWidgetItem(time_val))
            self.table.setItem(row, 4, QTableWidgetItem(visited_val))
            self.table.setItem(row, 5, QTableWidgetItem(path_val))
            self.table.setItem(row, 6, QTableWidgetItem(mem_val))

            # Add numeric items for proper sorting
            if maze_id_hex:
                maze_id_item_numeric = QTableWidgetItem()
                maze_id_item_numeric.setData(Qt.ItemDataRole.DisplayRole, int(maze_id_hex[:8], 16))
                self.table.setItem(row, 0, maze_id_item_numeric)

            time_item_numeric = QTableWidgetItem()
            time_item_numeric.setData(Qt.ItemDataRole.DisplayRole, float(f"{stat['tempo_execucao']:.2f}"))
            self.table.setItem(row, 3, time_item_numeric)

            visited_item_numeric = QTableWidgetItem()
            visited_item_numeric.setData(Qt.ItemDataRole.DisplayRole, int(stat['celulas_visitadas']))
            self.table.setItem(row, 4, visited_item_numeric)

            path_item_numeric = QTableWidgetItem()
            path_item_numeric.setData(Qt.ItemDataRole.DisplayRole, int(stat['tamanho_caminho']))
            self.table.setItem(row, 5, path_item_numeric)

            mem_item_numeric = QTableWidgetItem()
            mem_item_numeric.setData(Qt.ItemDataRole.DisplayRole, float(f"{stat['memoria']:.2f}"))
            self.table.setItem(row, 6, mem_item_numeric)

        self.table.setSortingEnabled(True)