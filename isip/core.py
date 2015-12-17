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

from scapy.all import *
from dpkt import sip, UnpackError
import utils
i = 0


def new_variable_adder(name, pkt, variable_list):
    global i
    t = ISipInterface(name="{0}.{1}".format(name, i))
    t.ip = pkt[IP]
    t.udp = pkt[UDP]
    t.message = ISipRequestMessage(str(pkt[Raw]))
    del t.ip[UDP]
    del t.udp[Raw]
    variable_list.add(t)
    utils.print_message("New variable: '{0}'".format(t.name))
    i += 1


def sniff_the_network(name, count, variable_list):
    global i
    i = 0
    sniff(count=count,
          lfilter=lambda x: x.haslayer(IP) and x.haslayer(UDP) and x.haslayer(Raw),
          filter="port 5060", prn=lambda x: new_variable_adder(name, x, variable_list))


def open_wireshark(packets):
    wireshark(packets)


def parse_sip_message(raw_data):
    try:
        sip_msg = ISipRequestMessage(raw_data)
    except UnpackError:
        try:
            sip_msg = ISipResponseMessage(raw_data)
        except UnpackError:
            sip_msg = None
    return sip_msg


def sip_packet_loader(file_name):
    packet_list = rdpcap(file_name)
    sip_packet_list = []
    for packet in packet_list:
        if packet.haslayer(IP) and packet.haslayer(UDP) and packet.haslayer(Raw):
            ip_layer = IP(packet[IP].build())
            udp_layer = ip_layer[UDP]
            del ip_layer[UDP]
            del udp_layer[Raw]
            sip_layer = packet[Raw].build()
            try:
                sip_packet_list.append((ip_layer, udp_layer, ISipRequestMessage(sip_layer)))
            except UnpackError:
                sip_packet_list.append((ip_layer, udp_layer, ISipResponseMessage(sip_layer)))
    return sip_packet_list


def sip_packet_saver(packet_list, file_name):
    try:
        wrpcap(file_name, packet_list)
    except:
        pass


class ISipError(Exception):
    """

    """

    def __init__(self, message):
        """
        """
        self.message = message

        Exception.__init__(self, "{0}".format(self.message))


class ISipRequestMessage(sip.Request):
    """

    """
    __hdr_defaults__ = {
        'method': 'INVITE',
        'uri': 'sip:user@example.com',
        'version': '2.0',
        'headers': {'To': '', 'From': '', 'Call-ID': '', 'CSeq': '', 'Contact': ''}
    }
    __methods = dict.fromkeys((
        'ACK', 'BYE', 'CANCEL', 'INFO', 'INVITE', 'MESSAGE', 'NOTIFY',
        'OPTIONS', 'PRACK', 'PUBLISH', 'REFER', 'REGISTER', 'SUBSCRIBE',
        'UPDATE'
    ))
    __proto = 'SIP'


class ISipResponseMessage(sip.Response):
    """

    """
    __hdr_defaults__ = {
        'version': '2.0',
        'status': '200',
        'reason': 'OK',
        'headers': {'To': '', 'From': '', 'Call-ID': '', 'CSeq': '', 'Contact': ''}
    }
    __proto = 'SIP'


class ISipInterface():
    """

    """

    count = 0

    def __init__(self, name=None, source_ip="", source_port=5060, target_ip="", target_port=5060, msg_type="request"):
        """

        """
        self.name = name if name else self.__make_name()
        self.source_ip = source_ip
        self.source_port = source_port
        self.target_ip = target_ip
        self.target_port = target_port
        self.msg_type = msg_type
        self.message = ISipRequestMessage() if msg_type.lower() == "request" else ISipResponseMessage()
        self.ip = IP(src=self.source_ip, dst=self.target_ip) if source_ip and target_ip else IP()
        self.udp = UDP(sport=self.source_port, dport=self.target_port) if source_port and target_port else UDP()

    def send(self, count=1):
        """

        :param count: int
        :param test: boolean
        """

        if isinstance(count, int):
            sendp(Ether()/self.ip/self.udp/self.message.pack(), count=count, verbose=1)

    def get_ether(self):
        return Ether()/self.ip/self.udp/self.message.pack()

    def test_register(self):
        """

        """
        self.ip.src = utils.random_ip()
        self.udp.sport = utils.random_port()

        self.message.uri = 'sip:{0}@{1}'.format(utils.random_data(20), utils.random_data(15))
        self.message.method = 'REGISTER'
        self.message.headers = {
            'Call-ID': utils.random_tag(),
            'CSeq': '0 REGISTER',
            'From': '"{0}" <sip:{1}@{2}>;tag={3}'.format(utils.random_data(10),
                                                         utils.random_data(20),
                                                         utils.random_data(15),
                                                         utils.random_tag()),
            'Max-Forwards': '{0}'.format(utils.random_number(2)),
            'To': '<sip:{0}@{1}>'.format(utils.random_data(20), utils.random_data(15)),
            'Via': 'SIP/2.0/UDP {0}:{1};branch={2};rport'.format(utils.random_ip(),
                                                                 utils.random_port(),
                                                                 utils.random_tag()),
            'Content-Length': '0',
            'User-Agent': '{0}'.format(utils.random_data(30)),
            'Contact': '<sip:{0}@{1}:{2};transport=UDP>;'
                       'q=1.00;agentid="{3}";'
                       'methods="INVITE,NOTIFY,MESSAGE,ACK,BYE,CANCEL";'
                       'expires={4}'.format(utils.random_data(20),
                                            utils.random_ip(),
                                            utils.random_data(20),
                                            utils.random_tag(),
                                            utils.random_number(2)),
            'Authorization': 'Digest username="{0}@{1}", '
                             'realm="{2}", '
                             'nonce="{3}", '
                             'uri="sip:{4}", '
                             'qop=auth, nc=00000001, '
                             'cnonce="{5}", '
                             'response="{6}", '
                             'opaque=""'.format(utils.random_data(20),
                                                utils.random_data(15),
                                                utils.random_data(15),
                                                utils.random_tag(),
                                                utils.random_data(15),
                                                utils.random_tag(),
                                                utils.random_data(32))}

    def test_invite(self):
        """

        """
        self.ip.src = utils.random_ip()
        self.udp.sport = utils.random_port()

        self.message.uri = 'sip:{0}@{1}'.format(utils.random_data(20), utils.random_data(15))
        self.message.method = 'INVITE'
        self.message.headers = {
            'Call-ID': utils.random_tag(),
            'CSeq': '0 INVITE',
            'From': '"{0}" <sip:{1}@{2}>;tag={3}'.format(utils.random_data(10),
                                                         utils.random_data(20),
                                                         utils.random_data(15),
                                                         utils.random_tag()),
            'Max-Forwards': '{0}'.format(utils.random_number(2)),
            'To': '<sip:{0}@{1}>'.format(utils.random_data(20), utils.random_data(15)),
            'Via': 'SIP/2.0/UDP {0}:{1};branch={2};rport'.format(utils.random_ip(),
                                                                 utils.random_port(),
                                                                 utils.random_tag()),
            'Content-Length': '0',
            'User-Agent': '{0}'.format(utils.random_data(30)),
            'Contact': '<sip:{0}@{1}:{2};transport=UDP>;'
                       'q=1.00;agentid="{3}";'
                       'methods="INVITE,NOTIFY,MESSAGE,ACK,BYE,CANCEL";'
                       'expires={4}'.format(utils.random_data(20),
                                            utils.random_ip(),
                                            utils.random_data(20),
                                            utils.random_tag(),
                                            utils.random_number(2)),
            'Authorization': 'Digest username="{0}@{1}", '
                             'realm="{2}", '
                             'nonce="{3}", '
                             'uri="sip:{4}", '
                             'qop=auth, nc=00000001, '
                             'cnonce="{5}", '
                             'response="{6}", '
                             'opaque=""'.format(utils.random_data(20),
                                                utils.random_data(15),
                                                utils.random_data(15),
                                                utils.random_tag(),
                                                utils.random_data(15),
                                                utils.random_tag(),
                                                utils.random_data(32))}

    def __make_name(self):
        """

        :return:
        """
        ISipInterface.count += 1
        return "message.{count}".format(count=ISipInterface.count)

    def __str__(self):
        """

        :return:
        """
        return "<ISipMessage: name: {0}, type: {1}>".format(self.name, self.msg_type)

    def __repr__(self):
        """

        :return:
        """
        return "<ISipMessage: name: {0}, type: {1}>".format(self.name, self.msg_type)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)