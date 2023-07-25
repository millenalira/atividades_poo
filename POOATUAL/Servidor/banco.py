import psycopg2

class Banco:
    """
    A classe usada para representar o banco de dados

    Essa classe e responsavel por definir as funcionalidades do banco de dados,ou seja, suas operacoes e conexoes

    Attributes
    ----------
    host : str
        string responsavel por conter o numero do ip do computador conectado a rede
    database : str
        nome da minha base de dados, do meu banco de dados
    user : str
        nome do banco responsavel pelos dados
    password : str
        senha utilizada para acessar o banco de dados
    con : object, opicional     
        Objeto de conexao que representa a conexao estabelecida com o banco de dados
    cursor : object, opicional
        Objeto usado para executar comandos SQL e recuperar resultados de consultas no banco de dados

    Methods
    -------
    conecta()
        Responsavel por conectar o banco de dados 
    desconecta()
        Realiza a desconexao do banco de dados 
    qselect()
        Realiza a selecao, a busca de algum dado no banco
    qinsert()
        Realiza a insercao dos dados no banco 
    """


    def __init__(self,host='localhost',database='redCalender',user='postgres',password='milena'):
        """
        Parameters
        ----------
        host : str
            string responsavel por conter o numero do IP do computador conectado a rede
        database : str 
            nome da minha base de dados, do meu banco de dados
        user : str 
            nome do banco responsavel pelos dados
        password : str
            senha utilizada para acessar o banco de dados
        """
        
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.con = None
        self.cursor = None

    def conecta(self):
        """
        Responsavel por conectar o banco de dados 

        Funcao que estabelece uma conexao com o banco e prepara o cursor para executar consultas
        """

        self.con = psycopg2.connect(host=self.host,database=self.database,user=self.user, password=self.password)
        self.cursor = self.con.cursor()
        

    def desconecta(self):
        """Responsavel por desconectar o banco de dados 

        Essa funcao encerra a conexao com o banco apos ter sido concluido todas as operacoes necessarias.
        Fechar a conexao e importante para liberar recursos e garantir que a conexao nao permaneca aberta indefinidamente
        """

        self.con.close()
    
    def qselect(self,sql):
        """
        Responsavel por realizar uma consulta no banco de dados

        Faz uma selecao, uma busca de algum dado pelo banco

        Parameters
        ----------
        sql : str
            variavel que contem a instrucao SQL completa para realizar a consulta

        Returns
        -------
        list
        Retorna os resultados da consulta SQL que e uma lista de tuplas, onde cada tupla representa uma linha do resultado da consulta
        """

        self.conecta()
        self.cursor.execute(sql)
        resposta = self.cursor.fetchall()
        self.desconecta()
        return resposta
    
    def qinsert(self,sql):
        """
        Responsavel por realizar a insercao no banco de dados

        Essa funcao faz a insercao dos dados em uma tabela do banco de dados. 
        Ela estabelece a conexao, executa a operação de insercao, confirma a transacao e fecha a conexao apos a conclusao

        Parameters
        ----------
        sql : str
            variavel que contem a instrucao SQL completa para realizar a consulta, incluindo a tabela de destino e os valores a serem inseridos.

        """

        self.conecta()
        self.cursor.execute(sql)
        self.con.commit()  #finalizar o operação no bd
        self.desconecta()
