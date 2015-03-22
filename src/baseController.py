from cement.core import controller
from time import sleep
import csv

class baseController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'base'
        description = 'Email batch credential verifer'

        config_defaults = {}

        arguments = [
                (['-c', '--csv'], dict(action='store', help='CSV file containing email login and password')),
                (['-v', '--verbose'], dict(action='store_true', help='Verbose Output'))
                ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        if (self.app.pargs.csv):
            self.__parseCSV()

        return True

    # parses CSV file
    def __parseCSV(self):

        c = None

        try:

            lines = 0
            c = open(self.app.pargs.csv)
            ch = csv.reader(c)

            # lines = int(len(list(ch)))

            if (self.app.pargs.verbose):
                print("[!] Total Lines: %u" % lines)

            #default email/password columns
            emailCol = 0
            passwdCol = 0
            hasHeader = True

            # gets some basic info about file to properly parse file
            firstLineHeader = raw_input("[?] Does the first row contain column titles? [Y/n]: ")

            if (firstLineHeader.upper() == 'N'):
                hasHeader = False
                lines -= 1

            emailCol = int(raw_input("[?] Enter column number of email login. 0 equals column A. [0]: ") or emailCol)
            passwdCol =  int(raw_input("[?] Enter column number of passwords [0]: ") or passwdCol)

            for k,r in enumerate(ch):

                if (k == 0 and hasHeader == True):
                    if (self.app.pargs.verbose):
                        print("[!] Skipping header row")
                    continue

                print("[%s] Checking: %s:%s" % ((k + 1),r[emailCol], r[passwdCol]))
                sleep(1)

        except ValueError:
            print("Invalid Integer")
        except Exception as e:
            print("Error parsing CSV File: %s" % str(e))
        finally:
            c.close()

        return True
