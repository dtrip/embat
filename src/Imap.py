import Credentials
import traceback
import imaplib
import socket
from colorama import init, Fore, Back, Style
from pprint import pprint

class Imap:
    creds = Credentials.Credentials()

    def init(self):
        pass

    def checkAccount(self, email, pw):

        con = Imap.creds.getConnectionInfo(email)

        if (con == False):
            print(Fore.RED + "[!]\tNo connection data in connections.json!" + Style.RESET_ALL)
        else:
            print("[!]\tTesting Imap connection ...")

            c = None

            # print(con['host'])

            try:
                c = imaplib.IMAP4_SSL(con['host'])

                #5 second timeout
                socket.setdefaulttimeout(5)

                c.login(email, pw)
                print(Style.BRIGHT + Fore.GREEN + "[+]\tSuccess!" + Style.RESET_ALL)
                return True
            except Exception as e:
                print(Style.BRIGHT + Fore.RED + "[-]\tFail: " + str(e) + Style.RESET_ALL)
                # print traceback.format_exc()
            finally:
                if (c is not None):
                    c.logout()

        return False

