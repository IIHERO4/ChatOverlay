import colorama
import threading
import os, re, time, sys
colorama.init(autoreset=True)
print('\033[31mStarted..')
class Listener(object):
    
    def __init__(self, fp: str):

        self.path = fp
        self.listener_thread = threading.Thread(target=self.listening)
        self.last_time_modified = os.path.getmtime(self.path)
        self.fileSize = os.path.getsize(self.path)
        self.game_info = []
        self.status = 0
        self.wantClose = False
        
        
    
    # Start Listening in a Seprate Thread also Check listening Thread health
    def startListening(self):
        self.listener_thread = threading.Thread(target=self.listening, daemon=True)
        self.listener_thread.start()
        stateupdate = threading.Thread(target=self.showStatus, daemon=True)
        stateupdate.start()
        # Main App Loop (Keeps the Client opened)
        while not self.wantClose:
            pass
        else:
            print('Shutting Main Thread-1')
            sys.exit()
    
    def listening(self):
        
        last_index = len(re.split('\n', open(self.path, 'r').read())) - 1
        while True:
            
            curr_size = os.path.getsize(self.path)
            modified_time = os.path.getmtime(self.path)
            self.status = 1

            
            if self.fileSize > curr_size:
                print('\033[31mDetected Change in Size')
                print('\033[32mDid You reopen Minecraft?')
                self.fileSize = curr_size
                last_index = len(re.split('\n', open(self.path, 'r').read())) - 1
                
            
            if self.last_time_modified != modified_time:
                
                self.last_time_modified = modified_time
                chat = open(self.path, 'r').read()
                newChatLines = re.split('\n', chat)[last_index:]
                
                
                
                curr_index = -1

                for line in newChatLines:

                    curr_index += 1
                    
                    if line:
                        last_index += 1
                    if '[Client thread/INFO]: [CHAT]' in line:
                        print('\n\033[32mNew Line'+line)
                        self.last_time_modified = modified_time
                        print('\r\033[36mStatus: \033[32mHealthy and Listening....', end='')
    
    def showStatus(self):

        while True:

            if not self.listener_thread.is_alive():

                print('\r\033[36mStatus: \033[31mNotHealthy and NotListening...., Do You Wish to Close?[y/n]', end='')
                ans = input()

                if ans.lower() == 'y':
                    break
                
                elif ans.lower() == 'n':
                    print('\r\033[36mLmao Im not gonna anything anyway, Hows Your Day?')
                    input('You =:')
                    print('\033[32mNice, I kinda need to go My Manager is shouting, \033[35mBye~~')
                    
                    break
        print('\033[36mThanks For Using Me, Looking Forward to work for You again \033[31m♥ ')
        input('Press Enter To Close')
        self.wantClose = True
        sys.exit()


listener = Listener('C:/Users/alias/AppData/Roaming/.minecraft/logs/latest.log')
listener.startListening()


