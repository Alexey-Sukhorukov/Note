import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример PySide6")

        # Создаем основные компоненты
        self.label = QLabel("Текст будет здесь", self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Показать текст", self)
        self.combo_box = QComboBox(self)

        # Добавляем элементы в выпадающий список
        self.combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])

        # Создаем вертикальный layout и добавляем в него компоненты
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.combo_box)

        # Создаем контейнер для layout и устанавливаем его как центральный виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Подключаем сигналы к слотам
        self.button.clicked.connect(self.on_button_clicked)
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_changed)

    def on_button_clicked(self):
        # Получаем текст из поля ввода и устанавливаем его в метку
        text = self.line_edit.text()
        self.label.setText(text)

    def on_combo_box_changed(self, index):
        # Получаем выбранный элемент из выпадающего списка и устанавливаем его в метку
        selected_text = self.combo_box.currentText()
        self.label.setText(f"Выбрано: {selected_text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())