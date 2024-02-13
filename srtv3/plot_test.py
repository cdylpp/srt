import sys
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class DistributionPlotWidget(QWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a PlotWidget for each column in the DataFrame
        for column in self.df.columns:
            plot_widget = pg.PlotWidget()
            layout.addWidget(plot_widget)

            # Plot histogram of the column values
            hist = pg.HistogramLUTItem()
            hist.setImageItem(plot_widget.getPlotItem())
            hist.gradient.loadPreset('flame')  # Color gradient preset
            plot_widget.addItem(hist)

            # Extract column values and plot histogram
            values = self.df[column].dropna().values
            hist.plot(values, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))


if __name__ == '__main__':
    # Create a sample pandas DataFrame
    data = {'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'C': [2, 4, 6, 8, 10]}
    df = pd.DataFrame(data)

    # Create the application and main window
    app = QApplication(sys.argv)  # Initialize QApplication first
    window = QMainWindow()
    window.resize(800, 600)

    # Create and set the DistributionPlotWidget as central widget
    widget = DistributionPlotWidget(df)
    window.setCentralWidget(widget)

    # Show the main window
    window.show()
    sys.exit(app.exec_())
