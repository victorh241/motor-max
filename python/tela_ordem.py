from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel, QMessageBox, QTabWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt
import traceback

from bancoDados import carregarBD, fechar_coneccao
from tela_ordemCadastro import atualizarOrdem

#region botões da ordem de serviços
def excluirOrdem(idx, ui, stackWidget):
    id_ordem = idx
    #mensagem de confirmação
    msg = QMessageBox()
    msg.setWindowTitle("Aviso !")
    msg.setText("Você tem certeza que quer excluir essa ordem de serviço ?")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    resposta = msg.exec_()
    if resposta == QMessageBox.Ok:
        cnx = carregarBD()
        cursor = cnx.cursor(buffered=True)
        cursor.execute("DELETE FROM Venda_final WHERE id_ordem = %s", (id_ordem,))
        cursor.execute("DELETE FROM equipe_mecanicos WHERE `Ordem de Serviço_id_ordemServiço` = %s", (id_ordem,))
        cursor.execute("DELETE FROM `produtos_detalhes` WHERE id_ordem = %s", (id_ordem,))
        cursor.execute("DELETE FROM `serviço_detalhes` WHERE id_ordem = %s", (id_ordem,))
        cursor.execute("DELETE FROM `Ordem de Serviços` WHERE id_ordemServiço = %s", (id_ordem,))
        cnx.commit()
        fechar_coneccao()
        
        
        #atualizar tela
        ui.tableWidget_2.setRowCount(0)
        mostrarOrdemServiço(ui, stackWidget)

def editarOrdem(idx, stackWidget):
    try:
        stackWidget.setCurrentIndex(11)
        atualizarOrdem(stackWidget.widget(11), stackWidget, idx)
    except Exception as e:
        print(f"Erro na função de editar {e}")
#endregion

#region botões do serviço
def excluirServiço(id_servico, ui, stackWidget):
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
            cursor.execute("DELETE FROM Serviços WHERE id_serviço = %s", (id_servico,))
            cnx.commit()
            fechar_coneccao()

            ui.tableWidget.setRowCount(0)
            mostrarServicos(ui, stackWidget)
    except Exception as e:
        print(f"Erro na exclussão: {e}")
#endregion

def mudaListagem(idx, ui, stackWidget):
    if idx == 0:
        ui.tableWidget_2.setRowCount(0)
        mostrarOrdemServiço(ui, stackWidget)
    elif idx == 1:
        ui.tableWidget.setRowCount(0)
        mostrarServicos(ui,stackWidget)

def tabelasListagem(ui, stackWidget):
    if ui.tabWidget.currentIndex() == 0:
        ui.tableWidget_2.setRowCount(0)
        mostrarOrdemServiço(ui, stackWidget)
    else:
        ui.tableWidget.setRowCount(0)
        mostrarServicos(ui, stackWidget)
    ui.tabWidget.currentChanged.connect(lambda idx: mudaListagem(idx, ui, stackWidget))

def mostrarOrdemServiço(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_ordemServiço, id_veiculo, codigo, id_atendente,status, desconto, agendamento FROM `Ordem de Serviços`")
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

        tabela.setColumnWidth(0, 1000)

        for r in range(len(dadosOrdem)):
            tabela.setRowHeight(r, 280)

        tabela.setStyleSheet('''
                QTableWidget{
                    border: 1px solid;
                    background-color: white;
                }
                                
                QTableWidget::item {
                    padding: 10px;
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
        for idx, _os in enumerate(dadosOrdem):
            #region dados
            cursor.execute("SELECT Clientes_id_cliente FROM atendente WHERE id_atendente = %s", (_os[3],))
            _Cliente = cursor.fetchone()
            id_cliente = _Cliente[0]

            cursor.execute("SELECT nome FROM clientes WHERE id_cliente = %s", (id_cliente,))
            dadosCliente = cursor.fetchone()

            cursor.execute("SELECT marca, modelo FROM veiculos WHERE id_veiculo = %s", (_os[1],))
            dadosVeiculo = cursor.fetchone()

            #detalhes e quantidades
            cursor.execute("SELECT quantidade_serviço, valor_unitario, id_serviço FROM Serviço_detalhes WHERE id_ordem = %s", (_os[0],))
            _detalheServico = cursor.fetchall()

            cursor.execute("SELECT quantidade_produto, valor_unitario, id_produto FROM produtos_detalhes WHERE id_ordem = %s", (_os[0],))
            _detalheProduto = cursor.fetchall()
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

            for i ,_servico in enumerate(_detalheServico):
                valor_total = 0
                valor_total += float(_servico[0] * float(_servico[1]))
                labelValorServicos = QLabel(f"R$ {valor_total}",frame)
                labelValorServicos.setGeometry(890, 120, 90, 15)
                labelValorServicos.setStyleSheet('''
                    QLabel{
                    border: none;
                    background: transparent;
                    font-size: 12px;
                    color: rgb(67, 72, 99);
                    }
                ''')

                textoServico = ""
                cursor.execute("SELECT descrição FROM serviços WHERE id_serviço = %s", (_servico[2],))
                _dadosServicos = cursor.fetchone()
                textoServico = _dadosServicos[0]

                labelDescriServico = QLabel(f"{textoServico} x{_servico[0]}",frame)
                labelDescriServico.setGeometry(20 + (110 * i), 70, 110, 15)
                labelDescriServico.setStyleSheet('''
                    QLabel{
                    border: none;
                    background: transparent;
                    font-size: 12px;
                    color: rgb(67, 72, 99);
                    }
                ''')

            for i ,_produto in enumerate(_detalheProduto):
                valor_total = 0
                valor_total += float(_produto[0] * float(_produto[1]))
                labelValorProdutos = QLabel(f"R$ {valor_total}",frame)
                labelValorProdutos.setGeometry(890, 140, 90, 15)
                labelValorProdutos.setStyleSheet('''
                    QLabel{
                    border: none;
                    background: transparent;
                    font-size: 12px;
                    color: rgb(67, 72, 99);
                    }
                ''')
                
                textoProduto = ""
                cursor.execute("SELECT descrição FROM produtos WHERE id_produto = %s", (_produto[2],))
                _dados = cursor.fetchone()
                textoProduto = _dados[0]

                labelDescriProduto = QLabel(f"{textoProduto} x{_produto[0]}",frame)
                labelDescriProduto.setGeometry(20 + (110 * i), 90, 110, 15)
                labelDescriProduto.setStyleSheet('''
                    QLabel{
                    border: none;
                    background: transparent;
                    font-size: 12px;
                    color: rgb(67, 72, 99);
                    }
                ''')

            labelTituloValor = QLabel("Total", frame)

            cursor.execute("SELECT `valor final` FROM venda_final WHERE id_ordem = %s", (_os[0],))
            dadosVendaFinal = cursor.fetchone()
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
            labelTituloServico.setGeometry(-5, 120, 90, 15)
            labelTituloServico.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 12px;
                color: rgb(67, 72, 99);
                }
            ''')
            labelTituloServico.setAlignment(Qt.AlignRight)

            labelTituloProdutos.setGeometry(0, 140, 90, 15)
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

            botaoExcluir.setGeometry(950, 220, 30, 30)
            botaoEditar.setGeometry(910, 220, 30, 30)

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

            botaoEditar.clicked.connect(lambda _, idx=_os[0]: editarOrdem(idx, stackWidget))
            botaoExcluir.clicked.connect(lambda _, idx=_os[0]: excluirOrdem(idx, ui,stackWidget))
            fechar_coneccao()
    except Exception as e:
        print(f"listagem da os erro: {e}")
        traceback.print_exc()

def mostrarServicos(ui, stackWidget):#mostrar baseado no conteiner tab
    try:
        cnx = carregarBD()
        cursor = cnx.cursor(buffered=True)

        cursor.execute("SELECT id_serviço , descrição, valorMaoObra FROM serviços")
        resultados = cursor.fetchall()

        tabela = ui.tableWidget #essa é a tabela do serviço

        colunas = 1
        tabela.setRowCount(len(resultados))
        tabela.setColumnCount(colunas)

        for r in range(len(resultados)):
            tabela.setRowHeight(r, 75)

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

            butaoExcluir.clicked.connect(lambda _, idx = _servico[0]: excluirServiço(idx, ui, stackWidget))
    except Exception as e:
        print(f"Erro ao carregar componentes: {e}")

#region butões
def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaServicoCadastro(stackWidget):
    stackWidget.setCurrentIndex(10)

def telaOrdemCadastro(stackWidget):
    stackWidget.setCurrentIndex(11)
#endregion

def configTelaOrdem(stackWidget):
    ui = uic.loadUi("Telas/tela ordem de serviço.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton_2.clicked.connect(lambda: telaServicoCadastro(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaOrdemCadastro(stackWidget))