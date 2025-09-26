from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD

def atualizarComboBox(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()

    if ui.comboBox.count() > 0:
        ui.comboBox.clear()

    cursor.execute("SELECT nome FROM clientes")
    result = cursor.fetchall()
    
    for i in result:
        ui.comboBox.addItem(i[0])


def voltarTela(ui ,stackWidget):
    stackWidget.setCurrentIndex(4)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")
    ui.lineEdit_7.setText("")
    ui.lineEdit_8.setText("")
    ui.comboBox.setCurrentIndex(-1)

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(4)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")
    ui.lineEdit_7.setText("")
    ui.lineEdit_8.setText("")
    ui.comboBox.setCurrentIndex(-1)

def erroCampos(ui):
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

    ui.lineEdit_7.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

    ui.lineEdit_8.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def configComboBoxCliente(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()
    
    cursor.execute("SELECT nome FROM clientes")
    result = cursor.fetchall()
    
    for i in result:
        ui.comboBox.addItem(i[0])

def registrarNovoVeiculo(stackWidget, ui):
    cnx = carregarBD()
    placa = ui.lineEdit_5.text()
    ano = ui.lineEdit_6.text()
    marca = ui.lineEdit_7.text()
    modelo = ui.lineEdit_8.text()
    clienteNome = ui.comboBox.currentText()

    cursor = cnx.cursor()

    if placa.strip() == "" or ano.strip() == "" or marca.strip() == "" or modelo.strip() == "" or clienteNome == "":
        erroCampos(ui)
    else:
        id_cliente = 0
        cursor.execute("SELECT id_cliente, nome FROM clientes")
        dadosCliente = cursor.fetchall()
        for _cliente in dadosCliente:
            if _cliente[1] == clienteNome:
                id_cliente = _cliente[0]

        sql = "INSERT INTO veiculos(id_cliente, placa, ano, marca, modelo) VALUES (%s, %s, %s, %s, %s)"
        dadosVeiculos = (id_cliente, placa, ano, marca, modelo)
        cursor.execute(sql, dadosVeiculos)
        cnx.commit()

        stackWidget.setCurrentIndex(4)

def configTelaVeiculosCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_veiculos_cadastro.ui")

    stackWidget.addWidget(ui)
    configComboBoxCliente(ui)

    ui.pushButton.clicked.connect(lambda: registrarNovoVeiculo(stackWidget, ui))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTela(ui ,stackWidget))