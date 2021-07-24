import config
import requests


class ApiRequest:
    def __init__(self, chat_id, file_name):
        if config.dbmask:
            self.bitmask = config.dbmask
        else:
            bitmask = ""
            for bit in config.bits:
                bitmask += config.bits[bit]
            self.bitmask = int(bitmask, 2)

    def get_result(self, files):
        url = (
            f"http://saucenao.com/search.php?output_type={config.output_type}"
            f"&numres={config.numres}&minsim={config.minsim}"
            f"&dbmask={self.bitmask}&api_key={config.saucenao_tkn}"
        )
        result = requests.post(url, files=files)
        return self.parse_result(result.json())

    def parse_result(self, result):
        # name = part = year = time = url = pic = sim = char = mat = ""
        name = part = year = time = ""
        urls = []
        sources = {
            "DeviantArt": "da_id",  # https://deviantart.com/view/515715132
            "Pixiv": "pixiv_id",  # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=4933944
            "Anidb": "anidb_aid",  # https://anidb.net/anime/15341
            "Furaffinity": "fa_id",  # https://www.furaffinity.net/view/38849036
            "Twitter": "tweet_id",  # https://twitter.com/i/web/status/742497834117668864
            "bcy": "bcy_id",  # https://bcy.net/illust/detail/55206
            "FurryNetwork": "fn_id",  # https://furrynetwork.com/artwork/103663
            "Pawoo": "pawoo_id",  # https://pawoo.net/@nez_ebi
            "seiga": "seiga_id",  # https://seiga.nicovideo.jp/seiga/im3917445
            "Sankaku": "sankaku_id",  # https://chan.sankakucomplex.com/post/show/1065498
        }

        if "results" in result and len(result["results"]) >= 1:
            for case in result["results"]:
                # name = part = year = time = url = pic = sim = char = mat = ""
                url_data = ["url", "source", "similarity"]

                if "source" in case["data"] and not name:
                    name = case["data"]["source"]
                elif "title" in case["data"] and not name:
                    name = case["data"]["title"]
                if "part" in case["data"] and not part:
                    part = case["data"]["part"]
                if "year" in case["data"] and not year:
                    year = case["data"]["year"]
                if "est_time" in case["data"] and not time:
                    time = case["data"]["est_time"]
                if "ext_urls" in case["data"]:
                    # url = case["data"]["ext_urls"][0]
                    url_data[0] = case["data"]["ext_urls"][0]
                # if "characters" in case["data"]:
                #    char = case["data"]["characters"]
                # if "material" in case["data"]:
                #    mat = case["data"]["material"]
                # if "thumbnail" in case["header"]:
                #    pic = case["header"]["thumbnail"]
                if "similarity" in case["header"]:
                    # sim = case["header"]["similarity"]
                    url_data[2] = case["header"]["similarity"]

                for source in sources:
                    if sources[source] in case["data"]:
                        url_data[1] = source

                urls.append(url_data)
            data = {
                "name": name,
                "part": part,
                "year": year,
                "time": time,
                "urls": urls,
            }
            return data
