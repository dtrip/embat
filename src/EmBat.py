
import sys
import os

from cement.core import foundation,handler

sys.path.append(os.getcwd())

import baseController
import Imap

print("\n__ EmBat: Batch E-mail credential verifier __\n")
print("Disclaimer: Be good, or be good at it.\n")


class EmBat:
    def init(self):
        pass

    def run(self):
        try:
            app = foundation.CementApp('EmBat')

            handler.register(baseController.baseController)
            handler.register(Imap.Imap)

            app.setup()

            app.run()
        except Exception as e:
            print("Error: %s" % str(e))
        finally:
            app.close()

e = EmBat()
e.run()
