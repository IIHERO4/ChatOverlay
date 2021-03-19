from fatdubs import Fatdubs
from minecraft import authentication as mineauth
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import serverbound, clientbound
import json


class Bot:

    def __init__(self, email: str, password: str, onMsg=None):
        """Init a Bot obj with email and password

        Args:
            email (str): mojang credentials [email]
            password (str): mojang credentials [password]
            onMsg (function): Function will be called on new message
        """

        self.email = email
        self.password = password
        self.authToken = mineauth.AuthenticationToken()
        self.connection = None
        self.is_connected = False
        self.onMsg = onMsg


    def connect(self, ip: str, port: int=25565) -> bool:
        """Connects To the ip specified with the account credentials

        Args:
            ip (str): mcServer IP

        Returns:
            bool: `True` if Connected OtherWise `False`
        """
        if self.is_auth:
            try: 
                self.connection = Connection(ip, port, auth_token=self.authToken)
                self.connection.connect()
                # self.connection.register_packet_listener(self.chat, clientbound.play.ChatMessagePacket)
                self.is_connected = True
            except (YggdrasilError, Exception): return False
            
            return True
        
        return False
    
        
    def send_message(self, message):
        """Sends a Message Packet to the Server

        Args:
            message (str): Message to be sent in Chat
        """
        
        msgPacket = serverbound.play.ChatPacket()
        msgPacket.message = message
        self.connection.write_packet(msgPacket)

    def authenticate(self) -> bool:
        """Authenticate with mojang


        Returns:
            bool: `True` if successfull OtherWise `False`
        """
        try:
            self.authToken.authenticate(self.email, self.password)
            print(f'\033[32mSuccessfully authenticated with email {self.email}')
            return True
        except YggdrasilError:
            return False
    
    @property
    def is_auth(self) -> bool:
        """Validate session

        Returns:
            bool: `True` if Valid Otherwise False
        """
        try: self.authToken.validate()
        except (YggdrasilError, ValueError): return False
        return True
    
    def disconnect(self):
        """Disconnects From Connected Servers
        """
        self.is_connected = False
        self.connection.disconnect(True)
        print('Disconnected from the Connected server')

    def chat(self, chat_packet):

        msg = Fatdubs.utils.msg_raw(json.loads(chat_packet.json_data))
        self.onMsg(msg)
        
        

