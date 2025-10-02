from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QFrame
from bancoDados import carregarBD

def mostrarServicos(ui, stackWidget):
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

        for idx, _servico in enumerate(resultados):
            frame = QFrame()

            #region configurações do frame
            frame.setFixedSize(970, 60)

            frame.setStyleSheet('''
                QFrame{
                    background-color: white;
                    border-radius: 15px;
                    border: 1px solid;
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

            row = idx // colunas
            column = idx % colunas

            ui.tableWidget.setCellWidget(row, column, frame)

    except Exception as e:
        print(f"Erro ao carregar serviços: {e}")

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