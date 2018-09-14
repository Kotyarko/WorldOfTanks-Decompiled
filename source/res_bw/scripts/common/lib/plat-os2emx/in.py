# Embedded file name: scripts/common/Lib/plat-os2emx/IN.py
PAGE_SIZE = 4096
HZ = 100
MAXNAMLEN = 260
MAXPATHLEN = 260

def htonl(X):
    return _swapl(X)


def ntohl(X):
    return _swapl(X)


def htons(X):
    return _swaps(X)


def ntohs(X):
    return _swaps(X)


IPPROTO_IP = 0
IPPROTO_ICMP = 1
IPPROTO_IGMP = 2
IPPROTO_GGP = 3
IPPROTO_TCP = 6
IPPROTO_EGP = 8
IPPROTO_PUP = 12
IPPROTO_UDP = 17
IPPROTO_IDP = 22
IPPROTO_TP = 29
IPPROTO_EON = 80
IPPROTO_RAW = 255
IPPROTO_MAX = 256
IPPORT_RESERVED = 1024
IPPORT_USERRESERVED = 5000

def IN_CLASSA(i):
    return long(i) & 2147483648L == 0


IN_CLASSA_NET = 4278190080L
IN_CLASSA_NSHIFT = 24
IN_CLASSA_HOST = 16777215
IN_CLASSA_MAX = 128

def IN_CLASSB(i):
    return long(i) & 3221225472L == 2147483648L


IN_CLASSB_NET = 4294901760L
IN_CLASSB_NSHIFT = 16
IN_CLASSB_HOST = 65535
IN_CLASSB_MAX = 65536

def IN_CLASSC(i):
    return long(i) & 3758096384L == 3221225472L


IN_CLASSC_NET = 4294967040L
IN_CLASSC_NSHIFT = 8
IN_CLASSC_HOST = 255

def IN_CLASSD(i):
    return long(i) & 4026531840L == 3758096384L


IN_CLASSD_NET = 4026531840L
IN_CLASSD_NSHIFT = 28
IN_CLASSD_HOST = 268435455

def IN_MULTICAST(i):
    return IN_CLASSD(i)


def IN_EXPERIMENTAL(i):
    return long(i) & 3758096384L == 3758096384L


def IN_BADCLASS(i):
    return long(i) & 4026531840L == 4026531840L


INADDR_ANY = 0
INADDR_LOOPBACK = 2130706433
INADDR_BROADCAST = 4294967295L
INADDR_NONE = 4294967295L
INADDR_UNSPEC_GROUP = 3758096384L
INADDR_ALLHOSTS_GROUP = 3758096385L
INADDR_MAX_LOCAL_GROUP = 3758096639L
IN_LOOPBACKNET = 127
IP_OPTIONS = 1
IP_MULTICAST_IF = 2
IP_MULTICAST_TTL = 3
IP_MULTICAST_LOOP = 4
IP_ADD_MEMBERSHIP = 5
IP_DROP_MEMBERSHIP = 6
IP_HDRINCL = 2
IP_TOS = 3
IP_TTL = 4
IP_RECVOPTS = 5
IP_RECVRETOPTS = 6
IP_RECVDSTADDR = 7
IP_RETOPTS = 8
IP_DEFAULT_MULTICAST_TTL = 1
IP_DEFAULT_MULTICAST_LOOP = 1
IP_MAX_MEMBERSHIPS = 20