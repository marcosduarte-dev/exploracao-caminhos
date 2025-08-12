import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF, QPointF

from enums.colour import *

class MazeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maze = None
        self.solution = None
        self.visited_cells = None
        self.visited_history = None
        self.current_step = 0
        self.total_steps = 0
        self.show_solution = False
        self.show_visited = True

        self.zoom_level = 1.0
        self.offset = QPointF(0, 0)
        self.last_mouse_pos = QPointF(0, 0)
        self.dragging = False

        self.setMinimumSize(600, 600)

    def set_maze_data(self, maze, solution=None, visited_cells=None):
        self.maze = maze
        self.solution = solution
        self.visited_cells = visited_cells
        self.visited_history = None
        self.update()

    def set_visited_steps(self, history):
        self.visited_history = history
        self.total_steps = len(history) - 1 if history else 0
        self.current_step = self.total_steps
        self.update()

    def set_current_step(self, step):
        self.current_step = step
        self.update()

    def paintEvent(self, event):
        if not self.maze:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clear background
        painter.fillRect(self.rect(), QColor(*WHITE))

        # Calculate cell size and total maze dimensions
        base_cell_size = min(self.width() / self.maze.width, self.height() / self.maze.height)
        cell_size = max(1.0, base_cell_size * self.zoom_level)

        total_width = self.maze.width * cell_size
        total_height = self.maze.height * cell_size

        # Center the maze
        start_x = (self.width() - total_width) / 2 + self.offset.x()
        start_y = (self.height() - total_height) / 2 + self.offset.y()

        painter.translate(start_x, start_y)

        # Draw visited cells
        if self.show_visited and self.visited_history and not self.show_solution:
            cells_to_draw = self.visited_history[self.current_step]
            painter.setBrush(QColor(*LIGHT_CYAN))
            painter.setPen(Qt.PenStyle.NoPen)
            for x, y in cells_to_draw:
                if (x, y) != self.maze.start and (x, y) != self.maze.end:
                    painter.drawRect(QRectF(x * cell_size, y * cell_size, cell_size, cell_size))

        # Draw solution path
        is_last_step = self.current_step == self.total_steps and self.total_steps > 0
        if (self.show_solution or is_last_step) and self.solution:
            # Also draw all visited cells if solution is shown
            if self.visited_cells:
                painter.setBrush(QColor(*LIGHT_CYAN))
                painter.setPen(Qt.PenStyle.NoPen)
                for x, y in self.visited_cells:
                    if (x, y) != self.maze.start and (x, y) != self.maze.end:
                        painter.drawRect(QRectF(x * cell_size, y * cell_size, cell_size, cell_size))

            painter.setBrush(QColor(*YELLOW))
            painter.setPen(Qt.PenStyle.NoPen)
            for x, y in self.solution:
                if (x, y) != self.maze.start and (x, y) != self.maze.end:
                    painter.drawRect(QRectF(x * cell_size, y * cell_size, cell_size, cell_size))


        # Draw maze grid
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell_value = self.maze.grid[y][x]
                color = QColor(*WHITE)
                if cell_value == 1: # Wall
                    color = QColor(*BLACK)
                elif cell_value == 2: # Start
                    color = QColor(*GREEN)
                elif cell_value == 3: # End
                    color = QColor(*RED)

                painter.setBrush(color)
                if color != QColor(*WHITE):
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(QRectF(x * cell_size, y * cell_size, cell_size, cell_size))

        # Draw grid lines if zoomed in enough
        if cell_size >= 5:
            pen = QPen(QColor(*GRAY), 0.5)
            painter.setPen(pen)
            for i in range(self.maze.width + 1):
                painter.drawLine(QPointF(i * cell_size, 0), QPointF(i * cell_size, total_height))
            for i in range(self.maze.height + 1):
                painter.drawLine(QPointF(0, i * cell_size), QPointF(total_width, i * cell_size))


    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
        self.zoom_level = max(0.1, min(self.zoom_level, 10.0))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset += QPointF(delta)
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False