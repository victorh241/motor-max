from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import user

#region butões funções
def botaoFuncionario(stackWidget):
    stackWidget.setCurrentIndex(2)

def botaoClientes(stackWidget):
    stackWidget.setCurrentIndex(3)

def botaoVeiculos(stackWidget):
    stackWidget.setCurrentIndex(4)

def botaoOrdem(stackWidget):
    stackWidget.setCurrentIndex(5)

def botaoUsuarios(stackWidget):
    stackWidget.setCurrentIndex(6)

def botaoProdutos(stackWidget):
    stackWidget.setCurrentIndex(7)
#endregion

def nivelAcesso(ui):
    acessoNivel = user.lvlPermiUserAtual
    match acessoNivel:
        case "admin":
            pass
        case "Mecânico":
            ui.pushButton_4.setEnabled(False)
            ui.pushButton_4.setDisabled(True)
            ui.pushButton.setEnabled(False)
            ui.pushButton.setDisabled(True)
            ui.pushButton_2.setEnabled(False)
            ui.pushButton_2.setDisabled(True)
        case "Atendente":
            ui.pushButton_4.setEnabled(False)
            ui.pushButton_4.setDisabled(True)

def configTelaPrincipal(stackWidget):
    ui = uic.loadUi("Telas/tela_principal.ui")

    stackWidget.addWidget(ui)

    ui.pushButton.clicked.connect(lambda: botaoFuncionario(stackWidget))#funcionarios
    ui.pushButton_2.clicked.connect(lambda: botaoClientes(stackWidget))#clientes
    ui.pushButton_6.clicked.connect(lambda: botaoVeiculos(stackWidget))#veiculos
    ui.pushButton_3.clicked.connect(lambda: botaoOrdem(stackWidget))#ordem
    ui.pushButton_4.clicked.connect(lambda: botaoUsuarios(stackWidget))#usuarios
    ui.pushButton_5.clicked.connect(lambda: botaoProdutos(stackWidget))#produtos