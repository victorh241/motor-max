from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QLabel
from bancoDados import carregarBD

#region butões
def mostrarFuncionarios(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()

    cursor.execute("SELECT nome, cpf, Email, disponivel FROM Funcionarios")
    dadosFuncionarios = cursor.fetchall()

    tabela = ui.tableWidget

    tabela.setRowCount(len(dadosFuncionarios))
    tabela.setColumnCount(1)

    #region criar o frame
    frame = QWidget()
    labelNome = QLabel("teste 1")
    labelFunc = QLabel("teste 2")
    botaoExcluir = QPushButton("Excluir")
    botaoEditar = QPushButton("Editar")

    frame.addWidget(labelNome)
    frame.addWidget(labelFunc)
    frame.addWidget(botaoEditar)
    frame.addWidget(botaoExcluir)

    tabela.setCellWidget(1, 1, frame)
    #endregion

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastroFuncionario(stackWidget):
    stackWidget.setCurrentIndex(8)
#endregion

def configTelaFuncionarios(stackWidget):
    ui = uic.loadUi("Telas/funcionarios.ui")

    stackWidget.addWidget(ui)

    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastroFuncionario(stackWidget))
