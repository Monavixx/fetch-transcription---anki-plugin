from aqt.qt import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
#from PyQt6.QtWidgets import QSizePolicy

class FlowLayout(QWidget):
    def __init__(self, max_width, parent=None):
        super().__init__(parent)
        self.max_width = max_width
        self.layout = QVBoxLayout(self)
        self.current_hbox = QHBoxLayout()
        self.layout.addLayout(self.current_hbox)
        self.listOfElements = []

    def addWidget(self, widget):
        # Установка фиксированного размера для предотвращения растягивания
        widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Добавление виджета во временный layout для проверки ширины
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(widget)
        temp_widget = QWidget()
        temp_widget.setLayout(temp_layout)
        temp_width = temp_widget.sizeHint().width()

        # Проверка, поместится ли виджет в текущий QHBoxLayout
        if self.current_hbox.count() > 0 and self.current_hbox.sizeHint().width() + temp_width > self.max_width:
            self.current_hbox = QHBoxLayout()
            self.layout.addLayout(self.current_hbox)

        self.current_hbox.addWidget(widget)
        self.listOfElements.append(widget)

    def getWidgets(self):
        return self.listOfElements
    def getWidgetById(self, id) -> QWidget:
        return self.listOfElements[id]

