from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QLineEdit, QSpinBox


def AddDecimalEditor(layout, name):
    label = QLabel(name)
    spin = QDoubleSpinBox()
    spin.setDecimals(15)

    layout.addWidget(label)
    layout.addWidget(spin)

    return label, spin


def AddStringEditor(layout, name):
    label = QLabel(name)
    line = QLineEdit()

    layout.addWidget(label)
    layout.addWidget(line)

    return label, line


def AddIntegerEditor(layout, name):
    label = QLabel(name)
    spin = QSpinBox()

    layout.addWidget(label)
    layout.addWidget(spin)

    return label, spin
