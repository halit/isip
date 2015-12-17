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

import random
import string
import logging


def random_data(size):
    """

    :param size:
    :return:
    """
    alpha_list = string.ascii_letters + "".join(map(str, range(10)))
    return "".join(random.sample(alpha_list, size))


def random_number(size):
    """

    :param size:
    :return:
    """
    return "".join(random.sample(map(str, range(10)), size))


def random_port(*args):
    """

    :return:
    """
    return random.randint(1, 65536)


def random_tag(*args):
    """

    :return:
    """
    return random_data(8) + "-" + random_data(4) + "-" + random_data(4) + "-" + random_data(4) + "-" + random_data(12)


def random_ip(*args):
    """

    :return:
    """
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


def random_headers_from(*args):
    """

    :param args:
    :return:
    """
    return '"{0}" <sip:{1}@{2}>;tag={3}'.format(random_data(10),
                                                random_data(20),
                                                random_data(15),
                                                random_tag())


def random_headers_call_id(*args):
    """

    :param args:
    :return:
    """
    return random_tag(*args)

def random_headers_max_forwards(*args):
    """

    :param args:
    :return:
    """
    return random_data(2)


def random_headers_to(*args):
    """

    :param args:
    :return:
    """
    return '<sip:{0}@{1}>'.format(random_data(20), random_data(15))


def random_headers_via(*args):
    """

    :param args:
    :return:
    """
    return 'SIP/2.0/UDP {0}:{1};branch={2};rport'.format(random_ip(), random_port(), random_tag())

def random_headers_user_agent(*args):
    """

    :param args:
    :return:
    """
    return '{0}'.format(random_data(30))


def random_headers_contact(*args):
    """

    :param args:
    :return:
    """
    return '<sip:{0}@{1}:{2};' \
           'transport=UDP>;' \
           'q=1.00;' \
           'agentid="{3}";' \
           'methods="INVITE,NOTIFY,MESSAGE,ACK,BYE,CANCEL";' \
           'expires={4}'.format(random_data(20), random_ip(), random_data(20), random_tag(), random_number(2))


def random_headers_invite_cseq(*args):
    """

    :param args:
    :return:
    """
    return '{0} {1}'.format(random_number(1), 'INVITE')


def random_headers_register_cseq(*args):
    """

    :param args:
    :return:
    """
    return '{0} {1}'.format(random_number(1), 'REGISTER')


def print_message_set(msg_set):
    """

    :param msg:
    :return:
    """
    if isinstance(msg_set, set):
        for msg in msg_set:
            print "# Sip Message: name='{0}', type='{1}'".format(msg.name, msg.msg_type)
    elif isinstance(msg_set, list):
        for i, msg in enumerate(msg_set):
            print "# History {0}: '{1}'".format(i, msg)
    else:
        logging.getLogger("isip.runtime").error("Variable set is invalid. {0}".format(__file__))


def print_message(msg):
    """

    :param msg:
    :return:
    """
    print "# Info: {0}".format(msg)


def show_sip_message(msg):
    """

    :param msg:
    :return:
    """
    print "###[ SIP ]###"
    print "  method    = {0}".format(msg.message.method)
    print "  uri       = {0}".format(msg.message.uri)
    print "  version   = {0}".format(msg.message.version)
    print "  headers   ="

    for header_key, header_value in msg.message.headers.items():
        print "            {0}: {1}".format(header_key, header_value)
    print "  body      = {0}".format(msg.message.body)
    print "  data      = {0}".format(msg.message.body)


def control_arg(var):
    """

    :param var:
    :return:
    """
    if var.isdigit():
        return int(var)
    else:
        return var
