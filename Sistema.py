import os, sqlite3
from datetime import date
import cadastros, listaProdutos

# Criando Banco de Dados

def criaBanco():
    if os.path.isfile('OSclientes.db'):
        db = sqlite3.connect('OSclientes.db')
        print('O Banco de Dados Já Existe.. Conectando')
        add_clientes()

    else:
        print('Inicializando novo Banco de Dados.')
        # Cria o arquivo connection
        db = sqlite3.connect('OSclientes.db')
        # Cria o cursor
        cursor = db.cursor()
        # Cria a tabela para a classe my_manager, e indica as três variáveis de dentro dela.
        cursor.execute('''CREATE TABLE ordens
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            nome TEXT,
            ordem TEXT,
            valor REAL,
            entrada REAL)''')
        print('Novo caderno criado com Sucesso..')
        add_clientes()

def add_clientes():
    print("-=-= Cadastrando Nova Ordem de Serviço -=-=")
    confirma = True
    while confirma:
        dt = date.today()
        data = dt.strftime("%d/%m/%Y")
        nome = input("Nome: ").title().strip()
        ordem = input("OS Nº: ").strip()
        # Aqui vai a função (add_produtos)
        #valor = input("Valor TOTAL R$: ").replace(",",".")
        #entrada = input("Valor Entrada R$: ").replace(",", ".")

        if nome:
            
            try: 
                #valor = float(valor)
                #entrada = float(entrada)

                db = sqlite3.connect('OSclientes.db')
                cursor = db.cursor()
                cursor.execute('''INSERT INTO ordens\
                                (data,
                                nome,
                                ordem,
                                valor,
                                entrada)VALUES(?,?,?,?,?)''',\
                                (data, nome, ordem, 0.0, 0.0))
                db.commit()

                cad_produtos = input(f"Deseja cadastrar os produtos da OS {ordem}? S ou N: ").upper()
                if cad_produtos in "S":
                    listaProdutos.add_produtos(ordem)
                    continua = input("Deseja cadastrar mais uma OS? S ou N: ")
                    if continua in "sS":
                        os.system("clear")
                        add_clientes()
                    else:
                        print("Voltando ao Menu Principal!\n\n\n\n\n")
                        confirma = False
                        main()
                        break
                else:
                   print("Você poderá cadastrar depois apenas informando a OS.")

                
                    

            except:
                print("Valor Inválido, favor Repetir a Operação.")
        else:
            print("ERRO! Precisa preencher todas as casas.")

def visualiza_cliente():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    print("-=-= Visualizando todas as Notas de um Cliente -=-=")
    opcao = input("Filtrar por:\n1.Nome\n2.Nº OS\n3. Voltar ao Menu Principal.\n")
    if opcao == "1":
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        db = sqlite3.connect('OSclientes.db')
        cursor = db.cursor()
        cursor.execute('SELECT data, nome, ordem, valor, entrada FROM ordens')
        caderno = cursor.fetchall()

        print('---------- Buscando Notas por Nome ----------')
        nome = input("Digite o Nome: ").title().strip()
        os.system("clear")

        conta = 0
        total = 0
        entrada = 0
        falta = 0
        for indice, dado in enumerate(caderno):
            if dado[1] in nome:
                print(f"Data: {dado[0]} | Nome: {dado[1]:<50} | OS:{dado[2]:<5} | Valor R$: {dado[3]:.2f} | Entrada R$: {dado[4]:.2f}")
                total += dado[3]
                entrada += dado[4]
                conta += 1
        
        if conta == 0:
            os.system("clear")
            print(f"Não foram encontradas nenhuma Nota em nome de {nome}.\n\n\n\n")
            visualiza_cliente()
        else:
            falta = total - entrada
            print("\n\n\n\n\n\n\n\n")
            print(f"Foram encontrados {conta} registros em nome de {nome}.")
            print(f"--------------------------------------------------------")
            print(f"Valor TOTAL R$:             {total:.2f}.")
            print(f"Valor PAGO Antecipado R$:   {entrada:.2f}.")
            print("---------------------------------------------------------")
            print(f"Falta PAGAR R$              {falta:.2f}.\n\n\n\n")
            visualiza_cliente()

    elif opcao == "2":
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        db = sqlite3.connect('OSclientes.db')
        cursor = db.cursor()
        cursor.execute('SELECT data, nome, ordem, valor, entrada FROM ordens')
        caderno = cursor.fetchall()

        print('---------- Buscando Notas pela OS ----------')
        numero = input("Digite o Nº da OS: ").strip()
        os.system("clear")
        if numero.isdigit():
            try:
                conta = 0
                total = 0
                entrada = 0
                falta = 0
                for indice, dado in enumerate(caderno):
                    if numero == dado[2]:
                        print(f"Data: {dado[0]} | Nome: {dado[1]:<50} | OS:{dado[2]:<5} | Valor R$: {dado[3]:.2f} | Entrada R$: {dado[4]:.2f}")
                        entrada += dado[4]
                        total += dado[3]
                        conta += 1
                            
                if conta == 0:
                    print(f"Não foi encontrado nenhum registro pelo Cadastro Nº{numero}.\n\n\n\n")
                    visualiza_cliente()
                else:
                    falta = total - entrada
                    print("\n")
                    print(f"Foram encontrados {conta} registros associados ao Cadastro Nº {numero}.")
                    print(f"--------------------------------------------------------")
                    print(f"Valor TOTAL R$:             {total:.2f}.")
                    print(f"Valor PAGO Antecipado R$:   {entrada:.2f}.")
                    print("---------------------------------------------------------")
                    print(f"Falta PAGAR R$              {falta:.2f}.\n")

                    listaProdutos.listar_produtos(numero)
            except:
                print("Cadastro Inválido! Tente Novamente.\n\n\n\n")
        else:
            print("Cadastro Inválido! Tente Novamente.\n\n\n\n")
            visualiza_cliente()
    elif opcao == "3":
        os.system("clear")
        print("Voltando ao Menu Principal.\n\n\n\n\n\n\n\n\n\n")
        main()
    else:
        os.system("clear")
        print("Opção Inválida\n\n\n\n")
        visualiza_cliente()

def visualiza_todos():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    db = sqlite3.connect('OSclientes.db')
    cursor = db.cursor()
    cursor.execute('SELECT id, data, nome, ordem, valor, entrada FROM ordens')
    caderno = cursor.fetchall()

    print('--------------------------------------------------- Visualizando Todas as Notas Pendentes ---------------------------------------------------')

    conta = 0
    total = 0
    entrada = 0
    for indice, dado in enumerate(caderno):
        print(f"ID: {dado[0]:<4} | Data: {dado[1]} | Nome: {dado[2]:<50} | OS:{dado[3]:<5} | Valor R$: {dado[4]:>.2f} | Entrada R$: {dado[5]:>.2f}")
        total += dado[4]
        entrada += dado[5]
        conta += 1
        
    if conta == 0:
        os.system("clear")
        print(f"Não foi encontrada nenhuma Nota Cadastrada.\n\n\n\n")
    else:
        print("-"*140)
        print(f"Foram encontrados {conta} Notas Pendentes.")
        print("-"*140)
        print(f"Total OS em aberto       -------------------------------------------------   : R${total:.2f}.")
        print(f"Total OS PAGO Antecipado -------------------------------------------------   : R${entrada:.2f}.")
        print(f"Total Pendente           -------------------------------------------------   : R${total - entrada:.2f}.\n")

def deletar_notas():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    os.system("clear")
    visualiza_todos()

    db = sqlite3.connect('OSclientes.db')
    cursor = db.cursor()


    OrdemS = input('DELETAR OS - Digite Nº da OS: ')
    sn = input(f"Você deseja mesmo excluir a OS {OrdemS}? S ou N: ").upper().strip()
    if sn in "S":
        if OrdemS != '':
            try:
                cursor.execute(f'''DELETE FROM ordens WHERE ordem="{OrdemS}"''')
                db.commit()
            except:
                print("ERRO!")
        else:
            print("ERRO! Digite o número da OS.")
    else:
        print("Voltando ao Menu Principal.")
        main()

def atualiza():
    print("Atualizando Dados de uma Entrada.")
    visualiza_todos()
    ide = input("Digite a ID: ")

    db = sqlite3.connect('OSclientes.db')
    cursor = db.cursor()
    cursor.execute('SELECT data, nome, ordem, valor, entrada FROM ordens')
    caderno = cursor.fetchall()

    if ide.isnumeric():
        print("Qual campo deseja atualizar?")
        print("1. Nome\n2. Valor\n3. Valor de Entrada")
        campo = input("Opção: 1-2-3: ")
        if campo != False or campo.isnumeric():
            if int(campo) == 1:
                nome = input("Digite o NOVO Nome: ").title()
                cursor.execute(f"""
                                    UPDATE ordens SET nome = '{nome}' WHERE id= '{ide}'
                                    """)
                db.commit()
                os.system("clear")
                visualiza_todos()

            elif int(campo) == 2:
                valor = input("Digite o NOVO Valor R$: ")
                if valor:
                    cursor.execute(f"""
                                    UPDATE ordens SET valor = '{float(valor)}' WHERE id= '{ide}'
                                    """)
                    db.commit()
                    os.system("clear")
                    visualiza_todos()
                else:
                    print("Não pode ser valor Vazio. Repita a operação.")
                    atualiza()
            elif int(campo) == 3:
                entrada = input("Digite o NOVO Valor R$: ")
                if entrada:
                    cursor.execute(f"""
                                        UPDATE ordens SET entrada = '{float(entrada)}' WHERE id= '{ide}'
                                        """)
                    db.commit()
                    os.system("clear")
                    visualiza_todos()
                else:
                    print("Não pode ser valor Vazio. Repita a operação.")
            else:
                print("Opção Inválida!")
                atualiza()
        else:
            print("ERRO! Argumento inválido! Não pode ser Vazio.")
    else:
        print("ERRO! Número inválido!")

def menu_add():
    visualiza_todos()
    print("1. Visualizar Produtos. | 2. Adicionar Produtos. | 3. Corrigir Produto. | 4. Delete Produto. | 5 - Salvar Pedido em TXT | 0 - Voltar ao Menu Principal.")
    op = input("Opção: 1-2-3-4-5-0: ")
    if op.isnumeric():
        os.system("clear")
        if int(op) == 0:
            main()
        elif int(op) == 1:
            ordem = input("OS Nº: ")
            listaProdutos.listar_produtos(ordem)
        elif int(op) == 2:
            ordem = input("OS Nº: ")
            os.system("clear")
            visualiza_todos()
            listaProdutos.add_produtos(ordem)     
        elif int(op) == 3:
            ordem = input("OS Nº ")
            os.system("clear")
            listaProdutos.atualiza_produto(ordem)
        elif int(op) == 4:
            ordem = input("OS Nº ")
            os.system("clear")
            visualiza_todos()
            listaProdutos.del_produto(ordem)
        elif int(op) == 5:
            ordem = input("OS Nº ")
            os.system("clear")
            listaProdutos.arquivo_txt(ordem)
        else:
            os.system("clear")
            print("Opção inválida!")                      
    else:
        print("Dígito Inválido")
    
def main():
    opc = 0
    while True:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- AM Sublimação - Gerenciamento de ORDENS DE SERVIÇO v1.0 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        print("1. Cadastrar Nova OS | 2. Ver Cliente | 3. Ver Tudo | 4. DEL OS | 5. Atualizar OS | 6. Ver/Add Produtos OS | 0. Sair")
        opc = input("Opção: 1-2-3-4-5-6-0: ")
        os.system("clear")
        if opc.isdigit():
            if int(opc) == 0:
                print("Deseja realmente sair? ")
                sn = input("S ou N: ").upper().strip()
                if sn in "S":
                    break
                else:
                    continue
            elif int(opc) == 1:
                criaBanco()
            elif int(opc) == 2:
                visualiza_cliente()
            elif int(opc) == 3:
                visualiza_todos()
            elif int(opc) == 4:
                deletar_notas()
            elif int(opc) == 5:
                atualiza()
            elif int(opc) == 6:
                menu_add()
            else:
                print("Opção Inválida!\n\n\n\n\n")
        else:
            print("Dígito Inválido!\n\n\n\n\n")

if __name__ == "__main__":
    main()

    """
    Ideias para implementar
    1. Inserir a coluna status na tabela pra indicar se pedido foi entregue. (será posto na função)
    2. Inserir no programa a funcionalidade de quitação parcial da OS e sua baixa automática.
            - Ela deve calcular o total menos a entrada - o pagamento parcial.
    
    3. Inserir a função de desfazer... Caso exclua alguma OS sem querer.
            - E também inserir uma pergunta de confirmação se quer excluir OS.
    
    4. Adicionar função de quando der baixa em uma OS, o sistema contabiliza esta quitação
    num outro banco de dados de notas baixadas e pagas... Pra vermos o total que foi pago em um mês.
    """

    """
    Aqui é o programa propriamente dito... Ele possui dois bancos de dados.
    1 para os logins e senhas.
    1 para as Ordens de Serviços.


    Foi escrito na Linguagem Python v3.7.5

    Mas eu não terminei, vou continuar fazendo melhorias.

    É isso! =D~ 
    """