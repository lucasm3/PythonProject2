import os

# Estruturas de dados para armazenar informações
usuarios = [
    {"nome": "Ana Silva", "email": "ana.silva@gmail.com", "senha": "123456"},
    {"nome": "Carlos Oliveira", "email": "carlos.oliveira@hotmail.com", "senha": "abcdef"},
    {"nome": "Mariana Santos", "email": "mariana.santos@yahoo.com", "senha": "senha123"}
]

caronas = [
    {
        "motorista": "ana.silva@gmail.com",
        "origem": "São Paulo",
        "destino": "Rio de Janeiro",
        "data": "25/06/2023",
        "horario": "08:00",
        "vagas": 2,
        "valor": 60.00,
        "passageiros": ["carlos.oliveira@hotmail.com"]
    },
    {
        "motorista": "carlos.oliveira@hotmail.com",
        "origem": "Belo Horizonte",
        "destino": "São Paulo",
        "data": "30/06/2023",
        "horario": "14:30",
        "vagas": 3,
        "valor": 75.00,
        "passageiros": []
    }
]

reservas = []
usuario_logado = None


# Funções principais
def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome completo: ")
    email = input("Email: ")

    if not validar_email(email):
        print("Erro: Email inválido! Deve conter '@' e terminar com '.com', '.com.br' ou similar")
        return

    senha = input("Senha: ")

    for usuario in usuarios:
        if usuario["email"] == email:
            print("Erro: Email já cadastrado!")
            return

    usuarios.append({"nome": nome, "email": email, "senha": senha})
    salvar_usuarios_arquivo()
    print("Usuário cadastrado com sucesso!")


def login():
    global usuario_logado
    print("\n--- Login ---")
    email = input("Email: ")

    if not validar_email(email):
        print("Erro: Email inválido! Deve conter '@' e terminar com '.com', '.com.br' ou similar")
        return False

    senha = input("Senha: ")

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            usuario_logado = usuario
            print(f"Bem-vindo, {usuario['nome']}!")
            return True

    print("Email ou senha incorretos!")
    return False


def validar_email(email):
    """Verifica se o email tem formato válido"""
    return "@" in email and (
                email.endswith(".com") or email.endswith(".com.br") or email.endswith(".org") or email.endswith(".net"))


def logout():
    global usuario_logado
    usuario_logado = None
    print("Logout realizado com sucesso!")


def cadastrar_carona():
    if not verificar_login():
        return

    print("\n--- Cadastrar Carona ---")
    origem = input("Local de origem: ")
    destino = input("Destino: ")
    data = input("Data (DD/MM/AAAA): ")
    horario = input("Horário (HH:MM): ")
    vagas = int(input("Quantidade de vagas: "))
    valor = float(input("Valor por vaga: R$"))

    nova_carona = {
        "motorista": usuario_logado["email"],
        "origem": origem,
        "destino": destino,
        "data": data,
        "horario": horario,
        "vagas": vagas,
        "valor": valor,
        "passageiros": [],
        "vagas_inicial": vagas  # Adicionado para o relatório
    }
    caronas.append(nova_carona)
    print("Carona cadastrada com sucesso!")


def listar_caronas_disponiveis():
    if not verificar_login():
        return

    print("\n--- Caronas Disponíveis ---")
    encontrou = False

    for carona in caronas:
        if carona["vagas"] > 0:
            encontrou = True
            print(f"Motorista: {obter_nome_por_email(carona['motorista'])}")
            print(f"Origem: {carona['origem']} | Destino: {carona['destino']}")
            print(f"Data: {carona['data']} | Horário: {carona['horario']}")
            print(f"Vagas: {carona['vagas']} | Valor: R${carona['valor']:.2f}")
            print("------------------------")

    if not encontrou:
        print("Nenhuma carona disponível no momento.")


def buscar_carona_origem_destino():
    if not verificar_login():
        return

    print("\n--- Buscar Carona ---")
    origem = input("Origem: ")
    destino = input("Destino: ")
    encontrou = False

    for carona in caronas:
        if (carona["origem"].lower() == origem.lower() and
                carona["destino"].lower() == destino.lower() and
                carona["vagas"] > 0):
            encontrou = True
            print(f"Motorista: {obter_nome_por_email(carona['motorista'])}")
            print(f"Data: {carona['data']} | Horário: {carona['horario']}")
            print(f"Vagas: {carona['vagas']} | Valor: R${carona['valor']:.2f}")
            print("------------------------")

    if not encontrou:
        print("Nenhuma carona encontrada com esses critérios.")


def reservar_vaga():
    if not verificar_login():
        return

    print("\n--- Reservar Vaga ---")
    email_motorista = input("Email do motorista: ")
    data_carona = input("Data da carona (DD/MM/AAAA): ")

    for carona in caronas:
        if (carona["motorista"] == email_motorista and
                carona["data"] == data_carona):
            if carona["vagas"] > 0:
                carona["vagas"] -= 1
                carona["passageiros"].append(usuario_logado["email"])
                print("Vaga reservada com sucesso!")
                return
            else:
                print("Não há vagas disponíveis nesta carona.")
                return

    print("Carona não encontrada.")


def cancelar_reserva():
    if not verificar_login():
        return

    print("\n--- Cancelar Reserva ---")
    email_motorista = input("Email do motorista: ")
    data_carona = input("Data da carona (DD/MM/AAAA): ")

    for carona in caronas:
        if (carona["motorista"] == email_motorista and
                carona["data"] == data_carona):
            if usuario_logado["email"] in carona["passageiros"]:
                carona["vagas"] += 1
                carona["passageiros"].remove(usuario_logado["email"])
                print("Reserva cancelada com sucesso!")
                return
            else:
                print("Você não tem reserva nesta carona.")
                return

    print("Carona não encontrada.")


def remover_carona():
    if not verificar_login():
        return

    print("\n--- Remover Carona ---")
    data_carona = input("Data da carona (DD/MM/AAAA): ")

    for i, carona in enumerate(caronas):
        if (carona["motorista"] == usuario_logado["email"] and
                carona["data"] == data_carona):
            caronas.pop(i)
            print("Carona removida com sucesso!")
            return

    print("Carona não encontrada ou você não tem permissão para removê-la.")


def mostrar_detalhes_carona():
    if not verificar_login():
        return

    print("\n--- Detalhes da Carona ---")
    email_motorista = input("Email do motorista: ")
    data_carona = input("Data da carona (DD/MM/AAAA): ")

    for carona in caronas:
        if (carona["motorista"] == email_motorista and
                carona["data"] == data_carona):
            print(f"Motorista: {obter_nome_por_email(carona['motorista'])}")
            print(f"Origem: {carona['origem']} | Destino: {carona['destino']}")
            print(f"Data: {carona['data']} | Horário: {carona['horario']}")
            print(f"Vagas restantes: {carona['vagas']} | Valor: R${carona['valor']:.2f}")
            print("Passageiros:")
            for passageiro in carona["passageiros"]:
                print(f"- {obter_nome_por_email(passageiro)}")
            return

    print("Carona não encontrada.")


def mostrar_minhas_caronas():
    if not verificar_login():
        return

    print("\n--- Minhas Caronas ---")
    encontrou = False

    for carona in caronas:
        if carona["motorista"] == usuario_logado["email"]:
            encontrou = True
            print(f"Origem: {carona['origem']} | Destino: {carona['destino']}")
            print(f"Data: {carona['data']} | Horário: {carona['horario']}")
            print(f"Vagas restantes: {carona['vagas']} | Valor: R${carona['valor']:.2f}")
            print("Passageiros:")
            for passageiro in carona["passageiros"]:
                print(f"- {obter_nome_por_email(passageiro)}")
            print("------------------------")

    if not encontrou:
        print("Você não tem caronas cadastradas.")


def relatorio_totalizadores():
    if not verificar_login():
        return

    print("\n--- Relatório de Totalizadores ---")
    total_geral = 0
    encontrou = False

    for carona in caronas:
        if carona["motorista"] == usuario_logado["email"]:
            encontrou = True
            vagas_ocupadas = carona["vagas_inicial"] - carona["vagas"]
            total_carona = vagas_ocupadas * carona["valor"]
            total_geral += total_carona

            print(f"Origem: {carona['origem']} | Destino: {carona['destino']}")
            print(f"Data/Horário: {carona['data']} {carona['horario']}")
            print(f"Valor: R${carona['valor']:.2f} | Vagas restantes: {carona['vagas']}")
            print(f"Total desta carona: R${total_carona:.2f}")
            print("------------------------")

    if encontrou:
        print(f"TOTAL GERAL: R${total_geral:.2f}")

        salvar = input("Deseja salvar este relatório em um arquivo? (sim/não): ")
        if salvar.lower() == "sim":
            nome_arquivo = f"relatorio_{usuario_logado['email']}.txt"
            with open(nome_arquivo, "w") as f:
                f.write(f"Relatório de Caronas - {usuario_logado['nome']}\n\n")
                for carona in caronas:
                    if carona["motorista"] == usuario_logado["email"]:
                        vagas_ocupadas = carona["vagas_inicial"] - carona["vagas"]
                        total_carona = vagas_ocupadas * carona["valor"]

                        f.write(f"Origem: {carona['origem']} | Destino: {carona['destino']}\n")
                        f.write(f"Data/Horário: {carona['data']} {carona['horario']}\n")
                        f.write(f"Valor: R${carona['valor']:.2f} | Vagas restantes: {carona['vagas']}\n")
                        f.write(f"Total desta carona: R${total_carona:.2f}\n")
                        f.write("------------------------\n")
                f.write(f"\nTOTAL GERAL: R${total_geral:.2f}\n")
            print(f"Relatório salvo em {nome_arquivo}")
    else:
        print("Não há caronas cadastradas")


def mostrar_minhas_reservas():
    if not verificar_login():
        return

    print("\n--- Minhas Reservas ---")
    encontrou = False

    for carona in caronas:
        if usuario_logado["email"] in carona["passageiros"]:
            encontrou = True
            print(f"Motorista: {obter_nome_por_email(carona['motorista'])}")
            print(f"Origem: {carona['origem']} | Destino: {carona['destino']}")
            print(f"Data: {carona['data']} | Horário: {carona['horario']}")
            print(f"Valor: R${carona['valor']:.2f}")
            print("------------------------")

    if not encontrou:
        print("Você não tem reservas.")


# Funções auxiliares
def verificar_login():
    if usuario_logado is None:
        print("Erro: Você precisa estar logado para acessar esta funcionalidade.")
        return False
    return True


def obter_nome_por_email(email):
    for usuario in usuarios:
        if usuario["email"] == email:
            return usuario["nome"]
    return "Desconhecido"


def salvar_usuarios_arquivo():
    with open("usuarios.txt", "w") as f:
        for usuario in usuarios:
            f.write(f"{usuario['nome']},{usuario['email']},{usuario['senha']}\n")


def importar_usuarios_arquivo():
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as f:
            for linha in f:
                dados = linha.strip().split(",")
                if len(dados) == 3:
                    usuarios.append({
                        "nome": dados[0],
                        "email": dados[1],
                        "senha": dados[2]
                    })


# Menu principal
def menu_principal():
    while True:
        print("\n--- Sistema de Caronas ---")
        if usuario_logado:
            print(f"Usuário: {usuario_logado['nome']}")
            print("1. Cadastrar Carona")
            print("2. Listar Caronas Disponíveis")
            print("3. Buscar Carona por Origem/Destino")
            print("4. Reservar Vaga")
            print("5. Cancelar Reserva")
            print("6. Remover Carona")
            print("7. Detalhes de Carona")
            print("8. Minhas Caronas")
            print("9. Minhas Reservas (Extra)")
            print("10. Relatório de Totalizadores")
            print("11. Logout")
        else:
            print("1. Cadastrar Usuário")
            print("2. Login")
            print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if usuario_logado:
            if opcao == "1":
                cadastrar_carona()
            elif opcao == "2":
                listar_caronas_disponiveis()
            elif opcao == "3":
                buscar_carona_origem_destino()
            elif opcao == "4":
                reservar_vaga()
            elif opcao == "5":
                cancelar_reserva()
            elif opcao == "6":
                remover_carona()
            elif opcao == "7":
                mostrar_detalhes_carona()
            elif opcao == "8":
                mostrar_minhas_caronas()
            elif opcao == "9":
                mostrar_minhas_reservas()
            elif opcao == "10":
                relatorio_totalizadores()
            elif opcao == "11":
                logout()
            else:
                print("Opção inválida!")
        else:
            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                login()
            elif opcao == "3":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")


# Inicialização do sistema
importar_usuarios_arquivo()
menu_principal()