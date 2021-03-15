import sys
class err_helper:
    """Helps User For Common Errors
    """
    @staticmethod
    def wait_close():
        input('Press Enter To Close')
        sys.exit()

    @staticmethod
    def showError(err_code, *args, crash=False):
        """Shows Error and help prompt based the err_code

        Args:
            err_code (str): an Error identifier in the com_err dict
        """
        # Common Errors format 
        # key = err_code -> `tuple` first element is the error, second element is the help prompt
        com_err = {
            '0x0': (f'Config File Not Found {args}', 'Try Adding it to The Same Directory as the overlay'),
            '0x1': (f'Logs File is Not Found {args}', 'Manually Specify The Latest.log filepath for your client in config.json with the filename(latest.log)'),
            '0x2': (f'Failed To Connect to server {args}', ('Check Internet Connection??? or Maybe Specify the host in config.json\n'+'Also Check out the server status from our discord. If you are using the Default Server')),
            '0x3': (f'Server Forbidden To access {args}', 'Check Your Key or Contact Support @Hero#0008'),
            '0x4': (f'Server Error {args}', 'if you are using the Default Server Contact Support @Hero#0008'),
            '0x5': (f'Invalid Key {args}', 'Check Your Overlay Key if you have one, if you are using the Default Server Contact Support @Hero#0008'),
            '0x6': (f'Api Key Exhausted {args}', ('Chill! hypixel api is getting mad.')),
            '0x7': (f'Invalid config.json Format {args}', 'Try Deleting config.json and relaunching the overlay, If the issue continues Contact Support @Hero#0008'),
            '0x8': (f'You Didnt Specifiy an API key aka hypixel api {args}', 'Type /api new while the Overlay is Running \n\033[36mIf That Did not work try putting your key in config.json'),
            '0x9': (f'Invalid Hypixel Api Key {args}', 'Type /api new while the overlay is Running'),
            '0x10': (f'Invalid IGN {args}', 'Put Your Correct IGN in the config.json'),
            '0x11': (f'Key Error {args}', 'Contact Support Hero#0008, send us config.json before Trying to Delete config.json')
        }

        print(f'\033[31m{com_err[err_code][0]}\n\033[32m{com_err[err_code][1]}')

        if crash: err_helper.wait_close()

   