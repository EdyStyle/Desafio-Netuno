import json
import hashlib
from datetime import datetime
import re
import getpass
import sys


def calcular_idade(data_nascimento):
    agora = datetime.now()
    idade = agora.year - data_nascimento.year - \
        ((agora.month, agora.day) < (data_nascimento.month, data_nascimento.day))
    return idade


def obter_data_nascimento():
    while True:
        try:
            data_nascimento_str = input(
                "Qual sua data de nascimento (DD/MM/AAAA): ")
            data_nascimento = datetime.strptime(
                data_nascimento_str, '%d/%m/%Y')
            idade = calcular_idade(data_nascimento)
            if idade < 18:
                print("Você ainda não está preparado para embarcar nessa aventura!")
                sys.exit()
            else:
                return data_nascimento
        except ValueError:
            print("Data de nascimento inválida. Digite no formato DD/MM/AAAA.")


def validar_email(email):
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao_email, email)


def cadastrar_usuario():
    print("\n==== Se Identifique: ====")

    nome_completo = input("\nNome completo: ")
    data_nascimento = obter_data_nascimento()

    if data_nascimento is None:
        return

    email = input("Digite seu Email: ")

    if not validar_email(email):
        print("Digite um email válido.")
        sys.exit()

    nome_usuario = input("Nome de usuário: ")

    senha = getpass.getpass("Digite sua senha (min 8 caracteres): ")
    confirmar_senha = getpass.getpass("Confirme sua senha: ")

    if senha == confirmar_senha:
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        usuario = {
            "nome_completo": nome_completo,
            "data_nascimento": data_nascimento.strftime('%d/%m/%Y'),
            "email": email,
            "senha_hash": senha_hash
        }

        with open(f"{nome_usuario}.json", "w") as file:
            json.dump(usuario, file)

        print("Cadastro realizado com sucesso!")
        login = input("\nDeseja realizar seu login agora? (S/N)")

        if login == "S" or login == "s":
            tela_login()
        else:
            sys.exit()
    else:
        print("As senhas não coincidem. Tente novamente.")
        sys.exit()


def tela_login():
    print("==== Tela de Login ====")
    nome_usuario = input("Nome de usuário: ")
    senha = getpass.getpass("Senha: ")

    try:
        with open(f"{nome_usuario}.json", "r") as file:
            usuario = json.load(file)
    except FileNotFoundError:
        print("Usuário não encontrado. Verifique o nome de usuário.")
        sys.exit()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if senha_hash == usuario['senha_hash']:
        print("Login bem-sucedido! Bem-vindo ao jogo.")
    else:
        print("Senha incorreta. Tente novamente.")
        sys.exit()


def tela_selecao_classe():
    print("\n===== Tela de Seleção de Classe =====")
    print("\nEscolha a classe para jogar:")
    print("1) Paladino   [lança e escudo]")
    print("2) Atirador [Arma]")
    print("3) Guerreiro [Espada e Escudo]")
    print("4) Bárbaro   [Machado ou Marreta]")
    print("5) Arqueiro [Arco]")

    escolha = int(input("Digite o número correspondente à classe desejada: "))


    if escolha == 1:
        return "Paladino"
    elif escolha == 2:
        return "Atirador"
    elif escolha == 3:
        return "Guerreiro"
    elif escolha == 4:
        return "Bárbaro"
    elif escolha == 5:
        return "Arqueiro"
    else:
        print("Opção inválida. Tente novamente.")
        return tela_selecao_classe()  


def customizar_avatar():
    print("\n===== Tela de Customização do =====")
    print("Opções de customização:")
    print("1) Gênero do seu Herói")
    print("2) Cor dos cabelos ")
    print("3) Cor dos olhos ")
    print("4) Cor da pele ")
    print("5) Altura ")

    avatar_customizado = {}

    opcao = int(input(
        "Digite o número correspondente à característica que deseja customizar (ou 0 para finalizar): "))

    while opcao != 0:
        if opcao == 1:
            genero = input("Digite o gênero de seu herói: ")
            avatar_customizado["genero"] = genero
        elif opcao == 2:
            cor_cabelo = input("Digite a cor de cabelo desejada: ")
            avatar_customizado["cor_cabelo"] = cor_cabelo
        elif opcao == 3:
            cor_olhos = input("Digite a cor dos olhos desejada: ")
            avatar_customizado["cor_olhos"] = cor_olhos
        elif opcao == 4:
            cor_pele = input("Digite a cor de pele desejada: ")
            avatar_customizado["cor_pele"] = cor_pele
        elif opcao == 5:
            altura = float(input("Digite a altura desejada: "))
            avatar_customizado["altura"] = altura
        else:
            print("Opção inválida. Tente novamente.")

        opcao = int(input(
            "Digite o número correspondente à característica que deseja customizar (ou 0 para finalizar): "))

    return avatar_customizado



def pontos_classe():
    print("\n===== Distribuição de Pontos para a Classe =====")
    print("Você tem 10 pontos para distribuir entre os atributos: Vida, Mana e Velocidade de Ataque")

    atributos = ["Vida", "Mana", "Velocidade de Ataque"]
    pontos_disponiveis = 10
    atributos_distribuidos = {}

    for atributo in atributos:
        pontos = int(
            input("Digite a quantidade de pontos para o atributo {}: ".format(atributo)))

        # Validação para garantir que o número de pontos seja válido.
        while pontos < 0 or pontos > pontos_disponiveis:
            print("Valor inválido. Digite um número de 0 a {}.".format(
                pontos_disponiveis))
            pontos = int(
                input("Digite a quantidade de pontos para o atributo {}: ".format(atributo)))

        atributos_distribuidos[atributo] = pontos
        pontos_disponiveis -= pontos

    return atributos_distribuidos


def pontos_montaria():
    print("\n===== Distribuição de Pontos para a Montaria =====")
    print("Você tem 5 pontos para distribuir entre os atributos: Velocidade e Tempo para descanso")

    atributos_montaria = ["Velocidade", "Tempo para descanso"]
    pontos_disponiveis = 5
    atributos_distribuidos_montaria = {}

    for atributo in atributos_montaria:
        pontos = int(
            input("Digite a quantidade de pontos para o atributo {}: ".format(atributo)))

        while pontos < 0 or pontos > pontos_disponiveis:
            print("Valor inválido. Digite um número de 0 a {}.".format(
                pontos_disponiveis))
            pontos = int(
                input("Digite a quantidade de pontos para o atributo {}: ".format(atributo)))

        atributos_distribuidos_montaria[atributo] = pontos
        pontos_disponiveis -= pontos

    return atributos_distribuidos_montaria


def mostrar_informacoes_heroi(heroi_escolhido, avatar_customizado, atributos_distribuidos, atributos_distribuidos_montaria):
    print("\n===== Informações do Herói =====")
    print("Classe: {}".format(heroi_escolhido))
    print("Características customizadas:")
    for chave, valor in avatar_customizado.items():
        print("{}: {}".format(chave, valor))
    print("\nAtributos distribuídos:")
    for chave, valor in atributos_distribuidos.items():
        print("{}: {}".format(chave, valor))
    print("\nAtributos da montaria:")
    for chave, valor in atributos_distribuidos_montaria.items():
        print("{}: {}".format(chave, valor))


def main():

    print("*"*30)
    print("\nSEJA BEM VINDO AO REINO DOS PERDIDOS: A JORNADA DE DIAMANTAURUS\n")
    print("*"*30)

    login = input("Você já possui login? (S/N) ")

    if "S" in login or "s" in login:
        tela_login()
    else:
        print("\nVejo que é novo por aqui estranho...\n")
        print(
            "Preciso que antes me forneça algumas informações para embarcar nessa aventura:")
        cadastrar_usuario()

    heroi_escolhido = tela_selecao_classe()
    print("\nVocê selecionou:", heroi_escolhido)

    trocar_classe = input("Deseja trocar de classe? (S/N): ")

    if trocar_classe.upper() == "S":
        heroi_escolhido = tela_selecao_classe()

    print("\nAgora você está jogando como:", heroi_escolhido)

    avatar_customizado = customizar_avatar()
    atributos_distribuidos = pontos_classe()
    atributos_distribuidos_montaria = pontos_montaria()

    mostrar_informacoes_heroi(heroi_escolhido, avatar_customizado,
                              atributos_distribuidos, atributos_distribuidos_montaria)

    print("*"*30)
    print("\nAGORA ESTAMOS PRONTOS PARA INICIAR NOSSA AVENTURA!\n")
    print("*"*30)


if __name__ == "__main__":
    main()
