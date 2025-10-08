from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel, QGraphicsDropShadowEffect, QMessageBox, QTabWidget
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD, fechar_coneccao

#region botões da ordem de serviços
def excluirOrdem(idx, ui):
    pass

def editarOrdem(idx, ui):
    pass
#endregion

#region botões do serviço
def excluirServiço(id_servico, ui):
    #mensagem de confirmação
    try:
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Você tem certeza que quer excluir esse Serviço ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resposta = msg.exec_()
        if resposta == QMessageBox.Ok:
            cnx = carregarBD()
            cursor = cnx.cursor()
            print(id_servico)
            cursor.execute("DELETE FROM Serviços WHERE id_serviço = %s", (id_servico,))
            cnx.commit()
            fechar_coneccao()
    except Exception as e:
        print(f"Erro na exclussão: {e}")

def editarServico(id_servico, ui):
    pass
#endregion

def mudaListagem(idx, ui, stackWidget):
    if idx == 0:
        mostrarOrdemServiço(ui, stackWidget)
    elif idx == 1:
        mostrarServicos(ui,stackWidget)

def tabelasListagem(ui, stackWidget):
    mostrarServicos(ui, stackWidget)
    ui.tabWidget.currentChanged.connect(lambda idx: mudaListagem(idx, ui, stackWidget))

def mostrarOrdemServiço(ui, stackWidget):
    cnx = carregarBD()
    cursor = cnx.cursor()
    cursor.execute("SELECT id_ordemServiço, id_serviço, codigo, status, deconto, agendamento, quantidade_produtos, quantidade_serviços FROM `Ordem de Serviços`")
    dadosOrdem = cursor.fetchall()

    tabela = ui.tableWidget_2

    for idx, _os in enumerate(dadosOrdem):
        #region dados
        cursor.execute("SELECT id_produto, descrição, valorMaoObra FROM serviço WHERE id_serviço = %s", (_os[1]))
        dadosServico = cursor.fetchone()

        cursor.execute("SELECT FROM WHERE id_produto = %s", (dadosServico[0]))
        dadosProduto = cursor.fetchone()

        cursor.execute("SELECT `valor final` FROM WHERE id_ordem = %s", (_os[0]))
        dadosVendaFinal = cursor.fetchone()
        #endregion

        frame = QFrame()
    

def mostrarServicos(ui, stackWidget):#mostrar baseado no conteiner tab
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()

        cursor.execute("SELECT id_serviço , descrição, valorMaoObra FROM serviços")
        resultados = cursor.fetchall()

        tabela = ui.tableWidget #essa é a tabela do serviço

        colunas = 1
        tabela.setRowCount(len(resultados))
        tabela.setColumnCount(colunas)

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
                padding: 10px;
            }
        ''')

        for idx, _servico in enumerate(resultados):
            frame = QFrame()

            #region configurações do frame
            frame.setFixedSize(970, 60)

            frame.setStyleSheet('''
                QFrame{
                    background-color: white;
                    border-radius: 15px;
                    border: 1px solid;
                    }
            ''')
            #endregion

            #labels

            #region labels
            labelDescricao = QLabel(_servico[1], frame)
            labelValor = QLabel(f"R$ {_servico[2]:.2f}", frame)

            labelDescricao.setGeometry(10, 10, 220, 20)
            labelValor.setGeometry(830, 10, 120, 20)

            labelDescricao.setStyleSheet('''
                QLabel{
                    font-size: 18px;
                    border: none;
                    background-color: transparent;
                }
            ''')

            labelValor.setStyleSheet('''
                QLabel{
                    font-size: 18px;
                    border: none;
                    background-color: transparent;
                }
            ''')
            #endregion

            #region push botão
            butaoExcluir = QPushButton("", frame)

            #region config
            butaoExcluir.setGeometry(920, 5, 30, 30)

            butaoExcluir.setCursor(Qt.PointingHandCursor)

            butaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))
            butaoExcluir.setIconSize(QSize(20, 20))

            butaoExcluir.setStyleSheet('''
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

            row = idx // colunas
            column = idx % colunas

            ui.tableWidget.setCellWidget(row, column, frame)

            butaoExcluir.clicked.connect(lambda _, idx = _servico[0]: excluirServiço(idx, ui))
    except Exception as e:
        print(f"Erro ao carregar componentes: {e}")

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaServicoCadastro(stackWidget):
    stackWidget.setCurrentIndex(10)

def telaOrdemCadastro(stackWidget):
    stackWidget.setCurrentIndex(11)

def configTelaOrdem(stackWidget):
    ui = uic.loadUi("Telas/tela ordem de serviço.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton_2.clicked.connect(lambda: telaServicoCadastro(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaOrdemCadastro(stackWidget))