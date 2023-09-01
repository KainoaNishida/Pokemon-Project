import random
import sys
from collections import deque, defaultdict
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QLayout, \
    QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QCoreApplication
from presets import PRESET1, PRESET2, PRESET3, PRESET4

WIDTH = 1300
HEIGHT = 900
DATA = 300


class ColorfulGrid(QWidget):
    def __init__(self, rows, columns):
        self.undirected_graph = defaultdict(int)
        super().__init__()

        self.rows = rows
        self.columns = columns
        self.data_width = DATA

        self.cell_width = (WIDTH - DATA) / self.columns
        self.cell_height = HEIGHT / self.rows
        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.walls = set()

        self.setWindowTitle('Maze Runner')
        self.setStyleSheet("background-color: rgb(220, 220, 220);")

        self.row_increment_button = QPushButton('+')
        self.row_decrement_button = QPushButton('-')
        self.column_increment_button = QPushButton('+')
        self.column_decrement_button = QPushButton('-')

        self.row_increment_button.setFocusPolicy(Qt.NoFocus)
        self.row_decrement_button.setFocusPolicy(Qt.NoFocus)
        self.column_increment_button.setFocusPolicy(Qt.NoFocus)
        self.column_decrement_button.setFocusPolicy(Qt.NoFocus)

        self.row_label = QLabel("Rows:")
        self.row_label.setMaximumWidth(50)
        self.row_label.setMaximumHeight(20)

        self.row_input = QLineEdit(str(self.rows))
        self.row_apply_button = QPushButton('Apply')

        self.column_label = QLabel("Cols:")
        self.column_label.setMaximumWidth(50)
        self.column_label.setMaximumHeight(20)
        self.column_input = QLineEdit(str(self.columns))
        self.column_apply_button = QPushButton('Apply')
        self.preset_one_button = QPushButton('Preset 1')
        self.preset_two_button = QPushButton('Preset 2')
        self.preset_three_button = QPushButton('Preset 3')
        self.preset_four_button = QPushButton('Preset 4')

        self.row_input.setMaximumWidth(50)
        self.column_input.setMaximumWidth(50)

        max_button_width = 50
        buttons = [
            self.preset_one_button,
            self.row_increment_button,
            self.row_decrement_button,
            self.column_increment_button,
            self.column_decrement_button,
            self.row_apply_button,
            self.column_apply_button,
            self.preset_two_button,
            self.preset_three_button,
            self.preset_four_button
        ]

        for button in buttons:
            button.setMaximumWidth(max_button_width)

        spacer = QWidget()
        spacer.setFixedWidth(70)

        layout = QVBoxLayout()
        layout.addStretch(1)

        self.title_label = QLabel("MAZE RUNNER")
        self.title_label.setMaximumWidth(290)
        font = QFont("Helvetica", 28, QFont.Bold)
        self.title_label.setStyleSheet("color: rgb(0, 50,0);")
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)

        vertical_spacer = QWidget()
        vertical_spacer.setFixedHeight(200)
        vertical_spacer.setFixedWidth(50)
        self.spacer_layout = QHBoxLayout()
        self.spacer_layout.addWidget(vertical_spacer)
        self.spacer_layout.addStretch(1)
        layout.addLayout(self.spacer_layout)

        self.min_label = QLabel("Minimum Steps: N/A")
        self.min_label.setMaximumWidth(100)
        layout.addWidget(self.min_label)

        preset_layout = QHBoxLayout()
        preset_layout.addWidget(self.preset_one_button)
        preset_layout.addWidget(self.preset_two_button)
        preset_layout.addWidget(self.preset_three_button)
        preset_layout.addWidget(self.preset_four_button)
        self.preset_one_button.clicked.connect(self.enable_preset_one)
        self.preset_two_button.clicked.connect(self.enable_preset_two)
        self.preset_three_button.clicked.connect(self.enable_preset_three)
        self.preset_four_button.clicked.connect(self.enable_preset_four)
        preset_layout.addStretch(1)
        layout.addLayout(preset_layout)

        row_input_layout = QHBoxLayout()
        row_input_layout.addWidget(self.row_label)
        row_input_layout.addStretch(1)

        row_input_selection = QHBoxLayout()
        row_input_selection.addWidget(self.row_input)
        row_input_selection.addWidget(self.row_apply_button)
        row_input_selection.addStretch(1)

        row_button_selection = QHBoxLayout()
        row_button_selection.addWidget(self.row_decrement_button)
        row_button_selection.addWidget(self.row_increment_button)
        row_button_selection.addStretch(1)

        layout.addLayout(row_input_layout)
        layout.addLayout(row_input_selection)
        layout.addLayout(row_button_selection)
        layout.addWidget(QWidget())

        column_input_layout = QHBoxLayout()
        column_input_layout.addWidget(self.column_label)
        column_input_layout.addStretch(1)

        column_input_selection = QHBoxLayout()
        column_input_selection.addWidget(self.column_input)
        column_input_selection.addWidget(self.column_apply_button)

        self.run_button = QPushButton('Run')
        self.run_button.setStyleSheet("background-color: green;")
        column_input_selection.addWidget(spacer)
        column_input_selection.addWidget(self.run_button)

        column_input_selection.addStretch(1)

        new_spacer = QWidget()
        new_spacer.setFixedWidth(50)

        self.run_button.clicked.connect(self.run)

        column_button_selection = QHBoxLayout()
        column_button_selection.addWidget(self.column_decrement_button)
        column_button_selection.addWidget(self.column_increment_button)

        self.reset_button = QPushButton('Reset Walls')
        column_button_selection.addWidget(spacer)
        column_button_selection.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset_walls)

        column_button_selection.addStretch(1)

        layout.addLayout(column_input_layout)
        layout.addLayout(column_input_selection)
        layout.addLayout(column_button_selection)

        self.start_row = -1
        self.start_column = -1
        self.end_row = -1
        self.end_column = -1

        self.setting_start = False
        self.setting_end = False

        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        button_box = QHBoxLayout()
        self.set_start_button = QPushButton('Set Start')

        self.set_start_button.clicked.connect(self.enable_set_start_mode)
        button_box.addWidget(self.set_start_button)

        self.set_end_button = QPushButton('Set End')
        self.set_end_button.clicked.connect(self.enable_set_end_mode)
        button_box.addWidget(self.set_end_button)

        self.generate_maze_button = QPushButton('Generate Maze')
        self.generate_maze_button.clicked.connect(self.generate_maze)
        button_box.addWidget(self.generate_maze_button)
        button_box.addStretch(1)

        layout.addLayout(button_box)

        self.setLayout(layout)

        self.row_increment_button.clicked.connect(self.increment_rows)
        self.row_decrement_button.clicked.connect(self.decrement_rows)
        self.column_increment_button.clicked.connect(self.increment_columns)
        self.column_decrement_button.clicked.connect(self.decrement_columns)

        self.row_apply_button.clicked.connect(self.apply_row_changes)
        self.column_apply_button.clicked.connect(self.apply_column_changes)

        self.dragging = False
        self.prev_row = None
        self.prev_column = None

    def bfs(self, start: tuple, end: tuple):
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        visited[start[0]][start[1]] = True
        queue = deque([(start[0], start[1], 1)])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            curr = len(queue)
            for _ in range(curr):
                row, col, steps = queue.popleft()
                self.min_label.setText(f"Minimum Steps: {steps + 1}")

                if (row, col) == end:
                    self.min_label.setText(f"Minimum Steps: {steps}")
                    return row, col, steps, visited

                for dx, dy in directions:
                    next_row, next_col = row + dx, col + dy
                    if self.valid(next_row, next_col) and not visited[next_row][next_col]:
                        self.undirected_graph[(next_row, next_col)] = (row, col)
                        self.grid[next_row][next_col] = 4
                        self.update()
                        visited[next_row][next_col] = True
                        queue.append((next_row, next_col, steps + 1))
            QCoreApplication.processEvents()
            time.sleep(0.05)

        return -1

    def enable_preset_one(self):
        self.walls = PRESET1

        while self.rows != 20:
            if self.rows > 20:
                self.decrement_rows()
            else:
                self.increment_rows()

        while self.columns != 20:
            if self.columns > 20:
                self.decrement_columns()
            else:
                self.increment_columns()

        for row in range(self.rows):
            for column in range(self.columns):
                if (row, column) in self.walls:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0

        self.start_row = 10
        self.start_column = 9
        self.grid[self.start_row][self.start_column] = 2

        self.end_row = 0
        self.end_column = 1
        self.grid[self.end_row][self.end_column] = 3
        self.update()

    def enable_preset_two(self):
        self.walls = PRESET2

        while self.rows != 20:
            if self.rows > 20:
                self.decrement_rows()
            else:
                self.increment_rows()

        while self.columns != 20:
            if self.columns > 20:
                self.decrement_columns()
            else:
                self.increment_columns()

        for row in range(self.rows):
            for column in range(self.columns):
                if (row, column) in self.walls:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0

        self.start_row = 10
        self.start_column = 9
        self.grid[self.start_row][self.start_column] = 2

        self.end_row = 0
        self.end_column = 0
        self.grid[self.end_row][self.end_column] = 3
        self.update()

    def enable_preset_three(self):
        while self.rows != 50:
            if self.rows > 50:
                self.decrement_rows()
            else:
                self.increment_rows()

        while self.columns != 50:
            if self.columns > 50:
                self.decrement_columns()
            else:
                self.increment_columns()

        self.walls = PRESET3

        for row in range(self.rows):
            for column in range(self.columns):
                if (row, column) in self.walls:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0

        self.start_row = 25
        self.start_column = 25
        self.grid[self.start_row][self.start_column] = 2

        self.end_row = 0
        self.end_column = 0
        self.grid[self.end_row][self.end_column] = 3
        self.update()

    def enable_preset_four(self):
        while self.rows != 15:
            if self.rows > 15:
                self.decrement_rows()
            else:
                self.increment_rows()

        while self.columns != 15:
            if self.columns > 15:
                self.decrement_columns()
            else:
                self.increment_columns()

        self.walls = PRESET4

        for row in range(self.rows):
            for column in range(self.columns):
                if (row, column) in self.walls:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0

        self.start_row = 0
        self.start_column = 0
        self.grid[self.start_row][self.start_column] = 2

        self.end_row = 14
        self.end_column = 14
        self.grid[self.end_row][self.end_column] = 3
        self.update()

    def backtrack(self, end, start):
        curr = end
        while curr != start:
            self.grid[curr[0]][curr[1]] = 5
            curr = self.undirected_graph[curr]
        self.grid[curr[0]][curr[1]] = 5
        self.update()

    def valid(self, row, col):
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]) and (row, col) not in self.walls

    def run(self):
        start = (self.start_row, self.start_column)
        end = (self.end_row, self.end_column)

        shortest_path = self.bfs(start, end)

        if shortest_path != -1:
            self.backtrack(end, start)
            self.min = shortest_path[2]
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        for row in range(self.rows):
            for column in range(self.columns):
                cell_color = QColor(190, 190, 190)
                border_color = QColor(210, 210, 210)

                if self.grid[row][column] == 1:
                    cell_color = QColor(50, 50, 50)
                    border_color = QColor(210, 210, 210)
                elif self.grid[row][column] == 2:
                    cell_color = QColor(0, 150, 0)
                elif self.grid[row][column] == 3:
                    cell_color = QColor(255, 0, 0)
                elif self.grid[row][column] == 4:
                    cell_color = QColor(150, 150, 150)
                elif self.grid[row][column] == 5:
                    cell_color = QColor(0, 128, 255)
                

                painter.setBrush(cell_color)
                painter.setPen(QPen(border_color, 2))

                x = int(self.data_width + column * self.cell_width)
                y = int(row * self.cell_height)
                cell_width_int = int(self.cell_width)
                cell_height_int = int(self.cell_height)
                border_radius = 4
                painter.drawRoundedRect(x, y, cell_width_int, cell_height_int, border_radius, border_radius)

    def reset_walls(self):
        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.walls.clear()
        self.update()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()

        if self.setting_start:
            if x >= self.data_width:
                column = int((x - self.data_width) // self.cell_width)
                row = int(y // self.cell_height)
                if 0 <= row < self.rows and 0 <= column < self.columns:
                    self.set_start(row, column)
                    self.setting_start = False
                    self.update()

        elif self.setting_end:
            column = int((x - self.data_width) // self.cell_width)
            row = int(y // self.cell_height)
            if 0 <= row < self.rows and 0 <= column < self.columns:
                self.set_end(row, column)
                self.setting_end = False
                self.update()

        else:
            if x >= self.data_width:
                column = int((x - self.data_width) // self.cell_width)
                row = int(y // self.cell_height)
                if 0 <= row < self.rows and 0 <= column < self.columns:
                    self.dragging = True
                    self.prev_row = row
                    self.prev_column = column
                    self.toggle_wall(row, column)
                    self.update()

    '''
    def is_edge_cell(self, x, y):
        return x >= self.data_width and (x - self.data_width <= self.cell_width or
                                         x - self.data_width >= (self.columns - 1) * self.cell_width) or \
            y >= 0 and (y <= self.cell_height or y >= (self.rows - 1) * self.cell_height)
    '''

    def set_start(self, row, column):
        if self.start_row != -1 and self.start_column != -1:
            self.grid[self.start_row][self.start_column] = 0
        self.start_row = row
        self.start_column = column
        self.grid[row][column] = 2
        self.update()

    def set_end(self, row, column):
        if self.end_row != -1 and self.end_column != -1:
            self.grid[self.end_row][self.end_column] = 0
        self.end_row = row
        self.end_column = column
        self.grid[row][column] = 3
        self.update()

    def enable_set_start_mode(self):
        self.setting_start = True
        self.setting_end = False

    def enable_set_end_mode(self):
        self.setting_start = False
        self.setting_end = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            x = event.x()
            y = event.y()

            if x >= self.data_width:
                column = int((x - self.data_width) // self.cell_width)
                row = int(y // self.cell_height)
                if (
                        0 <= row < self.rows
                        and 0 <= column < self.columns
                        and (row, column) != (self.prev_row, self.prev_column)
                ):
                    self.prev_row = row
                    self.prev_column = column
                    self.toggle_wall(row, column)
                    self.update()

    def recursive_backtracking(self, current_cell=(0, 0)):
        row, col = current_cell
        self.grid[row][col] = 0
        self.update()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + 2 * dr, col + 2 * dc

            if 0 <= new_row < self.rows and 0 <= new_col < self.columns and self.grid[new_row][new_col] == 1:
                neighbor_cell = (new_row, new_col)
                wall_row, wall_col = row + dr, col + dc
                self.grid[wall_row][wall_col] = 0

                QCoreApplication.processEvents()
                self.recursive_backtracking(neighbor_cell)

    def generate_maze(self):
        self.rows += 1
        self.columns += 1
        self.grid = [[1] * self.columns for _ in range(self.rows)]
        self.recursive_backtracking()
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == 1:
                    self.walls.add((row, col))
        self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def toggle_wall(self, row, column):
        if (row, column) in self.walls:
            self.grid[row][column] = 0
            self.walls.remove((row, column))
        else:
            self.grid[row][column] = 1
            self.walls.add((row, column))

    def increment_rows(self):
        self.rows += 1
        self.row_input.setText(str(self.rows))
        self.cell_height = HEIGHT / self.rows
        self.grid.append([0] * self.columns)
        self.update()

    def decrement_rows(self):
        if self.rows > 1:
            self.rows -= 1
            self.row_input.setText(str(self.rows))
            self.cell_height = HEIGHT / self.rows
            self.grid.pop()
            self.update()

    def increment_columns(self):
        self.columns += 1
        self.column_input.setText(str(self.columns))
        self.cell_width = (WIDTH - DATA) / self.columns
        for row in self.grid:
            row.append(0)
        self.update()

    def decrement_columns(self):
        if self.columns > 1:
            self.columns -= 1
            self.column_input.setText(str(self.columns))
            self.cell_width = (WIDTH - DATA) / self.columns
            for row in self.grid:
                row.pop()
            self.update()

    def apply_row_changes(self):
        new_rows = int(self.row_input.text())
        if new_rows > 0:
            self.rows = new_rows
            self.cell_height = HEIGHT / self.rows
            while len(self.grid) < self.rows:
                self.grid.append([0] * self.columns)
            while len(self.grid) > self.rows:
                self.grid.pop()
            self.update()

    def apply_column_changes(self):
        new_columns = int(self.column_input.text())
        if new_columns > 0:
            self.columns = new_columns
            self.cell_width = (WIDTH - DATA) / self.columns
            for row in self.grid:
                while len(row) < self.columns:
                    row.append(0)
                while len(row) > self.columns:
                    row.pop()
            self.update()


def main():
    app = QApplication(sys.argv)
    window = ColorfulGrid(65, 65)

    screen_center_x = (QApplication.desktop().screenGeometry().width() - WIDTH) // 2
    screen_center_y = (QApplication.desktop().screenGeometry().height() - HEIGHT) // 2

    window.setGeometry(screen_center_x, screen_center_y, WIDTH, HEIGHT)
    window.setFixedSize(WIDTH, HEIGHT)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
