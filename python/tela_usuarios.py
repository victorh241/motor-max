from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel, QTableWidgetItem, QTableWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD

def mostrarUsuarios(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_usuario, id_funcionario,login, nivelAcesso FROM usuarios")
        dados = cursor.fetchall()

        tabela = ui.tableWidget

        colunas = 1

        tabela.setRowCount(len(dados))
        tabela.setColumnCount(colunas)

        tabela.setHorizontalHeaderLabels([""] * colunas)
        tabela.setVerticalHeaderLabels([""] * tabela.rowCount())
        tabela.horizontalHeader().setVisible(False)
        tabela.verticalHeader().setVisible(False)
        tabela.setShowGrid(False)

        for idx, _usuario in enumerate(dados):
            frame = QFrame()

            

    except Exception as e:
        print(f"Erro ao mostrar usuários: {e}")

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastro(stackWidget):
    stackWidget.setCurrentIndex(12)

def configTelaUsuarios(stackWidget):
    ui = uic.loadUi("Telas/tela_usuarios.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastro(stackWidget))