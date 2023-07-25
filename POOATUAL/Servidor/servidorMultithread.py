import socket
import sys
from formatadados import formatadados
from banco import Banco # importo banco
import threading
import socket

class servidorMulthread(threading.Thread):
    """
    A classe servidorMulthread representa uma thread que lida com a comunicacao de um cliente especifico

    Essa funcao recebe os dados do cliente, processa e envia a resposta de volta ao cliente 

    Attributes
    ----------
    enderCliente : str
        Variavel que guarda o endereco de cada cliente
    socketCliente : object
        Objeto socket do cliente que e usado para realizar a comunicacao entre o servidor e o cliente.

    Methods
    -------
    run()
        Esse metodo e o ponto de entrada para a execucao da thread
    """

    def __init__(self,enderCliente,socketCliente):
        """
        Parameters
        ----------
        enderCliente : str
           Variavel que guarda o endereco de cada cliente
        datsocketClienteabase : str
            Objeto socket do cliente 
        """

        threading.Thread.__init__(self)
        self.enderCliente = enderCliente
        self.socketCliente = socketCliente
        self.sinc = threading.Lock()
        self.Banco = Banco()

    def run(self):
        """
        Esse metodo e o ponto de entrada para a execucao da thread
        
        E o ponto de execucao da thread, ele implementa o comportamento das mesmas
        """
        while True:
            self.sinc.acquire()
            dados = self.socketCliente.recv(1024).decode()
            print('aquii')
            recebe = formatadados(dados,self.Banco)
            self.sinc.release()
            self.socketCliente.send(recebe.encode('utf-8'))
            
    
if __name__ == '__main__':
    servidor = servidorMulthread()
    sys.exit() 
