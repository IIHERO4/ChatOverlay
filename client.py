print('STARTING IMPORTS...')
from colorama import init as colorinit
from error_helper import err_helper
from os import path, mkdir
from logging.handlers import TimedRotatingFileHandler
import sys
import listener
import json
import re
import defaults
import threading
import time
import requests
import logging

colorinit(autoreset=True)

class Overlay:
    """The Overlay Instance
    Args:
        configfile : ConfigFile Path with filename i.e ~/config.json
    """

    def __init__(self, configfile: str):

        # Wrtites Config.json if not found
        logging.info('\033[32mFINISHED IMPORTS')
        logging.info('\033[31mINITIALIZING OVERLAY')

        if not path.exists(configfile):
            logging.warning('\033[33mCouldn\'t Find Config.json, Rewriting one')
            self.saveConfig(defaults.CONFIG, configfile)

        self.config = self.loadConfig(configfile) 
        self.client = self.choosen_client()

        self.Listener = listener.Listener(self.config['clients'][self.client]['path'])
        
        try:
            self.host = self.config['host']['name']
            self.port = self.config['host']['port']
            self.route = self.config['host']['routes']
            self.api = self.config['Api_Key']
            
        except KeyError as e: err_helper.showError('0x7', e, crash=True)

        self.Listener_thread = threading.Thread(target=lambda: self.Listener.startListening(), daemon=True)

        
    # TODO ADD LOGGING + -D cmdline
    def run(self, debug=False):
        # TODO PING SERVER IF PUB, CHECK IF VALIDE IGN, API_KEY, KEY
        self.validateConfig()
        self.Listener.register_callback('newLine', self.onNewLine)
        self.Listener_thread.start()
        if self.config['Api_Key'] == 'PENDING':
            self.wait_api()
        self.check_api()
        logging.info('\033[32mOVERLAY STARTED')

        while self.Listener_thread.is_alive():
            time.sleep(1)
        # TODO MAYBE CHANGE THE STARTLISTENING????
        
    
    def onNewLine(self, line):
        
        print('\n'+line)
        if 'ONLINE:' in line:
            # TODO SEND PLAYER TO SERVER
            pass
        if 'Your new API key is' in line:
            self.api = line[len('[02:39:43] [Client thread/INFO]: [CHAT] Your new API key is'):]
            logging.info(f'\033[36mNew Api Key detected {self.api}')
            self.config['Api_Key'] = self.api
            self.saveConfig(self.config, './config.json')
            self.config = self.loadConfig('./config.json')
    
    def validateConfig(self):
        while True:
            if self.config.get('IGN') == '[YOUR_IGN]':

                logging.warning('\033[33mNo IGN was set')

                print('\033[32mHey, Before We start We need Answers For your config')
                print('\033[36mPut Your \033[35mIGN So We save your api key from death ==> ', end='')
                self.config['IGN'] = input()

                logging.debug(f'\033[31mAn attempt to change IGN was made {self.config["IGN"]}')

            elif self.config.get('Api_Key') == '[YOUR_API_KEY]':

                logging.warning('\033[33mNo Api Key Was Set')

                err_helper.showError('0x8', crash=False)
                self.config['Api_Key'] = 'PENDING'
                self.saveConfig(self.config, './config.json')
                self.config = self.loadConfig('./config.json')
                self.api = self.config['Api_Key']
                print('Wait Till Asked to Type /api new')
                break
            else: break

    def wait_api(self):
        print('\033[32mType /api new')
        logging.debug('Waiting For /api new')
        while self.api == 'PENDING':
            time.sleep(1)
            pass
        self.api = self.config['Api_Key']
        logging.debug(f'\033[31mAn attempt to change Api_Key was made {self.config["Api_Key"]}')
        self.check_api()

    def check_api(self):
        try:
            logging.debug(f'Running Checks On the Api Key {self.config["Api_Key"]}')

            hyinfo = requests.get(f'https://api.hypixel.net/player?key={self.config["Api_Key"].strip()}&name={self.config["IGN"].strip()}')
            hyinfo_data = hyinfo.json()
            logging.debug(f'API Check Results: {hyinfo.status_code} {hyinfo.json()} ')
            if hyinfo.status_code == 403:
                err_helper.showError('0x9', f'Follow Instructions, {self.api}')
                
                logging.debug(f'Invalid Key {hyinfo} {hyinfo.json()}')
                logging.error('Api Key Invalid')
                self.api = 'PENDING'
                self.config['Api_Key'] = self.api
                self.saveConfig(self.config, './config.json')
                self.config = self.loadConfig('./config.json')
                return self.wait_api()
                
                
            if hyinfo.status_code in range(200, 299):
                if not hyinfo_data.get('player'):
                    err_helper.showError('0x10', hyinfo.status_code, crash=False)
                logging.info(f'\033[32mSuccessfully Checked')
                self.saveConfig(self.config, './config.json')
                
            else:
                if 'recently' in hyinfo_data.get('cause') and hyinfo.status_code == 429:
                    logging.error('\033[31mFailed To check IGN by hypixel retrying with sk1er')
                    hyinfo = requests.get(f'https://api.sk1er.club/{self.config["IGN"]}')
                    
                    if hyinfo.status_code not in range(200, 299):
                        err_helper.showError('0x10', hyinfo.status_code)
                    
            
        except KeyError as e: err_helper.showError('0x7', e)
    
    def choosen_client(self):

        
        try:
            while True:
                valide_clients = []
                prompt = ''
                opts = 1
                for client, clpath in self.config['clients'].items():
                    
                    if path.exists(clpath['path']) and 'latest.log' in clpath['path']:
                        valide_clients.append({str(opts): client})
                        opts += 1
                
                for client in valide_clients:
                    for opts, client_ in client.items():

                        prompt += f'\n{opts}) '+client_
                
                if prompt:
                    logging.debug(f'Clients: {valide_clients}')
                    print(f'\033[32mSelect Your Client, \n\033[30m{defaults.CLIENTHELP}',
                        prompt, end='\n')
                else:
                    logging.warning(f'\033[31mCouldn\'t Find a Valid Client Path paths, crashing...')
                    logging.debug(f'Couldn\'t Find a Valid LOGS PATH : {self.config["clients"]}')
                    print(f'\033[31mCouldn\'t Find a Single Valid Client path\n\033[30m{defaults.CLIENTHELP}')
                    err_helper.showError('0x1', crash=True)
                               
                choice = input()
                
                for client in valide_clients:
                    if client.get(choice):
                        logging.debug(f'{choice}')
                        return client[choice]
                
        except KeyError as e: err_helper.showError('0x7', e, crash=True) 

    def saveConfig(self, json_, fp):
        logging.debug(f'\033[36mUpdating config.json {json_}')
        with open(fp, 'w+') as _file:

                # TODO LOGGING
                _file.write(json.dumps(json_, indent=4))
                _file.close()
    
    def fixConfig(self, config_str, fp):
        # TODO FIXING LOGGING
        fixes = re.sub(r'\\', '/', config_str)
        logging.warning(f'Applied Fixes to config ')
        logging.debug(f'Applied Fixes to config {fixes}')
        self.saveConfig(json.loads(fixes), fp)
    
    def loadConfig(self, fp: str) -> dict:
        
        raw_config = open(fp, 'r').read()
        logging.debug('Loading Config')
        try: return json.loads(raw_config)

        # this handle is never gonna get triggered unless....
        except (NotADirectoryError, FileNotFoundError, FileExistsError) as e: 
            err_helper.showError('0x0', e, crash=True)
        
        except json.JSONDecodeError: 
            self.fixConfig(raw_config, fp)
            try: return json.loads(open(fp, 'r').read())
            except json.JSONDecodeError: err_helper.showError('0x7', crash=True)
        

if __name__ == '__main__':
    if not path.exists('./logs'): mkdir('./logs')
    console_stdout = logging.StreamHandler()
    console_stdout.setLevel(logging.INFO)
    log_file = logging.handlers.TimedRotatingFileHandler("./logs/overlay.log", when="midnight", interval=1)
    log_file.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt= '%I:%M:%S %p',
        handlers=[
            console_stdout, 
            log_file
        ]

    )
    
    overlay = Overlay('./config.json')
    overlay.run()
