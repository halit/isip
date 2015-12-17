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

import cmd
import options
import os.path
import readline
import logging
from collections import defaultdict
from termcolor import colored
from utils import print_message_set


class ISipBaseConsole(cmd.Cmd):
    """

    """
    def __init__(self, name="base"):
        """

        """
        cmd.Cmd.__init__(self)

        self.name = name
        self.ruler = "-"
        self.doc_header = "Commands - type help <command> for more info"

        self._hist = []
        self._locals = defaultdict(set)
        self._globals = defaultdict(set)

        self.prompt = colored("isip:", "cyan") + colored(self.name + "> ", "red")

        self.hist_file = os.path.expanduser(options.CONSOLE_HISTORY)

        logging.basicConfig(filename=options.LOG_FILE, level=logging.INFO)
        self.logger = logging.getLogger("isip.runtime." + self.name)

    def do_hist(self, args):
        """
        Print a list of commands that have been entered
        """
        print_message_set(self._hist)

    def do_exit(self, args):
        """
        Exits from the console
        """
        readline.write_history_file(self.hist_file)
        print
        return -1

    def do_quit(self, args):
        """
        Exits from the console
        """
        return self.do_exit(args)

    def do_EOF(self, args):
        """
        Exit on system end of file character
        """
        return self.do_exit(args)

    def do_shell(self, args):
        """
        Pass command to a system shell when line begins with '!'
        """
        os.system(args)

    def preloop(self):
        """
        Initialization before prompting user for commands.
        Despite the claims in the Cmd documentation, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)

        self._hist = []
        self._locals = defaultdict(set)
        self._globals = defaultdict(set)

        try:
            readline.read_history_file(self.hist_file)
        except IOError:
            pass

    def postloop(self):
        """
        Take care of any unfinished business.
        Despite the claims in the Cmd documentation, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)

    def precmd(self, line):
        """
        This method is called after the line has been input but before
        it has been interpreted. If you want to modify the input line
        before execution (for example, variable substitution) do it here.
        """
        l = line.strip()
        if l != '' and l != 'EOF':
            if len(self._hist) > 0 and self._hist[-1] != l:
                self._hist.append(l)
            elif len(self._hist) == 0:
                self._hist.append(l)
            else:
                return line
        return line

    def postcmd(self, stop, line):
        """
        If you want to stop the console, return something that evaluates to true.
        If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """
        Do nothing on empty input line
        """
        pass