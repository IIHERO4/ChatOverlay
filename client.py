from colorama import init as colorinit
from os import path
import sys
import listener
import json
import re
import defaults
import threading
import requests
from error_helper import err_helper

colorinit(autoreset=True)

class Overlay:
    """The Overlay Instance
    Args:
        configfile : ConfigFile Path with filename i.e ~/config.json
    """

    def __init__(self, configfile: str):

        # Wrtites Config.json if not found
        if not path.exists(configfile):
            self.saveConfig(defaults.CONFIG, configfile)

        self.config = self.loadConfig(configfile)
        self.client = self.choosen_client()
        
        
        self.Listener = listener.Listener(self.config['clients']['LunarClient']['path'])
        
        try:
            self.host = self.config['host']['name']
            self.port = self.config['host']['port']
            self.route = self.config['host']['routes']
            
        except KeyError as e: err_helper.showError('0x7', e, crash=True)

        self.Listener_thread = threading.Thread(target=lambda: self.Listener.startListening(), daemon=True)

        
    # TODO ADD LOGGING + -D cmdline
    def run(self, debug=False):
        # TODO PING SERVER IF PUB, CHECK IF VALIDE IGN, API_KEY, KEY
        self.validateConfig()
        self.Listener.register_callback('newLine', self.onNewLine)
        self.Listener_thread.start()
        

        print('OVERLAY STARTED LISTENING.....')
        # TODO MAYBE CHANGE THE STARTLISTENING????
        
    
    def onNewLine(self, line):
        
        print('\n'+line)
        if 'ONLINE:' in line:
            # TODO SEND PLAYER TO SERVER
            pass
    
    def validateConfig(self):
        while True:
            if self.config.get('IGN') == '[YOUR_IGN]':
                print('\033[32mHey, Before We start We need Answers For your config')
                print('\033[36mPut Your \033[35mIGN So We save your api key from death ==> ', end='')
                self.config['IGN'] = input()

            elif self.config.get('Api_Key') == '[YOUR_API_KEY]':
                err_helper.showError('0x8', crash=False)
                self.config['Api_Key'] = 'PENDING'
                self.saveConfig(self.config, './config.json')
                self.config = self.loadConfig('./config.json')
                print('Wait Till Asked to Type /api new')
                break

            else:
                self.check_api
                break
        
            

    def check_api(self):
        try:
            hyinfo = requests.get(f'https://api.hypixel.net/player?key={self.config["API_KEY"]}&name={self.config["IGN"]}')
            hyinfo_data = hyinfo.json()
            if hyinfo.status_code in range(200, 299):
                if not hyinfo_data.get('player'):
                    err_helper.showError('0x10', crash=False)
            else:
                if 'recently' in hyinfo_data.get('cause')and hyinfo.status_code == 429:
                    print
                    hyinfo = requests.get(f'https://api.sk1er.club/{self.config["IGN"]}')
                    
                    if hyinfo.status_code not in range(200, 299):
                        err_helper.showError('0x10')
                    

        except KeyError as e: err_helper.showError('0x7', e)
    
    def choosen_client(self):

        
        try:
            while True:
                valide_clients = []
                prompt = ''
                opts = 1
                for client, clpath in self.config['clients'].items():
                    print(clpath)
                    if path.exists(clpath['path']) and 'latest.log' in clpath['path']:
                        valide_clients.append({str(opts): client})
                        opts += 1
                
                for client in valide_clients:
                    for opts, client_ in client.items():
                        prompt += f'\n{opts}) '+client_
                if prompt:
                    print(f'\033[32mSelect Your Client, \n\033[30m{defaults.CLIENTHELP}',
                        prompt, end='')
                else:
                    print(f'\033[31mCouldn\'t Find a Single Valid Client path\n\033[30m{defaults.CLIENTHELP}')
                    err_helper.wait_close()
                               
                choice = input()
                
                for client in valide_clients:
                    if client.get(choice):
                        return client[choice]
                
        except KeyError as e: err_helper.showError('0x7', e, crash=True) 

    def saveConfig(self, json_, fp):
        with open(fp, 'w+') as _file:

                # TODO LOGGING
                _file.write(json.dumps(json_, indent=4))
                _file.close()
    
    def fixConfig(self, config_str, fp):
        # TODO FIXING LOGGING
        print('FIXING JSON')
        self.saveConfig(json.loads(re.sub(r'\\', '/', config_str)), fp)
    
    def loadConfig(self, fp: str) -> dict:
        input('>>>')
        raw_config = open(fp, 'r').read()
        try: return json.loads(raw_config)

        # this handle is never gonna get triggered unless....
        except (NotADirectoryError, FileNotFoundError, FileExistsError) as e: 
            err_helper.showError('0x0', e, crash=True)
        
        except json.JSONDecodeError: 
            self.fixConfig(raw_config, fp)
            try: return json.loads(open(fp, 'r').read())
            except json.JSONDecodeError: err_helper.showError('0x7', crash=True)
        

if __name__ == '__main__':
    overlay = Overlay('./config.json')