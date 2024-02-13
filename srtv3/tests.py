import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

def create_uniform_plot(data):
    # Determine plot parameters
    num_plots = len(data)
    num_rows = int(np.ceil(np.sqrt(num_plots)))
    num_cols = int(np.ceil(num_plots / num_rows))
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10, 6))

    # Flatten the axs array if it's not 2D
    if not isinstance(axs, np.ndarray):
        axs = np.array([axs])

    # Plot data
    for i, ax in enumerate(axs.flatten()):
        if i < num_plots:
            ax.plot(data[i])
            ax.set_title(f"Plot {i+1}")
        else:
            ax.axis('off')  # Turn off extra subplots

    # Adjust layout
    fig.tight_layout()

    return fig

# Example usage with random data
data = [np.random.rand(10) for _ in range(5)]
fig = create_uniform_plot(data)

# Example PyQt integration
class PlotWindow(QMainWindow):
    def __init__(self, fig):
        super().__init__()
        self.setWindowTitle("Uniform Plot")
        self.canvas = FigureCanvas(fig)
        self.setCentralWidget(QWidget(self))
        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.canvas)

app = QApplication([])
window = PlotWindow(fig)
window.show()
app.exec()
