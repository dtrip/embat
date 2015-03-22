from cement.core import handler,controller, backend, handler
from cement.utils.misc import init_defaults
from colorama import init, Fore, Back, Style
from pprint import pprint
from time import sleep
import csv
import traceback
import Credentials
import Imap
import Tor
import Output

class baseController(controller.CementBaseController):

    imap = Imap.Imap()
    tor = Tor.Tor()

    class Meta:
        interface = controller.IController
        label = 'base'
        # config_defaults = defaults
        description = 'Email batch credential verifer'

        # default values
        config_defaults = dict(
                debug = False,
                imap = 'True',
                pop = False,
                tor = False,
                torport = 7000,
                delay = '0.5'
                )

        arguments = [
                # TODO Verify STMP
                (['-c', '--csv'], dict(action='store', help='CSV file containing email login and password')),
                (['-o', '--output'], dict(action='store', help='Output CSV file of successful logins')),
                (['-v', '--verbose'], dict(action='store_true', help='Verbose Output')),
                (['-p', '--pop'], dict(action='store_true', help='force connection to POP3 (default: False)')),
                (['-i', '--imap'], dict(action='store_true', help='force connection to IMAP (default: True)')),
                (['-d', '--delay'], dict(action='store', help='Delay in seconds after login attempt (default: 0.5)')),
                (['-t', '--tor'], dict(action='store_true', help='Connect to Tor? (default: False)')),
                (['-z', '--torport'], dict(action='store', help='Tor port (default: 7000)'))
                ]

        epilog = "Sample Usage: EmBat --csv ~/emails.csv -i -o ~/results.csv -t -z 7000"



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
            pprint(self.app.pargs)

            # if tor flag isset will attempt to connect
            if (self.app.pargs.tor):
                self.tor.connect(self.app.pargs.torport);

            lines = 0
            c = open(self.app.pargs.csv)
            ch = csv.reader(c)

            # lines = int(len(list(ch)))

            # if (self.app.pargs.verbose):
                # print("[!] Total Lines: %u" % lines)

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

            o = Output.Output();
            if (self.app.pargs.output is not None):
                # print("OUTPUT:" + self.app.pargs.output)
                oFile = o.createFile(self.app.pargs.output)

            for k,r in enumerate(ch):

                if (k == 0 and hasHeader == True):
                    if (self.app.pargs.verbose):
                        print("\n[!] Skipping header row")
                    continue

                email = cred.checkEmail(r[emailCol])
                pw = cred.checkPassword(r[passwdCol])

                if (email == False):
                    print("[-] Not a valid email address... skipping.")
                    continue

                if (pw == False):
                    print(Fore.RED + "[-] " + email + ": Password is empty... skipping." + Style.RESET_ALL + "\n")
                    continue

                print(Style.BRIGHT + "[" + str(k + 1) + "] Checking: " + email + ":" +  pw + Style.RESET_ALL)

                if (self.app.pargs.imap):
                    validImap = self.imap.checkAccount(email, pw)

                    if (validImap == True and self.app.pargs.output is not None):
                        o.addRow(email, pw)

                    # if valid login and saving success result - will add csv row
                    if (self.app.pargs.pop):
                        print("POP not currently supported")

                # if delay is set
                # print('DELAY:' + self.app.pargs.delay)
                if float(self.app.pargs.delay or 0.5) > 0:
                    sleep(float(self.app.pargs.delay or 0.5))

        except ValueError:
            print(Style.BRIGHT + Fore.RED + "[-] Invalid input value: " + str(e) + Style.RESET_ALL)
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + "[-] Error parsing CSV File: " + str(e) + Style.RESET_ALL)
            print traceback.format_exc()
        finally:
            c.close()

            # if tor flag is set, will disconnect before exiting
            if (self.app.pargs.tor):
                baseController.tor.disconnect();

        print("\n" + Style.BRIGHT + "[*] Finished. Exiting!" + Style.RESET_ALL + "\n")

        return True
