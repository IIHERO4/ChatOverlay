from os import path
from error_helper import err_helper
import threading
import time
import sys
import re


class Listener(object):
    """Listener Object For Listening to Files
    """

    def __init__(self, fp: str):
        
        if not path.exists(fp): err_helper.showError('0x1', crash=True)

        self.path = fp
        self.listener_thread = threading.Thread(target=self.listening)
        self.last_time_modified = path.getmtime(self.path)
        self.fileSize = path.getsize(self.path)
        self.game_info = []
        self.status = 0
        self.wantClose = False
        self.newLine_callback = None
        

    def startListening(self):
        """Starts Two Threads,
        One For Listening and the Other for Checking Overall Health
        """
        
        self.listener_thread = threading.Thread(target=self.listening, daemon=True)
        self.listener_thread.start()

        # stateupdate = threading.Thread(target=self.showStatus, daemon=True)
        # stateupdate.start()

        # Main App Loop (Keeps the Client opened)
        while self.listener_thread.is_alive():
            time.sleep(1)
        else:
            print('Shutting Main Thread-1')
            sys.exit()
    

    def listening(self):
        """The Main Function Ran By the Listening Thread
        """
        # starting point (CheckPoint)
        try:
            last_index = len(re.split('\n', open(self.path, 'r').read())) - 1
            
            while True:
                
                curr_size = path.getsize(self.path)
                modified_time = path.getmtime(self.path)
                
                time.sleep(.2)
                # Latest.log Either got Archived by Minecraft or a new Instance of Minecraft Opened
                if self.fileSize > curr_size:
                    print('\033[31mDetected Change in Size')
                    print('\033[32mDid You reopen Minecraft?')
                    self.fileSize = curr_size
                    last_index = len(re.split('\n', open(self.path, 'r').read())) - 1
                    
                # MODIFIED??? must be minecraft dumping chat onto lastest.log
                if self.last_time_modified != modified_time:
                    
                    self.last_time_modified = modified_time
                    chat = open(self.path, 'r').read()
                    newChatLines = re.split('\n', chat)[last_index:] # Reads Lines From the last checkpoint
                    
                    
                    
                    curr_index = -1

                    for line in newChatLines:

                        curr_index += 1
                        # if line is not a \n or \r tag then our Line checkpoint is the current line
                        if line:
                            last_index += 1
                        
                        # Ignores ERRORS / WARNINGS focuses on chat logs
                        if '[Client thread/INFO]: [CHAT]' in line:

                            self.newLineEvent(line)
                            # TODO LOGING
        except (FileExistsError, FileNotFoundError, PermissionError, NotADirectoryError) as e:
            err_helper.showError('0x1', e, crash=True)
    
    def newLineEvent(self, line):
        """Event When New Line is Found

        Args:
            line (str): Line from latest.log
        """
        self.newLine_callback(line)

    def register_callback(self, event, func) -> bool:
        """Register a callback to an Event which is called later

        Returns:
            bool: `True` if successfull OtherWise False
        """

        if event == 'newLine':
            self.newLine_callback = func
            return True
        
        return False

    # def showStatus(self):
    #     """Opened in another Thread, 
    #        Usage: Checks the listener's Thread Health to take actions
    #     """
    #     while True:

    #         # Checks The Thread Health True if the listener thread is ded
    #         if not self.listener_thread.is_alive():
                
    #             print('\r\033[36mStatus: \033[31mNotHealthy and NotListening...., Do You Wish to Close?[y/n]', end='')
    #             ans = input()

    #             if ans.lower() == 'y':
    #                 break
    #             # Ignore That Cringe
    #             elif ans.lower() == 'n':
    #                 print('\r\033[36mLmao Im not gonna anything anyway, Hows Your Day?')
    #                 input('You =:')
    #                 print('\033[32mNice, I kinda need to go WindowsOS is shouting, \033[35mBye~~')
                    
    #                 break
        
    #     print('\033[36mThanks For Using Me, Looking Forward to work for You again \033[31m♥ ')
    #     input('Press Enter To Close')
    #     self.wantClose = True
    #     sys.exit()
