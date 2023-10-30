from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget, QPushButton


class ItemsMenu(QWidget):
    def __init__(self, repository, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.repository = repository
        self.items = repository.List()

        self.itemsList = QListWidget()
        self.lay.addWidget(self.itemsList)

        self.addBtn = QPushButton()
        self.addBtn.setText("Add")

        self.deleteBtn = QPushButton()
        self.deleteBtn.setText("Delete")

        self.lay.addWidget(self.addBtn)
        self.lay.addWidget(self.deleteBtn)

        self.addBtn.clicked.connect(self.addBtnCommand)
        self.deleteBtn.clicked.connect(self.deleteBtnCommand)

    def addBtnCommand(self):
        self.repository.Add()

    def deleteBtnCommand(self):
        self.repository.Delete(self.itemsList.selectedItems())
