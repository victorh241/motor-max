from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD, fechar_coneccao
from tela_cadastroProduto import carregarProduto

def editarProduto(stackWidget, produtoId):
    try:
        stackWidget.setCurrentIndex(13)
        carregarProduto(stackWidget.currentWidget(), stackWidget, produtoId)
    except Exception as e:
        print(f"Erro tentar Editar: {e}")

def excluirProduto(ui, stackWidget, produtoId):
    try:
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Você tem certeza que quer excluir esse produto ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resposta = msg.exec_()
        if resposta == QMessageBox.Ok:
            cnx = carregarBD()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (produtoId,))
            cnx.commit()
            fechar_coneccao()

            ui.tableWidget.setRowCount(0)
            mostrarProdutos(ui, stackWidget)

    except Exception as e:
        print(f"Erro ao Excluir: {e}")

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
                    border: 1px solid;
                    background-color: white;
                }
                                
                QTableWidget::item {
                    padding-top: 5px;
                    padding-left: 25px;
                }
                             
                QScrollBar:vertical{
                 border: none;
                 background: #f0f0f0;
                 width: 12px;
                 margin: 0px;
                 border-radius: 6px;       
                }
                             
                QScrollBar::handle:vertical {
                background: #b0b0b0;
                min-height: 20px;
                border-radius: 6px;
                }
                             
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-origin: margin;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                }
            ''')
        
        for i, produto in enumerate(produtos):
            frame = QFrame()

            #region config do frame
            frame.setFixedSize(970, 100)
            
            frame.setStyleSheet('''
                QFrame{
                    background-color: white;
                    border-radius: 15px;
                    border: 1px solid;
                    }
            ''')
            #endregion

            #region labels
            labelProduto = QLabel(produto[2], frame)
            labelCodigo = QLabel(produto[1],frame)
            labelEstoqueTitulo = QLabel("Estoque: ", frame)
            labelEstoque = QLabel(f"{(str(produto[4]))} Disponível", frame)
            labelValor = QLabel(f"R$ {str(produto[3])}", frame)

            #region config dos labels
            #nome produto essencialmente
            labelProduto.setGeometry(20, 10, 180, 30)
            labelProduto.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 19px;
                }
            ''')

            #codigo
            labelCodigo.setGeometry(20, 40, 110, 30)

            labelCodigo.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 13px;
                font-weight: bold;
                color: rgb(154, 113, 130);
                }
            ''')

            #titulo estoque
            labelEstoqueTitulo.setGeometry(180, 40, 60, 20)

            labelEstoqueTitulo.setStyleSheet('''
                QLabel{
                    Border: none;
                    font-size: 14px;
                    }
            ''')

            #label estoque
            labelEstoque.setGeometry(240, 42, 170, 20)

            labelEstoque.setStyleSheet('''
                QLabel{
                color: rgb(41, 166, 62);
                border: none;
                font-size: 12px;
                font-weight: bold;
                }
            ''')

            #valor 
            labelValor.setGeometry(780, 10, 120, 20)

            labelValor.setStyleSheet('''
                QLabel{
                border: none;
                font-size: 18px;
                font-weight: bold;
                }
            ''')
            #endregion

            #region pushButtons
            botaoEditar = QPushButton("", frame)
            botaoExcluir = QPushButton("", frame)

            #region config buttons
            botaoEditar.setGeometry(880, 10, 30, 30)

            botaoEditar.setIcon(QIcon("imagem/icons/edit.png"))
            botaoEditar.setIconSize(QSize(20, 20))
            botaoEditar.setCursor(Qt.PointingHandCursor)

            botaoEditar.setStyleSheet('''
                QPushButton{
                    border: 1px solid rgba(156, 156, 156, 235);
                    background-color: rgb(255, 255, 255);
                    border-radius: 9px;
                }
                                                        
                QPushButton:hover{
                    background-color:  rgb(234, 236, 240);
                }
                                                        
                                    
                QPushButton:pressed{
                    background-color: rgb(167, 167, 167);
                }
            ''')

            botaoExcluir.setGeometry(920, 10, 30, 30)

            botaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))
            botaoExcluir.setIconSize(QSize(20,20))
            botaoExcluir.setCursor(Qt.PointingHandCursor)

            botaoExcluir.setStyleSheet('''
                QPushButton{
                    border: 1px solid rgba(156, 156, 156, 235);
                    background-color: rgb(255, 255, 255);
                    border-radius: 9px;
                }
                                                        
                QPushButton:hover{
                    background-color:  rgb(234, 236, 240);
                }
                                                        
                                    
                QPushButton:pressed{
                    background-color: rgb(167, 167, 167);
                }
            ''')
            #endregion
            
            #endregion
            #endregion

            tabela.setCellWidget(i, 0, frame)

            botaoEditar.clicked.connect(lambda _, produto_id=produto[0]: editarProduto(stackWidget, produto_id))
            botaoExcluir.clicked.connect(lambda _, produto_id=produto[0]: excluirProduto(ui , stackWidget, produto_id))

        fechar_coneccao()
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