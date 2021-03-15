from colorama import init as colorinit
import sys
import listener
import json
import os
import defaults
from error_helper import err_helper

colorinit(autoreset=True)

class Overlay:
    """The Overlay Instance
    Args:
        configfile : ConfigFile Path with filename i.e ~/config.json
    """

    def __init__(self, configfile: str):
        # Wrtites Config.json if not found
        if not os.path.exists('./config.json'):
            with open('./config.json', 'w') as _file:
                print('\033[36mDid Not Find CONFIG.json rewriting one...')
                _file.write(json.dumps(defaults.CONFIG))
                _file.close()

        try: self.config = json.loads(open(configfile).read())
        # this handle is never gonna get triggered unless....
        except (NotADirectoryError, FileNotFoundError, FileExistsError) as e: 
            err_helper.showError('0x0', e, crash=True)

        self.Listener = listener.Listener(self.config['clients']['LunarClient']['path'])
        

        try:
            self.host = self.config['host']['name']
            self.port = self.config['host']['port']
        except KeyError as e: err_helper.showError('0x7', e, crash=True)

        self.Listener.register_callback('newLine', self.onNewLine)
        print('OVERLAY STARTED LISTENING.....')
        # TODO MAYBE CHANGE THE STARTLISTENING????
        self.Listener.startListening()
        
    
    def onNewLine(self, line):
        
        print('\n'+line)
        if 'ONLINE:' in line:
            players = line.split('ONLINE:')[1]
            players.split(',')
            print(players.split(','))

            
        

if __name__ == '__main__':
    overlay = Overlay('./config.json')