###########################################################################################################
############### MANUAL DE USO DO BOT TIO BILL PARA MONITORAMENTO DE MENSAGENS INAPROPRIADAS NO TELEGRAM ########
###########################################################################################################
###########################################################################################################
########################################## by Fernando Oliveira Op07 (IguanaMan)##################################
###########################################################################################################


# É necessário instalar as seguintes bibliotecas Python antes de utilizar o código:

import logging

from datetime import datetime, timedelta

from telegram import Update

from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

from telegram import ChatPermissions

import argparse

import sqlite3

import os

# Você pode instalar essas bibliotecas usando o seguinte comando no terminal:

pip install telegram telegram.ext logging datetime sqlite3

# Configuração do Bot

Para configurar o bot, é necessário fornecer o ID do chat e o token da API do bot do Telegram. Essas informações são passadas como argumentos ao executar o script.

# Exemplo de uso:

python bot.py --chat_id <chat_id> --bot_token <bot_token>

# Funcionamento do Bot

O bot funciona monitorando as mensagens enviadas no chat e verificando se elas contêm palavras impróprias. Se uma mensagem for considerada inapropriada, o usuário que enviou a mensagem será silenciado por 24 horas. Se o mesmo usuário for pego enviando mensagens inapropriadas novamente dentro de um período de 30 dias, ele será banido do chat.

# Comandos do Bot

Além do monitoramento de mensagens, o bot também fornece alguns comandos para gerenciar a lista de palavras impróprias.

# Os comandos disponíveis são:

/badwords: exibe a lista de palavras impróprias monitoradas pelo bot.

/addwords palavra1 palavra2 : adiciona uma ou mais palavras à lista de palavras impróprias monitoradas pelo bot.
  
/removewords palavra1 palavra2 : remove uma ou mais palavras da lista de palavras impróprias monitoradas pelo bot.

# Considerações finais
  
Este bot foi desenvolvido com o objetivo de ajudar a monitorar e restringir mensagens inapropriadas em chats do Telegram. Use-o com responsabilidade e lembre-se de sempre respeitar as regras e a privacidade dos usuários do chat.

# Nos ajude a continuar desenvolvendo e faça uma doação do valor de R$ 10,00 no pix de celular abaixo:

(34) 99132-9872 - Fernando Martins de Oliveira


# desenvolvido por Fernando Martins de Oliveira
