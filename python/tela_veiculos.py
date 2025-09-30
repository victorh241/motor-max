from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel, QTableWidgetItem, QTableWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD
from tela_cadastroVeiculos import carregarDadosVeiculo

def editarVeiculo(idx, stackWidget):
    try:
        stackWidget.setCurrentIndex(14)
        carregarDadosVeiculo(stackWidget.widget(14), idx + 1, stackWidget)
    except Exception as e:
        print(f"Erro ao editar veiculo: {e}")

def excluirVeiculo(idx, ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Você tem certeza que quer excluir esse veiculo ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        respota = msg.exec_()
        if respota == QMessageBox.Ok:
            cnx = carregarBD()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM veiculos WHERE id_veiculo = %s", (idx + 1,))
            cnx.commit()
    except Exception as e:
        print(f"Erro ao excluir veiculo: {e}")

def mostrarVeiculos(ui, stackWidget):#tem algum erro aqui
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_veiculo, id_cliente, placa, ano, modelo, marca FROM veiculos")
        dados = cursor.fetchall()

        #region configurações da tabela
        tabela = ui.tableWidget
        tabela.setRowCount(len(dados))
        tabela.setColumnCount(1)

        tabela.setColumnWidth(0, 970)

        #espaçamento vertical
        esp_vertical = 20 # espaçamento vertical

        for r in range(len(dados)):
            tabela.setRowHeight(r, 190 + esp_vertical)
        
        #header
        tabela.setHorizontalHeaderLabels([""])
        tabela.setVerticalHeaderLabels([""] * tabela.rowCount())
        tabela.horizontalHeader().setVisible(False)
        tabela.verticalHeader().setVisible(False)

        tabela.setShowGrid(False)
        #endregion

        for index, _veiculo in enumerate(dados):
            #frame
            frame = QFrame()

            #region frame config
            frame.setFixedSize(970, 190)

            frame.setStyleSheet('''
                    QFrame{
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 15px;
                    }     
            ''')
            #endregion

            #cliente nome
            cursor.execute("SELECT nome FROM clientes WHERE id_cliente = %s", (_veiculo[1],))
            nomeCliente = cursor.fetchone()[0]
            
            #region icons
            iconeVeiculo = QLabel("", frame)
            imgVeiculo = QPixmap("imagem/icons/veiculo mini.png")

            #config icons
            iconeVeiculo.setPixmap(imgVeiculo)
            iconeVeiculo.setGeometry(25, 20, 30, 30) 

            iconeVeiculo.setScaledContents(True)

            iconeVeiculo.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                }
            ''')
            #endregion

            #region labels
            labelPlaca = QLabel(_veiculo[2], frame)
            labelTituloCliente = QLabel("Cliente: ", frame)
            labelCliente = QLabel(nomeCliente, frame)
            labelTituloAno = QLabel("Ano: ", frame)
            labelAno = QLabel(str(_veiculo[3]), frame)
            labelVeiculo = QLabel(f"{_veiculo[5]} {_veiculo[4]}", frame)

            #region labels config
            labelPlaca.setGeometry(60, 20, 100, 30)

            labelPlaca.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-weight: bold;
                font-size: 15px;
                }                         
            ''')

            labelVeiculo.setGeometry(30, 50, 150, 16)

            labelVeiculo.setStyleSheet('''
                QFrame{
                    background-color: transparent;
                    border: none;
                    font-size: 14px;
                    color: #4f4f4f;
                    }
                ''')
            
            labelTituloCliente.setGeometry(20, 100, 60, 20)
            labelCliente.setGeometry(85, 100, 100, 20)

            labelTituloCliente.setStyleSheet('''
                QLabel{
                border: none;
                font-weight: bold;
                font-size: 15px;
                }
            ''')

            labelCliente.setStyleSheet('''
                    QLabel{
                    border: none;
                    font-size: 14px;
                    background: transparent;
                    }
                ''')
            
            labelTituloAno.setGeometry(20, 120, 40, 20)
            labelAno.setGeometry(60, 120, 100, 20)

            labelTituloAno.setStyleSheet('''
                QLabel{
                border: none;
                font-weight: bold;
                font-size: 15px;
                }
            ''')

            labelAno.setStyleSheet('''
                    QLabel{
                    border: none;
                    font-size: 14px;
                    background: transparent;
                    }
                ''')
            #endregion
            #endregion

            #region botões
            botaoEditar = QPushButton("", frame)
            botaoExcluir = QPushButton("", frame)

            #region botões config
            botaoEditar.setCursor(Qt.PointingHandCursor)
            botaoExcluir.setCursor(Qt.PointingHandCursor)
            botaoEditar.setIcon(QIcon("imagem/icons/edit.png"))
            botaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))

            botaoEditar.setIconSize(QSize(20, 20))
            botaoExcluir.setIconSize(QSize(20, 20))

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

            botaoEditar.setGeometry(880, 30, 35, 35)
            botaoExcluir.setGeometry(920, 30, 35, 35)
            #endregion
            #endregion

            tabela.setCellWidget(index, 0, frame)

            botaoEditar.clicked.connect(lambda _, id=_veiculo[0]: editarVeiculo(id, stackWidget))
            botaoExcluir.clicked.connect(lambda _, id=_veiculo[0]: excluirVeiculo(id, ui, stackWidget))
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