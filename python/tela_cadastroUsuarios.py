from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD

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

    ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))

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

        sql = "INSERT INTO usuarios(id_funcionario, login, senha, função) VALUES (%s, %s, %s, %s)"
        val = (id_funcionario, login, senha, func)
        cursor.execute(sql, val)
        cnx.commit()

        if func == "Mecânico":
            novoId_funcionario = cursor.lastrowid
            sqlComando = "INSERT INTO mecanicos(id_funcionario) VALUES (%s)"
            dadosComando = (novoId_funcionario,)

            cursor.execute(sqlComando, dadosComando)
            cnx.commit()

        stackWidget.setCurrentIndex(6)


def configTelaUsuariosCadastro(stackWidget):
    global ui
    ui = uic.loadUi("Telas/tela_cadastro_usuario.ui")

    stackWidget.addWidget(ui)
    funcionarioComboBox(ui)

    ui.pushButton.clicked.connect(lambda: registrarNovoUsuario(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaUsuario(ui, stackWidget))