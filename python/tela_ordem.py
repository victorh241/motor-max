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
    cursor.execute("SELECT id_ordemServiço, id_serviço, codigo, id_veiculo, status, deconto, agendamento, quantidade_produtos, quantidade_serviços FROM `Ordem de Serviços`")
    dadosOrdem = cursor.fetchall()

    tabela = ui.tableWidget_2
    colunas = 1
    tabela.setRowCount(len(dadosOrdem))
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
    for idx, _os in enumerate(dadosOrdem):
        #region dados
        cursor.execute("SELECT id_produto, valorMaoObra FROM serviço WHERE id_serviço = %s", (_os[1]))
        dadosServico = cursor.fetchone()

        cursor.execute("SELECT preco_unitario FROM WHERE id_produto = %s", (dadosServico[0],))
        dadosProduto = cursor.fetchone()

        cursor.execute("SELECT `valor final` FROM WHERE id_ordem = %s", (_os[0],))
        dadosVendaFinal = cursor.fetchone()

        cursor.execute("SELECT id_cliente FROM WHERE id_veiculo = %s", (_os[3],))
        _iCliente = cursor.fetchone()
        id_cliente = _iCliente[0]

        cursor.execute("SELECT nome FROM clientes WHERE id_cliente = %s", (id_cliente,))
        dadosCliente = cursor.fetchone()

        cursor.execute("SELECT marca, modelo FROM veiculos WHERE id_veiculo = %s", (_os[3]),)
        dadosVeiculo = cursor.fetchone()
        #endregion

        frame = QFrame()

        #region configurações do frame
        frame.setFixedSize(1000, 260)

        frame.setStyleSheet('''
            QFrame{
                background-color: white;
                border-radius: 15px;
                border: 1px solid;
                }
        ''')
        #endregion
    
        #region labels
        labelCodigo = QLabel(_os[2], frame)
        labelCliente = QLabel(dadosCliente[0],frame)
        labelVeiculo = QLabel(f"{dadosVeiculo[0]} {dadosVeiculo[1]}", frame)
        labelTituloServico = QLabel("Serviços", frame)
        labelTituloProdutos = QLabel("Produtos", frame)
        labelValorServicos = QLabel(f"R$ {dadosServico[1] * _os[8]}",frame)
        labelValorProdutos = QLabel(f"R$ {dadosProduto[0] * _os[7]}",frame)
        labelTituloValor = QLabel("Total", frame)
        labelValorTotal = QLabel(f"R$ {dadosVendaFinal[0]}",frame)

        labelStatus = QLabel(_os[4], frame)

        #region label config
        #codigo
        labelCodigo.setGeometry(20, 10, 140, 20)
        labelCodigo.setStyleSheet('''
            QLabel{
            border: none;
            font-weight: bold;
            font-size: 14px;
            }
        ''')

        #cliente
        labelCliente.setGeometry(20, 30, 120, 15)
        labelCliente.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 12px;
                color: rgb(67, 72, 99);
                }
            ''')
        
        #veiculo
        labelVeiculo.setGeometry(20, 50, 120, 15)
        labelVeiculo.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 12px;
                color: rgb(67, 72, 99);
                }
        ''')

        #status
        match labelStatus.text():
            case "Concluido":
                textoCorreto = "Concluído"
                labelStatus.setText(textoCorreto)
                labelStatus.setGeometry(890, 10, 80, 20)
                labelStatus.setStyleSheet('''
                    QLabel{
                    border: none;
                    background-color: rgb(219, 252, 231);
                    color: rgb(15, 102, 65);
                    font-size: 14px;
                    border-radius: 8px;
                    padding-left: 4px;
                    }
                ''')
            case "Em Andamento":
                labelStatus.setGeometry(860, 10, 110, 20)
                labelStatus.setStyleSheet('''
                    QLabel{
                    border: none;
                    background-color: rgb(254, 249, 194);
                    color: rgb(152, 75, 0);
                    font-size: 14px;
                    border-radius: 8px;
                    padding-left: 4px;
                    }
                ''')
            case "Agendado":
                labelStatus.setGeometry(890, 10, 80, 20)
                labelStatus.setStyleSheet('''
                    QLabel{
                    border: none;
                    background-color: rgb(219, 234, 254);
                    color: rgb(93, 76, 184);
                    font-size: 14px;
                    border-radius: 8px;
                    padding-left: 4px;
                    }
                ''')
            case "Cancelado":
                labelStatus.setGeometry(890, 10, 80, 20)
                labelStatus.setStyleSheet('''
                    QLabel{
                    border: none;
                    background-color: rgb(255, 74, 74);
                    color: rgb(94, 6, 6);
                    font-size: 14px;
                    border-radius: 8px;
                    padding-left: 4px;
                    }
                ''')
            
            
        #titulo serviço
        labelTituloServico.setGeometry(890, 120, 90, 15)
        labelTituloServico.setStyleSheet('''
            QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')
        labelTituloServico.setAlignment(Qt.AlignRight)

        labelTituloProdutos.setGeometry(20, 140, 90, 15)
        labelTituloProdutos.setStyleSheet('''
            QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')
        labelTituloProdutos.setAlignment(Qt.AlignRight)

        labelTituloValor.setGeometry(20, 180, 120, 15)
        labelTituloValor.setStyleSheet('''
            QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')

        labelValorProdutos.setGeometry(890, 140, 90, 15)
        labelValorProdutos.setStyleSheet('''
            QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')

        labelValorServicos.setGeometry(890, 120, 90, 15)
        labelValorServicos.setStyleSheet('''
            QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')

        labelValorTotal.setGeometry(890, 180, 90, 15)
        labelValorTotal.setStyleSheet('''
             QLabel{
            border: none;
            background: transparent;
            font-size: 12px;
            color: rgb(67, 72, 99);
            }
        ''')
        #endregion
        #endregion

        #region linhas
        linha1 = QLabel("", frame)
        linha2 = QLabel("", frame)

        #region config linhas
        linha1.setGeometry(0, 110, 1000, 1)
        linha1.setStyleSheet('''
            border: 1px solid rgb(97, 97, 97);
        ''')

        linha2.setGeometry(0, 170, 1000, 1)
        linha2.setStyleSheet('''
            border: 1px solid rgb(97, 97, 97);
        ''')
        #endregion

        #endregion

        #region botões
        botaoExcluir = QPushButton("", frame)
        botaoEditar = QPushButton("", frame)

        #region botões config
        botaoExcluir.setCursor(Qt.PointingHandCursor)
        botaoEditar.setCursor(Qt.PointingHandCursor)
        botaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))
        botaoExcluir.setIconSize(QSize(20, 20))
        botaoEditar.setIcon(QIcon("imagem/icons/edit.png"))
        botaoEditar.setIconSize(QSize(20,20))

        botaoExcluir.setGeometry(910, 220, 30, 30)
        botaoEditar.setGeometry(950, 220, 30, 30)

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

        #endregion
        #endregion

        row = idx // colunas
        column = idx % colunas

        tabela.setCellWidget(row, column, frame)

        botaoEditar.clicked.connect(lambda _, idx=_os[0]: excluirOrdem(idx, ui))
        botaoExcluir.clicked.connect(lambda _, idx=_os[0]: editarOrdem(idx, ui))


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