import sys
import os
from datetime import datetime,date,timedelta
import socket

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QFileDialog, QListWidgetItem
from PyQt5.QtCore import QCoreApplication

from cadastrasintoma import telaCadSintoma
from cadastro import cadUsuario
from historico import historico
from inicial import inicial
from login import login
from main import main
from notificacoes import notificar
from redCalendar import redcalendar
from redCalendar2 import redCalendar2
from telaCad01 import telaCad1
from telaCad02 import telaCad2
from telaCad03 import telaCad3

class Ui_Main(QtWidgets.QWidget):
    """
    A classe Ui_Main estabelece e personaliza a interface grafica principal

    Ela se encarrega de criar e configurar os componentes visuais da interface, alem de lidar com as funcionalidades essenciais para o correto funcionamento do programa.

    Methods
    -------
    setupUi(Main)
        Responsavel por realizar as configuracoes principais 
    """
    
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(640,480)
        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()
        self.stack7 = QtWidgets.QMainWindow()
        self.stack8 = QtWidgets.QMainWindow()
        self.stack9 = QtWidgets.QMainWindow()
        self.stack10 = QtWidgets.QMainWindow()
        self.stack11 = QtWidgets.QMainWindow()
        
        # 0
        self.telaCadSintoma = telaCadSintoma()
        self.telaCadSintoma.setupUi(self.stack5)
        # 1
        self.cadUsuario = cadUsuario()
        self.cadUsuario.setupUi(self.stack1)
        # 2
        self.historico = historico()
        self.historico.setupUi(self.stack2)
        # 3
        self.inicial = inicial()
        self.inicial.setupUi(self.stack3)
        # 4
        self.login = login()
        self.login.setupUi(self.stack4)
        # 5
        self.main = main()
        self.main.setupUi(self.stack0)
        # 6
        self.notificar = notificar()
        self.notificar.setupUi(self.stack6)
        # 7
        self.redcalendar = redcalendar()
        self.redcalendar.setupUi(self.stack7)
        # 8 
        self.telaCad1 = telaCad1()
        self.telaCad1.setupUi(self.stack8)
        # 9
        self.telaCad2 = telaCad2()
        self.telaCad2.setupUi(self.stack9)
        # 10
        self.telaCad3 = telaCad3()
        self.telaCad3.setupUi(self.stack10)
        # 11
        self.redCalendar2 = redCalendar2()
        self.redCalendar2.setupUi(self.stack11)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1) # cadastro
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4) # login
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)
        self.QtStack.addWidget(self.stack8) # cadastro 1 - pergunta 1
        self.QtStack.addWidget(self.stack9) # cadastro 2 - pergunta 2
        self.QtStack.addWidget(self.stack10) # cadastro 3 - pergunta 3
        self.QtStack.addWidget(self.stack11)  #registro

class Main(QMainWindow,Ui_Main):
    """
    A classe Main estabelece e personaliza a interface grafica principal

    Ela tambem se encarrega de criar e configurar os componentes e aplicacoes para lidar com as funcionalidades de cada parte do sistema
    
    Attributes
    ----------
    parent : objeto/widget,opcional
        Variavel que representa o widget pai, ou seja, o widget no qual a janela principal será incorporada

    Methods
    -------
    registro()
        Responsavel por realizar um registro de cada usuario  
    registrar()
        Responsavel por realizar a selecao da data marcada no calendario
    verificaestado()
        Responsavel por verificar o registro da data de menstruacao e calcular a diferenca de dias
    calendario()
        Executa uma tela, e chamada a tela do calendario
    histo()
        Responsavel por apresentar todo o historico de sintomas do usuario
    notificacoes()
        Responsavel por obter as notificacoes do banco de dados 
    cadastro1()
        Executa uma tela, a tela da primeira pergunta para realizacao do cadastro
    cadastro2Sim()
        Executa uma tela, a tela da segunda pergunta para realizacao do cadastro
        Se a resposta for sim, os dias serao calculados
    cadastro2Nao()
        Executa uma tela, a tela da segunda pergunta para realizacao do cadastro
        Se a resposta for nao, os dias serao calculados com outra quantidade
    cadastro3()
        Executa uma tela, a tela da terceira pergunta para realizacao do cadastro
    retornaLogin()
        Executa uma tela, a tela de login para realizar a entrada do usuario no sistema
    retornaCadastro()
        Executa uma tela, a tela de cadastro em si para entrada do usuario
    voltar()
        Funcao para realizar a volta da tela inicial do sistema
    voltar2()
        Funcao para realizar a volta do calendario
    sair()
        Funcao para encerrar o programa
    realizaLogin()
        Funcao responsavel por realizar o login do usuario 
    retornaMain()
        Funcao para realizar a volta da tela inicial do sistema
    cadastrarUsuario()
        Funcao responsavel por cadastrar o usuario em si
    conectandosocket()
        Função responsavel por conectar o banco de dados
    recebe()
        Funcao responsavel por receber a mensagem do servidor
    manda()
        Funcao responsavel por enviar uma mensagem para o servidor
    """

    def __init__(self, parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)

        #id já salvo digamos assim
        #variaveis para guardar valores que vão auxiliar nas atribuições no banco de dados
        self.regular = None  #guarda o ciclo (dias)
        self.clienteLogado = None #Aqui guarda o id do usuario
        self.conexaosocket = None #variavel que guarda conexão (recebe e envia)
        self.idcalendario = None  #Aqui guarda o id do calendario do usuario
        self.ciclo = None  #guarda as informações do ciclo
        self.dataselecionada = None #guarda a data selecionada lá no calendario 

        self.main.pushButton.clicked.connect(self.cadastro1) # ok
        self.main.pushButton_1.clicked.connect(self.retornaLogin) # ok

        self.login.pushButton.clicked.connect(self.realizaLogin) # ok
        self.login.pushButton_2.clicked.connect(self.retornaMain) # ok

        self.telaCad1.pushButton.clicked.connect(self.cadastro2Nao) 
        self.telaCad1.pushButton_2.clicked.connect(self.cadastro2Sim) 

        self.telaCad2.pushButton.clicked.connect(self.cadastro3) # ok não
        self.telaCad2.pushButton_2.clicked.connect(self.cadastro3) # ok sim

        self.telaCad3.pushButton.clicked.connect(self.retornaCadastro) # ok não
        self.telaCad3.pushButton_2.clicked.connect(self.retornaCadastro) # ok sim

        self.cadUsuario.pushButton.clicked.connect(self.cadastrarUsuario)
        self.cadUsuario.pushButton_1.clicked.connect(self.retornaMain) # principal

        self.inicial.pushButton_2.clicked.connect(self.calendario)
        self.inicial.pushButton_7.clicked.connect(self.histo)
        self.inicial.pushButton_4.clicked.connect(self.notificacoes)
        self.inicial.pushButton_5.clicked.connect(self.sair)

        self.redcalendar.pushButton_2.clicked.connect(self.registrar)
        self.redcalendar.pushButton_3.clicked.connect(self.voltar)

        self.historico.pushButton_3.clicked.connect(self.voltar)

        self.notificar.pushButton_3.clicked.connect(self.voltar)

        self.redCalendar2.pushButton_3.clicked.connect(self.voltar2)
        self.redCalendar2.pushButton_2.clicked.connect(self.registro)

        self.telaCadSintoma.pushButton_3.clicked.connect(self.voltar2)

    def registro(self):
        """
        Funcao responsavel por realizar um registro de cada usuario

        Cada usuario possui um registro especifico de cada acao ocorrida naquele determiando periodo
        """
        
        fluxo = self.redCalendar2.lineEdit_1.text()
        sintomas = self.redCalendar2.lineEdit_2.text()
        descricao = self.redCalendar2.lineEdit_3.text()
        datafinal = self.redCalendar2.dateEdit.text()

        if (fluxo == '' or sintomas == '' or descricao == '' or datafinal == ''):
            QMessageBox.information(None,'RedCalender',"Preencha todos os campos!")

        else:
            lista = self.dataselecionada.split('/')
            tempo = date(day=int(lista[0]), month=int(lista[1]), year=int(lista[2]))
            td = timedelta(int(self.ciclo))
            dia = str(tempo+td)
            separar = dia.split('-')
            diaprevi = f'{separar[2]}/{separar[1]}/{separar[0]}'

            dadosregistros = f'criaregis;{self.dataselecionada};{fluxo};{sintomas};{descricao};{datafinal};{self.idcalendario};{diaprevi}'
            self.manda(dadosregistros)
            dadosregistros = self.recebe()
            
            dadosnot = f'crianot;{self.clienteLogado};A sua próxima menstruação está prevista para {diaprevi}'
            self.manda(dadosnot)
            dadosnot = self.recebe()
            QMessageBox.information(None,'RedCalender',dadosregistros[0]) 

            self.QtStack.setCurrentIndex(3)

    
    def registrar(self):
        """
        Funcao responsavel por realizar a selecao da data marcada no calendario

        Ao realizar essa selecao, essa funcao separa cada parte dessa data no formato comum da data (modelo padrao)
        """
        
        var = str(self.redcalendar.calendarWidget.selectedDate())
        separar = var[19:].split(',')
        for i in range(len(separar)):
            separar[i] = separar[i].replace(')','')
            separar[i] = separar[i].replace(' ','')

        self.dataselecionada = f'{separar[2]}/{separar[1]}/{separar[0]}' 

        self.QtStack.setCurrentIndex(11)

    
    def verificaestado(self):
        """
        Responsavel por verificar o registro da data de menstruação e calcular a diferença de dias

        Esse calculo da diferenca de dias e realizada em relacao com o da data do registro e a data atual,
        onde e enviado notificacoes com base nessa diferenca, para avisar ao usuario que a menstruacao esta proxima
        """
        pegaregienv = f'verificaregis;{self.idcalendario}'
        self.manda(pegaregienv)
        pegaregi = self.recebe()

        if pegaregi[0] !=  "Não possui registro!":
            agora = datetime.now()
            dataatual = agora.strftime('%d/%m/%Y')
            lista1 = pegaregi[0].split('/')
            lista2 = dataatual.split('/')
            tempo1 = date(day=int(lista1[0]), month=int(lista1[1]), year=int(lista1[2]))   
            tempo2 = date(day=int(lista2[0]), month=int(lista2[1]), year=int(lista2[2]))
            dias = tempo1 - tempo2
            aux = str(dias).split(' ')

            if aux[0] == '0:00:00':
                difdias = 0
            else:
                difdias = int(aux[0])
            
            if difdias <= 2 and difdias > 0:
                dadosnot = f'crianot;{self.clienteLogado};Sua menstruação está chegando! Falta(m) apena(s) {difdias} dia(s)'
                self.manda(dadosnot)
                dadosnot = self.recebe()

            elif difdias == 0:
                dadosnot = f'crianot;{self.clienteLogado};Sua menstruação chegou hoje? Registre-a!'
                self.manda(dadosnot)
                dadosnot = self.recebe()

            elif difdias < 0:
                dadosnot = f'crianot;{self.clienteLogado};Você esqueceu de nos informar sua menstruação, por favor registre-a!'
                self.manda(dadosnot)
                dadosnot = self.recebe()
                
    def calendario(self):
        """
        Funcao realizada para abrir a tela do calendario

        ...
        """
        self.QtStack.setCurrentIndex(7)

    
    def histo(self):
        """
        Responsavel por apresentar todo o historico de sintomas do usuario

        Apresentar todo os sintomas do usuario naquele respectivo período
        """
        pegahist = f'historico;{self.idcalendario}'
        self.manda(pegahist)
        pegahist = self.recebe()

        if pegahist != []:
            self.historico.listWidget.clear()
            for i in pegahist[1:]:
                separar = i.split('-')
                hist = f'Durante o período de {separar[1]} até {separar[2]} você sentiu: {separar[0]}'

                item = QListWidgetItem(hist)
                self.historico.listWidget.addItem(item)

        self.QtStack.setCurrentIndex(2)


    def notificacoes(self):
        """
        Funcao que recebe as notificacoes do banco 

        Obtem as notificacoes relacionadas ao cliente logado, limpa a lista de notificacoes exibida e adiciona as novas para exibir ao usuario
        """
        peganot = f'notifi;{self.clienteLogado}'
        self.manda(peganot)
        peganot = self.recebe()

        self.notificar.listWidget.clear()
        for i in peganot:
            item = QListWidgetItem(i)
            self.notificar.listWidget.addItem(item)

        self.QtStack.setCurrentIndex(6)

    def cadastro1(self):
        """
        Funcao realizada para abrir a tela da primeira pergunta de cadastro
        
        ...
        """

        self.QtStack.setCurrentIndex(8)
    
    def cadastro2Sim(self):
        """
        Funcao realizada para abrir a tela da segunda pergunta de cadastro
        
        Se a resposta selecionada dessa pergunta for sim e realizado o calculo da estimativa da 
        menstruacao por base no ciclo regular
        """
        self.regular =[True, 28]
        self.QtStack.setCurrentIndex(9)

    def cadastro2Nao(self):
        """
        Funcao realizada para abrir a tela da segunda pergunta de cadastro
        
        Se a resposta selecionada dessa pergunta for nao e realizado o calculo da estimativa da 
        menstruacao por base no ciclo irregular
        """
        self.regular = [False, 35]
        self.QtStack.setCurrentIndex(9)
    
    def cadastro3(self):
        """
        Funcao realizada para abrir a tela da primeira pergunta de cadastro
        
        ...
        """
        self.QtStack.setCurrentIndex(10)

    def retornaLogin(self):
        """
        Executa uma tela, a tela de login para realizar a entrada do usuario no sistema
        
        ...
        """
        self.QtStack.setCurrentIndex(4)

    def retornaCadastro(self):
        """
        Executa uma tela, a tela de cadastro em si

        E a tela de cadastro em si, com as informcoes do usuario para realizar a entrada do mesmo no sistema
        """
        self.QtStack.setCurrentIndex(1)

    def voltar(self):
        """
        Funcao para realizar a volta da tela inicial do sistema
        
        ...
        """
        self.QtStack.setCurrentIndex(3)
    
    def voltar2(self):
        """
        Funcao para realizar a volta do calendario
        
        ...
        """
        self.QtStack.setCurrentIndex(7)

    def sair(self):
        """
        Funcao para encerrar o programa
        
        ...
        """
        return exit()

    def realizaLogin(self):
        """
        Funcao responsavel por realizar o login do usuario 
        
        ...
        """
        email = self.login.lineEdit.text()
        senha = self.login.lineEdit_2.text()

        if self.conexaosocket == None: 
            self.conexaosocket = self.conectandosocket()

        dados_enviando = f'login;{email};{senha}'

        self.manda(dados_enviando)
        dados = self.recebe()

        if dados[0] == "Não existe email cadastrado!":
            QMessageBox.information(None,'RedCalender',"Não existe email cadastrado!")
            self.QtStack.setCurrentIndex(4)
        
        elif dados[0] == "Login realizado com sucesso!":
            self.clienteLogado = dados[1]
            self.idcalendario = dados[2]
            self.ciclo = dados[3]
            self.regular = dados[4]
            QMessageBox.information(None,'RedCalender',"Login realizado com sucesso!")
            self.verificaestado()
            self.QtStack.setCurrentIndex(3)

        elif dados[0] == "Senha incorreta!":
            QMessageBox.information(None,'RedCalender',"Senha incorreta!")
            self.QtStack.setCurrentIndex(4)

        else:
            QMessageBox.information(None,'RedCalender',"Erro não identificado!")
        #print(dados)
        # print(nome,email,nascimento,senha)
    
    def retornaMain(self):
        """
        Funcao para realizar a volta da tela inicial do sistema
        
        ...
        """
        self.QtStack.setCurrentIndex(0)
    
     
    def cadastrarUsuario(self):
        """
        Funcao responsavel por cadastrar o usuario em si
        
        ...
        """

        nome = self.cadUsuario.lineEdit_1.text()
        email = self.cadUsuario.lineEdit_2.text()
        nascimento = self.cadUsuario.dateEdit_3.text()
        senha = self.cadUsuario.lineEdit_4.text()
        
        if self.conexaosocket == None: 
            self.conexaosocket = self.conectandosocket()

        dados_enviando = f'cadastro;{nome};{email};{nascimento};{senha}'

        self.manda(dados_enviando)
        dados = self.recebe()
        
        #[o que aconteceu,id_usuario]
        #dados[1] = id usuario
        if dados[0] == 'Cadastro com sucesso!':
            self.clienteLogado = dados[1]
            dadosnot = f'crianot;{dados[1]};Bem vindo ao RedCalender!!!'
            self.manda(dadosnot)
            recebenoti = self.recebe()
            dadoscalend = f'criacalend;{self.regular[0]};{self.regular[1]};{dados[1]}'
            self.manda(dadoscalend)
            #mensagem que recebo na criação do calend
            dadosrecebidoscalen = self.recebe()
            #recebo uma lista normal
            self.idcalendario = dadosrecebidoscalen[1]
            self.ciclo = dadosrecebidoscalen[2]
            self.regular = dadosrecebidoscalen[3]
            QMessageBox.information(None,'RedCalender','Cadastro realizado com sucesso!')
            self.QtStack.setCurrentIndex(3)

        elif dados[0] == 'Já existe usuário com esse email!':
            QMessageBox.information(None,'RedCalender','Já existe usuário com esse email!')
            self.QtStack.setCurrentIndex(1)

    
    def conectandosocket(self):
        """
        Funcao responsavel por conectar o banco de dados
        
        ...

        Returns 
        -------
        object
            Retorna o objeto de conexao criado
        """

        ip = '10.0.1.103'
        port = 9090
        addr = ((ip,port))
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(addr)
        return cliente_socket
        #Retorna um atr do tipo socket que envia e recebe dados
        #já retorna o socket conectado

    
    def recebe(self):
        """
        Funcao responsavel por receber a mensagem do servidor
        
        ...

        Returns 
        -------
        list
            Retorna uma lista com os dados vindo do servidor
        """

        dados_recebidos = self.conexaosocket.recv(1024).decode('utf-8')
        dados = dados_recebidos.split(';')
        return dados

    
    def manda(self,dados):
        """
        Funcao que envia uma mensagem para o servidor
        
        ...
        """

        # o utf-8 pra palavras com acento
        self.conexaosocket.send(dados.encode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())