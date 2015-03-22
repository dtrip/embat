import Credentials
import imaplib
import socket
from pprint import pprint

class Imap:
    creds = Credentials.Credentials()


    def init(self):
        pass

    def checkAccount(self, email, pw):

        con = Imap.creds.getConnectionInfo(email)

        if (con == False):
            print("[!]\tNo connection data in connections.json!")
        else:
            print("[!]\tTesting Imap connection ...")

            c = None

            # print(con['host'])

            try:
                c = imaplib.IMAP4_SSL(con['host'])

                #5 second timeout
                socket.setdefaulttimeout(5)

                c.login(email, pw)
                print("[+]\tSuccess!")
                return True
            except Exception as e:
                print("[-]\tFail: %s" % str(e))
            finally:
                if (c is not None):
                    c.logout()

        return False

