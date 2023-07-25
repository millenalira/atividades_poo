from servidorMultithread import servidorMulthread
import socket
import sys


class Servidor():
    """
    A class servidor e utilizada para realizar as conexoes com o usuario

    Essa classe e responsavel por conectar-se com os usuarios e esta sempre a espera por uma nova conexao

    Methods
    -------
    run()
        Esse metodo configura o servidor,ou seja, inicia um loop para aguardar e aceitar conexoes dos clientes
    """
    
    def __init__(self):
        self.run()
        
    def run(self):
        """
        Cria um servidor e aceita as conexoes do usuario

        Esse metodo configura o servidor,ou seja, inicia um loop para aguardar e aceitar conexoes dos clientes
        """

        host = '10.0.1.103'
        port = 9090
        addr = (host, port)
        serv_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serv_socket.bind(addr)
        while True:
            # o sockte esta aguardando o usuario enviar informacoes
            serv_socket.listen(1)
            #quando cliente se conectar as informacoes do socket e do endereco do
            #cliente sao enviadas para o servidor multhread
             
            clientsock, clienteAddress = serv_socket.accept() 
            newthread = servidorMulthread(clienteAddress,clientsock)
            newthread.start()
        
if __name__ == '__main__':
    servidor = Servidor()
    sys.exit()