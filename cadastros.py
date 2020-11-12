import os, sqlite3
from datetime import date
import Sistema
import getpass

def senhasdb(login, senha):
    
    if os.path.isfile('pass.db'):
        dt = date.today()
        data = dt.strftime("%d/%m/%Y")

        db = sqlite3.connect('pass.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO users\
                                (data,
                                user,
                                senha)VALUES(?,?,?)''',\
                                (data, login, senha))
        db.commit()
        main()

    else:
        
        # Cria o arquivo connection
        db = sqlite3.connect('pass.db')
        # Cria o cursor
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE users
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            user TEXT,
            senha TEXT)''')
        db.close()

        dt = date.today()
        data = dt.strftime("%d/%m/%Y")
        db = sqlite3.connect('pass.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO users\
                                (data,
                                user,
                                senha)VALUES(?,?,?)''',\
                                (data, login, senha))
        db.commit()
        main()
        
def cadastro():
    while True:
        print("-=-=-=-=-=-=-=-= CADASTRO - AM SUBLIMAÇÃO -=-=-=-=-=-=-=-=")
        login = input("Usuário  : ").strip()
        if login:
            log_conf = input("Confirma USER:")
            if log_conf == login:
                print("Confirmado.")
                senha = input("Senha    : ").strip()
                if senha:
                    sen_conf = input("Confirma SENHA: ")
                    if sen_conf == senha:
                        print("Confirmado: ")
                        senhasdb(login, senha)
                    else:
                        print("Não confirmado.")
                        break
                else:
                    print("ERRO! Campo vazio não permitido.")
            else:
                print("Não confirmado")
                break
        else:
            print("ERRO! Campo vazio não permitido.")

        

def entrar():
    print("-=-=-=-=-=-=-=-=-=-= Validando USUARIO - AM SUBLIMAÇÃO -=-=-=-=-=-=-=-=-=-=-=-=-=")
    db = sqlite3.connect('pass.db')
    cursor = db.cursor()
    cursor.execute('SELECT data, user, senha FROM users')
    caderno = cursor.fetchall()

    print('---------- DIGITE SEU LOGIN E SENHA ----------')
    login = input("LOGIN: ").strip()
    senha = getpass.getpass("SENHA: ")
    os.system("clear")

    conta = 0
    for indice, dado in enumerate(caderno):
        if login == dado[1] and senha == dado[2]:
            conta += 1
        
    if conta == 0:
        os.system("clear")
        print(f"LOGIN ou SENHA Incorreto!\n\n\n\n")
        main()
    else:
        Sistema.main()

def main():
    opc = True
    while opc != 0:
        print("-=-=-=-=-=-=-=-=-=-= LOGIN - AM SUBLIMAÇÃO -=-=-=-=-=-=-=-=-=-=-=\n\n\n\n")
        print("1. Cadastro | 2. Entrar no sistema | 0. Sair do Sistema")
        opc = input("Opção 1-2-0: ")
        os.system("clear")
        if opc.isdigit():
            if int(opc) == 0:
                print("Saindo do sistema...")
                opc = False
                break
            elif int(opc) == 1:
                cadastro()
            elif int(opc) == 2:
                entrar()
            else:
                print("ERRO! Opção Inválida!")
        else:
            print("ERRO! Dígito Inválido!")
    
if __name__ == "__main__":
    main()



    """
    Esse arquivo aqui trata da validação de entrada so usuario: Login e Senha
    """