""" 
The Code Here belongs to @FatDubs (https://github.com/FatDubs)
Dubs' discord: dubs#9025

Used Under GPL v3 License?????? (maybe?)

Used From Repo:
https://github.com/FatDubs/HypixelStats/

Used From File:
https://github.com/FatDubs/HypixelStats/blob/stable/actual%20files/main.py
Class utils Line: 46 Column: 0
    Functions Used from the repo:
    def msg_raw(msg_json) -> Line: 48 Column: 5
"""
class Fatdubs:
    class utils:
        @staticmethod
        def msg_raw(msg_json) -> str:
            try:
                msg = ""
                if "text" in msg_json:
                    msg += msg_json["text"]
                if "extra" in msg_json:
                    for i in msg_json["extra"]:
                        if "text" in i:
                            msg += i["text"]
                return msg
            except Exception as e:
                print(f'\033[31m{e}')
                return msg