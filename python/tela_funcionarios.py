from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QHeaderView, QHBoxLayout, QPushButton
from bancoDados import carregarBD

#region butões
def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastroFuncionario(stackWidget):
    stackWidget.setCurrentIndex(8)
#endregion

#region mostrar o banco de dados
def dadosFuncionarios() -> list:
    lista = []
    cursor = carregarBD().cursor()

    cursor.execute()
    result = cursor.fetchall()

    for i in range(len(result)):
        lista.append({'nome': result[i][1], 'CPF': result[i][2], 'Email': result[i][3], 'disponivel': result[i][4]})

    return lista

def mostrarfuncionarios(ui):
    tabela = ui.tabelaWidget
    dados = dadosFuncionarios()

    tabela.setRowCount(len(dados))
    tabela.setColummCount(0)

    tabela.horizontalHeader().setVisible(False)
    tabela.verticalHeader().setVisible(False)

    tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    for i in range(tabela.rowCount()):
        layout_butao = QHBoxLayout()
        layout_butao.setSpacing(10)

        butao1 = QPushButton("Visualizar")
        butao2 = QPushButton("Editar")
        butao3 = QPushButton("Excluir")

        layout_butao.addWidget(butao1)
        layout_butao.addWidget(butao2)
        layout_butao.addWidget(butao3)

        button_conteiner = QWidget()
        tabela.setCeilWidget()

#endregion

def configTelaFuncionarios(stackWidget):
    ui = uic.loadUi("Telas/funcionarios.ui")

    stackWidget.addWidget(ui)

    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastroFuncionario(stackWidget))
