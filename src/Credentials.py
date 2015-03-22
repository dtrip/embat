import traceback
from pprint import pprint
from cement.core import controller
from colorama import init, Fore, Back, Style
import json
import sys

class Credentials(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'credentials'
        description = 'Validates e-mail address'

    jcon = 'connections.json'

    # def init(self):
        # pass

    @controller.expose(hide=True, aliases=['checkEmail'])
    def checkEmail(self, email):

        # casts, trims email address
        email = str(email)
        email.strip()

        # performs basic check to ensure at least 
        # basic required symbols are present such as @ and .
        # TODO: improve email validation
        if ('@' not in email):
            return False

        if ('.' not in email):
            return False

        return email

    def checkPassword(self, pw):

        pw = str(pw)
        pw.strip()

        if (len(pw) == 0):
            return False

        return pw

    # gets the domain of the email
    # basically everything after the @
    # should be ran after validating input obvs
    def __getEmailDomain(self, email):
        domain = False
        ap = 0

        # if (self.app.pargs.verbose):
            # print("[!]\tParsing E-mail domain")

        ap = email.index('@')
        domain = email[(ap + 1):]

        if (len(domain or 0) > 0):
            print("[!]\tDetermined Domain: %s" % domain)

        return domain

    # gets email connection from connections.json
    def getConnectionInfo(self, email):

        i = []

        try:
            d = self.__getEmailDomain(email)

            # if (self.app.pargs.verbose):
            print(Fore.YELLOW + "[!]\tGetting connection info for " + d + Style.RESET_ALL)
            
            with open(Credentials.jcon) as conData:
                # print(conData.read())
                jcons = json.loads(conData.read())

                # print(jcons)

                for domain in jcons:

                    # print('checking: %s' % domain['domain'])
                    if (d.lower() == domain['domain']):

                        # if (self.app.pargs.verbose):
                            # print("[+]\tFound connection settings")

                        i = domain['imap']
                        break
                    else:
                        continue

                if (len(i) <= 0):
                    return False

                return i

        except Exception as e:
            print("[!] Error: %s" % e)
            print traceback.format_exc()

        return False
