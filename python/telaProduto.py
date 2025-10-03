from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD, fechar_conecxao

def mostrarProdutos(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_produto, codigo_produto, descrição, preco_unitario, em_estoque FROM produtos")
        produtos = cursor.fetchall()

        tabela = ui.tableWidget

        colunas = 1
        tabela.setRowCount(len(produtos))
        tabela.setColumnCount(colunas)

        #tamanho das colunas e linhas
        tabela.setColumnWidth(0, 600)

        for r in range(len(produtos)):
            tabela.setRowHeight(r, 150)
        
        #configs da tabela
        tabela.setHorizontalHeaderLabels([""] * colunas)
        tabela.setVerticalHeaderLabels([""] * tabela.rowCount())
        tabela.horizontalHeader().setVisible(False)
        tabela.verticalHeader().setVisible(False)
        tabela.setShowGrid(False)
        tabela.setFocusPolicy(Qt.NoFocus)
        tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        tabela.setSelectionMode(QTableWidget.NoSelection)

        tabela.setStyleSheet('''
        QTableWidget{
            border: none;
            background-color: white;
        }
                         
        QTableWidget::item{
            padding: 10px;
        }
    ''')
        
        for i, produto in enumerate(produtos):
            frame = QFrame()

            #region config do frame

            #endregion

    except Exception as e:
        print("Erro ao mostrar produtos:", e)

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaCadastro(stackWidget):
    stackWidget.setCurrentIndex(13)

def configTelaProdutos(stackWidget):
    ui = uic.loadUi("Telas/tela_produtos.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaCadastro(stackWidget))