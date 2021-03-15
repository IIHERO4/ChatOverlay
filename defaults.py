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
        'LunarClient': {'path': '..'},
        'blc': {'path': '..'},
        'minecraft': {'path': '..'},
        'pvplounge': {'path': '..'}
    },
    'Key': 'pub',
    'IGN': '[YOUR_IGN]',
    'Api_Key': '[YOUR_API_KEY]'
}
CLIENTHELP = """If Your client is not here, Make Sure To Put the path of the client joined by latest.log in config.json"""