from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import re
from bancoDados import carregarBD
from listaTelefone import listaTelefone
import traceback

#TODO: erro na hora de registrar o mecanico resolva

def excluirCliente(ui, stackWidget, id_cliente):
    cnx = carregarBD()
    cursor = cnx.cursor()
    msg = QMessageBox()
    msg.setWindowTitle("Aviso !")
    msg.setText("Você tem certeza que quer excluir esse cliente ?")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    respota = msg.exec_()
    if respota == QMessageBox.Ok:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM telefones WHERE id_cliente = %s", (id_cliente,))
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cnx.commit()

        stackWidget.setCurrentIndex(3)

        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_3.setText("")
        ui.comboBox_2.clear()
        ui.lineEdit_7.setText("")
        ui.pushButton.setText("Salvar")
        ui.frame_3.hide()
        ui.pushButton_2.clicked.disconnect()
        ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))

def atualizarCliente(ui, clienteId, stackWidget):
    cnx = carregarBD()
    cursor = cnx.cursor()

    nome = ui.lineEdit.text()
    email = ui.lineEdit_2.text()
    cpf = ui.lineEdit_3.text()
    novoTelefone = ui.lineEdit_7.text()
    qntOpcoesTelefones = ui.comboBox_2.count()

    if nome.strip() == "" or email.strip() == "" or cpf.strip() == "" or novoTelefone.strip() == "" or qntOpcoesTelefones == 0:
        erroCampos(ui)
    else:
        #cliente
        sql = "UPDATE Clientes SET nome = %s, email = %s, cpf = %s WHERE id_cliente = %s"
        valores = (nome, email, cpf, clienteId)

        cursor.execute(sql, valores)
        cnx.commit()

        #telefone
        cursor.execute("SELECT id_telefone FROM telefones WHERE id_cliente = %s", (clienteId,))
        dadosTelefone = cursor.fetchall()

        listaTelefone[ui.comboBox_2.count() - 1] = ui.lineEdit_7.text()
        for i in range(len(listaTelefone)):
            print(listaTelefone[i], dadosTelefone[i][0])
            sqlTelefone = "UPDATE telefones SET telefone = %s WHERE id_telefone = %s"
            valoresTelefone = (listaTelefone[i] , dadosTelefone[i][0])
            cursor.execute(sqlTelefone, valoresTelefone)
            cnx.commit()

            cnx.close()
            
            ui.pushButton.clicked.disconnect()
            ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
            ui.lineEdit.setText("")
            ui.lineEdit_2.setText("")
            ui.lineEdit_3.setText("")
            ui.comboBox_2.clear()
            ui.lineEdit_7.setText("")
            ui.pushButton.setText("Salvar")
            ui.frame_3.hide()
            ui.pushButton_2.clicked.disconnect()
            ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))

        stackWidget.setCurrentIndex(3)

def carregarDadosCliente(ui, clienteId, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()

        cursor.execute("SELECT nome, cpf, email FROM Clientes WHERE id_cliente = %s", (clienteId,))
        dadosCliente = cursor.fetchone()

        if dadosCliente:
            ui.lineEdit.setText(dadosCliente[0])  # nome
            ui.lineEdit_2.setText(dadosCliente[2])  # email
            ui.lineEdit_3.setText(dadosCliente[1])  # cpf

            # nome do butão
            ui.pushButton.setText("Atualizar")
            ui.pushButton.clicked.disconnect()
            ui.pushButton.clicked.connect(lambda: atualizarCliente(ui, clienteId, stackWidget))
            ui.pushButton_2.clicked.disconnect()
            ui.pushButton_2.clicked.connect(lambda: excluirCliente(ui, stackWidget, clienteId))

            cursor.execute("SELECT telefone FROM telefones WHERE id_cliente = %s", (clienteId,))
            telefones = cursor.fetchall()
            listaTelefone.clear()
            ui.frame_3.show()
            ui.comboBox_2.clear()
            for _telefone in telefones:
                listaTelefone.append(_telefone[0])
                novoIndex = ui.comboBox_2.count() + 1
                ui.comboBox_2.addItem(f"telefone {novoIndex}")
                ui.comboBox_2.setCurrentIndex(novoIndex - 1)
                ui.lineEdit_7.setText(_telefone[0])
    except Exception as e:
        print(f"Erro ao carregar dados do cliente: {e}")

#region outros butões
def voltarTelaPrincipal(ui, stackWidget):
    stackWidget.setCurrentIndex(3)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_3.setText("")
    ui.comboBox_2.clear()
    ui.lineEdit_7.setText("")
    ui.frame_3.hide()

    if  ui.pushButton.text() == "Atualizar":
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_3.setText("")
        ui.comboBox_2.clear()
        ui.lineEdit_7.setText("")
        ui.pushButton.setText("Salvar")
        ui.frame_3.hide()
        ui.pushButton_2.clicked.disconnect()
        ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(3)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_3.setText("")
    ui.comboBox_2.clear()
    ui.lineEdit_7.setText("")
    ui.frame_3.hide()

    if ui.pushButton.text() == "Atualizar":
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_3.setText("")
        ui.comboBox_2.clear()
        ui.lineEdit_7.setText("")
        ui.pushButton.setText("Salvar")
        ui.frame_3.hide()
#endregion

def erroCampos(ui):
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
    '''
    )

    ui.lineEdit_3.setStyleSheet('''
    QLineEdit {
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #374151;
    }
    ''')

def mensagemEmail(ui):
    msg = QMessageBox()
    msg.setWindowTitle("Aviso !")
    msg.setText("O email que você inseriu já está em uso!")
    msg.setStandardButtons(QMessageBox.Ok)
    resposta = msg.exec_()
    
    ui.lineEdit_2.setStyleSheet('''
    QLineEdit{
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

def mensagemCpf(ui):
    try:
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Esse Cpf já está sendo usado")
        msg.StandardButton(QMessageBox.Ok)
        resposta = msg.exec_()
        ui.lineEdit_3.setStyleSheet('''
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
    except Exception as e:
        print(f"Erro na verificação de cpf {e}")
        traceback.print_exc()

def registrarNovoCliente(ui, stackWidget):
    #cliente
    cnx = carregarBD()
    cursor = cnx.cursor()
    nome = ui.lineEdit.text()
    email = ui.lineEdit_2.text()
    cpf = ui.lineEdit_3.text()
    novoTelefone = ui.lineEdit_7.text()

    cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
    dadosEmail = cursor.fetchone()

    #verificar se o email ja foi registrado
    if dadosEmail:
        mensagemEmail(ui)
        return

    #verificar se o cpf ja foi registrado
    cursor.execute("SELECT * FROM clientes WHERE cpf = %s", (cpf,))
    dadosCpf = cursor.fetchone()

    if dadosCpf:
        mensagemCpf(ui)
        return

    qntOpcoesTelefones = ui.comboBox_2.count()
    if nome.strip() == "" or email.strip() == "" or cpf.strip() == "" or novoTelefone.strip() == "" or qntOpcoesTelefones == 0:
        erroCampos(ui)
        return
    
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        cursor = cnx.cursor()
        #cliente
        comandoCliente = "INSERT INTO Clientes(cpf, nome, email) VALUES (%s, %s, %s)"
        dadosCliente = (cpf, nome, email)
        cursor.execute(comandoCliente, dadosCliente)
        cnx.commit()

        cursor.execute("SELECT id_cliente, nome FROM Clientes")
        listaCliente = cursor.fetchall()
        id_cliente = 0
        for i in listaCliente:
            if i[1] == nome:
                id_cliente = i[0]

        #telefones
        if ui.comboBox_2.count() == 1:
            comandoTelefone = "INSERT INTO telefones(id_cliente, telefone) VALUES (%s ,%s)"
            dadosTelefone = (id_cliente, novoTelefone)
            cursor.execute(comandoTelefone, dadosTelefone)
            cnx.commit()
        else:
            listaTelefone.append(novoTelefone)
            for _telefone in listaTelefone:
                comandoTelefone = "INSERT INTO telefones(id_cliente, telefone) VALUES (%s ,%s)"
                dadosTelefone = (id_cliente, _telefone)
                cursor.execute(comandoTelefone, dadosTelefone)
                cnx.commit()
        
        stackWidget.setCurrentIndex(3)
        ui.frame_3.hide()
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_3.setText("")
        ui.comboBox_2.clear()
        ui.lineEdit_7.setText("")
    else:
        ui.lineEdit_2.setStyleSheet('''
        QLineEdit {
        border: 2px solid red;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        color: #374151;
        }
        ''')

def salvarTextoEditado(ui):
    if ui.comboBox_2.count() > 1 and len(ui.lineEdit_7.text()) == 15:
        indexAtual = ui.comboBox_2.currentIndex()
        novoIndex = ui.comboBox_2.count() - 1

        if indexAtual != novoIndex:
            listaTelefone[indexAtual] = ui.lineEdit_7.text()

def mudaTextoTelefone(ui):
    novoIndex = ui.comboBox_2.count() - 1
    indexAtual = ui.comboBox_2.currentIndex()
    if ui.comboBox_2.count() > 1:
        
        if indexAtual != novoIndex:
            print(indexAtual)
            ui.lineEdit_7.setText(listaTelefone[indexAtual])
        else:
            if ui.pushButton.text() == "Atualizar":
                ui.lineEdit_7.setText("")
            else:
                ui.lineEdit_7.setText(listaTelefone[novoIndex])

def excluirTelefone(ui):
    itemAtual = ui.comboBox_2.currentIndex()

    ui.comboBox_2.removeItem(itemAtual)
    qntOpcoes = ui.comboBox_2.count()

    if qntOpcoes == 0:
        ui.frame_3.hide()
        ui.lineEdit_7.setText("")

def exibirFrameTelefone(ui):
    ui.frame_3.show()
    novoTelefone = ui.lineEdit_7.text()
    ui.lineEdit_7.setText("")
    ui.comboBox_2.addItem(f"telefone {ui.comboBox_2.count() + 1}")
    novoIndex = ui.comboBox_2.count() - 1
    ui.comboBox_2.setCurrentIndex(novoIndex)

    if ui.comboBox_2.count() > 1:
        listaTelefone.append(novoTelefone)

def configClienteCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_cliente_cadastro.ui")

    stackWidget.addWidget(ui)
    ui.frame_3.hide()

    ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(ui,stackWidget))
    ui.pushButton_4.clicked.connect(lambda: exibirFrameTelefone(ui))
    ui.pushButton_5.clicked.connect(lambda: excluirTelefone(ui))

    ui.comboBox_2.currentIndexChanged.connect(lambda: mudaTextoTelefone(ui))
    ui.lineEdit_7.textEdited.connect(lambda: salvarTextoEditado(ui))