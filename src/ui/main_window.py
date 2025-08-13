import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTabWidget, QSlider, QCheckBox, QLabel, QFrame, QGroupBox, QApplication, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QFontDatabase

from utils.config import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from utils.bd_utils import open_conection, inserir_estatistica, gerar_id_labirinto
from maze.solvers.bfs_solver import solveBfs
from maze.solvers.AStartManhattan_solver import solveAstarManhattan
from maze.solvers.bidirectional_search_solver import solveBidirectionalSearch
from maze.solvers.bidirectional_astar_solver import solveBidirectionalAstar
from maze.solvers.greedy_bfs_solver import solveGreedyBFS
from maze.solvers.dfs_solver import solveDfs

from ui.maze_widget import MazeWidget
from ui.report_dialog import ReportDialog

# Worker thread for long-running algorithm execution
class SolverWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, solver_function, maze):
        super().__init__()
        self.solver = solver_function
        self.maze = maze

    def run(self):
        result = self.solver(self.maze)
        self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Basic Setup ---
        self.setWindowTitle(TITULO_PROJETO)
        self.setGeometry(100, 100, LARGURA_TELA, ALTURA_TELA)
        
        # --- Data Initialization ---
        self.database = open_conection()
        self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, _ = generate_mazes(self.database)
        self.current_tab = MazeSize.SMALL
        self.current_algorithm = None
        self.alg_buttons = {}
        self.step_check = QCheckBox("Mostrar Passo a Passo")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.step_label = QLabel("Passo: 0/0")
        self.stats_label = QLabel("Selecione um algoritmo para ver as estatísticas.")

        # --- UI Components ---
        self.setup_ui()
        self.update_maze_view()

    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # --- Maze Display Area ---
        self.maze_widget = MazeWidget()
        main_layout.addWidget(self.maze_widget, 7) # 70% of the width

        # --- Sidebar ---
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar_layout = QVBoxLayout(sidebar)
        main_layout.addWidget(sidebar, 3) # 30% of the width

        # --- Sidebar Controls ---
        # 1. Maze Size Tabs
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.tab_changed)
        for size in MazeSize:
            if size == MazeSize.REPORT:
                self.tabs.addTab(QWidget(), size.display_name)
            else:
                self.tabs.addTab(QWidget(), size.display_name)
        sidebar_layout.addWidget(self.tabs)

        # 2. Controls Group
        controls_group = QGroupBox("Controles")
        controls_layout = QVBoxLayout()

        self.generate_button = QPushButton("Gerar Novos Labirintos")
        self.generate_button.clicked.connect(self.generate_new_mazes)
        controls_layout.addWidget(self.generate_button)

        controls_group.setLayout(controls_layout)
        sidebar_layout.addWidget(controls_group)

        # 3. Algorithms Group
        alg_group = QGroupBox("Algoritmos")
        self.alg_layout = QVBoxLayout()
        self.alg_buttons = {}
        for alg in Algorithm:
            btn = QPushButton(alg.display_name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, a=alg: self.select_algorithm(a))
            self.alg_buttons[alg] = btn
            self.alg_layout.addWidget(btn)
        
        self.run_all_button = QPushButton("Rodar Todos")
        self.run_all_button.clicked.connect(self.run_all_algorithms)
        self.alg_layout.addWidget(self.run_all_button)

        alg_group.setLayout(self.alg_layout)
        sidebar_layout.addWidget(alg_group)

        # 4. Visualization Group
        vis_group = QGroupBox("Visualização")
        vis_layout = QVBoxLayout()
        self.step_check = QCheckBox("Mostrar Passo a Passo")
        self.step_check.toggled.connect(self.toggle_step_view)
        vis_layout.addWidget(self.step_check)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_changed)
        vis_layout.addWidget(self.slider)
        self.slider.setEnabled(False)

        self.step_label = QLabel("Passo: 0/0")
        vis_layout.addWidget(self.step_label)
        vis_group.setLayout(vis_layout)
        sidebar_layout.addWidget(vis_group)

        # 5. Statistics Display
        self.stats_label = QLabel("Selecione um algoritmo para ver as estatísticas.")
        self.stats_label.setWordWrap(True)
        sidebar_layout.addWidget(self.stats_label)

        sidebar_layout.addStretch()

    # --- Event Handlers / Slots ---
    def tab_changed(self, index):
        new_size = list(MazeSize)[index]
        if new_size == MazeSize.REPORT:
            self.show_report()
            # Revert to previous tab visually
            self.tabs.setCurrentIndex(list(MazeSize).index(self.current_tab))
            return

        self.current_tab = new_size
        self.current_algorithm = None
        self.uncheck_all_alg_buttons()
        self.update_maze_view()
        self.update_controls()

    def select_algorithm(self, algorithm):
        if self.current_algorithm == algorithm:
            self.current_algorithm = None
            self.alg_buttons[algorithm].setChecked(False)
        else:
            self.current_algorithm = algorithm
            for alg, btn in self.alg_buttons.items():
                if alg != algorithm:
                    btn.setChecked(False)
        
        if self.current_algorithm:
            self.run_solver(self.current_algorithm)
        else:
            self.update_maze_view()
            self.update_controls()

    def run_solver(self, algorithm):
        if self.solutions[self.current_tab].get(algorithm) is not None:
            self.update_maze_view()
            self.update_controls()
            return

        solver_map = {
            Algorithm.BFS: solveBfs,
            Algorithm.DFS: solveDfs,
            Algorithm.GREEDY_BFS: solveGreedyBFS,
            Algorithm.ASTAR_MANHATTAN: solveAstarManhattan,
            Algorithm.BIDIRECTIONAL_SEARCH: solveBidirectionalSearch,
            Algorithm.BIDIRECTIONAL_ASTAR: solveBidirectionalAstar,
        }
        solver_function = solver_map[algorithm]
        maze = self.mazes[self.current_tab]

        self.progress_dialog = QProgressDialog("Resolvendo o labirinto...", "Cancelar", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.show()

        self.worker = SolverWorker(solver_function, maze)
        self.worker.finished.connect(lambda result: self.on_solver_finished(algorithm, result))
        self.worker.start()

    def on_solver_finished(self, algorithm, result):
        path, visited, history, time_taken, memory_used = result
        self.solutions[self.current_tab][algorithm] = path
        self.visited_cells[self.current_tab][algorithm] = visited
        self.visited_history[self.current_tab][algorithm] = history
        maze = self.mazes[self.current_tab]
        maze_id = gerar_id_labirinto(maze.grid)
        self.solutions[self.current_tab][algorithm] = path
        self.visited_cells[self.current_tab][algorithm] = visited
        self.visited_history[self.current_tab][algorithm] = history
        self.statistics[self.current_tab][algorithm] = {
            "id_labirinto": maze_id,
            "visited_count": len(visited),
            "time_taken": time_taken,
            "path_length": (len(path) - 1) if path else 0,
            "memory_used": memory_used
        }
        inserir_estatistica(self.database, maze, algorithm, time_taken, len(visited), len(path)-1 if path else 0, memory_used)
        
        self.progress_dialog.close()
        self.update_maze_view()
        self.update_controls()

    def run_all_algorithms(self):
        # This should also be in a worker thread in a real app, but for simplicity...
        for alg in Algorithm:
            if self.solutions[self.current_tab].get(alg) is None:
                self.current_algorithm = alg
                for a, b in self.alg_buttons.items():
                    b.setChecked(a == alg)
                QApplication.processEvents()

                self.run_solver(alg)
                self.worker.wait()
        
        self.current_algorithm = None
        self.uncheck_all_alg_buttons()
        self.update_maze_view()
        self.update_controls()
        QMessageBox.information(self, "Concluído", "Todos os algoritmos foram executados.")

    def generate_new_mazes(self):
        self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, _ = generate_mazes(self.database)
        self.current_algorithm = None
        self.uncheck_all_alg_buttons()
        self.update_maze_view()
        self.update_controls()
        QMessageBox.information(self, "Concluído", "Novos labirintos foram gerados.")

    def toggle_step_view(self, checked):
        self.slider.setEnabled(checked)
        self.maze_widget.show_solution = not checked
        self.update_maze_view()
        self.update_controls()

    def slider_changed(self, value):
        self.maze_widget.set_current_step(value)
        self.update_step_label()

    def show_report(self):
        dialog = ReportDialog(self.database, self.statistics, self)
        dialog.exec()

    # --- UI Update Helpers ---
    def update_maze_view(self):
        maze = self.mazes[self.current_tab]
        solution = None
        history = None
        visited = None

        if self.current_algorithm:
            solution = self.solutions[self.current_tab].get(self.current_algorithm)
            history = self.visited_history[self.current_tab].get(self.current_algorithm)
            visited = self.visited_cells[self.current_tab].get(self.current_algorithm)

        self.maze_widget.set_maze_data(maze, solution, visited)
        if history:
            self.maze_widget.set_visited_steps(history)

    def update_controls(self):
        is_algorithm_selected = self.current_algorithm is not None
        history = self.visited_history[self.current_tab].get(self.current_algorithm)
        show_steps = self.step_check.isChecked()

        self.slider.setEnabled(bool(is_algorithm_selected and history and show_steps))
        if is_algorithm_selected and history and show_steps:
            self.slider.setRange(0, len(history) - 1)
            self.slider.setValue(len(history) - 1)
        
        self.update_step_label()
        self.update_stats_label()

    def update_step_label(self):
        if self.slider.isEnabled():
            self.step_label.setText(f"Passo: {self.slider.value() + 1}/{self.slider.maximum() + 1}")
        else:
            self.step_label.setText("Passo: N/A")

    def update_stats_label(self):
        if self.current_algorithm and self.current_algorithm in self.statistics[self.current_tab]:
            stats = self.statistics[self.current_tab][self.current_algorithm]
            text = f"""
            <b>Estatísticas ({self.current_algorithm.display_name}):</b><br>
            - Células visitadas: {stats['visited_count']}<br>
            - Tempo: {stats['time_taken']:.2f} ms<br>
            - Tamanho do caminho: {stats['path_length']}<br>
            - Uso de memória: {stats['memory_used']:.2f} MB
            """
            self.stats_label.setText(text)
        else:
            self.stats_label.setText("Selecione um algoritmo para ver as estatísticas.")

    def uncheck_all_alg_buttons(self):
        for btn in self.alg_buttons.values():
            btn.setChecked(False)