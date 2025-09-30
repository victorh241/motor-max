from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon
from bancoDados import carregarBD
import user

def voltarLogin(ui ,stackWidget):
    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    stackWidget.setCurrentIndex(0)

def erro(ui):
    ui.lineEdit.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

    ui.lineEdit_2.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def atulizarSenha(stackWidget, ui):
    novaSenhaText = ui.lineEdit.text()
    repSenha = ui.lineEdit_2.text()

    if novaSenhaText.strip() == "" or repSenha.strip() == "":
        erro(ui)
    else:
        if novaSenhaText.strip() == repSenha.strip():
            cnx = carregarBD()
            cursor = cnx.cursor()
            id_usuario = 0
            comandoId = ("SELECT id_usuario FROM usuarios WHERE login = %s")
            dadosId = user.login
            val = (dadosId,)
            cursor.execute(comandoId, val)
            resultadoId = cursor.fetchall()
            for i in resultadoId:
                id_usuario = i[0]

            comando = "UPDATE usuarios SET senha = %s WHERE id_usuario = %s"
            dados = (repSenha, id_usuario)

            cursor.execute(comando, dados)
            cnx.commit()

            stackWidget.setCurrentIndex(0)

def configNovaSenha(stackWidget):
    ui = uic.loadUi("Telas/Tela_nova_senha.ui")

    stackWidget.addWidget(ui)

    ui.pushButton.clicked.connect(lambda: atulizarSenha(stackWidget, ui))
    ui.pushButton_2.clicked.connect(lambda: voltarLogin(ui ,stackWidget))
