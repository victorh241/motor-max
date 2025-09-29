from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QFrame, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from bancoDados import carregarBD

def funcEditar(ui):
    pass

def funcExcluir(ui):
    pass

#region butões
def mostrarFuncionarios(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()

    cursor.execute("SELECT nome, cpf, Email, disponivel FROM Funcionarios")
    dadosFuncionarios = cursor.fetchall()

    tabela = ui.tableWidget

    tabela.setRowCount(len(dadosFuncionarios))
    tabela.setColumnCount(1)

    #region criar o frame
    frame = QFrame()
    labelNome = QLabel("teste 1", frame)
    labelFunc = QLabel("teste 2", frame)
    botaoExcluir = QPushButton("", frame)
    botaoEditar = QPushButton("", frame)

    #config dos labels
    labelNome.setGeometry(10, 10, 80, 20)
    labelFunc.setGeometry(10, 50, 80, 20)

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

    botaoEditar.setIcon(QIcon("Projeto_Oficina_Motomax\imagem\icons\edit.png"))
    botaoExcluir.setIcon(QIcon("Projeto_Oficina_Motomax\imagem\icons\delete.png"))

    botaoEditar.setIconSize(QSize(20, 20))
    botaoExcluir.setIconSize(QSize(20, 20))

    #configs do frame
    frame.setFixedSize(220, 120)
    frame.setGeometry(0, 0, 220, 120)
    frame.setStyleSheet('''
        QFrame{
        background-color: white;
        border-radius: 15px;
        border: 1px solid
        }
        ''')

    tabela.setCellWidget(0, 0, frame)
    #endregion

    #funções botões
    botaoEditar.clicked.connect()

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
