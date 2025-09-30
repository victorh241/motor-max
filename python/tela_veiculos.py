from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel

from bancoDados import carregarBD
#função de carregar Dados no cadastro

def mostrarVeiculos(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        dados = cursor.execute("SELECT id_veiculo, id_cliente, placa, ano, modelo, marca FROM veiculos")

        for index, _veiculo in enumerate(dados):
            frame = QFrame()

            cursor.execute("SELECT nome FROM clientes WHERE id_cliente = %s", (dados[1],))
            nomeCliente = cursor.fetchone()[0]


    except Exception as e:
        print("Erro ao conectar ao banco de dados: ", e)
        return

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaCadastro(stackWidget):
    stackWidget.setCurrentIndex(14)

def configTelaVeiculos(stackWidget):
    ui = uic.loadUi("Telas/tela_veiculos.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaCadastro(stackWidget))