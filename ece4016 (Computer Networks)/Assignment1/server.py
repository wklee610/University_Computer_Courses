from dnslib import DNSRecord, RR
from dnslib.server import *
import sys
import time
import datetime as dt


IP = "127.0.0.1"
PORT = 1234
IP_PORT = (IP, PORT)


# QTYPE =  Bimap('QTYPE',
#         {1:'A', 2:'NS', 5:'CNAME', 6:'SOA', 10:'NULL', 12:'PTR', 13:'HINFO',
#                     15:'MX', 16:'TXT', 17:'RP', 18:'AFSDB', 24:'SIG', 25:'KEY',
#                     28:'AAAA', 29:'LOC', 33:'SRV', 35:'NAPTR', 36:'KX',
#                     37:'CERT', 38:'A6', 39:'DNAME', 41:'OPT', 42:'APL',
#                     43:'DS', 44:'SSHFP', 45:'IPSECKEY', 46:'RRSIG', 47:'NSEC',
#                     48:'DNSKEY', 49:'DHCID', 50:'NSEC3', 51:'NSEC3PARAM',
#                     52:'TLSA', 53:'HIP', 55:'HIP', 59:'CDS', 60:'CDNSKEY',
#                     61:'OPENPGPKEY', 62:'CSYNC', 63:'ZONEMD', 64:'SVCB',
#                     65:'HTTPS', 99:'SPF', 108:'EUI48', 109:'EUI64', 249:'TKEY',
#                     250:'TSIG', 251:'IXFR', 252:'AXFR', 255:'ANY', 256:'URI',
#                     257:'CAA', 32768:'TA', 32769:'DLV'}, DNSError)

class TestResolver:
    def __init__(self):
        self.cache = dict()
        # use Google DNS Server
        self.PUBLIC_SERVER = '8.8.8.8'

    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype
        reply = request.reply()

        self.recursive_search(str(qname), qtype, reply)

        return reply


    def iterative_search(self, qname: str, qtype: int, reply: DNSRecord):
        print("enter iterative - {}".format(qname))
        packet = DNSRecord.question(qname=qname).send(self.PUBLIC_SERVER)
        res = DNSRecord.parse(packet)
        for rr in res.rr:
            reply.add_answer(rr)
            rr_cache = self.cache.get(str(rr.rname), list())
            rr_cache.clear()
            self.cache[str(rr.rname)] = rr_cache
        for rr in res.rr:
            self.cache[str(rr.rname)].append((rr, dt.datetime.now() + dt.timedelta(seconds=rr.ttl)))


    def recursive_search(self, qname: str, qtype: int, reply: DNSRecord):
        # apply BFS algo
        data = self.cache.get(qname, list())
        queue = [rr for rr in data]
        # cache miss
        if not len(queue):
            self.iterative_search(qname, qtype, reply)
            return

        while len(queue):
            size = len(queue)
            for i in range(size):
                rr_tuple = queue.pop(0)
                #print(rr_tuple)
                rr = rr_tuple[0]
                local_ttl = rr_tuple[1]
                # if expired
                if local_ttl < dt.datetime.now():
                    self.iterative_search(rr.rname, rr.rtype, reply)
                    continue
                new_ttl = local_ttl - dt.datetime.now()
                rr.ttl = new_ttl.seconds
                reply.add_answer(rr)
                if rr.rtype == 5:
                    for rr in self.cache[str(rr.rdata)]:
                        queue.append(rr)

def main():
    resolver = TestResolver()
    logger = DNSLogger(prefix=False)
    print('DNS is listening on {0}:{1} ...'.format(IP, PORT))
    dns_server = DNSServer(resolver, port=1234, address='127.0.0.1', logger=logger)
    dns_server.start_thread()
    try:
        while True:
            time.sleep(600)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()

