import sqlite3
import time
from datetime import datetime


conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS contas_bancarias(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                titular TEXT NOT NULL,
                saldo REAL NOT NULL,
                cpf TEXT NOT NULL UNIQUE
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (conta_id) REFERENCES contas_bancarias(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS emprestimos(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (conta_id) REFERENCES contas_bancarias(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS pagamentos(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (conta_id) REFERENCES contas_bancarias(id)
                )''')

conexao.commit()



def inicio():
    while True:
        print("\nBem-vindo ao sistema bancário!")
        cpf = input("Digite seu CPF (apenas números): ")

        if len(cpf) != 11 or not cpf.isdigit():
            print("CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos.")
            continue

        print("Verificando CPF...")
        time.sleep(1)

        if verificar_cpf(cpf):
            print("CPF encontrado. Acesso concedido.")
            return cpf  # ✅ Retorna o CPF para uso no menu
        else:
            print("CPF não encontrado no banco de dados.")
            opcao = input("Deseja criar uma nova conta? (s/n): ").strip().lower()
            if opcao == 's':
                titular = input("Digite o nome do titular: ").strip()
                criar_conta(titular, 0.0, cpf)
                return cpf
            else:
                print("Encerrando...")
                break


def verificar_cpf(cpf):
    cursor.execute('SELECT cpf FROM contas_bancarias WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()
    return resultado is not None  


def verificar_saldo(cpf):
    cursor.execute('SELECT saldo FROM contas_bancarias WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return None


def _get_conta_id(cpf):
    
    cursor.execute('SELECT id FROM contas_bancarias WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def realizar_deposito(cpf, valor):
    if valor <= 0:
        print("O valor do depósito deve ser positivo.")
        return

    saldo_atual = verificar_saldo(cpf)
    if saldo_atual is not None:
        novo_saldo = saldo_atual + valor
        cursor.execute('UPDATE contas_bancarias SET saldo = ? WHERE cpf = ?', (novo_saldo, cpf))

        
        conta_id = _get_conta_id(cpf)
        cursor.execute(
            'INSERT INTO transacoes (conta_id, tipo, valor, data_hora) VALUES (?, ?, ?, ?)',
            (conta_id, 'deposito', valor, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )

        conexao.commit()
        print(f"Depósito de R${valor:.2f} realizado com sucesso. Novo saldo: R${novo_saldo:.2f}")
    else:
        print("CPF não encontrado. Depósito não realizado.")


def realizar_saque(cpf, valor):
    if valor <= 0:
        print("O valor do saque deve ser positivo.")
        return

    saldo_atual = verificar_saldo(cpf)
    if saldo_atual is not None:
        if valor <= saldo_atual:
            novo_saldo = saldo_atual - valor
            cursor.execute('UPDATE contas_bancarias SET saldo = ? WHERE cpf = ?', (novo_saldo, cpf))

            
            conta_id = _get_conta_id(cpf)
            cursor.execute(
                'INSERT INTO transacoes (conta_id, tipo, valor, data_hora) VALUES (?, ?, ?, ?)',
                (conta_id, 'saque', valor, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )

            conexao.commit()
            print(f"Saque de R${valor:.2f} realizado com sucesso. Novo saldo: R${novo_saldo:.2f}")
        else:
            print("Saldo insuficiente para realizar o saque.")
    else:
        print("CPF não encontrado. Saque não realizado.")


def ver_dados(cpf):
    cursor.execute('SELECT titular, saldo FROM contas_bancarias WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()
    if resultado:
        titular, saldo = resultado
        print(f"\nTitular: {titular}\nCPF: {cpf}\nSaldo: R${saldo:.2f}")
    else:
        print("CPF não encontrado.")


def criar_conta(titular, saldo, cpf):
    try:
        cursor.execute(
            'INSERT INTO contas_bancarias (titular, saldo, cpf) VALUES (?, ?, ?)',
            (titular, saldo, cpf)
        )
        conexao.commit()
        print("Conta criada com sucesso!")
    except sqlite3.IntegrityError:
        
        print("Erro: já existe uma conta com esse CPF.")


def excluir_conta(cpf):
    cursor.execute('DELETE FROM contas_bancarias WHERE cpf = ?', (cpf,))
    conexao.commit()
    print("Conta excluída com sucesso.")


def emprestimo(cpf, valor):
    if valor <= 0:
        print("O valor do empréstimo deve ser positivo.")
        return

    saldo_atual = verificar_saldo(cpf)
    if saldo_atual is not None:
        novo_saldo = saldo_atual + valor
        cursor.execute('UPDATE contas_bancarias SET saldo = ? WHERE cpf = ?', (novo_saldo, cpf))

        # ✅ CORRIGIDO: agora registra na tabela de empréstimos
        conta_id = _get_conta_id(cpf)
        cursor.execute(
            'INSERT INTO emprestimos (conta_id, valor, data_hora) VALUES (?, ?, ?)',
            (conta_id, valor, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )

        conexao.commit()
        print(f"Empréstimo de R${valor:.2f} concedido com sucesso. Novo saldo: R${novo_saldo:.2f}")
    else:
        print("CPF não encontrado. Empréstimo não concedido.")


def pagar_emprestimo(cpf, valor):
    if valor <= 0:
        print("O valor do pagamento deve ser positivo.")
        return

    saldo_atual = verificar_saldo(cpf)
    if saldo_atual is not None:
        if valor <= saldo_atual:
            novo_saldo = saldo_atual - valor
            cursor.execute('UPDATE contas_bancarias SET saldo = ? WHERE cpf = ?', (novo_saldo, cpf))

        
            conta_id = _get_conta_id(cpf)
            cursor.execute(
                'INSERT INTO pagamentos (conta_id, valor, data_hora) VALUES (?, ?, ?)',
                (conta_id, valor, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )

            conexao.commit()
            print(f"Pagamento de R${valor:.2f} realizado com sucesso. Novo saldo: R${novo_saldo:.2f}")
        else:
            print("Saldo insuficiente para realizar o pagamento.")
    else:
        print("CPF não encontrado. Pagamento não realizado.")


def ver_extrato(cpf):
    conta_id = _get_conta_id(cpf)
    if conta_id is None:
        print("CPF não encontrado.")
        return

    cursor.execute(
        'SELECT tipo, valor, data_hora FROM transacoes WHERE conta_id = ? ORDER BY data_hora DESC',
        (conta_id,)
    )
    transacoes = cursor.fetchall()

    if transacoes:
        print("\n--- Extrato de Transações ---")
        for tipo, valor, data_hora in transacoes:
            print(f"  [{data_hora}] {tipo.capitalize()}: R${valor:.2f}")
    else:
        print("Nenhuma transação encontrada.")


def menu(cpf):
    opcoes = {
        '1': 'Ver dados da conta',
        '2': 'Depositar',
        '3': 'Sacar',
        '4': 'Extrato',
        '5': 'Solicitar empréstimo',
        '6': 'Pagar empréstimo',
        '7': 'Excluir conta',
        '0': 'Sair',
    }

    while True:
        print("\n========== MENU ==========")
        for k, v in opcoes.items():
            print(f"  [{k}] {v}")
        print("===========================")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            ver_dados(cpf)

        elif escolha == '2':
            try:
                valor = float(input("Valor do depósito: R$"))
                realizar_deposito(cpf, valor)
            except ValueError:
                print("Valor inválido.")

        elif escolha == '3':
            try:
                valor = float(input("Valor do saque: R$"))
                realizar_saque(cpf, valor)
            except ValueError:
                print("Valor inválido.")

        elif escolha == '4':
            ver_extrato(cpf)

        elif escolha == '5':
            try:
                valor = float(input("Valor do empréstimo: R$"))
                emprestimo(cpf, valor)
            except ValueError:
                print("Valor inválido.")

        elif escolha == '6':
            try:
                valor = float(input("Valor do pagamento: R$"))
                pagar_emprestimo(cpf, valor)
            except ValueError:
                print("Valor inválido.")

        elif escolha == '7':
            confirmacao = input("Tem certeza que deseja excluir sua conta? (s/n): ").strip().lower()
            if confirmacao == 's':
                excluir_conta(cpf)
                print("Até logo!")
                break

        elif escolha == '0':
            print("Saindo... Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    cpf_logado = inicio()
    if cpf_logado:
        menu(cpf_logado)

    conexao.close()