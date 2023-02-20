############################################################################################################
####.______     ______   .___________.   .___________. __    ______      .______    __   __       __      ##
####|   _  \   /  __  \  |           |   |           ||  |  /  __  \     |   _  \  |  | |  |     |  |     ##
####|  |_)  | |  |  |  | `---|  |----`   `---|  |----`|  | |  |  |  |    |  |_)  | |  | |  |     |  |     ##
####|   _  <  |  |  |  |     |  |            |  |     |  | |  |  |  |    |   _  <  |  | |  |     |  |     ##
####|  |_)  | |  `--'  |     |  |            |  |     |  | |  `--'  |    |  |_)  | |  | |  `----.|  `----.##
####|______/   \______/      |__|            |__|     |__|  \______/     |______/  |__| |_______||_______|##
############################################################################################################
############ MANUAL DE USO DO BOT TIO BILL PARA MONITORAMENTO DE MENSAGENS INAPROPRIADAS NO TELEGRAM #######
############################################################################################################
############################################################################################################
##################################### by Fernando Oliveira Op07 (IguanaMan)#################################
############################################################################################################

# Importando as bibliotecas python
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram import ChatPermissions
import argparse
import sqlite3
import os

# Define os argumentos
parser = argparse.ArgumentParser()
parser.add_argument('--chat_id', required=True, help='ID do chat')
parser.add_argument('--bot_token', required=True, help='API token do bot')
args = parser.parse_args()

# Cria o nome do BD vinculado ao chat ID do telegram
chat_id = args.chat_id
db_name = f"bad_words_{chat_id}.db"

# Verifica a existência do banco de dados
if not os.path.exists(db_name):
    # Banco de dados não existe, perguntar ao usuário se deseja criar um novo
    response = input("O banco de dados não existe. Deseja criar um novo? (S/N) ")
    if response.lower() == "s":
        database_connection = sqlite3.connect(db_name)
        database_connection.execute('''CREATE TABLE IF NOT EXISTS bad_words
                     (word TEXT PRIMARY KEY NOT NULL);''')
        database_connection.close()
    else:
        # Usuário não deseja criar um novo banco de dados, finalizar o programa
        print(f"Ocorreu um erro ao acessar o Banco de dados do sistema {db_name} inexistente!")
        exit()

# Restrições de tipos de mensagens permitidas (midia, figurinhas...)
restrictions = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_send_stickers=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)

# Habilitar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Lista de usuários que foram restringidos nos últimos 30 dias
restricted_users = {}

# Conexão com o banco de dados
try:
    database_connection = sqlite3.connect(db_name)
except Exception as e:
    print(f"Ocorreu um erro ao conectar ao banco de dados: {e}")
    exit()


# Tabela de palavras impróprias
database_connection.execute('''CREATE TABLE IF NOT EXISTS bad_words
             (word TEXT PRIMARY KEY NOT NULL);''')

# Carrega as palavras do banco de dados para a lista
bad_words = [row[0] for row in database_connection.execute("SELECT word FROM bad_words").fetchall()]

# Função para verificar palavras impróprias na biblioteca python
def check_message(text):
    for word in bad_words:
        if word in text:
            return True
    return False

# Função para verificar se um usuário foi restringido nos últimos 30 dias
def is_restricted(user_id):
    if user_id in restricted_users:
        last_restriction_time = restricted_users[user_id]
        now = datetime.now()
        if now < last_restriction_time + timedelta(days=30):
            return True
    return False

# Manipulador de mensagens para mensagens de monitoramento
def message_handler(update: Update, context: CallbackContext):
    message = update.effective_message
    print(message)
    if message.text is not None:
        if check_message(message.text):
            if message.from_user:
                user_id = message.from_user.id
                if is_restricted(user_id):
                    user_name = message.from_user.full_name
                    context.bot.ban_chat_member(chat_id=args.chat_id, user_id=user_id)
                    context.bot.send_message(chat_id=args.chat_id, text=f"O Usuário {user_name} banido por repetição de mensagem inapropriada.")
                else:
                    # Silenciar o usuário por 24 horas
                    user_name = message.from_user.full_name
                    now = datetime.now()
                    restricted_until = now + timedelta(hours=24)
                    update.effective_chat.restrict_member(user_id, permissions=restrictions, until_date=restricted_until.timestamp())
                    restricted_users[user_id] = now
                    context.bot.send_message(chat_id=args.chat_id, text=f"O Usuário {user_name} foi silenciado por 24 horas devido a mensagem inapropriada.")
            else:
                logging.info("Mensagem de Usuário Dono/Adm ou sem Remetente")

try:
    words = []
    database_connection.execute("BEGIN")
    for word in words:
        database_connection.execute("INSERT OR IGNORE INTO bad_words (word) VALUES (?)", (word,))
    database_connection.commit()
except Exception as e:
    database_connection.rollback()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ocorreu um erro ao adicionar as palavras.")
    logging.error("Erro ao adicionar as palavras: " + str(e))

# Carrega as palavras do banco de dados para a lista
bad_words = [row[0] for row in database_connection.execute("SELECT word FROM bad_words").fetchall()]

# Manipulador de comandos para listar as palavras impróprias monitoradas pelo bot
def bad_words_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Palavras impróprias: " + ", ".join(bad_words))

# Manipulador de comandos para adicionar palavras à lista de palavras impróprias
def add_words_handler(update: Update, context: CallbackContext):
    # Separa a mensagem em palavras e remove o comando /addwords
    words = update.message.text.split()[1:]
    if len(words) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nenhuma palavra fornecida.")
    else:
        try:
            # Inicia a transação
            database_connection.execute("INICIANDO...")
            for word in words:
                database_connection.execute("INSERIR OU IGNORAR EM bad_words (word) VALUES (?)", (word,))
                logging.info(f"Palavra-chave adicionada ao banco de dados: {word}")

            # Encerra a transação
            database_connection.commit()
            # Carrega as palavras atualizadas para a lista bad_words
            bad_words.clear()
            bad_words.extend([row[0] for row in database_connection.execute("SELECT word FROM bad_words").fetchall()])
            context.bot.send_message(chat_id=update.effective_chat.id, text="Palavras adicionadas com sucesso: " + ", ".join(words))
        except Exception as e:
            # Em caso de erro, faz rollback da transação
            database_connection.rollback()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ocorreu um erro ao adicionar as palavras.")
            logging.error("Erro ao adicionar as palavras: " + str(e))

# Manipulador de comandos para remover palavras da lista de palavras impróprias
def remove_words_handler(update: Update, context: CallbackContext):
    # Separa a mensagem em palavras e remove o comando /removewords
    words = update.message.text.split()[1:]
    if len(words) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nenhuma palavra fornecida.")
    else:
        try:
            # Inicia a transação
            database_connection.execute("INICIANDO...")
            for word in words:
                database_connection.execute("DELETE FROM bad_words WHERE word=?", (word,))
                logging.info(f"Palavra-chave removida do banco de dados: {word}")
            # Encerra a transação
            database_connection.commit()
            # Carrega as palavras atualizadas para a lista bad_words
            bad_words.clear()
            bad_words.extend([row[0] for row in database_connection.execute("SELECT word FROM bad_words").fetchall()])
            context.bot.send_message(chat_id=update.effective_chat.id, text="Palavras removidas com sucesso: " + ", ".join(words))
        except Exception as e:
            # Em caso de erro, faz rollback da transação
            database_connection.rollback()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ocorreu um erro ao remover as palavras.")
            logging.error("Erro ao remover as palavras: " + str(e))

# Cria o Updater com o token do bot
updater = Updater(args.bot_token)

# Adiciona o manipulador de mensagens ao dispatcher
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, message_handler))

# Adiciona o manipulador de comandos "/badwords" ao dispatcher
dp.add_handler(CommandHandler("badwords", bad_words_handler))

# Adiciona o manipulador de comandos "/addwords" ao dispatcher
dp.add_handler(CommandHandler("addwords", add_words_handler))

# Adiciona o manipulador de comandos "/removewords" ao dispatcher
dp.add_handler(CommandHandler("removewords", remove_words_handler))

# Iniciar o bot
updater.start_polling()

#Execute o bot até pressionar Ctrl-C ou o processo receber SIGINT,
#SIGTERM ou SIGABRT. Isso deve ser usado na maioria das vezes, pois
#start_polling() não bloqueia e interromperá o bot normalmente.
updater.idle()

##################################### by Fernando Oliveira Op07 (IguanaMan)#################################
