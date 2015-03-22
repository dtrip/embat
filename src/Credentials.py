import traceback
from pprint import pprint
import json
import sys

class Credentials:

    jcon = 'connections.json'

    def init(self):
        pass

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
        print("[!]\tParsing E-mail domain")

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
            print("[!]\tGetting connection info for %s from %s" % (d, Credentials.jcon))
            
            with open(Credentials.jcon) as conData:
                jcons = json.loads(conData.read())

                for domain in jcons:

                    # print('checking: %s' % domain)
                    if (d.lower() == domain.lower()):

                        # if (self.app.pargs.verbose):
                        print("[+]\tFound connection settings")

                        i = domain
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
