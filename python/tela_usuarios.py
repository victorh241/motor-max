from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastro(stackWidget):
    stackWidget.setCurrentIndex(12)

def configTelaUsuarios(stackWidget):
    ui = uic.loadUi("Telas/tela_usuarios.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastro(stackWidget))