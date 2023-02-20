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

#APOS BAIXAR O BANCO DE DADOS E COLOCAR NA MESMA PASTA DO ARQUIVO


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

Para configurar o bot, é necessário fornecer o ID do chat e o token da API do bot do Telegram.
Essas informações são passadas como argumentos ao executar o script.

# Exemplo de uso:

python bot.py --chat_id <chat_id> --bot_token <bot_token>

# Funcionamento do Bot

O bot funciona monitorando as mensagens enviadas no chat e verificando se elas contêm palavras impróprias.
Se uma mensagem for considerada inapropriada, o usuário que enviou a mensagem será silenciado por 24 horas.
Se o mesmo usuário for pego enviando mensagens inapropriadas novamente dentro de um período de 30 dias, ele será banido do chat.

# Comandos do Bot

Além do monitoramento de mensagens, o bot também fornece alguns comandos para gerenciar a lista de palavras impróprias.

# Os comandos disponíveis são:

/badwords: exibe a lista de palavras impróprias monitoradas pelo bot.

/addwords <palavra1> <palavra2> ...: adiciona uma ou mais palavras à lista de palavras impróprias monitoradas pelo bot.

/removewords <palavra1> <palavra2> ...: remove uma ou mais palavras da lista de palavras impróprias monitoradas pelo bot.

# Considerações finais e Política de Isenção de Responsabilidade e Direitos de Uso
  
Este bot foi desenvolvido com o objetivo de ajudar a monitorar e restringir mensagens inapropriadas em chats do Telegram.
Use-o com responsabilidade e lembre-se de sempre respeitar as regras e a privacidade dos usuários do chat.

Este software (denominado "Código") foi desenvolvido por Fernando Martins de Oliveira.
O objetivo deste Código é fornecer um assistente de moderação para chats do Telegram.

Ao usar este Código, você concorda em seguir as seguintes condições:

Isenção de Responsabilidade:
O Criador deste Código não será responsável por quaisquer danos ou perdas resultantes do uso deste Código.
Além disso,o Criador não garante a integridade, precisão ou disponibilidadee ou funcionamento correto deste Código.

Direitos de Uso:
Este Código está disponível para uso pessoal ou comercial, desde que sejam seguidas as condições de uso estabelecidas pelo Telegram.
O Código não pode ser vendido, alugado ou distribuído sem a permissão prévia do Criador.

Modificações:
Você pode modificar este Código conforme suas necessidades, desde que sigas as condições de uso estabelecidas pelo Telegram.
No entanto, o Criador não será responsável por quaisquer danos ou perdas resultantes dessas modificações.

Este Código é fornecido "como está", sem garantias expressas ou implícitas.
O Criador não será responsável por quaisquer danos ou perdas resultantes do uso deste Código.

Se você tiver alguma dúvida sobre esta política de isenção de responsabilidade e direitos de uso, entre em contato com o Criador.

###############################################################################################################
## _______   ______    _______ ## Nos ajude a continuar desenvolvendo e faça uma doação do valor de R$ 10,00 ##
##|       \ /  __  \  |   ____|############################## NO PIX DE CELULAR ABAIXO ########################
##|  .--.  |  |  |  | |  |__   ################################################################################
##|  |  |  |  |  |  | |   __|  ###################(34) 99132-9872 - Fernando Martins de Oliveira###############
##|  '--'  |  `--'  | |  |____ ################################################################################
##|_______/ \______/  |_______|################### desenvolvido por Fernando Martins de Oliveira ##############
###############################################################################################################
