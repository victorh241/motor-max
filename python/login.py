from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QWidget, QProgressBar, QLabel, QFrame 
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, Qt
import user
import mysql.connector
from bancoDados import carregarBD

#concluido
def dados_usuarios() -> list:
    db = carregarBD()
    lista = []

    cursor = db.cursor()
    cursor.execute("SELECT login, senha, função FROM usuarios")
    result = cursor.fetchall()

    for i in range(len(result)):
        lista.append({'login': result[i][0], 'senha': result[i][1], 'acesso': result[i][2]})
    
    return lista

def barraProgressoConfig(ui):
    ui.progressBar.show()
    ui.progressBar.setRange(0, 0)
    ui.pushButton.setEnabled(False)
    ui.pushButton.setDisabled(True)
    ui.pushButton_2.setEnabled(False)
    ui.pushButton_2.setDisabled(True)
    ui.lineEdit.setDisabled(True)
    ui.lineEdit_2.setDisabled(True)
    ui.lineEdit.setEnabled(False)
    ui.lineEdit.setEnabled(False)

def entrarButton(ui, stackWidget):
    barraProgressoConfig(ui)
    QTimer.singleShot(2000,lambda: autenticarUsuario(ui, stackWidget))

def senhaErrada(ui):
    ui.progressBar.hide()
    ui.pushButton.setEnabled(True)
    ui.pushButton.setDisabled(False)
    ui.pushButton_2.setEnabled(True)
    ui.pushButton_2.setDisabled(False)
    ui.lineEdit.setDisabled(False)
    ui.lineEdit_2.setDisabled(False)
    ui.lineEdit.setEnabled(True)
    ui.lineEdit.setEnabled(True)

    ui.label_2.show()
    ui.label_4.show()

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

def autenticarUsuario(ui, stackWidget):
    dados = dados_usuarios()
    usuario = ui.lineEdit.text()
    senha = ui.lineEdit_2.text()
    
    for userAtual in dados:
        if userAtual['login'] == usuario.strip() and userAtual['senha'] == senha.strip():
            acesso = userAtual['acesso']
            user.lvlPermiUserAtual = acesso
            stackWidget.setCurrentIndex(1)
        else:
            senhaErrada(ui)

def mostrarSenha(ui):
    if ui.lineEdit_2.echoMode() == QLineEdit.EchoMode.Password:
        ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Normal)
        closedEyeIcon = QIcon("imagem/icons/eye_closed.png")
        ui.pushButton_3.setIcon(closedEyeIcon)
    else:
        openEye = QIcon("imagem/icons/eye_open.png")
        ui.pushButton_3.setIcon(openEye)
        ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

def telaReperarSenha(stackWidget):
    stackWidget.setCurrentIndex(15)

def configLogin(stackWidget):
    ui = uic.loadUi("Telas/Tela_login.ui")

    stackWidget.addWidget(ui)
    ui.progressBar.hide()
    ui.label_2.hide()
    ui.label_4.hide()

    ui.pushButton.clicked.connect(lambda: entrarButton(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: mostrarSenha(ui))
    ui.pushButton_2.clicked.connect(lambda: telaReperarSenha(stackWidget))