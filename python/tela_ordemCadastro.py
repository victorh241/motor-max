from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from bancoDados import carregarBD
import user
import random
import string

#status quase concluido falta revisar

def gere_codigo_ordem() -> str:
    letters = "".join(random.choice(string.ascii_letters) for _ in range(3))
    digits = "".join(random.choice(string.digits) for _ in range(3))
    return f"{digits}-{letters}"

def atualizarComboBox(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()
    comboCliente = ui.comboBox_2
    comboServico = ui.comboBox_6
    comboProdutos = ui.comboBox_7
    comboCliente.clear()
    comboServico.clear()
    comboProdutos.clear()

    #cliente
    cursor.execute("SELECT nome FROM clientes")
    result = cursor.fetchall()

    for _cliente in result:
        comboCliente.addItem(_cliente[0])
    
    #servico
    cursor.execute("SELECT descrição FROM serviços")
    dadosServico = cursor.fetchall()

    for _servico in dadosServico:
        comboServico.addItem(_servico[0])
    
    #produtos
    cursor.execute("SELECT descrição, em_estoque FROM produtos")
    dadosProduto = cursor.fetchall()

    for _produto in dadosProduto:
        if _produto[1] > 0:
            comboProdutos.addItem(_produto[0])
    
def voltarTelaPrincipal(ui, stackWidget):
    stackWidget.setCurrentIndex(5)

    ui.comboBox.setCurrentIndex(-1)
    ui.comboBox.setCurrentIndex(-1)
    ui.comboBox_3.setCurrentIndex(-1)
    ui.frame_5.hide()
    ui.frame_6.hide()

def excluir(ui, stackWidget):
    stackWidget.setCurrentIndex(5)

    ui.comboBox.setCurrentIndex(-1)
    ui.comboBox.setCurrentIndex(-1)
    ui.comboBox_3.setCurrentIndex(-1)
    ui.frame_5.hide()
    ui.frame_6.hide()

def configVeiculosComboBox(ui):
    clienteAtual = ui.comboBox_2.currentText()
    cnx = carregarBD()
    cursor = cnx.cursor()

    if ui.comboBox.count() > 0:
        ui.comboBox.clear()

    cursor.execute("SELECT id_cliente, nome FROM clientes")
    dadosCliente = cursor.fetchall()

    cursor.execute("SELECT id_cliente, marca, modelo FROM veiculos")
    dadosVeiculo = cursor.fetchall()

    id_cliente = 0

    for _cliente in dadosCliente:
        if _cliente[1] == clienteAtual:
            id_cliente = _cliente[0]

    for _veiculo in dadosVeiculo:
        if _veiculo[0] == id_cliente:
            text = f"{_veiculo[1]} {_veiculo[2]}"
            ui.comboBox.addItem(text)

#region mudar o texto dos labels
def alterarLabelServico(ui):
    global TotalServico
    cnx = carregarBD()
    cursor = cnx.cursor()
    servicoAtual = ui.comboBox_4.currentText()

    cursor.execute("SELECT descrição, valorMaoObra FROM serviços")
    dadosServico = cursor.fetchall()
    for _servico in dadosServico:
        if servicoAtual == _servico[0]:
            ui.label_12.setText(_servico[0])
            ui.label_19.setText(f"Preço unitario: {_servico[1]}")
            valor = ui.spinBox.value() * _servico[1]
            ui.label_13.setText(str(valor))
    
    TotalServico = ui.label_13.text()
    ui.label_26.setText(TotalServico)

def alterarLabelProduto(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()
    global TotalProdutos
    produtoAtual = ui.comboBox_5.currentText()

    cursor.execute("SELECT descrição, preco_unitario, em_estoque FROM produtos")
    dadosProduto = cursor.fetchall()
    for _produto in dadosProduto:
        if produtoAtual == _produto[0]:
            ui.label_20.setText(f"Preço unitario: {_produto[1]}")
            valor = _produto[1] * ui.spinBox_2.value()
            ui.label_17.setText(str(valor))
    
    TotalProdutos = ui.label_17.text()
    ui.label_28.setText(TotalProdutos)

def configSubTotal(ui):
    if ui.comboBox_4.currentText() != "" and ui.comboBox_5.currentText() == "":

        subTotal = float(TotalServico)
        ui.label_30.setText(str(subTotal))
        if ui.lineEdit_4.text().strip != "":
            desconto = float(ui.lineEdit_4.text())/100
            subTotal = float(TotalServico) * desconto
            ui.label_30.setText(str(subTotal))
    elif ui.comboBox_4.currentText() != "" and ui.comboBox_5.currentText() != "":
        subTotal = float(TotalServico) + float(TotalProdutos)
        ui.label_30.setText(str(subTotal))
        
        if ui.lineEdit_4.text().strip != "":
            desconto = float(ui.lineEdit_4.text())/100
            subTotal = (float(TotalServico) + float(TotalProdutos))* desconto
            ui.label_30.setText(str(subTotal))

def configCodigoServico(ui):
    codigo = gere_codigo_ordem()
    
    ui.lineEdit_5.setText(codigo)
    ui.lineEdit_5.setDisabled(True)
#endregion

#region de butões do spin box
def aumentarServico(ui):
    valorAtual = ui.spinBox.value()
    novoValor = valorAtual + 1
    ui.spinBox.setValue(novoValor)

def diminuirServico(ui):
    valorAtual = ui.spinBox.value()
    novoValor = valorAtual - 1
    ui.spinBox.setValue(novoValor)

def aumentarProduto(ui):
    valorAtual = ui.spinBox_2.value()
    novoValor = valorAtual + 1
    ui.spinBox_2.setValue(novoValor)

def diminuirProduto(ui):
    valorAtual = ui.spinBox_2.value()
    novoValor = valorAtual - 1
    ui.spinBox_2.setValue(novoValor)
#endregion

#region adcionar serviço e produto
def adcionarNovoServico(ui):
    global listaServico
    ui.frame_5.show()

    index = 0
    listaServico = []
    if ui.comboBox_4.count() > 0:
        ui.comboBox_4.addItem(f"Serviço {index + 1}")
        servico = ui.comboBox_6.currentText()
        qnt = ui.spinBox.value()
        novoServico = [servico, qnt]
        listaServico.append(novoServico)


def adcionarNovoProduto(ui):
    global listaProduto
    ui.frame_6.show()

    index = 0
    listaProduto = []
    if ui.comboBox_5.count() > 0:
        ui.comboBox_5.addItem(f"Produto {index + 1}")
        produto = ui.comboBox_7.currentText()
        qnt = ui.spinBox_2.value()
        novoProduto = [produto, qnt]
        listaProduto.append(novoProduto)
#endregion

def registrarOrdem(ui, stackWidget):
    #region campos
    cnx = carregarBD()
    desconto = ui.lineEdit_4.text()
    cliente = ui.comboBox_2.currentText()
    veiculo = ui.comboBox.currentText()
    status = ui.comboBox.currentText()
    codigo = ui.lineEdit_5.text()
    data = ui.lineEdit_6.text()
    servico = ui.comboBox_4.currentText()
    produto = ui.comboBox_5.currentText()
    quantidadeServicos = ui.spinBox.value()
    quantidadeProdutos = ui.spinBox_2.value()
    #endregion

    #region procura e assimilação de dados
    #servico
    cursor = cnx.cursor()
    id_servico = 0
    valorServico = 0
    cursor.execute("SELECT id_servico, descrição, valor mão de obra FROM serviços")
    dadosServico = cursor.fetchall()

    for _servico in dadosServico:
        if _servico[1] == servico:
            id_servico = _servico[0]
            valorServico = _servico[2]
    
    #veiculo
    id_veiculo = 0
    cursor.execute("SELECT id_veiculo, marca, modelo FROM veiculos")
    dadosVeiculos = cursor.fetchall()
    for _veiculo in dadosVeiculos:
        if veiculo.strip() == _veiculo[1] + _veiculo[2]:
            id_veiculo = _veiculo[0]

    #id_funcioario
    cursor.execute("SELECT id_funcionario, login FROM usuarios")
    dadosUser = cursor.fetchall()
    id_funcionario = 0

    for _usuario in dadosUser:
        if _usuario[1] == user.login:
            id_funcionario = _usuario[0]

    #cliente
    cursor.execute("SELECT id_cliente, nome FROM clientes")
    dadoscliente = cursor.fetchall()
    id_cliente = 0

    for _cliente in dadoscliente:
        if cliente == _cliente[1]:
            id_cliente = _cliente[0]

    if produto != "":
        id_produto = 0
        valorProduto = 0
        cursor.execute("SELECT id_produto, preco_unitario, descrição FROM produtos")
        dadosProdutos = cursor.fetchall()

        for _produto in dadosProdutos:
                if _produto[2] == produto:
                    valorProduto = _produto[1]
                    id_produto = _produto[0]

        comandoSqlUpdateServico = "UPDATE serviço SET id_produto WHERE id_servico = %s"
        val = (id_produto,)
        cursor.execute(comandoSqlUpdateServico, val)
    #endregion

    if desconto.strip() != "":
        desconto = float(desconto)/100
        comandoInsertOrdem = "INSERT INTO `ordem de serviços`(id_funcionario, id_cliente, id_serviço, codigo, id_carro, Status, desconto,agendamento, quantidade_produtos, quantidade_serviços) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dadosOrdem = (id_funcionario, id_cliente, id_servico, codigo, id_veiculo, status, desconto,data, quantidadeServicos, quantidadeProdutos)
        cursor.execute(comandoInsertOrdem, dadosOrdem)

    comandoInsertOrdem = "INSERT INTO `ordem de serviços`(id_funcionario, id_cliente, id_serviço, codigo, id_carro, Status, agendamento, quantidade_produtos, quantidade_serviços) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    dadosOrdem = (id_funcionario, id_cliente, id_servico, codigo, id_veiculo, status, data, quantidadeServicos, quantidadeProdutos)
    cursor.execute(comandoInsertOrdem, dadosOrdem)

def configTelaOrdemCadastro(stackWidget):
    ui = uic.loadUi("Telas/tela ordem de serviço cadastro.ui")

    stackWidget.addWidget(ui)
    configCodigoServico(ui)
    ui.frame_5.hide()
    ui.frame_6.hide()

    #butões
    ui.pushButton.clicked.connect(lambda: registrarOrdem(ui, stackWidget))
    ui.pushButton_2.clicked.connect(lambda: excluir(ui, stackWidget))
    ui.pushButton_3.clicked.connect(lambda: voltarTelaPrincipal(ui ,stackWidget))
    ui.pushButton_4.clicked.connect(lambda: aumentarServico(ui))
    ui.pushButton_5.clicked.connect(lambda: diminuirServico(ui))
    ui.pushButton_6.clicked.connect(lambda: aumentarProduto(ui))
    ui.pushButton_7.clicked.connect(lambda: diminuirProduto(ui))
    ui.pushbutton_8.clicked.connect(lambda: adcionarNovoServico(ui))
    ui.pushButton_9.clicked.connect(lambda: adcionarNovoProduto(ui))

    #combo box
    ui.comboBox_2.currentIndexChanged.connect(lambda: configVeiculosComboBox(ui))
    ui.comboBox_4.currentIndexChanged.connect(lambda: alterarLabelServico(ui))
    ui.comboBox_5.currentIndexChanged.connect(lambda: alterarLabelProduto(ui))
    ui.comboBox_4.currentIndexChanged.connect(lambda: configSubTotal(ui))
    ui.comboBox_5.currentIndexChanged.connect(lambda: configSubTotal(ui))
    
    #spin box
    ui.spinBox.valueChanged.connect(lambda: alterarLabelServico(ui))
    ui.spinBox.valueChanged.connect(lambda: configSubTotal(ui))
    ui.spinBox_2.valueChanged.connect(lambda: alterarLabelProduto(ui))
    ui.spinBox_2.valueChanged.connect(lambda: configSubTotal(ui))