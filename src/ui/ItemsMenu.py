from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget, QPushButton, QDialog


class ItemsMenu(QWidget):
    def __init__(self, repository, itemDialog, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.repository = repository
        self.itemDialog = itemDialog
        self.items = None

        self.itemsList = QListWidget()
        self.updateItems()

        self.addBtn = QPushButton()
        self.addBtn.setText("Add")

        self.deleteBtn = QPushButton()
        self.deleteBtn.setText("Delete")

        self.lay.addWidget(self.itemsList)
        self.lay.addWidget(self.addBtn)
        self.lay.addWidget(self.deleteBtn)

        self.itemsList.itemDoubleClicked.connect(self.editCommand)
        self.addBtn.clicked.connect(self.addBtnCommand)
        self.deleteBtn.clicked.connect(self.deleteBtnCommand)

    def updateItems(self):
        self.items = self.repository.List()

        names = [str(item) for item in self.items]
        self.itemsList.clear()
        self.itemsList.addItems(names)

    def addBtnCommand(self):
        self.itemDialog.setWindowTitle("Add")
        self.itemDialog.resetValues()
        self.itemDialog.exec_()

        if self.itemDialog.result() == QDialog.Rejected:
            return

        item = self.itemDialog.getItem()
        self.repository.Add(item)
        self.items.append(item)
        self.itemsList.addItem(item)

    def deleteBtnCommand(self):
        itemToDeleteRow = self.itemsList.selectedIndexes()[0].row()
        self.repository.Delete(self.items[itemToDeleteRow])
        self.items.remove(self.items[itemToDeleteRow])
        self.itemsList.takeItem(itemToDeleteRow)

    def editCommand(self):
        itemToEditRow = self.itemsList.selectedIndexes()[0].row()
        self.itemDialog.setWindowTitle("Edit")
        self.itemDialog.setValues(self.items[itemToEditRow].getValues())
        self.itemDialog.exec_()

        if self.itemDialog.result() == QDialog.Rejected:
            return

        item = self.itemDialog.getItem()
        self.repository.Edit(item)
        self.items[itemToEditRow] = item
        self.itemsList.item(itemToEditRow).setText(str(item))
