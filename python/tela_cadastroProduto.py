from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD
import random
import string

def atualizarProduto(ui, stackWidget, id_produto):
    cnx = carregarBD()
    descricao = ui.lineEdit.text()
    codigoProduto = ui.lineEdit_3.text()
    preco = ui.lineEdit_2.text()
    quantidade_emEstoque = ui.lineEdit_4.text()

    if descricao.strip() == "" or codigoProduto.strip() == "" or preco.strip() == "" or quantidade_emEstoque.strip() == "":
        erro(ui)
    else:
        cursor = cnx.cursor()

        sqlComando = "UPDATE produtos SET descrição = %s, codigo_produto = %s, preco_unitario = %s, em_estoque = %s WHERE id_produto = %s"
        dados = (descricao, codigoProduto, preco, quantidade_emEstoque, id_produto)
        cursor.execute(sqlComando, dados)
        cnx.commit()

        stackWidget.setCurrentIndex(7)
        ui.pushButton.setText("Salvar")
        ui.pushButton.clicked.disconnect()
        ui.pushButton.clicked.connect(lambda: registraProduto(ui, stackWidget, id_produto))
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_4.setText("")

def carregarProduto(ui, stackWidget, id_produto):
    cnx = carregarBD()
    cursor = cnx.cursor()

    cursor.execute("SELECT codigo_produto, descrição, preco_unitario, em_estoque FROM produtos WHERE id_produto = %s", (id_produto,))
    dadosProduto = cursor.fetchone()
    cnx.close()

    ui.lineEdit.setText(dadosProduto[1])
    ui.lineEdit_3.setText(dadosProduto[0])
    ui.lineEdit_2.setText(str(dadosProduto[2]))
    ui.lineEdit_4.setText(str(dadosProduto[3]))

    ui.pushButton.setText("Atualizar")
    ui.pushButton.clicked.disconnect()
    ui.pushButton.clicked.connect(lambda: atualizarProduto(ui, stackWidget, id_produto))

def voltarTelaPrincipal(ui ,stackWidget):
    stackWidget.setCurrentIndex(7)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_4.setText("")

    if ui.pushButton.text() == "Atualizar":
        ui.pushButton.setText("Salvar")

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(7)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_3.setText("")
    ui.lineEdit_4.setText("")

    if ui.pushButton.text() == "Atualizar":
        ui.pushButton.setText("Salvar")

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

    ui.lineEdit_3.setStyleSheet('''
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
    ''')

def gere_codigo_produto() -> str:
    """Generate a random string of fixed length."""
    letters = "".join(random.choice(string.ascii_letters) for _ in range(2))
    digits = "".join(random.choice(string.digits) for _ in range(4))
    return f"{letters}-{digits}"

def atualizarCodigo(ui):
    codigo = gere_codigo_produto()

    ui.lineEdit_3.setText(codigo)

def configCodigoProduto(ui):
    codigo = gere_codigo_produto()

    ui.lineEdit_3.setText(codigo)
    ui.lineEdit_3.setDisabled(True)

def registraProduto(ui, stackWidget):
    cnx = carregarBD()
    descricao = ui.lineEdit.text()
    codigoProduto = ui.lineEdit_3.text()
    preco = ui.lineEdit_2.text()
    quantidade_emEstoque = ui.lineEdit_4.text()

    if descricao.strip() == "" or codigoProduto.strip() == "" or preco.strip() == "" or quantidade_emEstoque.strip() == "":
        erro(ui)
    else:
        cursor = cnx.cursor()

        sqlComando = "INSERT INTO produtos(codigo_produto, descrição, preco_unitario, em_estoque) VALUES (%s, %s, %s, %s)"
        dados = (codigoProduto, descricao, preco, quantidade_emEstoque)
        cursor.execute(sqlComando, dados)
        cnx.commit()

        stackWidget.setCurrentIndex(7)
        ui.lineEdit.setText("")
        ui.lineEdit_2.setText("")
        ui.lineEdit_4.setText("")

def configTelaProdutoCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_produtos_cadastro.ui")

    stackWidget.addWidget(ui)
    configCodigoProduto(ui)

    ui.pushButton.clicked.connect(lambda: registraProduto(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(ui ,stackWidget))