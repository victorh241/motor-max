#region imports
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import uic

#region telas
from login import configLogin
from tela_principal import configTelaPrincipal, nivelAcesso
from tela_funcionarios import configTelaFuncionarios
from tela_clientes import configTelaClientes
from tela_veiculos import configTelaVeiculos
from tela_ordem import configTelaOrdem
from tela_usuarios import configTelaUsuarios
from telaProduto import configTelaProdutos
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

#region notacão das telas
#Esse arquivo já foi concluido
#TODO: substituir todas funções de carregarBD

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
    if index == 1:
        nivelAcesso(stackWidget.currentWidget())

    if index == 11:
        atualizarComboBox(stackWidget.currentWidget())

    if index == 12:
        updateCdsUsuario(stackWidget.currentWidget())

    if index == 14:
        updateCdsVeiculos(stackWidget.currentWidget())

def janela():
    app = QApplication([])
    tela = QMainWindow()
    stack_widget = QStackedWidget()
    tela.setCentralWidget(stack_widget)

    #region funções de iniciação das 
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
    #endregion

    stack_widget.setCurrentIndex(0)

    stack_widget.currentChanged.connect(lambda index: verificarTela(index, stack_widget))
    tela.show()
    app.exec()

janela()