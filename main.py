#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Made by @alcortazzo
# v0.2-beta

import io
import os
import re
import sys
import time
import json
import urllib
import config
import shutil
import codecs
import logging
import sqlite3
import requests
import eventlet
import unicodedata
from PIL import Image
from datetime import datetime
from collections import OrderedDict
from telebot import TeleBot, types, apihelper

#sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())
#sys.stderr = codecs.getwriter('utf8')(sys.stderr.detach())


print('bot starts...')

bot = TeleBot(config.tgBotToken)

'''
keyboard = types.ReplyKeyboardMarkup(True)
keyboard.row('Фото', 'Видео')
hideBoard = types.ReplyKeyboardRemove()
'''


@bot.message_handler(commands=['start'])
def cmd_start(message):
    '''def AddUserDB(message):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Add new user to DB
        # if data exist user has banned bot
        sql_select = f'SELECT * FROM users where chatid={message.chat.id}'
        sql_insert = f"INSERT INTO users VALUES ({message.chat.id}, '{''}', '{''}', '{''}', {0})"
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if data is None:
            cursor.execute(sql_insert)
            conn.commit()
        conn.close()'''

    def SendMessages(message):
        bot.send_message(message.chat.id,
                         # request for tgChannel value
                         # 'Я ищу сорс аниме тайтлов по фото или видео. Что ты хочешь мне отправить?', reply_markup=keyboard)
                         'Я ищу сорс аниме тайтлов по фото или видео. Что ты хочешь мне отправить?')
        # bot.send_photo(message.chat.id, open('img/img_permissions_white.png', 'rb'),
        #                caption='И не забудь сделать меня администратором канала с разрешением отправлять в него сообщения!')

    def SetState(message):
        config.set_state(message.chat.id, config.States.S_REQUEST_Media.value)

    # AddUserDB(message)
    SendMessages(message)
    SetState(message)


@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    '''def ResetUserData(message):
        # Delete data for user from DB
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # cursor.fetchone()
        cursor.execute('DELETE FROM users WHERE chatid = {}'.format(message.chat.id))
        cursor.execute("INSERT INTO users VALUES ({}, '{}', '{}', '{}', {})".format(message.chat.id, '', '', '', 0))
        conn.commit()
        conn.close()'''

    def SendMessages(message):
        bot.send_message(message.chat.id,
                         'Снова здравствуй!\n\nТвои данные были удалены из базы данных, поскольку ты перезапустил бота.')
        bot.send_message(message.chat.id,
                         # 'Привет. Я ищу сорс аниме тайтлов по фото или видео. Что ты хочешь мне отправить?', reply_markup=hideBoard)
                         'Привет. Я ищу сорс аниме тайтлов по фото или видео. Что ты хочешь мне отправить?')
        # bot.send_photo(message.chat.id, open('img/img_permissions_white.png', 'rb'),
        #                caption='И не забудь сделать меня администратором канала с разрешением отправлять в него сообщения!')

    def SetState(message):
        config.set_state(message.chat.id, config.States.S_REQUEST_Media.value)

    # ResetUserData(message)
    SendMessages(message)
    SetState(message)


'''
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'фото':
        bot.send_message(message.chat.id, 'Хорошо. Кидай фотку')
'''


@bot.message_handler(content_types=['photo'])
def work_with_photo(message):
    def getPhoto(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        if not os.path.isdir('media'):
            os.mkdir('media')

        if not os.path.isdir(f'media/{message.chat.id}'):
            os.mkdir(f'media/{message.chat.id}')

        with open(f"media/{message.chat.id}/image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        getData(message)

    def getData(message):
        extensions = {".jpg", ".jpeg", ".png"}
        thumbSize = (250, 250)

        for root, _, files in os.walk(f'./media/{message.chat.id}', topdown=False):
            for f in files:
                fname = os.path.join(root, f)
                for ext in extensions:
                    if fname.lower().endswith(ext):
                        print(fname)
                        image = Image.open(fname)
                        image = image.convert('RGB')
                        image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
                        imageData = io.BytesIO()
                        image.save(imageData, format='PNG')

                        url = f'http://saucenao.com/search.php?output_type={config.output_type}&numres={config.numres}&minsim={config.minsim}&dbmask={str(getBitmask())}&api_key={config.api_key}'
                        files = {'file': ("image.png", imageData.getvalue())}
                        imageData.close()

                        processResults = True
                        r = requests.post(url, files=files)
                        print(r.json())
                        sendResults(message, r.json())

    def sendResults(message, result):
        '''
        i = 1
        while i <= config.numres:
            result_case = result['results'][i - 1]
            result_name = result['results'][i - 1]['data']['title']
            result_picture = result['results'][i - 1]['header']['thumbnail']
            result_similarity = result['results'][i - 1]['header']['similarity']

            bot.send_message(message.chat.id, f'<a href="{result_picture}"> </a>Result ({i} of {config.numres}): {result_name}\n' +
                             f'Similarity = {result_similarity}%', parse_mode='HTML')
            i = i + 1
        '''
        i = 1
        while i <= config.numres:
            try:
                result_case = result['results'][i - 1]
            except:
                result_case = ''
                
            try:
                result_name = result['results'][i - 1]['data']['source']
            except:
                try:
                    result_name = result['results'][i - 1]['data']['title']
                except:
                    result_name = ''
                
            try:
                result_part = result['results'][i - 1]['data']['part']
            except:
                result_part = ''
                
            try:
                result_year = result['results'][i - 1]['data']['year']
            except:
                result_year = ''
                
            try:
                result_time = result['results'][i - 1]['data']['est_time']
            except:
                result_time = ''
                
            try:
                result_url = result['results'][i - 1]['data']['ext_urls'][0]
            except:
                result_url = ''
                
            try:
                result_picture = result['results'][i - 1]['header']['thumbnail']
            except:
                result_picture = ''
                
            try:
                result_similarity = result['results'][i - 1]['header']['similarity']
            except:
                result_similarity = ''
                
            try:
                message_text = ''
                if result_name != '':
                    message_text = message_text + f'<b>{result_name}</b>\n\n'
                if result_part != '':
                    message_text = message_text + f'<b>Part:</b> {result_part}\n'
                if result_year != '':
                    message_text = message_text + f'<b>Year:</b> {result_year}\n'
                if result_time != '':
                    message_text = message_text + f'<b>Time:</b> {result_time}\n\n'
                if result_url != '':
                    if 'anidb' in result_url.lower():
                        message_text = message_text + f'<a href="{result_url}"><b>Anidb</b></a>'
                    else:
                        message_text = message_text + f'<a href="{result_url}"><b>url1</b></a>'
            except:
                x = 0
            
            try:
                bot.send_message(message.chat.id, message_text, parse_mode='HTML')
            except:
                x = 0
            
            i = i + 1
        clearTemp(message)

    def clearTemp(message):
        if os.path.isdir(f'media/{message.chat.id}'):
            shutil.rmtree(f'media/{message.chat.id}')

    getPhoto(message)


def getBitmask():
    # enable or disable indexes
    index_hmags = '1'
    index_reserved = '1'
    index_hcg = '1'
    index_ddbobjects = '1'
    index_ddbsamples = '1'
    index_pixiv = '1'
    index_pixivhistorical = '1'
    index_reserved = '1'
    index_seigaillust = '1'
    index_danbooru = '1'
    index_drawr = '1'
    index_nijie = '1'
    index_yandere = '1'
    index_animeop = '1'
    index_reserved = '1'
    index_shutterstock = '1'
    index_fakku = '1'
    index_hmisc = '1'
    index_2dmarket = '1'
    index_medibang = '1'
    index_anime = '1'
    index_hanime = '1'
    index_movies = '1'
    index_shows = '1'
    index_gelbooru = '1'
    index_konachan = '1'
    index_sankaku = '1'
    index_animepictures = '1'
    index_e621 = '1'
    index_idolcomplex = '1'
    index_bcyillust = '1'
    index_bcycosplay = '1'
    index_portalgraphics = '1'
    index_da = '1'
    index_pawoo = '1'
    index_madokami = '1'
    index_mangadex = '1'

    db_bitmask = int(index_mangadex+index_madokami+index_pawoo+index_da+index_portalgraphics+index_bcycosplay+index_bcyillust+index_idolcomplex+index_e621+index_animepictures+index_sankaku+index_konachan+index_gelbooru+index_shows+index_movies+index_hanime+index_anime+index_medibang +
                     index_2dmarket+index_hmisc+index_fakku+index_shutterstock+index_reserved+index_animeop+index_yandere+index_nijie+index_drawr+index_danbooru+index_seigaillust+index_anime+index_pixivhistorical+index_pixiv+index_ddbsamples+index_ddbobjects+index_hcg+index_hanime+index_hmags, 2)
    return db_bitmask


def infinity_polling_start():
    bot.infinity_polling()


def create_table(type_of_table):
    """def create_table_db():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS users (chatid INTEGER, tgChannel TEXT, vkDomain TEXT, vkToken TEXT, last_id INTEGER)''')
        conn.commit()
        conn.close()"""

    def create_table_states():
        conn = sqlite3.connect('states.db')
        cursor = conn.cursor()
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS states (user_id INTEGER, state INTEGER)''')
        conn.commit()
        conn.close()

    # if type_of_table == 'db':
    #    create_table_db()
    if type_of_table == 'states':
        create_table_states()


if __name__ == '__main__':
    # if not os.path.isfile('database.db'):
    #    create_table('db')
    if not os.path.isfile('states.db'):
        create_table('states')
    infinity_polling_start()
