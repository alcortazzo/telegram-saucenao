tgBotToken = "TELEGRAM BOT TOKEN"  # bot token from t.me/BotFather
saucenao_tkn = "SAUCENAO TOKEN"  # saucenao token from saucenao.com
output_type = "2"
numres = 3
minsim = "70!"

dbmask = 34359738367  # set dbmask = "" if you want to configure bits manually
bits = {
    "index_hmags": "1",
    "index_reserved": "1",
    "index_hcg": "1",
    "index_ddbobjects": "1",
    "index_ddbsamples": "1",
    "index_pixiv": "1",
    "index_pixivhistorical": "1",
    "index_reserved": "1",
    "index_seigaillust": "1",
    "index_danbooru": "1",
    "index_drawr": "1",
    "index_nijie": "1",
    "index_yandere": "1",
    "index_animeop": "1",
    "index_reserved": "1",
    "index_shutterstock": "1",
    "index_fakku": "1",
    "index_hmisc": "1",
    "index_2dmarket": "1",
    "index_medibang": "1",
    "index_anime": "1",
    "index_hanime": "1",
    "index_movies": "1",
    "index_shows": "1",
    "index_gelbooru": "1",
    "index_konachan": "1",
    "index_sankaku": "1",
    "index_animepictures": "1",
    "index_e621": "1",
    "index_idolcomplex": "1",
    "index_bcyillust": "1",
    "index_bcycosplay": "1",
    "index_portalgraphics": "1",
    "index_da": "1",
    "index_pawoo": "1",
    "index_madokami": "1",
    "index_mangadex": "1",
}

bitmask = ""
for bit in bits:
    bitmask += bits[bit]
print(bitmask)
print(int(bitmask, 2))
