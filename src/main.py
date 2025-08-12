import os
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from utils.bd_utils import open_conection, inserir_estatistica
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set App Icon
    current_path = os.path.dirname(__file__)
    logo_path = os.path.join(current_path, 'ui', 'sprites', 'labirinto.png')
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
