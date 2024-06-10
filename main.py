import textwrap
import re

def menu_principal():
    menu = """\n
    ================ MENU ================
    [nc]\tNova conta
    [lc]\tListar contas
    [ec]\tEntrar na conta
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def menu_conta():
    menu = """\n
    ============== CONTA ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair da conta
    => """
    return input(textwrap.dedent(menu))


def depositar(conta):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        conta['saldo'] += valor
        conta['extrato'] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return conta


def sacar(conta, limite, limite_saques):
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > conta['saldo']
    excedeu_limite = valor > limite
    excedeu_saques = conta['numero_saques'] >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta['numero_saques'] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return conta


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")


def criar_conta(agencia, numero_conta, contas):
    cpf = input("Informe o CPF (somente número): ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    if filtrar_conta_por_cpf(cpf, contas):
        print("\n@@@ Já existe uma conta com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    if not validar_nome(nome):
        print("\n@@@ Nome inválido! Use apenas letras. @@@")
        return

    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    if not validar_data_nascimento(data_nascimento):
        print("\n@@@ Data de nascimento inválida! @@@")
        return

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    senha = input("Crie uma senha para a conta: ")

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        },
        "senha": senha,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0,
    }

    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def filtrar_conta(cpf, senha, contas):
    contas_filtradas = [conta for conta in contas if conta["usuario"]["cpf"] == cpf and conta["senha"] == senha]
    return contas_filtradas[0] if contas_filtradas else None


def filtrar_conta_por_cpf(cpf, contas):
    contas_filtradas = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
    return contas_filtradas[0] if contas_filtradas else None


def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11 and cpf != "00000000000"


def validar_nome(nome):
    return all(x.isalpha() or x.isspace() for x in nome)


def validar_data_nascimento(data):
    return bool(re.match(r'\d{2}-\d{2}-\d{4}', data))


def entrar_conta(contas):
    cpf = input("Informe o CPF da conta: ")
    senha = input("Informe a senha da conta: ")
    conta = filtrar_conta(cpf, senha, contas)
    if conta:
        print("\n=== Login realizado com sucesso! ===")
        return conta
    else:
        print("\n@@@ Conta não encontrada ou senha incorreta! @@@")
        return None


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    limite = 500
    contas = []
    conta_logada = None

    while True:
        if conta_logada:
            opcao = menu_conta()

            if opcao == "d":
                conta_logada = depositar(conta_logada)

            elif opcao == "s":
                conta_logada = sacar(conta_logada, limite, LIMITE_SAQUES)

            elif opcao == "e":
                exibir_extrato(conta_logada)

            elif opcao == "q":
                conta_logada = None
                print("=== Você saiu da conta. ===")

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

        else:
            opcao = menu_principal()

            if opcao == "nc":
                numero_conta = len(contas) + 1
                criar_conta(AGENCIA, numero_conta, contas)

            elif opcao == "lc":
                listar_contas(contas)

            elif opcao == "ec":
                conta_logada = entrar_conta(contas)

            elif opcao == "q":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
