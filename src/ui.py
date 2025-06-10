from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTableView, QHeaderView, QSizePolicy
from PyQt6.QtCore import QAbstractTableModel, Qt, QTimer
from PyQt6.QtGui import QFont
from func import get_top_five_yielders, get_progress, get_data, get_current_plot
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]  # Column names
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)  # Optional: row numbers

    def update_data(self, data, headers):
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()

class Card(QWidget):
    def __init__(self, title: str, value: str, parent = None):
        super().__init__(parent)

        #title label
        self.titleLabel = QLabel(title)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.titleLabel.setStyleSheet("color: #666;")

        #value label
        self.valueLabel = QLabel(value)
        self.valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.valueLabel.setStyleSheet("color: #333;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.valueLabel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        self.setLayout(layout)
        
class graphWidget(QWidget):
    def __init__(self, data, columns):
        super().__init__()

        self.plotTitle = QLabel("Size Distribution")
        self.plotTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plotTitle.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.plotTitle.setStyleSheet("color: #666;")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.plotTitle)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_histograms(data, columns)

    def plot_histograms(self, data, columns):
        self.ax.clear()

        for col in columns:
            sns.kdeplot(data[col].dropna(), label = col, ax = self.ax, fill = True)
        
        self.ax.set(xlabel = None)
        self.ax.set(ylabel = None)
        self.ax.legend(title = "Grades")

        self.canvas.draw()

class MainWindowUI(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(800,600)


        # Initial load
        self.df = get_data()
        self.setup_ui()

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(4000)

    def setup_ui(self):
        df_view = get_top_five_yielders(self.df)
        print(self.df)
        data = df_view.values.tolist()
        headers = df_view.columns.tolist()

        self.tableTitle = QLabel("Highest Yielders")
        self.tableTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableTitle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.tableTitle.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")

        self.table = QTableView()
        self.model = TableModel(data, headers)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.table.verticalHeader().setStyleSheet("font-weight: bold;")

        self.progressBar = Card("Plots Completed", get_progress(self.df), self)

        self.thisPlot = Card("Current Plot", get_current_plot(self.df), self)

        self.histGraph = graphWidget(self.df, ['C+B','Pickouts ', 'Marketable Yield'])

        mainLayout = QHBoxLayout()

        yieldLayout = QVBoxLayout()
        yieldLayout.addWidget(self.tableTitle)
        yieldLayout.addWidget(self.table)

        infoLayout = QVBoxLayout()
        plotAndProgressLayout = QHBoxLayout()
        plotAndProgressLayout.addWidget(self.progressBar)
        plotAndProgressLayout.addWidget(self.thisPlot)
        infoLayout.addLayout(plotAndProgressLayout, stretch = 1)

        infoLayout.addWidget(self.histGraph)
        self.histGraph.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        infoLayout.addStretch(3)
        

        mainLayout.addLayout(yieldLayout, stretch = 5)
        mainLayout.addLayout(infoLayout, stretch = 3)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(0)

        self.setLayout(mainLayout)
    
    def refresh_data(self):
        self.df = get_data()
        df_view = get_top_five_yielders(self.df)
        data = df_view.values.tolist()
        headers = df_view.columns.tolist()
        self.model.update_data(data, headers) 
        self.table.setModel(self.model)
        self.progressBar.valueLabel.setText(get_progress(self.df))