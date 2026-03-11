def normalizar_curso(curso):
    return curso.strip().upper().replace(" ", "")


def email_valido(email):
    return "@" in email and "." in email


def gerar_matricula(curso, contadores):
    if curso not in contadores:
        contadores[curso] = 0
    contadores[curso] += 1
    return f"{curso}{contadores[curso]}"


def buscar_aluno_por_matricula(alunos, matricula):
    for indice, aluno in enumerate(alunos):
        if aluno["matricula"] == matricula:
            return indice, aluno
    return None, None


def cadastrar_aluno(alunos, contadores):
    print("\n=== Cadastro de Aluno ===")

    nome = input("Nome: ").strip()
    while not nome:
        print("Nome não pode ser vazio.")
        nome = input("Nome: ").strip()

    email = input("Email: ").strip()
    while not email_valido(email):
        print("Email inválido. Exemplo: nome@dominio.com")
        email = input("Email: ").strip()

    curso = normalizar_curso(input("Curso (ex.: GES, GEC, GET, GEP): "))
    while not curso:
        print("Curso não pode ser vazio.")
        curso = normalizar_curso(input("Curso (ex.: GES, GEC, GET, GEP): "))

    matricula = gerar_matricula(curso, contadores)
    aluno = {
        "nome": nome,
        "email": email,
        "curso": curso,
        "matricula": matricula,
    }
    alunos.append(aluno)

    print(f"Aluno cadastrado com sucesso! Matrícula: {matricula}")


def listar_alunos(alunos):
    print("\n=== Lista de Alunos ===")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for numero, aluno in enumerate(alunos, start=1):
        print(
            f"{numero}. Nome: {aluno['nome']} | "
            f"Email: {aluno['email']} | "
            f"Curso: {aluno['curso']} | "
            f"Matrícula: {aluno['matricula']}"
        )


def atualizar_aluno(alunos, contadores):
    print("\n=== Atualização de Aluno ===")
    matricula = input("Informe a matrícula do aluno: ").strip().upper()

    _, aluno = buscar_aluno_por_matricula(alunos, matricula)
    if aluno is None:
        print("Aluno não encontrado.")
        return

    novo_nome = input(f"Novo nome [{aluno['nome']}]: ").strip()
    if novo_nome:
        aluno["nome"] = novo_nome

    novo_email = input(f"Novo email [{aluno['email']}]: ").strip()
    if novo_email:
        while not email_valido(novo_email):
            print("Email inválido. Exemplo: nome@dominio.com")
            novo_email = input("Novo email: ").strip()
        aluno["email"] = novo_email

    novo_curso_input = input(f"Novo curso [{aluno['curso']}]: ").strip()
    if novo_curso_input:
        novo_curso = normalizar_curso(novo_curso_input)
        if novo_curso != aluno["curso"]:
            matricula_antiga = aluno["matricula"]
            nova_matricula = gerar_matricula(novo_curso, contadores)
            aluno["curso"] = novo_curso
            aluno["matricula"] = nova_matricula
            print(f"Matrícula atualizada de {matricula_antiga} para {nova_matricula}.")

    print("Aluno atualizado com sucesso.")


def remover_aluno(alunos):
    print("\n=== Remoção de Aluno ===")
    matricula = input("Informe a matrícula do aluno: ").strip().upper()

    indice, aluno = buscar_aluno_por_matricula(alunos, matricula)
    if aluno is None:
        print("Aluno não encontrado.")
        return

    confirmacao = input(f"Confirma remover {aluno['nome']}? (s/n): ").strip().lower()
    if confirmacao == "s":
        alunos.pop(indice)
        print("Aluno removido com sucesso.")
    else:
        print("Remoção cancelada.")


def exibir_menu():
    print("\n===== Sistema de Alunos =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Atualizar aluno")
    print("4 - Remover aluno")
    print("0 - Sair")


def main():
    alunos = []
    contadores = {}

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno(alunos, contadores)
        elif opcao == "2":
            listar_alunos(alunos)
        elif opcao == "3":
            atualizar_aluno(alunos, contadores)
        elif opcao == "4":
            remover_aluno(alunos)
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
