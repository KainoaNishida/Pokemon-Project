import sys
from collections import deque, defaultdict
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QLayout, \
    QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QCoreApplication

WIDTH = 1300
HEIGHT = 900
DATA = 300

PRESET1 = {(6, 18), (18, 17), (4, 0), (4, 9), (17, 3), (19, 0), (8, 0), (5, 1), (8, 9), (19, 9), (11, 5), (2, 2), (19, 18), (9, 17), (0, 14), (15, 5), (6, 11), (16, 13), (18, 19), (7, 19), (8, 2), (17, 5), (12, 18), (14, 15), (19, 2), (19, 11), (8, 11), (5, 3), (0, 7), (2, 4), (5, 12), (3, 15), (9, 19), (13, 1), (0, 16), (13, 19), (7, 3), (16, 15), (18, 3), (17, 7), (19, 4), (14, 17), (17, 16), (11, 0), (0, 0), (3, 17), (0, 9), (13, 3), (15, 0), (13, 12), (15, 9), (7, 5), (15, 18), (18, 5), (1, 19), (17, 0), (12, 13), (14, 10), (17, 9), (19, 6), (5, 7), (9, 5), (14, 19), (11, 2), (0, 2), (3, 10), (4, 18), (13, 5), (16, 1), (10, 15), (7, 7), (16, 19), (14, 3), (5, 0), (12, 15), (14, 12), (17, 11), (5, 9), (9, 7), (11, 4), (10, 8), (13, 7), (10, 17), (18, 0), (7, 0), (2, 13), (7, 9), (5, 2), (4, 4), (12, 17), (14, 14), (9, 0), (13, 0), (19, 13), (10, 10), (8, 13), (2, 6), (16, 5), (10, 19), (7, 2), (0, 18), (2, 15), (6, 15), (12, 10), (14, 7), (5, 4), (4, 6), (12, 19), (9, 2), (4, 15), (13, 2), (1, 0), (19, 15), (8, 15), (2, 8), (16, 7), (7, 4), (0, 11), (2, 17), (12, 3), (6, 17), (14, 0), (3, 0), (12, 12), (14, 9), (4, 17), (19, 8), (10, 5), (1, 2), (0, 4), (19, 17), (10, 14), (8, 17), (11, 13), (16, 0), (2, 10), (0, 13), (2, 19), (6, 19), (14, 2), (3, 2), (4, 10), (19, 1), (17, 13), (19, 10), (10, 7), (8, 10), (19, 19), (8, 19), (0, 6), (2, 12), (0, 15), (6, 12), (12, 7), (3, 4), (12, 16), (4, 12), (19, 3), (10, 0), (17, 15), (19, 12), (8, 12), (0, 8), (10, 18), (0, 17), (2, 14), (15, 17), (12, 0), (6, 14), (18, 13), (12, 9), (5, 15), (4, 14), (17, 8), (10, 2), (9, 4), (19, 5), (17, 17), (19, 14), (10, 11), (11, 10), (2, 7), (11, 19), (0, 10), (0, 19), (6, 7), (15, 19), (6, 16), (7, 15), (4, 7), (17, 1), (17, 10), (19, 7), (11, 3), (17, 19), (19, 16), (10, 13), (2, 0), (0, 3), (0, 12), (13, 6), (15, 3), (6, 0), (2, 18), (13, 15), (16, 11), (7, 8)}
PRESET2 = {(12, 4), (6, 18), (4, 0), (8, 0), (3, 13), (5, 10), (10, 6), (9, 8), (8, 18), (11, 14), (6, 2), (18, 1), (1, 15), (15, 14), (16, 13), (7, 10), (18, 10), (4, 2), (3, 6), (8, 2), (12, 18), (3, 15), (5, 12), (9, 10), (11, 16), (1, 8), (6, 4), (16, 6), (18, 3), (1, 17), (15, 16), (7, 12), (18, 12), (14, 8), (5, 5), (8, 4), (3, 8), (11, 0), (5, 14), (17, 16), (9, 12), (15, 0), (13, 12), (1, 10), (16, 8), (18, 5), (15, 18), (7, 14), (18, 14), (17, 0), (14, 10), (5, 7), (3, 10), (11, 2), (5, 16), (4, 18), (9, 14), (1, 3), (15, 2), (13, 14), (1, 12), (16, 10), (7, 7), (18, 7), (7, 16), (18, 16), (12, 6), (3, 3), (5, 0), (14, 12), (5, 9), (3, 12), (11, 4), (5, 18), (9, 16), (10, 8), (1, 5), (16, 3), (18, 0), (13, 16), (7, 0), (1, 14), (16, 12), (7, 9), (18, 9), (18, 18), (12, 8), (14, 5), (5, 2), (3, 5), (9, 0), (14, 14), (5, 11), (3, 14), (9, 9), (13, 0), (10, 10), (1, 7), (16, 5), (7, 2), (18, 2), (1, 16), (11, 18), (16, 14), (7, 11), (18, 11), (13, 18), (12, 10), (14, 7), (5, 4), (3, 7), (9, 2), (3, 16), (5, 13), (14, 16), (8, 6), (13, 2), (1, 0), (17, 18), (10, 12), (1, 9), (16, 7), (7, 4), (18, 4), (1, 18), (16, 16), (14, 0), (3, 0), (12, 12), (14, 9), (5, 6), (3, 9), (18, 8), (3, 18), (14, 18), (13, 4), (1, 2), (16, 0), (10, 14), (1, 11), (16, 9), (14, 2), (3, 2), (7, 18), (12, 14), (14, 11), (3, 11), (1, 4), (11, 6), (16, 2), (10, 16), (1, 13), (9, 18), (12, 7), (14, 4), (3, 4), (12, 16), (10, 0), (8, 12), (1, 6), (16, 4), (10, 18), (12, 0), (6, 14), (18, 13), (12, 9), (14, 6), (10, 2), (9, 4), (8, 14), (11, 10), (7, 6), (18, 6), (12, 2), (6, 16), (16, 18), (18, 15), (4, 16), (5, 8), (10, 4), (9, 6), (1, 1), (2, 0), (8, 16), (11, 12), (2, 18), (6, 0), (16, 11), (7, 8)}
PRESET3 = {(26, 30), (18, 26), (26, 39), (18, 35), (19, 0), (29, 32), (30, 9), (19, 18), (21, 37), (0, 14), (6, 48), (0, 23), (41, 33), (4, 2), (10, 36), (44, 38), (33, 47), (3, 6), (14, 15), (45, 30), (22, 28), (37, 26), (3, 33), (14, 42), (15, 7), (49, 9), (18, 3), (26, 16), (15, 16), (38, 18), (49, 18), (36, 48), (26, 25), (18, 21), (48, 22), (48, 31), (48, 40), (40, 36), (41, 1), (30, 13), (0, 9), (40, 45), (6, 43), (33, 6), (41, 28), (10, 22), (44, 24), (33, 24), (41, 37), (25, 20), (33, 33), (2, 27), (34, 16), (2, 45), (3, 10), (34, 25), (3, 19), (37, 21), (26, 2), (49, 4), (36, 34), (7, 7), (47, 43), (17, 39), (7, 16), (18, 16), (21, 18), (6, 29), (21, 27), (21, 36), (10, 8), (10, 17), (2, 13), (25, 24), (22, 0), (2, 31), (25, 33), (34, 11), (3, 5), (37, 7), (43, 41), (37, 16), (35, 46), (24, 46), (3, 23), (13, 46), (36, 29), (36, 38), (7, 11), (47, 47), (36, 47), (29, 8), (40, 8), (9, 39), (6, 24), (40, 26), (40, 44), (21, 40), (33, 14), (39, 48), (44, 23), (10, 30), (22, 4), (34, 6), (37, 2), (43, 36), (32, 36), (24, 32), (3, 9), (37, 11), (14, 18), (47, 15), (36, 15), (36, 24), (26, 1), (17, 20), (36, 33), (5, 27), (28, 29), (29, 3), (9, 34), (6, 28), (29, 30), (6, 37), (41, 4), (21, 35), (33, 0), (33, 9), (20, 39), (32, 31), (14, 4), (1, 43), (47, 10), (35, 45), (24, 45), (13, 45), (36, 10), (47, 19), (17, 15), (28, 15), (36, 28), (9, 11), (28, 24), (36, 37), (48, 2), (17, 33), (3, 47), (48, 11), (5, 40), (6, 5), (40, 7), (9, 38), (28, 42), (29, 16), (17, 42), (6, 23), (21, 30), (39, 47), (25, 9), (31, 43), (23, 48), (12, 48), (16, 18), (32, 44), (35, 40), (47, 5), (36, 5), (13, 49), (36, 14), (47, 14), (17, 10), (28, 10), (5, 17), (48, 6), (5, 35), (29, 2), (6, 0), (40, 2), (28, 37), (21, 7), (27, 41), (42, 39), (39, 24), (39, 33), (31, 29), (20, 29), (31, 38), (32, 3), (12, 34), (31, 47), (20, 47), (13, 17), (24, 17), (32, 39), (16, 22), (13, 35), (24, 35), (35, 44), (24, 44), (17, 5), (17, 14), (17, 23), (5, 21), (9, 19), (6, 4), (40, 6), (42, 25), (27, 36), (6, 13), (42, 34), (27, 45), (39, 10), (8, 41), (20, 15), (0, 46), (12, 20), (23, 20), (31, 33), (39, 46), (31, 42), (23, 38), (13, 3), (13, 12), (35, 12), (4, 43), (16, 8), (24, 21), (46, 27), (1, 37), (16, 35), (28, 0), (1, 46), (46, 36), (5, 7), (9, 5), (7, 44), (42, 38), (30, 36), (39, 14), (8, 45), (39, 23), (12, 6), (31, 19), (20, 28), (4, 11), (12, 24), (23, 24), (20, 37), (32, 2), (43, 2), (12, 42), (1, 5), (24, 7), (35, 7), (43, 20), (13, 16), (45, 48), (35, 25), (28, 4), (7, 39), (42, 15), (11, 18), (19, 31), (30, 31), (11, 27), (19, 40), (20, 5), (31, 5), (0, 36), (39, 18), (30, 49), (12, 10), (23, 19), (43, 6), (23, 37), (1, 0), (13, 2), (4, 33), (34, 34), (24, 11), (16, 7), (34, 43), (37, 48), (49, 13), (3, 46), (46, 26), (38, 22), (15, 29), (49, 31), (5, 6), (15, 47), (27, 12), (7, 43), (0, 4), (19, 17), (42, 19), (11, 13), (8, 26), (8, 35), (19, 35), (0, 31), (11, 31), (19, 44), (39, 22), (12, 5), (11, 40), (31, 18), (11, 49), (44, 46), (33, 46), (4, 19), (43, 1), (24, 6), (37, 25), (34, 38), (1, 13), (45, 47), (22, 45), (49, 8), (38, 17), (46, 30), (15, 24), (49, 26), (46, 39), (26, 42), (27, 7), (7, 38), (19, 3), (27, 16), (18, 47), (8, 12), (19, 12), (30, 12), (11, 8), (19, 21), (42, 23), (11, 17), (19, 30), (41, 27), (20, 4), (0, 35), (23, 0), (20, 13), (33, 32), (12, 9), (23, 9), (4, 14), (45, 15), (2, 44), (22, 22), (45, 24), (22, 31), (46, 7), (37, 38), (15, 1), (49, 3), (38, 3), (14, 45), (15, 10), (7, 6), (26, 19), (18, 15), (49, 30), (26, 28), (7, 24), (26, 37), (27, 2), (7, 33), (8, 7), (30, 7), (42, 9), (48, 43), (19, 16), (0, 12), (19, 25), (30, 25), (11, 30), (23, 4), (25, 23), (10, 34), (25, 32), (4, 9), (44, 45), (33, 45), (22, 17), (14, 13), (34, 28), (22, 26), (14, 22), (22, 35), (14, 31), (37, 33), (38, 7), (46, 20), (18, 1), (15, 14), (38, 16), (7, 10), (7, 19), (18, 28), (48, 29), (42, 4), (48, 38), (40, 34), (29, 34), (8, 11), (30, 11), (40, 43), (6, 41), (0, 16), (33, 13), (44, 22), (33, 31), (41, 44), (10, 38), (34, 5), (45, 5), (44, 40), (37, 1), (2, 43), (37, 10), (25, 45), (45, 23), (14, 17), (45, 32), (3, 26), (14, 35), (3, 44), (26, 9), (38, 11), (7, 5), (7, 14), (48, 15), (17, 46), (7, 23), (27, 1), (40, 29), (29, 29), (19, 6), (21, 25), (48, 42), (21, 34), (40, 47), (41, 12), (29, 47), (44, 8), (25, 4), (10, 15), (25, 13), (33, 26), (41, 39), (2, 20), (34, 0), (45, 9), (3, 3), (14, 12), (43, 48), (14, 21), (37, 23), (14, 30), (36, 27), (47, 36), (15, 13), (47, 45), (48, 19), (48, 28), (21, 11), (29, 24), (40, 33), (21, 29), (10, 1), (10, 10), (44, 12), (2, 15), (14, 7), (35, 39), (24, 39), (3, 16), (24, 48), (14, 25), (17, 18), (18, 4), (5, 34), (36, 49), (40, 10), (48, 23), (6, 17), (40, 19), (48, 32), (21, 15), (6, 26), (29, 28), (40, 37), (41, 11), (21, 42), (10, 5), (44, 7), (2, 1), (2, 10), (10, 23), (32, 29), (2, 37), (14, 2), (43, 38), (35, 34), (24, 34), (32, 47), (36, 8), (47, 17), (36, 26), (5, 20), (28, 22), (5, 29), (28, 31), (47, 44), (48, 18), (5, 47), (6, 12), (40, 14), (6, 21), (40, 23), (6, 39), (44, 2), (32, 15), (23, 46), (12, 46), (2, 23), (35, 20), (32, 33), (13, 29), (35, 29), (24, 29), (47, 3), (35, 38), (16, 34), (1, 45), (47, 12), (24, 47), (13, 47), (36, 21), (28, 17), (17, 26), (36, 39), (5, 33), (29, 0), (28, 35), (48, 13), (28, 44), (6, 7), (42, 37), (20, 27), (44, 6), (39, 40), (2, 0), (25, 2), (20, 36), (12, 32), (23, 32), (2, 9), (32, 10), (31, 45), (43, 19), (43, 28), (24, 24), (35, 24), (32, 37), (35, 33), (32, 46), (16, 29), (35, 42), (36, 7), (16, 38), (17, 3), (47, 16), (16, 47), (17, 12), (46, 48), (47, 25), (38, 44), (28, 21), (9, 17), (21, 0), (6, 20), (42, 41), (19, 39), (39, 17), (0, 44), (39, 26), (20, 22), (39, 35), (12, 18), (31, 31), (39, 44), (12, 27), (2, 4), (32, 5), (43, 5), (35, 1), (31, 49), (43, 14), (12, 45), (43, 23), (35, 28), (35, 37), (16, 33), (16, 42), (36, 20), (38, 39), (49, 39), (5, 14), (28, 16), (15, 46), (5, 32), (27, 29), (8, 25), (21, 4), (42, 36), (30, 43), (20, 8), (8, 43), (11, 39), (20, 17), (31, 26), (32, 0), (12, 31), (23, 31), (43, 9), (13, 5), (16, 1), (4, 36), (1, 12), (32, 18), (43, 27), (34, 46), (1, 21), (32, 27), (1, 30), (35, 32), (17, 2), (28, 2), (5, 9), (38, 43), (26, 41), (5, 18), (27, 15), (42, 13), (6, 1), (8, 20), (30, 20), (8, 29), (42, 40), (39, 16), (42, 49), (31, 12), (12, 8), (23, 17), (4, 13), (23, 26), (31, 39), (23, 35), (34, 32), (13, 9), (24, 9), (35, 9), (16, 5), (34, 41), (1, 16), (1, 25), (37, 46), (46, 24), (47, 1), (49, 20), (46, 33), (15, 27), (5, 4), (9, 2), (38, 38), (5, 13), (49, 38), (26, 45), (27, 10), (7, 41), (42, 8), (8, 15), (30, 15), (42, 17), (8, 24), (19, 24), (0, 20), (27, 28), (27, 46), (11, 29), (20, 7), (12, 3), (23, 3), (12, 12), (4, 8), (12, 21), (12, 30), (23, 30), (4, 26), (1, 2), (35, 4), (22, 34), (16, 9), (1, 20), (46, 19), (49, 15), (38, 24), (49, 33), (27, 5), (18, 36), (19, 1), (30, 1), (7, 45), (30, 10), (11, 6), (19, 19), (30, 19), (27, 32), (8, 37), (19, 37), (39, 15), (31, 11), (12, 7), (41, 43), (23, 16), (4, 12), (37, 18), (45, 31), (34, 40), (22, 38), (49, 1), (26, 8), (38, 10), (49, 10), (46, 23), (15, 17), (26, 17), (46, 32), (15, 26), (38, 28), (18, 22), (26, 35), (7, 31), (18, 40), (11, 1), (30, 14), (29, 46), (19, 23), (30, 23), (30, 32), (0, 28), (41, 29), (33, 34), (23, 11), (41, 47), (33, 43), (45, 8), (10, 41), (34, 17), (3, 20), (14, 20), (37, 22), (22, 33), (46, 9), (37, 40), (15, 3), (26, 12)}
PRESET4 = {(12, 4), (12, 10), (4, 9), (5, 4), (5, 10), (6, 11), (12, 3), (5, 3), (6, 4), (6, 10), (12, 5), (4, 10), (5, 5), (6, 3), (12, 7), (4, 3), (11, 2), (6, 5), (7, 7), (12, 9), (12, 6), (4, 5), (5, 9), (4, 11), (12, 11), (12, 8), (4, 4), (5, 11), (10, 1), (10, 13), (11, 12), (6, 9)}
class ColorfulGrid(QWidget):
    def __init__(self, rows, columns):

        self.undirected_graph = defaultdict(int)
        super().__init__()

        self.rows = rows
        self.columns = columns
        self.data_width = DATA

        self.cell_width = (WIDTH - DATA) / self.columns
        self.cell_height = HEIGHT / self.rows
        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]  # 0: Empty, 1: Wall
        self.walls = set()

        self.setWindowTitle('Interactive Grid')
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


        self.row_input.setMaximumWidth(50)  # Set maximum width for row input
        self.column_input.setMaximumWidth(50)  # Set maximum width for column input


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
        new_spacer.setFixedWidth(50 )

        self.run_button.clicked.connect(self.run)


        column_button_selection = QHBoxLayout()
        column_button_selection .addWidget(self.column_decrement_button)
        column_button_selection .addWidget(self.column_increment_button)

        self.reset_button = QPushButton('Reset Walls')

        column_button_selection.addWidget(spacer)
        column_button_selection.addWidget(self.reset_button)

        # Connect the button to the reset_walls method
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
        button_box.addWidget(new_spacer)
        self.set_start_button.clicked.connect(self.enable_set_start_mode)
        button_box.addWidget(self.set_start_button)


        self.set_end_button = QPushButton('Set End')
        self.set_end_button.clicked.connect(self.enable_set_end_mode)
        button_box.addWidget(self.set_end_button)
        button_box.addStretch(1)

        layout.addLayout(button_box)
       # layout.addWidget(self.set_start_button)

       # layout.addWidget(self.set_end_button)

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
            queue = deque([(start[0], start[1], 1)])  # row, col, steps
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                curr = len(queue)


                for _ in range(curr):


                    row, col, steps = queue.popleft()
                    self.min_label.setText(f"Minimum Steps: {steps + 1}")

                    if (row, col) == end:
                        self.min_label.setText(f"Minimum Steps: {steps}")
                        return (row, col, steps, visited)


                    for dx, dy in directions:
                        next_row, next_col = row + dx, col + dy

                        if self.valid(next_row, next_col) and not visited[next_row][next_col]:
                            self.undirected_graph[(next_row, next_col)] = (row, col)
                            self.grid[next_row][next_col] = 4  # 4: Visited cell
                            self.update()
                            visited[next_row][next_col] = True
                            queue.append((next_row, next_col, steps + 1))
                QCoreApplication.processEvents()  # Process events to keep GUI responsive
                time.sleep(0.05)

            return -1

    def backtrack(self, end, start):

        path = deque([end])
        while path:
            row, col = path.popleft()
            self.grid[row][col] = 5

            if (row, col) == start:
                break
            next_row, next_col = self.undirected_graph[(row, col)]
            path.append((next_row, next_col))

        self.update()

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
                    self.grid[row][column] = 1  # Set the corresponding grid cell to a wall
                else:
                    self.grid[row][column] = 0  # Set the corresponding grid cell to empty

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
                    self.grid[row][column] = 1  # Set the corresponding grid cell to a wall
                else:
                    self.grid[row][column] = 0  # Set the corresponding grid cell to empty

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
                    self.grid[row][column] = 1  # Set the corresponding grid cell to a wall
                else:
                    self.grid[row][column] = 0  # Set the corresponding grid cell to empty

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
                    self.grid[row][column] = 1  # Set the corresponding grid cell to a wall
                else:
                    self.grid[row][column] = 0  # Set the corresponding grid cell to empty

        self.start_row = 0
        self.start_column = 0
        self.grid[self.start_row][self.start_column] = 2

        self.end_row = 14
        self.end_column = 14
        self.grid[self.end_row][self.end_column] = 3
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
        #pen = QPen(QColor(192, 192, 192), 2)  # Increased pen width for thicker border

        for row in range(self.rows):
            for column in range(self.columns):
                cell_color = QColor(190, 190, 190)
                border_color = QColor(210, 210, 210)
                if self.grid[row][column] == 1:
                    cell_color = QColor(100, 100, 100)  # Dark gray for walls
                    border_color = QColor(210, 210, 210)
                elif self.grid[row][column] == 2:  # Check for start cell
                    cell_color = QColor(0, 150, 0)
                elif self.grid[row][column] == 3:
                    cell_color = QColor(255, 0, 0)
                elif self.grid[row][column] == 4:
                    cell_color = QColor(150, 150, 150)
                elif self.grid[row][column] == 5:
                    cell_color = QColor(0, 128, 255)

                painter.setBrush(cell_color)
                painter.setPen(QPen(border_color, 2))  # Set border color

                x = int(self.data_width + column * self.cell_width)
                y = int(row * self.cell_height)
                cell_width_int = int(self.cell_width)
                cell_height_int = int(self.cell_height)
                border_radius = 4  # Adjust the border radius value as needed
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

            if self.is_edge_cell(x, y):

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

    def is_edge_cell(self, x, y):
        return x >= self.data_width and (x - self.data_width <= self.cell_width or
                                         x - self.data_width >= (self.columns - 1) * self.cell_width) or \
            y >= 0 and (y <= self.cell_height or y >= (self.rows - 1) * self.cell_height)
    def set_start(self, row, column):
        if self.start_row != -1 and self.start_column != -1:
            self.grid[self.start_row][self.start_column] = 0  # Clear the previous start cell
        self.start_row = row
        self.start_column = column
        self.grid[row][column] = 2  # 2: Start cell
        self.update()

    def set_end(self, row, column):
        if self.end_row != -1 and self.end_column != -1:
            self.grid[self.end_row][self.end_column] = 0  # Clear the previous end cell
        self.end_row = row
        self.end_column = column
        self.grid[row][column] = 3  # 3: End cell
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

    window = ColorfulGrid(20, 20)

    screen_center_x = (QApplication.desktop().screenGeometry().width() - WIDTH) // 2
    screen_center_y = (QApplication.desktop().screenGeometry().height() - HEIGHT) // 2

    window.setGeometry(screen_center_x, screen_center_y, WIDTH, HEIGHT)
    window.setFixedSize(WIDTH, HEIGHT)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()