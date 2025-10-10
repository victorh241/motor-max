from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import re
from bancoDados import carregarBD

#TODO: fazer os campos vazios

def atualizarDadosFuncionario(ui, id_funcionario, stackWidget):
    cnx = carregarBD()
    cursor = cnx.cursor()

    ui.pushButton.setText("Atualizar")
    nome = ui.lineEdit_5.text()
    email = ui.lineEdit_4.text()
    cpf = ui.lineEdit_6.text()

    if nome.strip() == "" or email.strip() == "" or cpf.strip() == "":
        errorCampos(ui)
    else:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            sql = "UPDATE funcionarios SET nome = %s, email = %s, cpf = %s WHERE id_funcionario = %s"
            val = (nome, email, cpf, id_funcionario)

            cursor.execute(sql, val)
            cnx.commit()

            ui.lineEdit_5.setText("")
            ui.lineEdit_4.setText("")
            ui.lineEdit_6.setText("")

            ui.pushButton.clicked.disconnect()
            ui.pushButton.clicked.connect(lambda: cadastrarNovoFuncionario(ui, stackWidget))
            ui.pushButton.setText("Salvar")
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

def carregarDadosFuncionario(ui, id_funcionario, stackWidget):
    cnx = carregarBD()
    cursor = cnx.cursor()

    cursor.execute("SELECT nome, email, cpf FROM Funcionarios WHERE id_funcionario = %s", (id_funcionario,))
    dados = cursor.fetchone() #Explicação isso serve para pegar apenas um resultado
    if dados:
        ui.lineEdit_5.setText(dados[0])
        ui.lineEdit_4.setText(dados[1])
        ui.lineEdit_6.setText(dados[2])

    ui.pushButton.setText("Atualizar")

    ui.pushButton.clicked.disconnect()
    ui.pushButton.clicked.connect(lambda: atualizarDadosFuncionario(ui, id_funcionario, stackWidget))

def voltarTelaPrincipal(stackWidget, ui):
    ui.lineEdit_5.setText("")
    ui.lineEdit_4.setText("")
    ui.lineEdit_6.setText("")
    

    stackWidget.setCurrentIndex(2)
    camposSemErro(ui)

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(2)

    ui.lineEdit_5.setText("")
    ui.lineEdit_4.setText("")
    ui.lineEdit_6.setText("")
    camposSemErro(ui)

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

def camposSemErro(ui):
    ui.lineEdit_5.setStyleSheet('''
    QLineEdit[echoMode="2"], QLineEdit[echoMode="0"] {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #374151;
            }
        QLineEdit:focus{
        border: 2px solid #7f8082;
        }

        QLineEdit:hover{
        background-color: rgb(234, 236, 240);
        }
    ''')

    ui.lineEdit_4.setStyleSheet('''
    QLineEdit[echoMode="2"], QLineEdit[echoMode="0"] {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #374151;
            }
        QLineEdit:focus{
        border: 2px solid #7f8082;
        }

        QLineEdit:hover{
        background-color: rgb(234, 236, 240);
        }
    ''')

    ui.lineEdit_6.setStyleSheet('''
    QLineEdit[echoMode="2"], QLineEdit[echoMode="0"] {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #374151;
            }
        QLineEdit:focus{
        border: 2px solid #7f8082;
        }

        QLineEdit:hover{
        background-color: rgb(234, 236, 240);
        }
    ''')

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
            val = (nome, cpf, email)

            cursor.execute(sql, val)
            cnx.commit()

            stackWidget.setCurrentIndex(2)
            ui.lineEdit_5.setText("")
            ui.lineEdit_4.setText("")
            ui.lineEdit_6.setText("")
            camposSemErro(ui)
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
