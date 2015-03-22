
from cement.core import controller

class Imap(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'Imap'
        description = 'Object that performs Imap connection testing'
        stacked_on = 'base'

    @controller.expose(hide=True, help='default command', aliases=['start'])
    def login(self):

        if (self.app.pargs.verbose):
            print("Imap connection is starting ...")

        self.__checkConnection()

        return True


    def __checkConnection(self):
        print("CHecking")
  
        return True
