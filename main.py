from dnspython.build.lib.dns.rdatatype import RdataType
import dns.message as mes
from client import Client
from sys import exit
from time import time
from config import NS_IP

def is_address(el):
    return el.rdtype == RdataType.A

def parse_answer(answer, message):
    message_type = message.question[0].rdtype
    if message_type == RdataType.A:
        sets = filter(is_address, answer)
        return [el.address for RRset in sets for el in RRset]
    else:
        exit(0)


def run_trace(client, message, server_ip, verbose = True, auxiliary = False):
    res = client.run_query(message, server_ip)
    if verbose:
        print(res, end = '\n\n\n')
    if res.answer:
        if auxiliary:
            ans = parse_answer(res.answer, message)
            return ans
        else:
            print("that's all")
            exit(0)

    #if any addresses in additional section, try them first
    for server in res.additional:
        print("jestem tu 2") ## debug
        for ip_rrset in server:
            if ip_rrset.rdtype == RdataType.A:
                ans = run_trace(client, message, ip_rrset.address, verbose, auxiliary)
                if ans:
                    return ans

    #if all of them failed try resolving names from authority section
    print("jestem tu 3") ## debug
    print(res)
    for servers in res.authority:
        for name in servers:
            name_message = mes.make_query(name, "A")
            ans_server = run_trace(client, name_message, NS_IP, True, True)
            for ip in ans_server:
                ans = run_trace(client, message, ip, verbose, auxiliary)
                if ans:
                    return ans

    print("trace failed to find the domain")
    exit(1)





def main(domain_name, server_ip, query_type, protocol, trace):
    message = mes.make_query(domain_name, query_type)
    message.flags = 0
    client = Client(protocol)
    if trace:
        ans = run_trace(client, message, server_ip, True)
        print(ans)
    else:
        response = client.run_query(message, server_ip)
        print(response)



#client("allegro.pl", "198.41.0.4", "A")

