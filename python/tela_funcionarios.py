from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt

from bancoDados import carregarBD
from tela_funcionarioCadastro import carregarDadosFuncionario

#TODO: melhorar os espaçamentos

def funcEditar(stackWidget, index):
    funcId = index + 1
    stackWidget.setCurrentIndex(8)
    carregarDadosFuncionario(stackWidget.widget(8), funcId, stackWidget)

def funcExcluir(ui, index):# aqui existe um problema, se o usuario quer que exclua o funcionario ele precisa primeiro excluir o usuario vinculado a ele
    id_funcionario = index + 1

    #mensagem de confirmação
    msg = QMessageBox()
    msg.setWindowTitle("Aviso !")
    msg.setText("Você tem certeza que quer excluir esse funcionário ?")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    resposta = msg.exec_()
    if resposta == QMessageBox.Ok:
        cnx = carregarBD()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM Funcionarios WHERE id_funcionario = %s", (id_funcionario,))

    

#region butões
def mostrarFuncionarios(ui, stackWidget):
    cnx = carregarBD()
    cursor = cnx.cursor()

    cursor.execute("SELECT nome , disponivel FROM Funcionarios")
    dadosFuncionarios = cursor.fetchall()

    tabela = ui.tableWidget
    colunas = 3

    tabela.setRowCount(len(dadosFuncionarios))
    tabela.setColumnCount(colunas)


    #region configs
    #espaçamento 
    esp_horizontal = 30 # espaçamento horizontal
    esp_vertical = 20 # espaçamento vertical

    for c in range(colunas):
        tabela.setColumnWidth(c , 220 + esp_horizontal)

    for r in range(len(dadosFuncionarios)):
        tabela.setRowHeight(r, 120 + esp_vertical)
    
    #header
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
    #endregion

    #region criar o frame
    for i, _funcionario in enumerate(dadosFuncionarios):
        frame = QFrame()

        textoDisponivel = ""
        if _funcionario[1] == 0:
            textoDisponivel = "Indisponível"
        else:
            textoDisponivel = "Disponível"

        labelNome = QLabel(f"Nome: {_funcionario[0]}", frame)
        labelFunc = QLabel(f"Disponibilidade: {textoDisponivel}", frame)
        botaoExcluir = QPushButton("", frame)
        botaoEditar = QPushButton("", frame)

        #config dos labels
        labelNome.setGeometry(10 , 10 , 100, 20)
        labelFunc.setGeometry(10 , 50 , 180, 20)

        labelNome.setStyleSheet('''
            QLabel{
            border: none;
            font-size: 14px;
            }   
        ''')

        labelFunc.setStyleSheet('''
            QLabel{
            border: none;
            font-size: 14px;
            }   
        ''')

        #config dos botões
        botaoEditar.setGeometry(140, 80, 30, 30)
        botaoExcluir.setGeometry(180, 80, 30, 30)

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

        botaoEditar.setIcon(QIcon("imagem/icons/edit.png"))
        botaoExcluir.setIcon(QIcon("imagem/icons/delete.png"))

        botaoEditar.setIconSize(QSize(20, 20))
        botaoExcluir.setIconSize(QSize(20, 20))

        botaoEditar.setCursor(Qt.PointingHandCursor)
        botaoExcluir.setCursor(Qt.PointingHandCursor)

        #texto e coisas
        #for _funcionario in dadosFuncionarios:
        

        #configs do frame
        frame.setFixedSize(220, 120)
        frame.setStyleSheet('''
            QFrame{
            background-color: white;
            border-radius: 15px;
            border: 1px solid;
            }
            ''')
        
        #funções botões
        botaoEditar.clicked.connect(lambda _,idx=i: funcEditar(stackWidget, idx))
        botaoExcluir.clicked.connect(lambda _, idx=i: funcExcluir(ui, idx))

        #formatação de tabela de widget
        row = i // colunas
        col = i % colunas

        tabela.setCellWidget(row, col, frame)
        #endregion

        

def voltarTelaPrincipal(stackWidget):
    stackWidget.setCurrentIndex(1)

def cadastroFuncionario(stackWidget):
    stackWidget.setCurrentIndex(8)
#endregion

def configTelaFuncionarios(stackWidget):
    ui = uic.loadUi("Telas/funcionarios.ui")

    stackWidget.addWidget(ui)

    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(stackWidget))
    ui.pushButton.clicked.connect(lambda: cadastroFuncionario(stackWidget))
