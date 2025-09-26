from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import re
from bancoDados import carregarBD

def voltarTela(ui ,stackWidget):
    stackWidget.setCurrentIndex(5)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(5)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")

def campoErro(ui):
    ui.lineEdit_5.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

    ui.lineEdit_6.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def registrarVeiculos(ui, stackWidget):
    cnx = carregarBD()
    descrição = ui.lineEdit_5.text()
    valor = ui.lineEdit_6.text()

    if descrição.strip() == "" or valor.strip() == "":
        campoErro(ui)
    else:
        cursor = cnx.cursor()

        sqlCommand = "INSERT INTO serviços(descrição, Valor_mãodeObra) VALUES (%s, %s)"
        dados = (descrição, valor)
        cursor.execute(sqlCommand, dados)
        cnx.commit()

def configCadastroServico(stackWidget):
    ui = uic.loadUi("Telas/tela_serviços_cadastro.ui")

    stackWidget.addWidget(ui)

    ui.pushButton.clicked.connect(lambda: registrarVeiculos(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTela(ui ,stackWidget))