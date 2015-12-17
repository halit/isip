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

import argparse
import shlex

from core import *
from base import ISipBaseConsole


class ISipPacketConsole(ISipBaseConsole):
    """

    """
    def __init__(self, name="packet"):
        """

        """
        ISipBaseConsole.__init__(self, name)

    def do_new(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="new", description="Create the new sip message packet.")
        parser.add_argument("packet_name", help="New packet name", nargs="?")
        parser.add_argument("message_template", help="Template of the message", nargs="?")

        try:
            new_args = parser.parse_args(shlex.split(args))
            if new_args.packet_name:
                t = ISipInterface(name=new_args.packet_name)
                if new_args.message_template:
                    try:
                        getattr(t, "test_{0}".format(new_args.message_template))()
                    except:
                        utils.print_message("Not found message template.")
                        self.logger.info("Not found message template: {0}".format(new_args.message_template))
                        return
                self._locals['variables'].add(t)
                self.logger.info("New variable: {0}".format(t.name))
            else:
                t = ISipInterface()
                self._locals['variables'].add(t)
                self.logger.info("New variable: {0}".format(t.name))
        except:
            self.logger.error("Error in new function with {0}".format(args))
            pass

    def do_set(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="set", description="Set the properties of packet.")
        parser.add_argument("packet_name", help="Name of packet")
        parser.add_argument("packet_protocol", help="Protocol of packet")
        parser.add_argument("protocol_field", help="Field of protocol")
        parser.add_argument("field_value", help="New value of field")
        parser.add_argument("value_size", help="Size of value", nargs="?", type=int, default=5)

        try:
            new_args = parser.parse_args(shlex.split(args))
            if "random-" in new_args.field_value:
                try:
                    module_name = new_args.field_value.replace("-", "_")
                    randomize_module = getattr(utils, module_name)
                    field_value = randomize_module(new_args.value_size)
                except:
                    print "Doesn't exist this randomize module."
                    return
            else:
                field_value = utils.control_arg(new_args.field_value)

            sip_msg_list = {v.name: v for v in self._locals['variables']}
            if new_args.packet_name in sip_msg_list:
                sip_msg = sip_msg_list[new_args.packet_name]
                if new_args.packet_protocol in ("ip", "udp"):
                    setattr(getattr(sip_msg, new_args.packet_protocol), new_args.protocol_field, field_value)
                elif new_args.packet_protocol == "sip":
                    field_list = new_args.protocol_field.split(".")
                    if len(field_list) > 1 and field_list[0] == "headers":
                        sip_msg.message.headers[field_list[1]] = field_value
                        return
                    else:
                        setattr(sip_msg.message, new_args.protocol_field, field_value)
                else:
                    utils.print_message("Message doesn't has this layer.")
                    self.logger.info("Message doesn't has {0} layer.".format(new_args.packet_protocol))
                    return
            else:
                utils.print_message("Doesn't exist this variable.")
                self.logger.info("Doesn't exist {0} variable.".format(new_args.packet_name))
                return
        except:
            self.logger.error("Error in set function with {0}".format(args))
            pass

    def complete_set(self, text, line, begidx, endidx):
        """
        """
        if not text:
            completions = map(lambda x: x.name, self._locals['variables'])
        else:
            var_list = map(lambda x: x.name, self._locals['variables'])
            completions = [f for f in var_list if f.startswith(text)]
        return completions


    def do_show(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="show", description="Show the properties of packet.")
        parser.add_argument("packet_name", help="Name of packet")
        parser.add_argument("packet_protocol", help="Protocol of packet", nargs="?")
        parser.add_argument("protocol_field", help="Field of packet", nargs="?")

        try:
            new_args = parser.parse_args(shlex.split(args))
            sip_msg_list = {v.name: v for v in self._locals['variables']}
            if new_args.packet_name in sip_msg_list:
                sip_msg = sip_msg_list[new_args.packet_name]
                if new_args.packet_protocol in ("ip", "udp"):
                    if new_args.protocol_field:
                        print getattr(getattr(sip_msg, new_args.packet_protocol), new_args.protocol_field)
                        return
                    getattr(sip_msg, new_args.packet_protocol).show2()
                elif new_args.packet_protocol == "sip":
                    if new_args.protocol_field:
                        if len(new_args.protocol_field.split(".")) > 1:
                            print sip_msg.message.headers[new_args.protocol_field.split(".")[1].capitalize()]
                            return
                        print getattr(sip_msg.message, new_args.protocol_field)
                        return
                    utils.show_sip_message(sip_msg)
                else:
                    getattr(sip_msg, "ip").show2()
                    getattr(sip_msg, "udp").show2()
                    utils.show_sip_message(sip_msg)
            else:
                utils.print_message("Doesn't exist this variable.")
                self.logger.info("Doesn't exist {0} variable.".format(new_args.packet_name))
                return
        except:
            self.logger.error("Error in show function with {0}".format(args))
            pass

    def complete_show(self, text, line, begidx, endidx):
        """
        """
        if not text:
            completions = map(lambda x: x.name, self._locals['variables'])
        else:
            var_list = map(lambda x: x.name, self._locals['variables'])
            completions = [f for f in var_list if f.startswith(text)]
        return completions


    def do_send(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="send", description="Send the packets.")
        parser.add_argument("packet_name", help="Name of packet")
        parser.add_argument("count", help="Number of packets", nargs="?", type=int, default=1)

        try:
            new_args = parser.parse_args(shlex.split(args))
            sip_msg_list = {v.name: v for v in self._locals['variables']}
            if new_args.packet_name in sip_msg_list:
                sip_msg = sip_msg_list[new_args.packet_name]
                sip_msg.send(new_args.count)
            else:
                utils.print_message("Doesn't exist this variable.")
                self.logger.info("Doesn't exist {0} variable.".format(new_args.packet_name))
        except:
            self.logger.error("Error in send function with {0}".format(args))
            pass

    def complete_send(self, text, line, begidx, endidx):
        """
        """
        if not text:
            completions = map(lambda x: x.name, self._locals['variables'])
        else:
            var_list = map(lambda x: x.name, self._locals['variables'])
            completions = [f for f in var_list if f.startswith(text)]
        return completions


    def do_sniff(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="sniff", description="Sniff the networks.")
        parser.add_argument("packet_name", help="Name of packet")
        parser.add_argument("count", help="Number of packet", type=int, default=1)

        try:
            new_args = parser.parse_args(shlex.split(args))
            sniff_the_network(new_args.packet_name, new_args.count, self._locals['variables'])
        except:
            self.logger.error("Error in sniff function with {0}".format(args))
            pass

    def do_load(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="load", description="Load the packets from file to variable.")
        parser.add_argument("file_name", help="Name of pcap file")
        parser.add_argument("variable_name", help="Name of variable", nargs="?")

        try:
            new_args = parser.parse_args(shlex.split(args))
            for i, packet in enumerate(sip_packet_loader(new_args.file_name)):
                t = ISipInterface()
                t.ip = packet[0]
                t.udp = packet[1]
                t.message = packet[2]
                t.name = "{0}.{1}".format(new_args.variable_name, i) if new_args.variable_name else t.name
                self._locals['variables'].add(t)
                utils.print_message("Loaded packet '{0}'".format(t.name))
        except:
            utils.print_message("Didn't load sip packets")
            self.logger.error("Error in load function with {0}".format(args))
            pass

    def do_save(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="save", description="Save the packets to pcap file.")
        parser.add_argument("variable_name", help="Name of variable")
        parser.add_argument("file_name", help="Name of pcap file")

        try:
            new_args = parser.parse_args(shlex.split(args))
            sip_msg_list = []
            for v in self._locals['variables']:
                if v.name == new_args.variable_name:
                    sip_msg_list.append(v.get_ether())
                    break
                else:
                    if '.' in v.name:
                        if v.name.split('.')[0] == new_args.variable_name:
                            sip_msg_list.append(v.get_ether())
            sip_packet_saver(sip_msg_list, new_args.file_name)
        except:
            utils.print_message("Didn't save sip packets")
            self.logger.error("Error in save function with {0}".format(args))
            pass

    def complete_save(self, text, line, begidx, endidx):
        """
        """
        if not text:
            completions = map(lambda x: x.name, self._locals['variables'])
        else:
            var_list = map(lambda x: x.name, self._locals['variables'])
            completions = [f for f in var_list if f.startswith(text)]
        return completions


    def do_parse(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="parse", description="Parse the text files for sip message.")
        parser.add_argument("file_name", help="Name of text file")
        parser.add_argument("variable_name", help="Name of variable")

        try:
            new_args = parser.parse_args(shlex.split(args))
            if os.path.isfile(new_args.file_name):
                with open(new_args.file_name, "r") as fd:
                    file_data = fd.read()
                sip_msg = parse_sip_message(file_data)
                if sip_msg:
                    t = ISipInterface(name=new_args.variable_name)
                    t.message = sip_msg
                    self._locals['variables'].add(t)
                    self.logger.info("Parsed file: {0}".format(t.name))
                else:
                    utils.print_message("Didn't parsed file: {0}".format(new_args.file_name))
                    self.logger.error("Error in parse function with {0}".format(args))
            else:
                utils.print_message("File not found '{0}'".format(new_args.file_name))
        except:
            self.logger.error("Error in parse function with {0}".format(args))
            pass

    def do_wireshark(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="wireshark", description="Open the messages on wireshark.")
        parser.add_argument("variable_name", help="Name of variable")

        try:
            new_args = parser.parse_args(shlex.split(args))
            sip_msg_list = []
            for v in self._locals['variables']:
                if v.name == new_args.variable_name:
                    sip_msg_list.append(v.get_ether())
                    break
                else:
                    if '.' in v.name:
                        if v.name.split('.')[0] == new_args.variable_name:
                            sip_msg_list.append(v.get_ether())
            open_wireshark(sip_msg_list)
        except:
            self.logger.error("Error in wireshark function with {0}".format(args))
            pass

    def complete_wireshark(self, text, line, begidx, endidx):
        """
        """
        if not text:
            completions = map(lambda x: x.name, self._locals['variables'])
        else:
            var_list = map(lambda x: x.name, self._locals['variables'])
            completions = [f for f in var_list if f.startswith(text)]
        return completions


    def do_use(self, args):
        """
        """
        parser = argparse.ArgumentParser(prog="use", description="Use the history command.")
        parser.add_argument("row_number", help="History row number", type=int)

        try:
            new_args = parser.parse_args(shlex.split(args))
            if new_args.row_number <= len(self._hist):
                func_list = self._hist[new_args.row_number].split()
                func = getattr(self, "do_{0}".format(func_list[0]))
                func(" ".join(func_list[1:]))
            else:
                utils.print_message("Your typed number is large then length of history")
        except:
            self.logger.error("Error in use function with {0}".format(args))
            pass

    def do_list(self, args):
        """
        """
        utils.print_message_set(self._locals['variables'])
