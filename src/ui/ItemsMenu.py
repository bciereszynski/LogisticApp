from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget, QPushButton


class ItemsMenu(QWidget):
    def __init__(self, repository, itemDialog, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.repository = repository
        self.itemDialog = itemDialog
        self.items = repository.List()

        self.itemsList = QListWidget()
        self.lay.addWidget(self.itemsList)

        self.itemsList.itemDoubleClicked.connect(self.editCommand)

        names = [str(item) for item in self.items]
        self.itemsList.addItems(names)

        self.addBtn = QPushButton()
        self.addBtn.setText("Add")

        self.deleteBtn = QPushButton()
        self.deleteBtn.setText("Delete")

        self.lay.addWidget(self.addBtn)
        self.lay.addWidget(self.deleteBtn)

        self.addBtn.clicked.connect(self.addBtnCommand)
        self.deleteBtn.clicked.connect(self.deleteBtnCommand)

    def addBtnCommand(self):
        self.itemDialog.setWindowTitle("Add")
        self.itemDialog.resetValues()
        self.itemDialog.exec_()

    def deleteBtnCommand(self):
        itemToDeleteRow = self.itemsList.selectedIndexes()[0].row()
        self.repository.Delete(self.items[itemToDeleteRow])
        self.itemsList.takeItem(itemToDeleteRow)

    def editCommand(self):
        itemToEditRow = self.itemsList.selectedIndexes()[0].row()
        self.itemDialog.setWindowTitle("Edit")
        self.itemDialog.setValues(self.items[itemToEditRow].getValues())
        self.itemDialog.exec_()
