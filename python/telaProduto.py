from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

def mostrarProdutos(ui, stackWidget):
    pass

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaCadastro(stackWidget):
    stackWidget.setCurrentIndex(13)

def configTelaProdutos(stackWidget):
    ui = uic.loadUi("Telas/tela_produtos.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaCadastro(stackWidget))