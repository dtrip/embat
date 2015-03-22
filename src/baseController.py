from cement.core import controller
from cement.utils.misc import init_defaults
from colorama import init, Fore, Back, Style
from time import sleep
import csv
import Credentials
import Imap

defaults = init_defaults('EmBat')

defaults['EmBat']['imap'] = True
defaults['EmBat']['pop'] = False


class baseController(controller.CementBaseController):

    imap = Imap.Imap()

    class Meta:
        interface = controller.IController
        label = 'base'
        config_defaults = defaults
        description = 'Email batch credential verifer'


        arguments = [
                # TODO Verify STMP
                (['-c', '--csv'], dict(action='store', help='CSV file containing email login and password')),
                (['-v', '--verbose'], dict(action='store_true', help='Verbose Output')),
                (['-p', '--pop'], dict(action='store_true', help='force connection to POP3 (default: False)')),
                (['-i', '--imap'], dict(action='store_true', help='force connection to IMAP (default: True)'))
                ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        if (self.app.pargs.csv):
            self.__parseCSV()

        return True

    # parses CSV file
    def __parseCSV(self):

        c = None

        cred = Credentials.Credentials()

        try:

            lines = 0
            c = open(self.app.pargs.csv)
            ch = csv.reader(c)

            # lines = int(len(list(ch)))

            if (self.app.pargs.verbose):
                print("[!] Total Lines: %u" % lines)

            #default email/password columns
            emailCol = 0
            passwdCol = 1
            hasHeader = True

            # gets some basic info about file to properly parse file
            firstLineHeader = raw_input("[?] Does the first row contain column titles? [Y/n]: ")

            if (firstLineHeader.upper() == 'N'):
                hasHeader = False
                lines -= 1

            emailCol = int(raw_input("[?] Enter column number of email login. 0 equals column A. [0]: ") or emailCol)
            passwdCol =  int(raw_input("[?] Enter column number of passwords [1]: ") or passwdCol)

            for k,r in enumerate(ch):

                if (k == 0 and hasHeader == True):
                    if (self.app.pargs.verbose):
                        print("[!] Skipping header row")
                    continue

                email = cred.checkEmail(r[emailCol])
                pw = cred.checkPassword(r[passwdCol])

                if (email == False):
                    print("[-] Not a valid email address... skipping.")
                    continue

                if (pw == False):
                    print(Fore.YELLOW + "[-] Password is empty... skipping." + Style.RESET_ALL)
                    continue

                print("\n" + Style.BRIGHT + "[" + str(k + 1) + "] Checking: " + email + ":" +  pw + Style.RESET_ALL)

                if (self.app.pargs.imap):
                    validImap = self.imap.checkAccount(email, pw)

                if (self.app.pargs.pop):
                    print("POP not currently supported")

                sleep(1)

        except ValueError:
            print("Invalid Integer")
        except Exception as e:
            print("[!] Error parsing CSV File: %s" % str(e))
        finally:
            c.close()

        return True
