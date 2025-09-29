from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import re
from bancoDados import carregarBD

#TODO: fazer os campos vazios

def carregarDadosFuncionario(ui, id_funcionario):
    pass

def voltarTelaPrincipal(stackWidget, ui):
    ui.lineEdit_5.setText("")
    ui.lineEdit_4.setText("")
    ui.lineEdit_6.setText("")

    stackWidget.setCurrentIndex(2)

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(2)

    ui.lineEdit_5.setText("")
    ui.lineEdit_4.setText("")
    ui.lineEdit_6.setText("")

def errorCampos(ui):
    ui.lineEdit_5.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

    ui.lineEdit_4.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    '''
    )

    ui.lineEdit_6.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def validarEmail(ui):
    pass

def cadastrarNovoFuncionario(ui, stackWidget):
    nome = ui.lineEdit_5.text()
    email = ui.lineEdit_4.text()
    cpf = ui.lineEdit_6.text()

    if nome.strip() == "" or email.strip() == "" or cpf.strip() == "":
        errorCampos(ui)
    else:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            cnx = carregarBD()
            cursor = cnx.cursor()
            sql = "INSERT INTO funcionarios(nome, cpf, email, disponivel) VALUES (%s, %s, %s, 1)"
            val = (nome, email, cpf)

            cursor.execute(sql, val)
            cnx.commit()

            stackWidget.setCurrentIndex(2)
        else:
            ui.lineEdit_4.setStyleSheet('''
            QLineEdit {
            border: 2px solid red;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: #374151;
            }
            ''')

def configTelaFuncionarioCadastro(stackWidget):
    ui = uic.loadUi("Telas/funcionario_cadastro.ui")

    stackWidget.addWidget(ui)

    ui.pushButton.clicked.connect(lambda: cadastrarNovoFuncionario(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget, ui))
