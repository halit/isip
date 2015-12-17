# The MIT License (MIT)
# Copyright (c) 2014 Halit Alptekin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import options
from termcolor import colored
from packet import ISipPacketConsole
from base import ISipBaseConsole


class ISipMainConsole(ISipBaseConsole):
    """

    """
    def __init__(self, name="main"):
        """

        """
        ISipBaseConsole.__init__(self, name)

        self.intro = """\t _       _        \n"""
        self.intro += """\t(_)     (_)       \n"""
        self.intro += """\t _  ___  _  _ __  \n"""
        self.intro += """\t| |/ __|| || '_ \ \n"""
        self.intro += """\t| |\__ \| || |_) |\n"""
        self.intro += """\t|_||___/|_|| .__/ \n"""
        self.intro += """\t           | |    \n"""
        self.intro += """\t           |_|    \n\n"""
        self.intro += "\tWelcome to interactive sip toolkit.\n"
        self.intro += "\t\tVersion: {version}\n".format(version=options.VERSION)
        self.intro += "\t\tHistory File: {history}\n".format(history=options.CONSOLE_HISTORY)
        self.intro += "\t\tLog File: {log}\n".format(log=options.LOG_FILE)
        self.intro = colored(self.intro, "cyan")

    def do_packet(self, args):
        """

        """
        subconsole = ISipPacketConsole()
        subconsole.cmdloop()