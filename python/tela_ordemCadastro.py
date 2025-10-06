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
    servicoAtual = ui.comboBox_6.currentText()
    TotalServico = 0

    cursor.execute("SELECT descrição, valorMaoObra FROM serviços")
    dadosServico = cursor.fetchall()
    for _servico in dadosServico:
        if servicoAtual == _servico[0]:
            ui.label_19.setText(str(_servico[1]))
            valor = ui.spinBox.value() * _servico[1]
            ui.label_13.setText(str(valor))
    
    if ui.comboBox_4.count() == 1:
        TotalServico += float(ui.label_13.text())
        ui.label_26.setText(str(TotalServico))
    else:
        for _servico in listaServico:
            TotalServico += _servico[1] + float(ui.label_13.text())
        
        ui.label_26.setText(str(TotalServico))

def alterarLabelProduto(ui):
    global TotalProdutos
    cnx = carregarBD()
    cursor = cnx.cursor()
    produtoAtual = ui.comboBox_7.currentText()
    TotalProdutos = 0

    cursor.execute("SELECT descrição, preco_unitario, em_estoque FROM produtos")
    dadosProduto = cursor.fetchall()
    for _produto in dadosProduto:
        if produtoAtual == _produto[0]:
            ui.label_20.setText(str(_produto[1]))
            valor = ui.spinBox_2.value() * _produto[1]
            ui.label_17.setText(str(valor))

    if ui.comboBox_5.count() == 1:
        TotalProdutos += float(ui.label_17.text())
        ui.label_28.setText(str(TotalProdutos))
    else:
        for _produto in listaProduto:
            TotalProdutos += _produto[1] + float(ui.label_17.text())
        
        ui.label_28.setText(str(TotalProdutos))

def configSubTotal(ui):
    textoDesconto = ui.lineEdit_4.text()
    subTotal = 0
    
    if textoDesconto.strip() != ".":
        if ui.spinBox_2.value() == 0:
            valorDesconto = float(textoDesconto)
            subTotal = TotalServico * valorDesconto/100
            ui.label_31.setText(str(subTotal))
        else:
            valorDesconto = float(textoDesconto)
            subTotal = (TotalServico + TotalProdutos)* valorDesconto/100
            ui.label_31.setText(str(subTotal))
    else:
        if ui.spinBox_2.value() == 0:
            subTotal = TotalServico
            ui.label_31.setText(str(subTotal))
        else:
            subTotal = TotalServico + TotalProdutos
            ui.label_31.setText(str(subTotal))

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
    ui.comboBox_4.addItem(f"Serviço {ui.comboBox_4.count() + 1}")
    novoIndex = ui.comboBox_4.count() - 1
    ui.comboBox_4.setCurrentIndex(novoIndex)
    
    listaServico = []
    if ui.comboBox_4.count() > 0:
        servico = ui.comboBox_6.currentText()
        totalServicoAtual = float(ui.label_13.text())
        qnt = ui.spinBox.value()
        novoServico = [servico, totalServicoAtual,qnt]
        listaServico.append(novoServico)
        ui.spinBox.setValue(0)

def adcionarNovoProduto(ui):
    global listaProduto
    ui.frame_6.show()
    ui.comboBox_5.addItem(f"Produto {ui.comboBox_5.count() + 1}")
    novoIndex = ui.comboBox_5.count() - 1
    ui.comboBox_5.setCurrentIndex(novoIndex)
    
    listaProduto = []
    if ui.comboBox_5.count() > 0:
        produto = ui.comboBox_7.currentText()
        qnt = ui.spinBox_2.value()
        totalProdutoAtual = float(ui.label_17.text()) 
        novoProduto = [produto, totalProdutoAtual, qnt]
        listaProduto.append(novoProduto)
        ui.spinBox_2.setValue(0)
#endregion

def cadastrarItemAtendente(ui):
    cnx = carregarBD()
    cursor = cnx.cursor()

    #buscar id do cliente
    cursor.execute("SELECT id_cliente, nome FROM clientes")
    dadosCliente = cursor.fetchall()
    id_cliente = 0

    for _cliente in dadosCliente:
        if ui.comboBox_2.currentText() == _cliente[1]:
            id_cliente = _cliente[0]
    
    #busca id do funcionario que registra a nota
    cursor.execute("SELECT id_funcionario, login FROM usuarios")
    dadosUser = cursor.fetchall()
    id_funcionario = 0

    for _user in dadosUser:
        if _user[1] == user.login:
            id_funcionario= _user[0]

    #registrar
    sqlComando = "INSERT INTO Atendente(Clientes_id_cliente, Funcionario_id_funcionario) VALUES (%s, %s)"
    dadosComando = (id_cliente, id_funcionario)
    cursor.execute(sqlComando, dadosComando)
    cnx.commit()

def registrarOrdem(ui, stackWidget):
    #region campos
    cnx = carregarBD()
    cursor = cnx.cursor(buffered=True)
    desconto = ui.lineEdit_4.text()
    cliente = ui.comboBox_2.currentText()
    veiculo = ui.comboBox.currentText()
    status = ui.comboBox_3.currentText()
    codigo = ui.lineEdit_5.text()
    data = ui.lineEdit_6.text()
    servico = ui.comboBox_6.currentText()
    produto = ui.comboBox_7.currentText()
    quantidadeServicos = ui.spinBox.value()
    quantidadeProdutos = ui.spinBox_2.value()
    #endregion

    #registrar atendente
    cursor.execute("SELECT id_funcionario, login FROM usuarios")
    dadosUser = cursor.fetchall()
    id_funcionario = 0

    for _user in dadosUser:
        if _user[1] == user.login:
            id_funcionario= _user[0]

    cadastrarItemAtendente(ui)
    cursor.execute("SELECT id_atendente FROM atendente WHERE Funcionario_id_funcionario = %s", (id_funcionario,))
    dadosAtendente = cursor.fetchone()
    id_atendente = dadosAtendente[0]

    #region procura e assimilação de dados
    #servico
    id_servico = 0
    valorServico = 0
    cursor.execute("SELECT id_serviço, descrição FROM serviços")
    dadosServico = cursor.fetchall()

    for _servico in dadosServico:
        if _servico[1] == servico:
            id_servico = _servico[0]
    
    #veiculo
    id_veiculo = 0
    cursor.execute("SELECT id_veiculo, marca, modelo FROM veiculos")
    dadosVeiculos = cursor.fetchall()
    for _veiculo in dadosVeiculos:
        nomeVeiculo = f"{_veiculo[1]} {_veiculo[2]}"
        if veiculo == nomeVeiculo:
            id_veiculo = _veiculo[0]

    for _usuario in dadosUser:
        if _usuario[1] == user.login:
            id_funcionario = _usuario[0]

    #produto
    if produto != "":
        id_produto = 0
        cursor.execute("SELECT id_produto, descrição FROM produtos")
        dadosProdutos = cursor.fetchall()

        for _produto in dadosProdutos:
                if _produto[1] == produto:
                    id_produto = _produto[0]

        comandoSqlUpdateServico = "UPDATE serviços SET id_produto = %s WHERE id_serviço = %s"
        val = (id_produto, id_servico)
        cursor.execute(comandoSqlUpdateServico, val)
    #endregion

    #tem o codigo
    cursor.execute("SELECT codigo FROM `ordem de serviços`")
    codigosResultado = cursor.fetchall()
    for _codigo in codigosResultado:
        if codigo == _codigo[0]:
            print("codigo igual")
            ui.lineEdit_5.setText(gere_codigo_ordem())

    if desconto.strip() != ".":
        print(id_atendente, id_servico, id_veiculo, codigo, status, desconto, data, quantidadeServicos, quantidadeProdutos)
        desconto = float(desconto)/100
        comandoInsertOrdem = "INSERT INTO `ordem de serviços`(id_atendente, id_serviço, id_veiculo, codigo, Status, desconto, agendamento, quantidade_produtos, quantidade_serviços) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dadosOrdem = (id_atendente, id_servico, id_veiculo, codigo, status, desconto, data, quantidadeServicos, quantidadeProdutos)
        cursor.execute(comandoInsertOrdem, dadosOrdem)
        cnx.commit()
        print("sucesso !")
        
        stackWidget.setCurrentIndex(5)

        #armazenar o valor Total no banco de dados (vou esperar o professor para ver essa questão)
        #registrar equipe mecanicos

        # #id da nova ordem de serviço
        # cursor.execute("SELECT MAX(id_ordemServiço) FROM `Ordem de Serviços`")
        # id_novaOrdem = cursor.fetchone() # depois me informa mais sobre isso parece super util
        
        # #id do mecanico
        # cursor.execute("SELECT MAX(id_mecanico) FROM mecanicos")
        # id_mecanico = cursor.fetchone()

        # comandosqlRegistroEquipe = "INSERT INTO equipe_mecanicos(mecanicos_id_mecanico, `Ordem de Serviço_id_ordemServiço`) VALUES (%s, %s)"
        # dadosRegistroEquipe = (id_mecanico[0], id_novaOrdem[0])
        # cursor.execute(comandoInsertOrdem, dadosOrdem)
        # cnx.commit()
    else:
        print(id_atendente, id_servico, id_veiculo, codigo, status, data, quantidadeServicos, quantidadeProdutos)
        comandoInsertOrdem = "INSERT INTO `ordem de serviços`(id_atendente, id_serviço, id_veiculo, codigo, Status, agendamento, quantidade_produtos, quantidade_serviços) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        dadosOrdem = (id_atendente, id_servico, id_veiculo, codigo, status, data, quantidadeServicos, quantidadeProdutos)
        cursor.execute(comandoInsertOrdem, dadosOrdem)
        cnx.commit()

        print("sucesso !")        
        stackWidget.setCurrentIndex(5)
    

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
    ui.pushButton_8.clicked.connect(lambda: adcionarNovoServico(ui))
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