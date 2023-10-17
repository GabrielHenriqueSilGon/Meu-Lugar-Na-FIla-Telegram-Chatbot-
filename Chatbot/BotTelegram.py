import telebot

ID_ADM = 5120345331

CHAVE_API = "6667065980:AAH-cee6ABvdKELBJHFEyZUDnuo3Num8nqw"

bot = telebot.TeleBot(CHAVE_API)

class Pessoa:
    def __init__(nafila, nome, id_do_chat, tempo_ate_atender, tempo_ate_fim_de_consulta):
        nafila.nome = nome
        nafila.id_do_chat = id_do_chat
        nafila.tempo_ate_atender = tempo_ate_atender
        nafila.tempo_ate_fim_de_consulta = tempo_ate_fim_de_consulta

fila: list[Pessoa] = []

@bot.message_handler(commands=["sim"])
def sim(mensagem):
    n = mensagem.chat.id
    Pessoa1 = Pessoa (f"{mensagem.from_user.first_name} {mensagem.from_user.last_name}", n,"25:00","25:00")
    fila.append(Pessoa1)

    bot.send_message(mensagem.chat.id, "Requisição enviada.")

    texto = (f"""NOVA REQUISIÇÃO:
    Nome: {mensagem.from_user.first_name} {mensagem.from_user.last_name}
    ID: {mensagem.chat.id}
    /registrar Registra a pessoa na fila, favor escrever o horário previsto para atender e o de termino no formato 00:00 após o comando (Ex: /registrar 15:20 16:50)
    /negar Tira a pessoa da fila. Favor colocar o ID do destinatário após o comando (Ex: /negar 5555555555)
    /mensagem Manda uma mensagem para o(a) dono(a) da requisição. Favor colocar o ID do destinatário após o comando (Ex: /mensagem 5555555555 Atendimento inalcançãvel, favor retornar mais tarde)""")
    bot.send_message(ID_ADM, texto)

@bot.message_handler(commands=["registrar"])
def registrar(mensagem):
    if mensagem.chat.id != ID_ADM:
        bot.send_message(mensagem.chat.id, "Permição negada.")
    msg_quebrada = mensagem.text.split()
    if len(msg_quebrada) != 3:
        bot.send_message(mensagem.chat.id, "Formatação incorreta")
    for x in fila:
        if x.tempo_ate_atender == "25:00":
            x.tempo_ate_atender = msg_quebrada[1]
            x.tempo_ate_fim_de_consulta = msg_quebrada[2]
            break

@bot.message_handler(commands=["mensagem"])
def mensagem(mensagem):
    msg_quebrada = mensagem.text.split()
    id_rec = int(msg_quebrada(1))
    msg_quebrada.remove(0)
    msg_quebrada.remove(1)
    texto = " ".join(msg_quebrada)
    bot.send_message(id_rec, texto)
    bot.send_message(id_rec, "Para responder, digite sua resposta após /responder. (Ex: /responder preciso de ajuda)")

@bot.message_handler(commands=["responder"])
def responder(mensagem):
    msg_quebrada = mensagem.text.split()
    msg_quebrada.remove(0)
    texto = " ".join(msg_quebrada)
    bot.send_message(ID_ADM, texto)
    bot.send_message(ID_ADM, f"ID do chat: {mensagem.chat.id}. Para responder, digite /mensagem ID [texto de resposta]")

@bot.message_handler(commands=["negar"])
def negar(mensagem):
    if mensagem.chat.id != ID_ADM:
        bot.send_message(mensagem.chat.id, "Permição negada.")
    msg_quebrada = mensagem.text.split()
    for x in fila:
        if x.id_do_chat == msg_quebrada[1]:
            fila.remove(x)
    bot.send_message(mensagem.chat.id, "Negação concluída.")
    bot.send_message(msg_quebrada[1], "Infelizmente seu lugar foi negado, tente mais tarde.")
    bot.send_message(msg_quebrada[1], "Para entrar em contato, digite sua mensagem após /responder. (Ex: /responder preciso de ajuda)")

@bot.message_handler(commands=["finalizar"])
def finalizar(mensagem):
    if mensagem.chat.id != ID_ADM:
        bot.send_message(mensagem.chat.id, "Permição negada.")
    PessFinal = fila.pop(0)
    bot.send_message(ID_ADM, "Primeira consulta na fila terminada.")
    bot.send_message(PessFinal.id_do_chat, "Consulta finalizada. Se algo de errado tiver ocorrido, entre em contato com o hospital")

@bot.message_handler(commands=["editar"])
def editar(mensagem):
    if mensagem.chat.id != ID_ADM:
        bot.send_message(mensagem.chat.id, "Permição negada.")
    msg_quebrada = mensagem.text.split()
    if len(msg_quebrada) != 4:
        bot.send_message(mensagem.chat.id, "Formatação incorreta")
    bot.send_message(msg_quebrada[1], f"Seu horário foi editado para {msg_quebrada[2]} até {msg_quebrada[3]}.")
    bot.send_message(msg_quebrada[1], f"Se houver alguma reclamação, digite sua resposta após /responder. (Ex: /responder preciso de ajuda)")
    for x in fila:
        if x.id_do_chat == int(msg_quebrada[1]):
            x.tempo_ate_atender = msg_quebrada[2]
            x.tempo_ate_fim_de_consulta = msg_quebrada[3]
            break

@bot.message_handler(commands=["sair"])
def sair(mensagem):
    for x in fila:
        if x.id_do_chat == mensagem.chat.id:
            fila.remove(x)
    bot.send_message(mensagem.chat.id, "Cancela concluída.")
    bot.send_message(ID_ADM, f"{mensagem.chat.id} cancelou a vaga na fila.")

@bot.message_handler(commands=["verfila"])
def verfila(mensagem):
    i = ""
    for P in fila:
        i = P.tempo_ate_fim_de_consulta
    texto = (f"Atualmente, a fila tem {len(fila)} membros. A ultima consulta na fila dura até: {i}.")
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["verfilaADM"])
def verfilaADM(mensagem):
    if mensagem.chat.id != ID_ADM:
        bot.send_message(mensagem.chat.id, "Permição negada.")
    for P in fila:
        texto = (f"{P.nome}; ID: {P.id_do_chat}; Hora Atendimento: {P.tempo_ate_atender}; Hora Fim: {P.tempo_ate_fim_de_consulta}")
        bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["entrar"])
def entrar(mensagem):
    o = ""
    for P in fila:
        o = P.tempo_ate_fim_de_consulta
    texto = (f"""Atualmente, a fila tem {len(fila)} membros. A ultima consulta na fila dura até: {o}.
    Deseja entrar em espera?
    /sim
    /não""")
    bot.send_message(mensagem.chat.id, texto)

def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    print(mensagem)
    trueID = mensagem.chat.id

    if trueID != ID_ADM:
        texto = """
    Escolha uma opção para continuar (Clique no item):
     /verfila Ver fila atual
     /entrar Entrar na fila
     /sair Cancelar vaga na fila
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    else:
        texto = """
Bem vindo(a) adm!
    /verfilaADM Ver fila atual
    /editar edita o tempo de alguém específico. Seguir comando com ID e horários novos (EX: /editar 5555555555 12:00 12:30)
    /finalizar Remove a primeira consulta na fila
    /negar Tira a pessoa da fila. Favor colocar o ID do destinatário após o comando (Ex: /negar 5555555555)
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)


bot.polling()
