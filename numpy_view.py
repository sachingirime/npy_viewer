import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class NpyViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_index = 0
        self.npy_files = []
        self.directory = None  # Added instance variable for directory

        self.init_ui()

    def init_ui(self):
        self.central_widget = QLabel(self)
        self.central_widget.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)

        self.load_button = QPushButton('Load Directory', self)
        self.load_button.clicked.connect(self.load_directory)
        self.layout.addWidget(self.load_button)

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.show_previous_image)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next_button)

        central_widget = QLabel(self)
        central_widget.setAlignment(Qt.AlignCenter)

        central_widget.setLayout(self.layout)

        self.setCentralWidget(central_widget)

    def load_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if self.directory:
            self.npy_files = [f for f in os.listdir(self.directory) if f.endswith(('.npy', '.npz'))]
            if not self.npy_files:
                print("No .npy or .npz files found in the selected directory.")
                return

            self.image_index = 0
            self.show_image()

    def show_image(self):
        file_name = self.npy_files[self.image_index]
        data = self.load_data(file_name)
        if data is not None:
            self.display_image(data)

    def load_data(self, file_name):
        file_path = os.path.join(self.directory, file_name)
        try:
            if file_name.endswith('.npy'):
                data = np.load(file_path)
            elif file_name.endswith('.npz'):
                with np.load(file_path) as npz:
                    data = npz['arr_0']
            else:
                raise ValueError("Unsupported file format.")
            return data
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return None

    def display_image(self, data):
        try:
            plt.imshow(data)  # Display in color
            plt.axis('off')
            plt.tight_layout()
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Adjust subplot to fill the entire window
            plt.savefig('temp.png', bbox_inches='tight', pad_inches=0)  # Save image without padding
            pixmap = QPixmap('temp.png')
            self.central_widget.setPixmap(pixmap)
            plt.close()  # Close the Matplotlib figure
        except Exception as e:
            print(f"Error displaying image: {e}")
        finally:
            self.cleanup_temporary_file()


    def cleanup_temporary_file(self):
        try:
            os.remove('temp.png')
        except Exception as e:
            print(f"Error removing temporary file: {e}")

    def show_previous_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.image_index < len(self.npy_files) - 1:
            self.image_index += 1
            self.show_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = NpyViewer()
    viewer.setGeometry(100, 100, 800, 600)
    viewer.setWindowTitle('Npy Viewer')
    viewer.show()
    sys.exit(app.exec_())
