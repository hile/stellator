"""
Utility functions
"""

from subprocess import Popen, PIPE

def  arp_resolve_ip_address(mac_address):
    """ARP lookup

    Lookup mac address from ARP table
    """

    short_format = ':'.join('%x' % int(v, 16) for v in mac_address.split(':'))

    p = Popen(['/usr/sbin/arp', '-an'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    for line in stdout.splitlines():
        fields = line.split()
        if fields[3] in (mac_address, short_format):
            return fields[1].strip('()')

    return None

