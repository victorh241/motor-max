from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD

def atualizarVeiculo(stackWidget, ui, id_veiculo):
    placa = ui.lineEdit_5.text()
    ano = ui.lineEdit_6.text()
    marca = ui.lineEdit_7.text()
    modelo = ui.lineEdit_8.text()
    clienteNome = ui.comboBox.currentText()

    cnx = carregarBD()
    cursor = cnx.cursor()
    if placa.strip() == "" or ano.strip() == "" or marca.strip() == "" or modelo.strip() == "" or clienteNome == "":
        erroCampos(ui)
    else:
        cursor.execute("SELECT id_cliente, nome FROM clientes")
        dadosCliente = cursor.fetchall()
        id_cliente = 0
        for _cliente in dadosCliente:
            if _cliente[1] == clienteNome:
                id_cliente = _cliente[0]
        
        sql = "UPDATE veiculos SET id_cliente = %s, placa = %s, ano = %s, marca = %s, modelo = %s WHERE id_veiculo = %s"
        dadosVeiculos = (id_cliente, placa, ano, marca, modelo, id_veiculo)
        cursor.execute(sql, dadosVeiculos)
        cnx.commit()

        stackWidget.setCurrentIndex(4)


def carregarDadosVeiculo(ui, id_veiculo, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_veiculo, id_cliente, placa, ano, modelo, marca FROM veiculos WHERE id_veiculo = %s", (id_veiculo,))
        dadosVeiculo = cursor.fetchone()

        if dadosVeiculo:
            ui.lineEdit_5.setText(dadosVeiculo[2])  # placa
            ui.lineEdit_6.setText(str(dadosVeiculo[3]))  # ano
            ui.lineEdit_7.setText(dadosVeiculo[5])  # marca
            ui.lineEdit_8.setText(dadosVeiculo[4])  # modelo

            # Carregar o nome do cliente no comboBox
            cursor.execute("SELECT nome FROM clientes WHERE id_cliente = %s", (dadosVeiculo[1],))
            cliente = cursor.fetchone()

            ui.comboBox.clear()
            if cliente:
                ui.comboBox.addItem(cliente[0])
            
            ui.pushButton.setText("Atualizar")
            ui.pushButton.disconnect()
            ui.pushButton.clicked.connect(lambda: atualizarVeiculo(stackWidget, ui, id_veiculo))
    except Exception as e:
        print(f"Erro ao carregar dados do veiculo: {e}")

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
    try:
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

            ui.lineEdit_5.setText("")
            ui.lineEdit_6.setText("")
            ui.lineEdit_7.setText("")
            ui.lineEdit_8.setText("")
            stackWidget.setCurrentIndex(4)
    except Exception as e:
        print(f"Erro: {e}")

def configTelaVeiculosCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_veiculos_cadastro.ui")

    stackWidget.addWidget(ui)
    configComboBoxCliente(ui)

    ui.pushButton.clicked.connect(lambda: registrarNovoVeiculo(stackWidget, ui))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTela(ui ,stackWidget))