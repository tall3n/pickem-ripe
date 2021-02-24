from pickem import Pickem


def example() -> str:
    ip = "199.127.92.0"
    p = Pickem(ip)
    found, found_cidr = p.find_ip()
    print(found, found_cidr)


example()
