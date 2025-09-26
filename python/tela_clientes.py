from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaCadastro(stackWidget):
    stackWidget.setCurrentIndex(9)

def configTelaClientes(stackWidget):
    ui = uic.loadUi("Telas/tela_cliente.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaCadastro(stackWidget))


