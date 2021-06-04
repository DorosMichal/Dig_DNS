from dns.rdatatype import RdataType
from dns.flags import Flag
import dns.message as mes
from client import Client
from sys import exit
from config import NS_IP

def parse_answer(answer):
    #used only for auxilary calls. Returns just ip's from response
    sets = filter(lambda el: el.rdtype == RdataType.A, answer.answer)
    return [el.address for RRset in sets for el in RRset]

def run_trace(client, message, server_ip, verbose = True, auxiliary = False):
    res = client.run_query(message, server_ip)
    if res == None:
        return None
    if verbose:
        print(res, end = '\n\n')

    #if response from authoritative server, finish
    if Flag.AA in res.flags:
        if not auxiliary:
            print("that's all")
        return res

    #if any addresses in additional section, try them first
    for server in res.additional:
        for ip_rrset in server:
            if ip_rrset.rdtype == RdataType.A:
                ans = run_trace(client, message, ip_rrset.address, verbose, auxiliary)
                if ans:
                    return ans

    #if all of them failed try resolving names from authority section
    for servers in res.authority:
        for name in servers:
            name_message = mes.make_query(name, "A")
            ans_server = run_trace(client, name_message, NS_IP, False, True)
            for ip in parse_answer(ans_server):
                ans = run_trace(client, message, ip, verbose, auxiliary)
                if ans:
                    return ans

    return None


def main(domain_name, server_ip, query_type, protocol, trace):
    message = mes.make_query(domain_name, query_type)
    client = Client(protocol)
    if trace:
        #turn recursion off
        message.flags = 0
        res = run_trace(client, message, server_ip, True)
        if res == None:
            print("failed to find the domain")
    else:
        response = client.run_query(message, server_ip)
        print(response)

    del client


