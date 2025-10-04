from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD
import random
import string

def carregarProduto(ui, stackWidget, id_produto):
    pass

def voltarTelaPrincipal(ui ,stackWidget):
    stackWidget.setCurrentIndex(7)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_3.setText("")
    ui.lineEdit_4.setText("")

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(7)

    ui.lineEdit.setText("")
    ui.lineEdit_2.setText("")
    ui.lineEdit_3.setText("")
    ui.lineEdit_4.setText("")

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


def configTelaProdutoCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela_produtos_cadastro.ui")

    stackWidget.addWidget(ui)
    configCodigoProduto(ui)

    ui.pushButton.clicked.connect(lambda: registraProduto(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(ui ,stackWidget))