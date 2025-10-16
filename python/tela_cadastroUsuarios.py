from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from bancoDados import carregarBD

def excluirUsuario(ui, stackWidget, usuario_id):
    try:
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Você tem certeza que quer excluir esse usuário ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resposta = msg.exec_()
        if resposta == QMessageBox.Ok:
            cnx = carregarBD()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
            cnx.commit()
            cnx.close()
            
            stackWidget.setCurrentIndex(6)

            ui.lineEdit_5.setText("")
            ui.lineEdit_6.setText("")
            ui.comboBox.setCurrentIndex(-1)
            ui.comboBox_2.setCurrentIndex(-1)
            ui.pushButton.setText("Salvar")
            ui.pushButton.clicked.disconnect()
            ui.pushButton.clicked.connect(lambda: registrarNovoUsuario(ui, stackWidget))
            ui.pushButton_2.clicked.disconnect()
            ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))    
    except Exception as e:
        print(f"erro na exclusão usuario: {e}")

def atualizarUsuario(ui, stackWidget, usuario_id):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor(buffered=True)

        login = ui.lineEdit_5.text()
        senha = ui.lineEdit_6.text()
        funcionario = ui.comboBox_2.currentText()
        func = ui.comboBox.currentText()
        if login.strip() == "" or senha.strip() == "" or func == "" or funcionario == "":
            errorCampos(ui)
            return
        
        id_funcionario = 0
        cursor.execute("SELECT id_funcionario, nome FROM funcionarios")
        dadosFuncionarios = cursor.fetchall()
        for _funcio in dadosFuncionarios:
            if funcionario == _funcio[1]:
                id_funcionario = _funcio[0]
        
        sql = "UPDATE usuarios SET id_funcionario = %s, login = %s, senha = %s, função = %s WHERE id_usuario = %s"
        val = (id_funcionario, login, senha, func, usuario_id)
        cursor.execute(sql, val)
        cnx.commit()

        #verificar se o mecanico já foi registrado
        cursor.execute("SELECT * FROM mecanicos WHERE id_funcionario = %s", (id_funcionario,))
        dadosMec = cursor.fetchone()

        if dadosMec:
            print("já era um mecanico")
            #verificando se o usuario atual tinha um mecanico
            cursor.execute("SELECT * FROM mecanicos WHERE id_funcionario = %s", (id_funcionario,))
            dadosMecanico = cursor.fetchone()

            if dadosMecanico:
                cursor.execute("DELETE FROM mecanicos WHERE id_funcionario = %s", (id_funcionario,))
                print("antigo mecanico excluido")
        else:
            if func == "Mecânico":
                sqlComando = "INSERT INTO mecanicos(id_funcionario) VALUES (%s)"
                dadosComando = (id_funcionario,)

                cursor.execute(sqlComando, dadosComando)
                cnx.commit()
        cnx.close()

        stackWidget.setCurrentIndex(6)

        ui.lineEdit_5.setText("")
        ui.lineEdit_6.setText("")
        ui.comboBox.setCurrentIndex(-1)
        ui.comboBox_2.setCurrentIndex(-1)
        ui.pushButton.setText("Salvar")
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registrarNovoUsuario(ui, stackWidget))
        ui.pushButton_2.clicked.disconnect()
        ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))

    except Exception as e:
        print(f"erro na atualização: {e}")

def carregarDadosUsuario(ui, usuario_id, stackWidget):#verificar isso depois
    cnx = carregarBD()
    cursor = cnx.cursor()
    cursor.execute("SELECT id_usuario, id_funcionario, login, senha, função FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    dados = cursor.fetchone()

    if dados:
        ui.lineEdit_5.setText(dados[2])  # login
        ui.lineEdit_6.setText(dados[3])  # senha
        funcao = dados[4]

        index = ui.comboBox.findText(funcao)
        if index != -1:
            ui.comboBox.setCurrentIndex(index)

        cursor.execute("SELECT nome FROM funcionarios WHERE id_funcionario = %s", (dados[1],))
        funcionario = cursor.fetchone()
        if funcionario:
            func_nome = funcionario[0]
            index_func = ui.comboBox_2.findText(func_nome)
            if index_func != -1:
                ui.comboBox_2.setCurrentIndex(index_func)

        ui.pushButton.setText("Atualizar")
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: atualizarUsuario(ui, stackWidget, usuario_id))
        ui.pushButton_2.clicked.disconnect()
        ui.pushButton_2.clicked.connect(lambda: excluirUsuario(ui, stackWidget, usuario_id))

def atualizarTabelas(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()

    if ui.comboBox_2.count() > 0:
        ui.comboBox_2.clear()

    cursor.execute("SELECT nome FROM funcionarios")
    result = cursor.fetchall()

    for i in range(len(result)):
        ui.comboBox_2.addItem(result[i][0])

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

    ui.lineEdit_6.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def voltarTelaUsuario(ui, stackWidget):
    stackWidget.setCurrentIndex(6)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")
    ui.comboBox.setCurrentIndex(-1)
    ui.comboBox_2.setCurrentIndex(-1)

    if ui.pushButton.text() == "Atualizar":
        ui.pushButton.setText("Salvar")
        ui.lineEdit_5.setText("")
        ui.lineEdit_6.setText("")
        ui.comboBox.setCurrentIndex(-1)
        ui.comboBox_2.setCurrentIndex(-1)
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registrarNovoUsuario(ui, stackWidget))
        ui.pushButton_2.clicked.disconnect()
        ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))

def funcionarioComboBox(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()
    cursor.execute("SELECT nome FROM funcionarios")
    result = cursor.fetchall()

    for i in range(len(result)):
        ui.comboBox_2.addItem(result[i][0])

def registrarNovoUsuario(ui, stackWidget):
    login = ui.lineEdit_5.text()
    senha = ui.lineEdit_6.text()
    funcionario = ui.comboBox_2.currentText()
    func = ui.comboBox.currentText()

    if login.strip() == "" or senha.strip() == "" or func == "" or funcionario == "":
        errorCampos(ui)
    else:
        cnx = carregarBD()
        cursor = cnx.cursor()
        id_funcionario = 0
        cursor.execute("SELECT id_funcionario, nome FROM funcionarios")
        dadosFuncionarios = cursor.fetchall()
        for _funcio in dadosFuncionarios:
            if funcionario == _funcio[1]:
                id_funcionario = _funcio[0]

        sql = "INSERT INTO usuarios(id_funcionario, login, senha, função, primeiroAcesso) VALUES (%s, %s, %s, %s, %s)"
        val = (id_funcionario, login, senha, func, 1)
        cursor.execute(sql, val)
        cnx.commit()

        if func == "Mecânico":
            sqlComando = "INSERT INTO mecanicos(id_funcionario) VALUES (%s)"
            dadosComando = (id_funcionario,)

            cursor.execute(sqlComando, dadosComando)
            cnx.commit()

        stackWidget.setCurrentIndex(6)

        ui.lineEdit_5.setText("")
        ui.lineEdit_6.setText("")
        ui.comboBox.setCurrentIndex(-1)
        ui.comboBox_2.setCurrentIndex(-1)

def configTelaUsuariosCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_cadastro_usuario.ui")

    stackWidget.addWidget(ui)
    funcionarioComboBox(ui)

    ui.pushButton.clicked.connect(lambda: registrarNovoUsuario(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))