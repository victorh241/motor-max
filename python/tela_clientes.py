from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidgetItem, QTableWidget, QFrame, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD
from tela_clienteCadastro import carregarDadosCliente
#carregar tela de cadastro cliente

#TODO: melhorar os espeçamentos

def editarCliente(idx, ui, stackWidget):
    try:
        stackWidget.setCurrentIndex(9)
        carregarDadosCliente(stackWidget.widget(9), idx + 1, stackWidget)

    except Exception as e:
        print(f"Erro ao editar cliente: {e}")

def excluirCliente(idx, ui, stackWidget):# aqui também tem dependencias no veiculo, ordem de serviço e telefones
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        msg = QMessageBox()
        msg.setWindowTitle("Aviso !")
        msg.setText("Você tem certeza que quer editar esse cliente ?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        respota = msg.exec_()
        if respota == QMessageBox.Ok:
            cnx = carregarBD()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (idx + 1,))
            cursor.execute("DELETE FROM telefones WHERE id_cliente = %s", (idx + 1,))#não é muito um ponto de discurssão porque o telefone depende diretamente de cliente
            cnx.commit()
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")

def mostraClientes(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_cliente, nome, cpf, email FROM clientes")
        dados = cursor.fetchall()

        tabela = ui.tableWidget

        #configurações da tabela
        colunas = 1

        tabela.setRowCount(len(dados))
        tabela.setColumnCount(colunas)

        #espaçamento
        esp_vertical = 20 # espaçamento vertical

        tabela.setColumnWidth(0, 970)

        for r in range(len(dados)):
            tabela.setRowHeight(r, 120 + esp_vertical)

        tabela.setHorizontalHeaderLabels([""] * colunas)
        tabela.setVerticalHeaderLabels([""] * tabela.rowCount())
        tabela.horizontalHeader().setVisible(False)
        tabela.verticalHeader().setVisible(False)

        tabela.setShowGrid(False)

        for idx, _cliente in enumerate(dados):
            frame = QFrame()

            #region telefone
            cursor.execute("SELECT telefone FROM telefones WHERE id_cliente = %s", (_cliente[0],))
            telefones = cursor.fetchall()
            #endregion

            #region config do frame
            #config do frame
            frame.setFixedSize(970, 120)

            frame.setStyleSheet('''
                QFrame{
                    background-color: white;
                    border-radius: 15px;
                    border: 1px solid;
                }
            ''')

            #endregion

            #icons
            iconEmail = QLabel("",frame)
            iconTelefone = QLabel("", frame)
            imgEmail = QPixmap("Imagens/email.png")
            imgTelefone = QPixmap("Imagens/telefone.png")
            
            #region icons configs 
            iconEmail.setPixmap(imgEmail)
            iconTelefone.setPixmap(imgTelefone)
            iconEmail.setScaledContents(True)
            iconTelefone.setScaledContents(True)

            iconEmail.setGeometry(20, 52, 16, 16)
            iconTelefone.setGeometry(250, 52, 16, 16)

            iconEmail.setStyleSheet('''
                QLabel{
                        border: none;
                    }
                ''')
            
            iconTelefone.setStyleSheet('''
                QLabel{
                        border: none;
                    }
                ''')
            #endregion

            #labels
            labelNome = QLabel(f"Nome: {_cliente[1]}", frame)
            labelTituloCpf = QLabel("Cpf:", frame)
            labelCpf = QLabel(f"{_cliente[2]}", frame)
            labelEmail = QLabel(f"Email: {_cliente[3]}", frame)
            labelTelefone = QLabel(f"Telefone: {telefones[0][0]}", frame)#depois eu coloco algo coisa pra falar que tem mais de um telefone


            #region labels configs
            labelNome.setStyleSheet('''
                QLabel{
                font-size: 20px;
                font-weight: bold;
                border: none;
                background: transparent;
                }
            ''')

            labelTituloCpf.setStyleSheet('''
                QLabel{
                    border: none;
                    font-weight: bold;
                    font-size: 14px;
                    }
                ''')

            labelCpf.setStyleSheet('''
                QLabel{
                border: none;
                font-size: 13px;
                }
            ''')

            labelEmail.setStyleSheet('''
                QLabel{
                border: none;
                font-size: 13px;
                }
                ''')

            labelTelefone.setStyleSheet('''
                QLabel{
                border: none;
                font-size: 13px;
                }
            ''')

            labelNome.setGeometry(30, 20, 370, 30)
            labelTituloCpf.setGeometry(10 , 80 , 30, 20)
            labelCpf.setGeometry(45, 80, 200, 20)
            labelEmail.setGeometry(40 , 50 , 200, 20)
            labelTelefone.setGeometry(270, 50, 200, 20)
            #endregion

            # Adiciona botões de editar e excluir
            botaoEditar = QPushButton("", frame)
            botaoExcluir = QPushButton("", frame)

            #region config dos botões
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

            botaoEditar.setGeometry(860, 15, 35, 35)
            botaoExcluir.setGeometry(900, 15, 35, 35)
            #endregion
            row = idx // colunas
            column = idx % colunas

            ui.tableWidget.setCellWidget(row, column, frame)

            # Conecta os botões às funções de editar e excluir
            botaoEditar.clicked.connect(lambda _, r=idx: editarCliente(r, ui, stackWidget))
            botaoExcluir.clicked.connect(lambda _, r=idx: excluirCliente(r, ui, stackWidget))

        ui.tableWidget.resizeColumnsToContents()
    except Exception as e:
        print(f"Erro ao mostrar clientes: {e}")

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def telaCadastro(stackWidget):
    stackWidget.setCurrentIndex(9)

def configTelaClientes(stackWidget):
    ui = uic.loadUi("Telas/tela_cliente.ui")

    stackWidget.addWidget(ui)

    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: telaCadastro(stackWidget))