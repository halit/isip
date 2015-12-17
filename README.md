# isip

> Interactive sip toolkit for packet manipulations, sniffing, man in the middle attacks, fuzzing, simulating of dos attacks.

## Video

https://asciinema.org/a/11128

## Setup

``` sh
git clone https://github.com/halitalptekin/isip.git
cd isip
pip install -r requirements.txt
```

## Usage

* Packet manipulation tools are in `packet` cmd loop. First start, you are in the `main` cmd loop.

```sh
isip:main> packet
isip:packet>
```

* Create a new sip packet with `new` command. If you don't write name, isip create the packet named by `message-{id}`.
    
``` sh
isip:packet> new
isip:packet> new r1
```

* List the all created sip packets with `list` command.

``` sh
isip:packet> list
```

* Show properties of packets with `show` command. You can type `ip`, `udp` or `sip` with `show` command.

``` sh
isip:packet> show message-1
isip:packet> show message-1 ip
isip:packet> show message-1 udp
isip:packet> show message-1 sip
isip:packet> show message-1 ip src
isip:packet> show message-1 udp sport
isip:packet> show message-1 sip uri
isip:packet> show message-1 sip headers.to
```

* Set the properties of packets with `set` command. You can type `ip`, `udp` or `sip` and properties label with `show` command.

``` sh
isip> set message-1 ip src 12.12.12.12
isip> set message-1 udp sport 4545
isip> set message-1 sip method OPTIONS
isip> set message-1 sip headers.from "blabla"
```

* Set the random properties of packets with `set` command. You can use with `random-headers-from`, `random-headers-to`, `random-headers-call-id`, `random-headers-max-forwards`, `random-headers-user-agent`, `random-headers-contact`, `random-headers-invite-cseq`, `random-headers-register-cseq` commands.

``` sh
isip:packet> set message-1 ip src random-ip
isip:packet> set message-1 udp sport random-port
isip:packet> set message-1 sip headers.from random-headers-from
isip:packet> set message-1 sip headers.to random-headers-to
isip:packet> set message-1 sip headers.contact random-headers-contact
isip:packet> set message-1 sip body random-data 50
```

* Send the packet with `send` command.

``` sh
isip:packet> send message-1 1
isip:packet> send message-1 150
```

* Parse the text file to packet with `parse` command.

``` sh
isip:packet> parse test/test1.txt r1
```

* Load the packets from `pcap` file with `load` command. If you don't write name, isip create the packet named by `message-{id}`.

``` sh
isip:packet> load test.pcap r1
isip:packet> load test.pcap
```

* Save the packets tp `pcap` file with `save` command. You can save the packet list just single command.

``` sh
isip:packet> save r1 test.pcap
isip:packet> save r2 test.pcap # assume you have r2.0, r2.1, r2.2, r2.3 ...
```

* Open the wireshark for packets with `wireshark` command.

``` sh
isip:packet> wireshark r1
isip:packet> wireshark r2 # assume you have r2.0, r2.1, r2.2, r2.3 ...
```

* List the history with `hist` command.

``` sh    
isip:packet> hist
```

* Execute the shell command with `shell` or `!`.

``` sh
isip:packet> shell ls -la
isip:packet> ! cat /etc/passwd
```

* Show the help page with `?` or `help` command.

``` sh
isip> ?
isip> help
isip:packet> ?
isip:packet> help
isip:packet> help new
isip:packet> help send
isip:packet> help set
isip:packet> help show
```
    
