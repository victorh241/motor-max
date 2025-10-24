from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QDoubleValidator
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

    #formatar valor
    textoLimpo = valor.replace('.', '').replace('R$', '').replace(',', '.')
    valorServico = float(textoLimpo)

    if descrição.strip() == "" or valor.strip() == "":
        campoErro(ui)
    else:
        cursor = cnx.cursor()

        sqlCommand = "INSERT INTO serviços(descrição, valorMaoObra) VALUES (%s, %s)"
        dados = (descrição, valorServico)
        cursor.execute(sqlCommand, dados)
        cnx.commit()
        
        ui.lineEdit_5.setText("")
        ui.lineEdit_6.setText("")
        stackWidget.setCurrentIndex(5)

def textoPreco(ui):
    texto = ui.lineEdit_6.text()

    sinais_bloqueados = ui.lineEdit_6.blockSignals(True)

    textoLimpo = texto.replace('R$', '').replace('.', '').replace(',', '').strip()

    if not textoLimpo:
        ui.lineEdit_6.setText("")
        return
    
    valor_centavos = int(textoLimpo)

    valor_reais = valor_centavos / 100.00

    texto_formatado = f"R$ {valor_reais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    ui.lineEdit_6.setText(texto_formatado)

    ui.lineEdit_6.blockSignals(sinais_bloqueados)

def configCadastroServico(stackWidget):
    ui = uic.loadUi("Telas/tela_serviços_cadastro.ui")

    stackWidget.addWidget(ui)

    ui.pushButton.clicked.connect(lambda: registrarVeiculos(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTela(ui ,stackWidget))

    validator = QDoubleValidator()
    validator.setRange(0.00, 999999.99)
    validator.setDecimals(2)

    ui.lineEdit_6.setValidator(validator)

    ui.lineEdit_6.textChanged.connect(lambda: textoPreco(ui))