
from colorama import init, Fore, Back, Style
import StringIO
import socket
import urllib2

import traceback
import socks
import stem.process

from stem.util import term

class Tor:

    torProc = None
    torPort = 7000

    def init(self):
        pass

    # makes connection to tor
    def connect(self, port):

        try:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', int(port))
            socket.socket = socks.socksocket

            socket.getaddrinfo = self.__getAddrInfo

            self.torPort = port

            # if (self.app.pargs.verbose):
            print(Fore.BLUE + Style.BRIGHT + "[+] Connecting to Tor on port " + self.torPort + Style.RESET_ALL)

            self.torProc = stem.process.launch_tor_with_config(
                config = {
                        'SocksPort': str(port),
                        'ExitNodes': '{ru}',
                    },
                init_msg_handler = self.__printBootstrapLines,
            )

            print term.format("\n" + Style.BRIGHT + "[!] Checking our endpoint:\n" + Style.RESET_ALL)

            ep = self.__query("https://www.atagar.com/echo.php")

            print term.format("[!] " + Fore.BLUE + ep + Style.RESET_ALL)

            print(Fore.GREEN + Style.BRIGHT + "Successfully connected to Tor. Lets rock! =D" + Style.RESET_ALL + "\n")

        except socket.error as se:
            print(Style.BRIGHT + Fore.RED + "[-] Socket Error: " + str(e) + Style.RESET_ALL)
            print traceback.format_exc()
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + "[-] Error connecting to Tor: " + str(e) + Style.RESET_ALL)
            print traceback.format_exc()

        return True

    # disconnects from tor
    def disconnect(self):
        if (Tor.torProc is not None):
            Tor.torProc.kill()
            tor.torProc = None
            return True
        else:
            return False

    def __printBootstrapLines(self, line):
        if ("Bootstrapped" in line):
            print(Fore.MAGENTA + "[!] " + line + Style.RESET_ALL)


    def __getAddrInfo(self, *args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    def __query(self, url):
        try:
            return urllib2.urlopen(url).read()
        except:
            return "Unable to read %s" % url

