#region imports
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import uic
import bancoDados

#region telas
from login import configLogin, verificarTelaLogin
from tela_principal import configTelaPrincipal, nivelAcesso
from tela_funcionarios import configTelaFuncionarios, mostrarFuncionarios
from tela_clientes import configTelaClientes, mostraClientes
from tela_veiculos import configTelaVeiculos, mostrarVeiculos
from tela_ordem import configTelaOrdem, tabelasListagem
from tela_usuarios import configTelaUsuarios, mostrarUsuarios
from telaProduto import configTelaProdutos, mostrarProdutos
from tela_funcionarioCadastro import configTelaFuncionarioCadastro
from tela_clienteCadastro import configClienteCadastro
from tela_cadastroServiços import configCadastroServico
from tela_ordemCadastro import configTelaOrdemCadastro, atualizarComboBox
from tela_cadastroUsuarios import configTelaUsuariosCadastro, atualizarTabelas as updateCdsUsuario
from tela_cadastroProduto import configTelaProdutoCadastro
from tela_recuperarSenha import configTelaRecuperar
from tela_novaSenha import configNovaSenha
from tela_cadastroVeiculos import configTelaVeiculosCadastro, atualizarComboBox as updateCdsVeiculos
#endregion
#endregion

#TODO: Fazer o try e exception para todas as telas

#region notes
'''
Ordem do stack: 
0 = login
1 = tela principal
2 = funcionarios
3 = cliente
4 = veiculos
5 = ordem de serviço
6 = usuarios
7 = produtos
8 = cadastro dos funcionarios
9 = cadastro dos clientes
10 = cadastro de serviço
11 = cadastro ordem de serviço
12 = cadastro usuarios
13 = cadastro produtos
14 = cadastro veiculo
15 = recuperar senha
16 = nova senha
'''
#endregion

def verificarTela(index, stackWidget):
    try:
        if index == 0:
            verificarTelaLogin(stackWidget.currentWidget())

        if index == 1:
            nivelAcesso(stackWidget.currentWidget())

        if index == 2:
            mostrarFuncionarios(stackWidget.currentWidget(), stackWidget)

        if index == 3:
            mostraClientes(stackWidget.currentWidget(), stackWidget)

        if index == 4:
            mostrarVeiculos(stackWidget.currentWidget(), stackWidget)

        if index == 5:
            tabelasListagem(stackWidget.currentWidget(), stackWidget)

        if index == 6:
            mostrarUsuarios(stackWidget.currentWidget(), stackWidget)

        if index == 7:
            mostrarProdutos(stackWidget.currentWidget(), stackWidget)

        if index == 11:
            atualizarComboBox(stackWidget.currentWidget())

        if index == 12:
            updateCdsUsuario(stackWidget.currentWidget())

        if index == 14:
            updateCdsVeiculos(stackWidget.currentWidget())
    except Exception as e:
        print(f"erro: {e}")

def janela():
    try:
        app = QApplication([])
        tela = QMainWindow()
        stack_widget = QStackedWidget()
        tela.setCentralWidget(stack_widget)

        #region funções de iniciação das 
        try:
            configLogin(stack_widget)
            configTelaPrincipal(stack_widget)
            configTelaFuncionarios(stack_widget)
            configTelaClientes(stack_widget)
            configTelaVeiculos(stack_widget)
            configTelaOrdem(stack_widget)
            configTelaUsuarios(stack_widget)
            configTelaProdutos(stack_widget)
            configTelaFuncionarioCadastro(stack_widget)
            configClienteCadastro(stack_widget)
            configCadastroServico(stack_widget)
            configTelaOrdemCadastro(stack_widget)
            configTelaUsuariosCadastro(stack_widget)
            configTelaProdutoCadastro(stack_widget)
            configTelaVeiculosCadastro(stack_widget)
            configTelaRecuperar(stack_widget)
            configNovaSenha(stack_widget)
        except Exception as e:
            print(f"Erro na configuração de uma das telas, Erro: {e}")
        #endregion

        stack_widget.setCurrentIndex(0)

        stack_widget.currentChanged.connect(lambda index: verificarTela(index, stack_widget))


        tela.show()
        app.exec()
        bancoDados.fechar_coneccao()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    janela()