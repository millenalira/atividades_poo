

def formatadados(dados_recebidos,banco):
    """
    Responsavel por transformar(reparticionar) os dados

    Recebe os dados vindo do usuario e formata esses dados em uma lista de informações

    Parameters
    ----------
    dados_recebidos : str
        The sound the animal makes (default is None)
    banco : 
        ...

    """

    dados = list(dados_recebidos.split(';'))
    #o que vai fazer,nome,email,datanascimento,senha    
    #dados[0],dados[1],dados[2],dados[3],dados[4]
    #cadastro;millena;millena@gmail.com;20/02/2002;123456
    


    def verificaremail (dadocliente):
        """
        Responsavel por verifica se o email e valido ou não

        Ao receber os dados vindo do usuario, ele verifica se o email informado esta no banco para ser validado

        Parameters
        ----------
        dadocliente : str
            ...

        """
        
        sql = f"select * from usuario where email='{dadocliente}'"
        resultado = banco.qselect(sql)
        
        if resultado == []:
            return False
        else:
            return True

    #pra fazer cadastro do usuario
    if dados[0] == "cadastro": 
        nome = dados[1]
        email = dados[2]
        data = dados[3]
        senha = dados[4]
    
        existe = verificaremail(email) #chama a função para verificar se o email 
        #que vai ser cadastro já existe ou não no banco, pois não pode ter usuário com o mesmo email.

        if existe == False: 
            sql = f"insert into usuario(nome,email,data_nas,senha) values('{nome}','{email}','{data}','{senha}')"
            banco.qinsert(sql)
            sql = f"select * from usuario where email='{email}'"
            resultado = banco.qselect(sql)
            mensagem = f"Cadastro com sucesso!;{resultado[0][0]}"
        else:
            mensagem = "Já existe usuário com esse email!"

    #pra fazer login do usuario
    elif dados[0] == "login":
        email = dados[1]
        senha = dados[2]
        # ["login","email","senha"]
        # tem aquele email no banco?
        # verificar se a senha 
        # ['id','nome','email','data_nas','senha']  Ver como vai vir do banco.
        
        existe = verificaremail(email) #chama a função para verificar se o email 
        #que vai ser logado já existe ou não no banco
        
        #se não existir, retorna que não possui cadastro 
        if existe == False:
            mensagem = "Não existe email cadastrado!"
        else:   # tem usuário com aquele email!
            sql = f"select * from usuario where email='{email}'"
            resultado = banco.qselect(sql)
            #print(resultado) 

            #Se o email estiver no banco, faço a verificação da senha
            #para saber se ela corresponde aquele email ou não 
            if senha == resultado[0][4]:
                id_usuario = resultado[0][0]
                sql = f"select * from calendario where id_usuario = {id_usuario}"
                resultado = banco.qselect(sql)
                #o que envio para o cliente depois de ter realizado o login
                #resultado[0][0] é o id do calendario
                #resultado[0][1] é o ciclo
                #resultado[0][2] é o regular
                mensagem = f"Login realizado com sucesso!;{id_usuario};{resultado[0][0]};{resultado[0][1]};{resultado[0][2]}"
            else:
                mensagem = "Senha incorreta!"

    #Cria uma notificação para cada usuario
    # ["crianot","id","mensagem"]
    elif dados[0] == 'crianot':   #envia ao servidor para criar uma notificaçao para cada usuário
        idusuario = int(dados[1])
        msg = dados[2]

        sql = f"insert into notificacoes(id_usuario,mensagem,visto) values({idusuario},'{msg}',False)"    
        mensagem = "Notificação enviada com sucesso!"
        resultado = banco.qinsert(sql)


    #envia para criar o calendario
    # ["criacalend","regular","ciclo","id_usuario"]
    elif dados[0] == 'criacalend':  #envia ao servidor para criar um calendario para cada usuário
        idusuario = int(dados[3])
        regular = dados[1]
        ciclo = dados[2]

        sql = f"insert into calendario(duracao_ciclo,regular,id_usuario) values({ciclo},{regular},{idusuario})"
        banco.qinsert(sql)
        
        #para pegar o id do calendario
        #e mando pro main para guardar 
        sql = f"select * from calendario where id_usuario = {idusuario}"
        resultado = banco.qselect(sql)
        mensagem = f"Foi criado um calendário!;{resultado[0][0]};{ciclo};{regular}"

    #envia para criar um registro de cada usuario 
    elif dados[0] == 'criaregis':
        dataselecionada = dados[1]
        fluxo = dados[2]
        sintomas = dados[3]
        descricao = dados[4]
        datafinal = dados[5]
        idcalend = dados[6]
        diaprevi = dados[7]

        sql = f"insert into registro (id_calendario,sintomas,dataini,datafinal,fluxo,descricao,dataprevi) values ('{idcalend}','{sintomas}','{dataselecionada}','{datafinal}','{fluxo}','{descricao}','{diaprevi}')"
        banco.qinsert(sql)

        mensagem = "Registro adicionado com sucesso!"

    #envia para o servidor criar notificação pra cada usuario 
    elif dados[0] == 'notifi':
        iduser = int(dados[1])

        #para mandar todas as notificações para o usuario
        sql = f"select mensagem from notificacoes where id_usuario = {iduser} order by id desc;"
        resultado = banco.qselect(sql)

        #vindo do banco
        mensagem = ''
        #formato no jeito para voltar para o usuario
        #pegando as outras mensagens e separando para não mandar
        #pro usuario tudo junto
        for i in resultado:
            mensagem = mensagem + ';' + i[0]


    #envia para criar o historico de sintomas de cada usuario 
    elif dados[0] == 'historico':
        idcalen = int(dados[1])

        sql = f"select sintomas,dataini,datafinal from registro where id_calendario = {idcalen} order by id desc;"
        resultado = banco.qselect(sql)
        mensagem = ''

        #para separar esses dados -, usei outro caractere
        for i in resultado:
            mensagem = mensagem + ';' + i[0] + '-' + i[1] + '-' + i[2]

    #Verifica se 
    elif dados[0] == 'verificaregis':
        idcal = int(dados[1])

        sql = f"select dataprevi from registro where id_calendario = {idcal} order by id desc;"
        resultado = banco.qselect(sql)

        if resultado == []:
            mensagem = "Não possui registro!"
        else:   #[(dataprevi)]
            mensagem = resultado[0][0]

    return mensagem
