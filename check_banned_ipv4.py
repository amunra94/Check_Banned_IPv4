"""
В классе RKN создал 4 различных метода is_banned, и пронумеровал по возрастанию времени исполнения.
Самый быстрый метод is_banned(). Два метода is_banned2 и is_banned3 не сильно отличаются по скорости работы.

"""

import netaddr
import socket, struct


class RKN:
    def __init__(self, subnets):
        self.subnets = subnets

    def is_banned(self, ipv4):

        """ Check IP in the banned subnets first way more fast than other """

        for subnet in self.subnets:
            if self.address_in_network(ipv4, subnet):
                return True
        return False

    def address_in_network(self, ip, net):

        "Is an address in a network"

        ipaddr = struct.unpack('L', socket.inet_aton(ip))[0]
        netaddr, bits = net.split('/')
        mask = (2 ** 32 - 1) >> (32 - int(bits))
        netmask = struct.unpack('L', socket.inet_aton(netaddr))[0] & mask
        return ipaddr & mask == netmask

    def is_banned2(self, ipv4):

        """ Check IP in the banned subnets second way """

        ip = int(netaddr.IPAddress(ipv4))
        for subnet in self.subnets:
            addr_subnet, bits = subnet.split('/')
            mask = int(''.join(['1' * int(bits), '0' * (32 - int(bits))]), base=2)
            addr_subnet = int(netaddr.IPAddress(addr_subnet))
            if addr_subnet & mask == ip & mask:
                return True
        return False

    def is_banned3(self, ipv4):

        """ Check IP in the banned subnets of another way """

        ip = list(map(int, ipv4.split('.')))
        for subnet in self.subnets:
            network, bits = subnet.split('/')
            ones = int(bits)
            addr = list(map(int, network.split('.')))
            mask_bin = ''.join(['1' * ones, '0' * (32 - ones)])
            mask = [int(mask_bin[:8], base=2), int(mask_bin[8:16], base=2),
                    int(mask_bin[16:24], base=2), int(mask_bin[24:32], base=2)]
            addr_subnet = self.and_values_lists(ip, mask)
            addr_subnet_banned = self.and_values_lists(addr, mask)
            if addr_subnet == addr_subnet_banned:
                return True
        return False

    def and_values_lists(self, arg1, arg2):
        result = []
        for i in range(len(arg1)):
            result.append(arg1[i] & arg2[i])
        return result

    def is_banned4(self, ipv4):

        """ Check IP in the banned subnets another way for check, slow"""

        for subnet in self.subnets:
            if netaddr.IPAddress(ipv4) in netaddr.IPNetwork(subnet):
                return True
        return False


if __name__ == '__main__':
    r = RKN(['10.0.0.0/8', '8.8.8.8/32', '234.45.3.2/23', '234.45.3.2/5',
             '45.67.3.2/16', '45.67.3.2/14', '36.21.45.6/24', '23.58.21.3/28'])

    print(r.is_banned('10.1.2.3'))  # True
    print(r.is_banned('127.0.0.1'))  # False
    print(r.is_banned('8.8.8.8'))  # True
    print(r.is_banned('8.8.8.7'))  # False
    print(r.is_banned('234.5.6.3'))  # True
    print(r.is_banned('45.67.1.2'))  # True
    print(r.is_banned('45.67.5.2'))  # True
    print(r.is_banned('45.68.1.2'))  # False
    print(r.is_banned('45.255.1.2'))  # False
    print(r.is_banned('36.21.45.45'))  # True
