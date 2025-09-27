from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import re
from bancoDados import carregarBD

#TODO: fazer o reporte do campos vazios

#region outros butões
def voltarTelaPrincipal(ui, stackWidget):
    stackWidget.setCurrentIndex(3)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")
    ui.lineEdit_4.setText("")
    ui.comboBox_2.clear()
    ui.lineEdit_7.setText("")
def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(3)

    ui.lineEdit_5.setText("")
    ui.lineEdit_6.setText("")
    ui.lineEdit_4.setText("")
    ui.comboBox_2.clear()
    ui.lineEdit_7.setText("")
#endregion

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

def registrarNovoCliente(ui, stackWidget):
    #cliente
    cnx = carregarBD()
    nome = ui.lineEdit_5.text()
    email = ui.lineEdit_4.text()
    cpf = ui.lineEdit_6.text()
    novoTelefone = ui.lineEdit_7.text()

    qntOpcoesTelefones = ui.comboBox_2.count()
    if nome.strip() == "" or email.strip() == "" or cpf.strip() == "" or novoTelefone.strip() == "" or qntOpcoesTelefones == 0:
        erroCampos(ui)
    else:
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
            if ui.comboBox_2.count() > 0:
                comandoTelefone = "INSERT INTO telefones(id_cliente, telefone) VALUES (%s ,%s)"
                dadosTelefone = (id_cliente, novoTelefone)
                cursor.execute(comandoTelefone, dadosTelefone)
                cnx.commit()
            else:
                telefones = listaTelefones
                for _telefone in telefones:
                    comandoTelefone = "INSERT INTO telefones(id_cliente, telefone) VALUES (%s ,%s)"
                    dadosTelefone = (id_cliente, _telefone)
                    cursor.execute(comandoTelefone, dadosTelefone)
                    cnx.commit()
            
            stackWidget.setCurrentIndex(3)
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

def excluirTelefone(ui):
    itemAtual = ui.comboBox_2.currentIndex()

    ui.comboBox_2.removeItem(itemAtual)
    qntOpcoes = ui.comboBox_2.count()

    if qntOpcoes == 0:
        ui.frame_3.hide()

def exibirFrameTelefone(ui):
    global listaTelefones
    ui.frame_3.show()
    ui.comboBox_2.addItem(f"telefone {ui.comboBox_2.count() + 1}")
    novoIndex = ui.comboBox_2.count() - 1
    ui.comboBox_2.setCurrentIndex(novoIndex)

    listaTelefones = []
    telefoneAtual = ui.lineEdit_7.text()
    if ui.comboBox_2.count() > 0:
        listaTelefones.append(telefoneAtual)

def configClienteCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_cliente_cadastro.ui")

    stackWidget.addWidget(ui)
    ui.frame_3.hide()

    ui.pushButton.clicked.connect(lambda: registrarNovoCliente(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(ui,stackWidget))
    ui.pushButton_4.clicked.connect(lambda: exibirFrameTelefone(ui))
    ui.pushButton_5.clicked.connect(lambda: excluirTelefone(ui))