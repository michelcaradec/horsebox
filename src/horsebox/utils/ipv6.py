import socket
from contextlib import contextmanager
from typing import (
    Any,
    Generator,
    List,
    Tuple,
)


@contextmanager
def ipv6_disabled(*args, **kwds) -> Generator[None, Any, None]:
    """IPv6 disabling context manager."""
    getaddrinfo = socket.getaddrinfo

    def _getaddrinfo_ipv4_only(
        host: str,
        port: int,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> List[Tuple]:
        return getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    # Disable IPv6
    socket.getaddrinfo = _getaddrinfo_ipv4_only
    try:
        yield
    finally:
        socket.getaddrinfo = getaddrinfo
