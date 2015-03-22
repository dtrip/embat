import Credentials
import imaplib
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

            pprint(con)

            try:
                c = imaplib.IMAP4_SSL(con.host)
                c.login(email, pw)
                print("Success!")
                return True
            except Exception as e:
                print("[-] Fail: %s" % str(e))
            finally:
                if (c is not None):
                    c.logout()

        return False

