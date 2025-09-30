from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import user
from bancoDados import carregarBD

#concluido

def dados() -> list:
    cnx = carregarBD()
    lista = []
    cursor = cnx.cursor()
    cursor.execute("SELECT login FROM usuarios")
    result = cursor.fetchall()
    for i in result:
        lista.append(i[0])
    
    return lista

def voltarParaTelaLogin(ui ,stackWidget):
    ui.lineEdit.setText("")
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

def novaSenhaTela(ui , stackWidget):
    dadosLogin = dados()
    loginText = ui.lineEdit.text()

    for login in dadosLogin:
        if loginText.strip() == login:
            user.login = login
            stackWidget.setCurrentIndex(16)
        else:
            erro(ui)

def configTelaRecuperar(stackWidget):
    ui = uic.loadUi("Telas/tela_recuperar_senha.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_2.clicked.connect(lambda: voltarParaTelaLogin(ui ,stackWidget))
    ui.pushButton.clicked.connect(lambda: novaSenhaTela(ui, stackWidget))