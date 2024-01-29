from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget, QPushButton, QDialog, QMessageBox


class ItemsMenu(QWidget):
    def __init__(self, itemsList, itemDialog, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.itemDialog = itemDialog
        self.itemsList = itemsList
        self.itemsList.listChanged.connect(self.updateItems)

        self.itemsWidget = QListWidget()
        self.updateItems()

        self.addBtn = QPushButton()
        self.addBtn.setText("Add")

        self.deleteBtn = QPushButton()
        self.deleteBtn.setText("Delete")

        self.lay.addWidget(self.itemsWidget)
        self.lay.addWidget(self.addBtn)
        self.lay.addWidget(self.deleteBtn)

        self.itemsWidget.itemDoubleClicked.connect(self.editCommand)
        self.addBtn.clicked.connect(self.addBtnCommand)
        self.deleteBtn.clicked.connect(self.deleteBtnCommand)

    def selectedIndex(self):
        if len(self.itemsWidget.selectedIndexes()) == 0:
            return None
        return self.itemsWidget.selectedIndexes()[0]

    def itemSelectionChanged(self):
        return self.itemsWidget.currentItemChanged

    def updateItems(self):
        names = [str(item) for item in self.itemsList.getItems()]
        self.itemsWidget.clear()
        self.itemsWidget.addItems(names)
        self.update()

    def addBtnCommand(self):
        self.itemDialog.setWindowTitle("Add")
        self.itemDialog.resetValues()
        self.itemDialog.exec_()

        if self.itemDialog.result() == QDialog.Rejected:
            return

        item = self.itemDialog.getItem()
        self.itemsList.append(item)

    def deleteBtnCommand(self):
        if len(self.itemsWidget.selectedIndexes()) == 0:
            return

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Are you sure u want to delete this item?")
        msgBox.setWindowTitle("Delete")
        msgBox.setStandardButtons( QMessageBox.Cancel|QMessageBox.Yes)
        if msgBox.exec_() == QMessageBox.Cancel:
            return
        itemToDeleteRow = self.itemsWidget.selectedIndexes()[0].row()
        self.itemsList.remove(self.itemsList.getItem(itemToDeleteRow))

    def editCommand(self):
        itemToEditRow = self.itemsWidget.selectedIndexes()[0].row()
        self.itemDialog.setWindowTitle("Edit")
        self.itemDialog.setValues(self.itemsList.getItem(itemToEditRow).getValues())
        self.itemDialog.exec_()

        if self.itemDialog.result() == QDialog.Rejected:
            return

        item = self.itemDialog.getItem()
        self.itemsList.update(itemToEditRow, item)
