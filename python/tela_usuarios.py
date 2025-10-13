from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QLabel, QTableWidgetItem, QTableWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD
from tela_cadastroUsuarios import carregarDadosUsuario

def userEditar(stackWidget, usuario_id):
    stackWidget.setCurrentIndex(12)
    carregarDadosUsuario(stackWidget.widget(12), usuario_id, stackWidget)

def userExcluir(ui, usuario_id, stackWidget):
    #mensagem de confirmação
    msg = QMessageBox()
    msg.setWindowTitle("Aviso !")
    msg.setText("Você tem certeza que quer excluir esse usuário ?")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    resposta = msg.exec_()
    if resposta == QMessageBox.Ok:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        cnx.commit()
        cnx.close()

        ui.tableWidget.setRowCount(0)
        mostrarUsuarios(ui, stackWidget)

def mostrarUsuarios(ui, stackWidget):
    try:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("SELECT id_usuario, id_funcionario, login, função FROM usuarios")
        dados = cursor.fetchall()

        tabela = ui.tableWidget

        colunas = 1

        tabela.setRowCount(len(dados))
        tabela.setColumnCount(colunas)

        #tamanhos das colunas
        tabela.setColumnWidth(0, 950)

        for i in range(len(dados)):
            tabela.setRowHeight(i, 120)

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

        for idx, _usuario in enumerate(dados):
            frame = QFrame()

            #region config do frame
            frame.setFixedSize(950, 100)

            frame.setStyleSheet('''
                QFrame{
                    background-color: white;
                    border-radius: 15px;
                    border: 1px solid;
                    }
                ''')
            #endregion

            #region labels
            labelLogin = QLabel(f"Login: {_usuario[2]}", frame)
            
            if _usuario[3] == 'admin':
                nivel = "Administrador"
                labelFunc = QLabel(nivel, frame)
            else:
                labelFunc = QLabel(_usuario[3], frame)
            
            #region config labels
            #login label
            labelLogin.setGeometry(10, 10, 220, 30)

            labelLogin.setStyleSheet('''
                QLabel{
                border: none;
                background: transparent;
                font-size: 20px;
                }
            ''')

            #função label
            labelFunc.setGeometry(250, 15, 90, 20)

            match labelFunc.text():
                case 'Administrador':
                    labelFunc.setStyleSheet('''
                    QLabel{
                        border: none;
                        background-color:rgb(255, 226, 226) ;
                        color: rgb(177, 14, 18);
                        font-size: 12px;
                        margin-left: 8px;
                        border-radius: 8px;
                        }
                    ''')
                case 'Atendente':
                    labelFunc.setStyleSheet('''
                                QLabel{
                                    border: none;
                                    background-color: rgb(219, 252, 231) ;
                                    color: rgb(8, 101, 82);
                                    font-size: 12px;
                                    margin-left: 8px; 
                                    border-radius: 8px;
                                    }
                                ''')
                case 'Mecânico':
                    labelFunc.setStyleSheet('''
                                QLabel{
                                    border: none;
                                    background-color: rgb(219, 234, 254) ;
                                    color: rgb(43, 79, 186);
                                    font-size: 12px;
                                    margin-left: 8px;
                                    border-radius: 8px;
                                    }
                                ''')
            #endregion

            #region pushButton
            botaoEditar = QPushButton("" , frame)
            botaoExcluir = QPushButton("" , frame)

            #region config botão
            botaoEditar.setGeometry(860, 10, 30, 30)

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
            
            botaoExcluir.setGeometry(900, 10, 30, 30)

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

            botaoEditar.setIcon(QIcon("imagem/icons/edit.png"))
            botaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))
            botaoEditar.setIconSize(QSize(20, 20))
            botaoExcluir.setIconSize(QSize(20, 20))
            botaoEditar.setCursor(Qt.PointingHandCursor)
            botaoExcluir.setCursor(Qt.PointingHandCursor)
            #endregion

            tabela.setCellWidget(idx, 0, frame)

            botaoEditar.clicked.connect(lambda _, usuario_id=_usuario[0]: userEditar(stackWidget, usuario_id))
            botaoExcluir.clicked.connect(lambda _, usuario_id=_usuario[0]: userExcluir(ui, usuario_id, stackWidget))
            #endregion

            #endregion
        
        cnx.close()
    except Exception as e:
        print(f"Erro ao mostrar usuários: {e}")

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastro(stackWidget):
    stackWidget.setCurrentIndex(12)

def configTelaUsuarios(stackWidget):
    ui = uic.loadUi("Telas/tela_usuarios.ui")

    stackWidget.addWidget(ui)
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastro(stackWidget))