import sqlite3, os
import Sistema

"""
Vai conter a funcionalidade de inserir produtos em uma OS.

Vai contar com os mesmos campos encontrados na OS tradicional.

0. OS - TEXT
1. item INTEGER
2. valor unitario - REAL
3. descrição TEXTO
4. Quantidade - INTEGER
5. total - REAL
6. Status PAGO TEXT - PARCIAL - INTEGRAL
7. Status ENTREGUE TEXT - S - N

"""
def arquivo_txt(ordem):
    db = sqlite3.connect('OSclientes.db')
    cursor = db.cursor()
    cursor.execute('SELECT data, nome, ordem FROM ordens')
    caderno = cursor.fetchall()

    print(f'--------------------------- Criando Arquivo TXT da OS: {ordem} -----------------------------')
   
    for indice, dado in enumerate(caderno):
        if ordem == dado[2]:
            with open(f"OS_{ordem}.txt", "a+") as arquivo:
                #print(f"Data: {dado[0]} | Nome: {dado[1]:<50} | OS:{dado[2]:<5}")
                arquivo.write(f"-------------------------------- AM SUBLIMAÇÃO - PEDIDO ----------------------------------\n")
                arquivo.write(f'Data: {dado[0]} | Nome: {dado[1]:<50} | OS:{dado[2]:<5}\n')
                arquivo.write("------------------------------------------------------------------------------------------\n\n\n")
                arquivo.write("Item Nº   Preço UNI   Descrição do Produto                                 Quantidade   Sub_total(R$)\n")
         
    db = sqlite3.connect('produtos.db')
    cursor = db.cursor()
    cursor.execute('SELECT id, os, item, valor_UNI, descricao, qtde, total_parcial FROM produtos')
    caderno = cursor.fetchall()

    conta = 0
    total = 0
    itens_total = 0
    for indice, dado in enumerate(caderno):
        if ordem == dado[1]:
            with open(f"OS_{ordem}.txt", "a+") as arquivo1:
                arquivo1.write("______________________________________________________________________________________________\n")
                #print(f"OS Nº:{dado[1]} |Item:{conta + 1} |Valor-UNI R$: {dado[3]:.2f} |Descr: {dado[4]:50} |Qtde:{dado[5]:4} |Sub-Total R$:{dado[6]:.2f}")
                arquivo1.write(f"Item:{conta + 1} |UNI R$:{dado[3]:.2f}|Produto:{dado[4]:48}|Qtde:{dado[5]:2}|R$:{dado[6]:.2f}\n")
                total += dado[6]
                itens_total += dado[5]
                conta += 1
        
    if conta == 0:
        os.system("clear")
        print(f"Itens não Encontrados.\n\n\n\n")
    else:
        with open(f"OS_{ordem}.txt", "a+") as arquivo1:
            arquivo1.write("--------------------------------------------------------------------------------------\n")
            arquivo1.write(f"TOTAL(R$): ------------------------------------------------------------  R$: {total:.2f}.\n")
            arquivo1.write(f"TOTAL(UNI): ------------------------------------------------------------ UNI: {itens_total} itens.\n")
            arquivo1.write("--------------------------------------------------------------------------------------\n")
    

def atualiza_produto(ordem):
    listar_produtos(ordem)

    ide = input("Digite o ID: ")

    db = sqlite3.connect('produtos.db')
    cursor = db.cursor()
    cursor.execute('SELECT id, os, item, valor_UNI, descricao, qtde, total_parcial FROM produtos')
    caderno = cursor.fetchall()

    if ide.isnumeric():
        print("Qual campo deseja atualizar?")
        print("1. Valor Unitário (R$)\n2. Descrição\n3. Quantidade")
        campo = input("Opção: 1-2-3: ")
        if campo != False or campo.isnumeric():
            if int(campo) == 1:
                valor = input("Digite o Valor R$: ")
                if valor:
                    try:
                        # Pegar quantidade
                        quantidade = 0
                        for indice, itens in enumerate(caderno):
                            if itens[0] == int(ide):
                                quantidade = itens[-2]
                                

                        cursor.execute(f"""
                                            UPDATE produtos SET valor_UNI = '{float(valor)}' WHERE id= '{ide}'
                                            """)
                        db.commit()

                        # Update o sub-total com o resultado de qtde * novo Valor_UNI
                        novo_sub = quantidade * float(valor)
                        cursor.execute(f"""
                                            UPDATE produtos SET total_parcial = '{float(novo_sub)}' WHERE id= '{ide}'
                                            """)
                        db.commit()

                        os.system("clear")
                        listar_produtos(ordem)
                    except:
                        print("Valor inválido. Tente Novamente.")
                        atualiza_produto(ordem)

                else:
                    print("Não pode ser Valor vazio. Repita a operação.")
                    atualiza_produto(ordem)

            elif int(campo) == 2:
                descricao = input("Digite a Descrição: ")
                if descricao:
                    cursor.execute(f"""
                                        UPDATE produtos SET descricao = '{descricao}' WHERE id= '{ide}'
                                        """)
                    db.commit()
                    os.system("clear")
                    listar_produtos(ordem)
                else:
                    print("Não pode ser valor Vazio. Repita a operação.")

            elif int(campo) == 3:
                quantidade = input("Digite a Quantidade: ")
                if quantidade:
                    if quantidade.isnumeric():
                        # Pegar o valor
                        valor_subtotal = 0
                        for indice, itens in enumerate(caderno):
                            if itens[0] == int(ide):
                                valor_subtotal = itens[3]                        

                        cursor.execute(f"""
                                            UPDATE produtos SET qtde = '{int(quantidade)}' WHERE id= '{ide}'
                                            """)
                        db.commit()

                        # UPDATE sub-total com o resultado entre valor * qtde digitada
                        novo_sub = valor_subtotal * int(quantidade)
                        cursor.execute(f"""
                                            UPDATE produtos SET total_parcial = '{float(novo_sub)}' WHERE id= '{ide}'
                                            """)
                        db.commit()

                        os.system("clear")
                        listar_produtos(ordem)
                    else:
                        print("Valor inválido. Repita a operação.")
                        atualiza_produto(ordem)
                else:
                    print("Não pode ser valor Vazio. Repita a operação.")
            else:
                print("Opção Inválida!")
        else:
            print("ERRO! Argumento inválido! Não pode ser Vazio.")
    else:
        print("ERRO! Número inválido!")
        atualiza_produto(ordem)

def del_produto(ordem):
    db = sqlite3.connect('produtos.db')
    cursor = db.cursor()

    sn = input(f"Você deseja mesmo excluir um item da OS Nº{ordem}? S ou N: ").upper().strip()
    if sn in "S":
        if ordem != '':
            listar_produtos(ordem)
            ide = input("Digite o ID: ")
            try:
                cursor.execute(f'''DELETE FROM produtos WHERE id="{int(ide)}"''')
                db.commit()
            except:
                print("ERRO!")
                Sistema.visualiza_todos()
        else:
            print("ERRO! Digite o número da OS.")
    else:
        print("Voltando ao Menu Principal.")
        Sistema.main()

def listar_produtos(ordem):
    db = sqlite3.connect('OSclientes.db')
    cursor = db.cursor()
    cursor.execute('SELECT data, nome, ordem FROM ordens')
    caderno = cursor.fetchall()

    print(f'--------------------------- Listando Produtos da OS: {ordem} -----------------------------')
   
    for indice, dado in enumerate(caderno):
        if ordem == dado[2]:
            print(f"Data: {dado[0]} | Nome: {dado[1]:<50} | OS:{dado[2]:<5}")
       
    print(f"--------------------------------------------------------------------------------------")
      
    db = sqlite3.connect('produtos.db')
    cursor = db.cursor()
    cursor.execute('SELECT id, os, item, valor_UNI, descricao, qtde, total_parcial FROM produtos')
    caderno = cursor.fetchall()

    conta = 0
    total = 0
    itens_total = 0
    for indice, dado in enumerate(caderno):
        if ordem == dado[1]:
            print("_________________________________________________________________________________________________________________________________________________")
            print(f"ID:{dado[0]:<3} |OS Nº:{dado[1]} |Item:{conta + 1} |Valor-UNI R$: {dado[3]:.2f} |Descr: {dado[4]:50} |Qtde:{dado[5]:4} |Sub-Total R$:{dado[6]:.2f}")
            total += dado[6]
            itens_total += dado[5]
            conta += 1
        
    if conta == 0:
        os.system("clear")
        print(f"Itens não Encontrados.\n\n\n\n")
    else:

        print("---------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"TOTAL(R$): -------------------------------------------------------------------------------------------------------------------  R$: {total:.2f}.")
        print(f"TOTAL(UNI): ------------------------------------------------------------------------------------------------------------------- UNI: {itens_total} itens.")
        print("---------------------------------------------------------------------------------------------------------------------------------------------")
    
def add_produtos(ordem):
    print("-=-=-=--=-=-=-= Adicionando Produtos -=-=-=-=-=-=-=-=-=")
    itens = []
    item = 1
    total_parcial = 0
    #total = 0
    while True:
        valor_UNI = input("Valor Uni(R$): ")
        descricao = input("Produto Descrição: ")
        qtde = input("Quantidade: ")
        if valor_UNI and qtde.isnumeric():
            valor_UNI = float(valor_UNI)
            qtde = int(qtde)
            total_parcial = qtde * valor_UNI

            try:
                itens.append(ordem)
                itens.append(item)
                itens.append(float(valor_UNI))
                itens.append(descricao)
                itens.append(int(qtde))
                itens.append(total_parcial)

                if os.path.isfile('produtos.db'):
                    db = sqlite3.connect('produtos.db')

                    cursor = db.cursor()
                    cursor.execute('''INSERT INTO produtos\
                                    (os,
                                    item,
                                    valor_UNI,
                                    descricao,
                                    qtde,
                                    total_parcial)VALUES(?,?,?,?,?,?)''',\
                                    (itens[0], itens[1], itens[2], itens[3], itens[4], itens[5]))
                    #total += itens[5]
                    db.commit()
                    sn = input("Deseja cadastrar mais um produto? S ou N: ").upper().strip()
                    if sn in "S":
                        item += 1
                        itens.clear()
                        total_parcial = 0
                        continue
                    else:
                        # Varrendo a OS para saber seu total
                        subtotais = 0
                        db = sqlite3.connect('produtos.db')
                        cursor = db.cursor()
                        cursor.execute('SELECT os, item, valor_UNI, descricao, qtde, total_parcial FROM produtos')
                        caderno = cursor.fetchall()

                        for indice, valores in enumerate(caderno):
                            if ordem == valores[0]:
                                subtotais += valores[-1]
                        
                        #print(subtotais)
                        # Atualizando Tabela de ordens pra atualizar o valor total.
                        db = sqlite3.connect('OSclientes.db')
                        cursor = db.cursor()
                        cursor.execute('SELECT data, nome, ordem, valor, entrada FROM ordens')
                        #caderno = cursor.fetchall()

                        cursor.execute(f"""
                                    UPDATE ordens SET valor = '{subtotais}' WHERE ordem= '{ordem}'
                                    """)
                        db.commit()
                        
                        print("Voltando ao Menu Principal.")
                        Sistema.main()
                        break

                else:
                    print('Inicializando novo Banco de Dados.')
                    # Cria o arquivo connection
                    db = sqlite3.connect('produtos.db')
                    # Cria o cursor
                    cursor = db.cursor()
                    # Cria a tabela para a classe my_manager, e indica as três variáveis de dentro dela.
                    cursor.execute('''CREATE TABLE produtos
                                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    os TEXT,
                                    item INTEGER,
                                    valor_UNI REAL,
                                    descricao TEXT,
                                    qtde INTEGER,
                                    total_parcial REAL)''')
                    print('Banco de Dados criado com Sucesso..')

                    db = sqlite3.connect('produtos.db')
                    cursor = db.cursor()
                    cursor.execute('''INSERT INTO produtos\
                                    (os,
                                    item,
                                    valor_UNI,
                                    descricao,
                                    qtde,
                                    total_parcial)VALUES(?,?,?,?,?,?)''',\
                                    (itens[0], itens[1], itens[2], itens[3], itens[4], itens[5]))
                    db.commit()
                    total += itens[5]
                    sn = input("Deseja cadastrar mais um produto? S ou N: ").upper().strip()
                    if sn in "S":
                        item += 1
                        itens.clear()
                        total_parcial = 0
                        total = 0
                        continue
                    else:
                        db = sqlite3.connect('OSclientes.db')
                        cursor = db.cursor()
                        cursor.execute('SELECT data, nome, ordem, valor, entrada FROM ordens')
                        #caderno = cursor.fetchall()

                        cursor.execute(f"""
                                    UPDATE ordens SET valor = '{total}' WHERE ordem= '{ordem}'
                                    """)
                        db.commit()
                        
                        print("Voltando ao Menu Principal.")
                        Sistema.main()
                        break
            except:
                print("ERRO! Dados Inválidos!")
           
        else:
            print("É necessário preencher todas as casas.")


