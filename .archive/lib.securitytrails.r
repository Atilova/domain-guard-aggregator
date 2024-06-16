get_usage: ApiKeyUsage(
    usage=12,
    monthly_available=50
)

get_domain: DomainData(
    hostname='atilova.com',
    records=DnsRecordsInfo(
        A=BaseRecordInfo(
            first_seen='2024-02-11',
            values=(
                ARecord(
                    ip='104.21.74.244',
                    ip_count=0,
                    ip_organization='Cloudflare, Inc.'
                ),
                ARecord(
                    ip='172.67.207.241',
                    ip_count=0,
                    ip_organization='Cloudflare, Inc.'
                )
            )
        ),
        AAAA=BaseRecordInfo(
            first_seen='2024-02-11',
            values=(
                AAAARecord(
                    ipv6='2606:4700:3032::ac43:cff1',
                    ipv6_count=0,
                    ipv6_organization=None
                ),
                AAAARecord(
                    ipv6='2606:4700:3033::6815:4af4',
                    ipv6_count=0,
                    ipv6_organization=None
                )
            )
        ),
        MX=None,
        NS=BaseRecordInfo(
            first_seen='2024-02-11',
            values=(
                NSRecord(
                    nameserver='shaz.ns.cloudflare.com',
                    nameserver_count=0,
                    nameserver_organization='Cloudflare, Inc.'
                ),
                NSRecord(
                    nameserver='kurt.ns.cloudflare.com',
                    nameserver_count=0,
                    nameserver_organization='Cloudflare, Inc.'
                )
            )
        ),
        SOA=BaseRecordInfo(
            first_seen='2024-02-11',
            values=(
                SOARecord(
                    ttl=10000,
                    email='dns.cloudflare.com',
                    email_count=0
                ),
            )
        ),
        TXT=None
    ),
    alexa_rank=None
)

get_subdomains: SubDomainData(
    count=4,
    subdomains=('aws', 'proxy', 'gateway', 'www')
)

get_history_dns -> A: DnsHistoryData(
    type=<RecordType.A: 'a'>,
    records=(
        HistoryRecordInfo(
            first_seen='2024-02-11',
            values=(
                ARecord(
                    ip='104.21.74.244',
                    ip_count=0,
                    ip_organization=None
                ),
                ARecord(
                    ip='172.67.207.241',
                    ip_count=0,
                    ip_organization=None
                )
            ),
            last_seen='2024-06-05',
            organizations=('Cloudflare, Inc.',)
        ),
        HistoryRecordInfo(
            first_seen='2024-02-01',
            values=(
                ARecord(
                    ip='192.64.119.75',
                    ip_count=0,
                    ip_organization=None
                ),
            ),
            last_seen='2024-02-10',
            organizations=('Namecheap, Inc.',)
        )
    )
)

get_history_dns -> AAAA: DnsHistoryData(
    type=<RecordType.AAAA: 'aaaa'>,
    records=()
)

get_history_dns -> MX: DnsHistoryData(
    type=<RecordType.MX: 'mx'>,
    records=(
        HistoryRecordInfo(
            first_seen='2024-02-01',
            values=(
                MXRecord(
                    priority=10,
                    host='eforward3.registrar-servers.com',
                    host_count=None,
                    hostname_organization=None
                ),
                MXRecord(
                    priority=10,
                    host='eforward2.registrar-servers.com',
                    host_count=None,
                    hostname_organization=None
                ),
                MXRecord(
                    priority=10,
                    host='eforward1.registrar-servers.com',
                    host_count=None,
                    hostname_organization=None
                ),
                MXRecord(
                    priority=15,
                    host='eforward4.registrar-servers.com',
                    host_count=None,
                    hostname_organization=None
                ),
                MXRecord(
                    priority=20,
                    host='eforward5.registrar-servers.com',
                    host_count=None,
                    hostname_organization=None
                )
            ),
            last_seen='2024-02-10',
            organizations=('Namecheap, Inc.',)
        ),
    )
)

get_history_dns -> NS: DnsHistoryData(
    type=<RecordType.NS: 'ns'>,
    records=(
        HistoryRecordInfo(
            first_seen='2024-02-11',
            values=(
                NSRecord(
                    nameserver='kurt.ns.cloudflare.com',
                    nameserver_count=0,
                    nameserver_organization=None
                ),
                NSRecord(
                    nameserver='shaz.ns.cloudflare.com',
                    nameserver_count=0,
                    nameserver_organization=None
                )
            ),
            last_seen='2024-06-05',
            organizations=('Cloudflare, Inc.',)
        ),
        HistoryRecordInfo(
            first_seen='2024-02-01',
            values=(
                NSRecord(
                    nameserver='dns1.registrar-servers.com',
                    nameserver_count=0,
                    nameserver_organization=None
                ),
                NSRecord(
                    nameserver='dns2.registrar-servers.com',
                    nameserver_count=0,
                    nameserver_organization=None
                )
            ),
            last_seen='2024-02-10',
            organizations=('Neustar Security Services', 'NeuStar, Inc.')
        )
    )
)

get_history_dns -> SOA: DnsHistoryData(
    type=<RecordType.SOA: 'soa'>,
    records=(
        HistoryRecordInfo(
            first_seen='2024-02-11',
            values=SOARecord(
                ttl=10000,
                email='dns.cloudflare.com',
                email_count=0
            ),
            last_seen='2024-06-05',
            organizations=('Cloudflare, Inc.',)
        ),
        HistoryRecordInfo(
            first_seen='2024-02-01',
            values=SOARecord(
                ttl=43200,
                email='hostmaster.registrar-servers.com',
                email_count=0
            ),
            last_seen='2024-02-10',
            organizations=('Namecheap, Inc.',)
        )
    )
)

get_history_dns -> TXT: DnsHistoryData(
    type=<RecordType.TXT: 'txt'>, 
    records=(
        HistoryRecordInfo(
            first_seen='2024-02-11', 
            values=(), 
            last_seen='2024-06-09', 
            organizations=()
        ), 
        HistoryRecordInfo(
            first_seen='2024-02-01', 
            values=(
                TXTRecord(
                    value='v=spf1 include:spf.efwd.registrar-servers.com ~all'
                ),
            ), 
            last_seen='2024-02-10', 
            organizations=()
        )
    )
)