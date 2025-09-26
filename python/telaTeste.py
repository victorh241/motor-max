import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QHeaderView

class JanelaComTabela(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Tabela com Múltiplos Botões")
        self.setGeometry(100, 100, 600, 300)
        
        # 1. Cria o QTableWidget
        self.tabela = QTableWidget()
        
        # 2. Define o número de linhas e colunas
        self.tabela.setRowCount(3)
        self.tabela.setColumnCount(2)
        
        # 3. Remove os cabeçalhos das colunas
        self.tabela.horizontalHeader().setVisible(False)
        self.tabela.verticalHeader().setVisible(False)
        
        # 4. Ajusta a primeira coluna para preencher o espaço
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        # 5. Preenche a tabela com dados e layouts de botões
        for i in range(self.tabela.rowCount()):
            # Adiciona o nome na primeira coluna
            nome = QTableWidgetItem(f"Usuário {i+1}")
            self.tabela.setItem(i, 0, nome)
            
            # Cria o layout de botões para a segunda coluna
            botoes_layout = QHBoxLayout()
            botoes_layout.setSpacing(10) # Define o espaçamento em pixels
            
            # Cria os 3 botões
            botao1 = QPushButton("Ver")
            botao2 = QPushButton("Editar")
            botao3 = QPushButton("Excluir")
            
            # Adiciona os botões ao layout horizontal
            botoes_layout.addWidget(botao1)
            botoes_layout.addWidget(botao2)
            botoes_layout.addWidget(botao3)
            
            # 6. Cria um QWidget de container para o layout de botões
            botoes_container = QWidget()
            botoes_container.setLayout(botoes_layout)
            
            # 7. Adiciona o container (com os 3 botões) na célula da tabela
            self.tabela.setCellWidget(i, 1, botoes_container)
            
            # Conecta os botões a uma função, passando a linha como argumento
            botao1.clicked.connect(lambda checked, row=i: self.botao_clicado(row, "Ver"))
            botao2.clicked.connect(lambda checked, row=i: self.botao_clicado(row, "Editar"))
            botao3.clicked.connect(lambda checked, row=i: self.botao_clicado(row, "Excluir"))
        
        # Redimensiona a segunda coluna para se ajustar ao conteúdo dos botões
        self.tabela.resizeColumnsToContents()
        
        # Adiciona a tabela à janela
        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def botao_clicado(self, linha, acao):
        # Mostra qual botão foi clicado e em qual linha
        print(f"Ação '{acao}' na linha {linha} foi executada.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaComTabela()
    janela.show()
    sys.exit(app.exec_())