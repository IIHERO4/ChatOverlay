import os
"""Default config, paths maybe??
"""
CONFIG = {
    'host': {
        'name': 'localhost', 
        'port': 5000,
        'routes': {
            'GET_players': 'localhost/players',
            'GET_status': 'localhost/status'
        }
    },
    'clients': {
        'LunarClient': {'path': f'{os.path.expanduser("~")+"/.lunarclient/offline/1.8/logs/latest.log"}'},
        'blc': {'path': f'{os.getenv("APPDATA") + "/.minecraft/logs/blclient/minecraft/latest.log"}'},
        'minecraft': {'path': f'{os.getenv("APPDATA") + "/.minecraft/logs/latest.log"}'},
        'pvplounge': {'path': f'{os.getenv("APPDATA") + "/.pvplounge/logs/latest.log"}'}
    },
    'Key': 'pub',
    'IGN': '[YOUR_IGN]',
    'Api_Key': '[YOUR_API_KEY]',
    'whitelist': [
        '[YOUR_TEAMMATE]'
    ],
    'nicks': [
        '[YOUR_NICK]'
    ]

}
CLIENTHELP = """If Your client is not here, Make Sure To Put the path of the client joined by latest.log in config.json"""

EDITPROMPT = {
    'nick':'\033[32mType Out Your Nicks\n\
            \033[31mWhen You are Finished Press CTRL+C To Resume and Save \n\
            \033[30mYou Can INF Numbers of NICKS, not so much to work smoothly',
    'teammate': '\033[32mInterrupted, Type Your Teammates one at a time\n\
                \033[31mWhen You are Finished Press CTRL+C To Resume and Save\n\
                \033[30mYou Can INF Numbers of teammates'
}

HEADER = '\033[31m'+r""" 
    
 ▒█████   ██▒   █▓▓█████  ██▀███   ██▓    ▄▄▄     ▓██   ██▓
▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒▓██▒   ▒████▄    ▒██  ██▒
▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒▒██░   ▒██  ▀█▄   ▒██ ██░
▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ▒██░   ░██▄▄▄▄██  ░ ▐██▓░
░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒░██████▒▓█   ▓██▒ ░ ██▒▓░
░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░▓  ░▒▒   ▓▒█░  ██▒▒▒ 
  ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░░ ░ ▒  ░ ▒   ▒▒ ░▓██ ░▒░ 
░ ░ ░ ▒       ░░     ░     ░░   ░   ░ ░    ░   ▒   ▒ ▒ ░░  
    ░ ░        ░     ░  ░   ░         ░  ░     ░  ░░ ░     
              ░                                    ░ ░     

    
    
    """