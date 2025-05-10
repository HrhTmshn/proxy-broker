from argparse import ArgumentParser

from proxybroker.core import ProxyBroker


argparser = ArgumentParser(description="Collects and verifies free proxies from public sources.")

argparser.add_argument('--no-refresh', action='store_true',
                       help="Skip refreshing proxy list")
argparser.add_argument('--limit', type=int,
                       help="Max number of valid proxies to collect")
argparser.add_argument('--queue-quota', type=int, dest='queue_quota',default=20,
                       help="Number of proxies checked in parallel before delay")
argparser.add_argument('--coeff-delay', type=int, dest='coeff_delay', default=20,
                       help="Delay factor for throttling validation speed")
argparser.add_argument('--timeout', type=int, default=5,
                       help="Seconds to wait before marking proxy as dead")

args = argparser.parse_args()

broker = ProxyBroker(
    should_refresh_proxies = not args.no_refresh,
    limit = args.limit,
    queue_quota = args.queue_quota,
    coeff_delay = args.coeff_delay,
    timeout=args.timeout
    )

broker.run()