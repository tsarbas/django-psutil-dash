import typing as t
from datetime import datetime

import humanize
import psutil


class CpuInfo(t.NamedTuple):
    cpu_count: int
    cpu_freq: t.Optional[psutil._common.scpufreq]
    cpu_percent: t.List[float]


class MemoryInfo(t.NamedTuple):
    total: str
    available: str
    percent: float
    used: str
    free: str


class SwapInfo(t.NamedTuple):
    total: str
    percent: float
    used: str
    free: str


class DiskInfo(t.NamedTuple):
    device: str
    mountpoint: str
    fstype: str
    opts: str
    total: str
    used: str
    free: str
    percent: float


class NetworkInfo(t.NamedTuple):
    interface: str
    ip: str


class NetworkInterface(t.NamedTuple):
    interface: str
    ip: str
    bytes_sent: str
    bytes_recv: str
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int


class ConnectionInfo(t.NamedTuple):
    fd: int
    pid: int
    family: str
    type: str
    local_address: str
    remote_address: str
    status: str


class ProcessInfo(t.NamedTuple):
    pid: int
    name: str
    status: str
    username: str
    created: str
    rss: str
    vms: str
    cpu_percent: float
    memory_percent: float


def get_cpu_info() -> CpuInfo:
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(percpu=True)

    return CpuInfo(
        cpu_count=cpu_count,
        cpu_freq=cpu_freq,
        cpu_percent=cpu_percent,
    )


def get_memory_info() -> MemoryInfo:
    memory = psutil.virtual_memory()

    return MemoryInfo(
        total=humanize.naturalsize(memory.total),
        available=humanize.naturalsize(memory.available),
        percent=memory.percent,
        used=humanize.naturalsize(memory.used),
        free=humanize.naturalsize(memory.free),
    )


def get_swap_info() -> SwapInfo:
    swap = psutil.swap_memory()

    return SwapInfo(
        total=humanize.naturalsize(swap.total),
        percent=swap.percent,
        used=humanize.naturalsize(swap.used),
        free=humanize.naturalsize(swap.free),
    )


def get_disks_info() -> t.List[DiskInfo]:
    disks = psutil.disk_partitions()

    return [
        DiskInfo(
            mountpoint=disk.mountpoint,
            device=disk.device,
            fstype=disk.fstype,
            opts=disk.opts,
            total=humanize.naturalsize(psutil.disk_usage(disk.mountpoint).total),
            used=humanize.naturalsize(psutil.disk_usage(disk.mountpoint).used),
            free=humanize.naturalsize(psutil.disk_usage(disk.mountpoint).free),
            percent=psutil.disk_usage(disk.mountpoint).percent,
        )
        for disk in disks
    ]


def get_networks_info() -> t.List[NetworkInfo]:
    if_addrs = psutil.net_if_addrs()

    result = []

    for name, addresses in if_addrs.items():
        for address in addresses:
            if address.family == 2:
                result.append(
                    NetworkInfo(
                        interface=name,
                        ip=address.address,
                    )
                )

    return result


def get_processes() -> t.List[ProcessInfo]:
    result = []

    for process in psutil.process_iter():

        memory_info = process.memory_info()

        result.append(
            ProcessInfo(
                pid=process.pid,
                name=process.name(),
                status=process.status(),
                username=process.username(),
                created=datetime.fromtimestamp(process.create_time()).strftime(
                    "%Y-%m-%d %H:%M:%S",
                ),
                rss=humanize.naturalsize(memory_info.rss),
                vms=humanize.naturalsize(memory_info.vms),
                cpu_percent=process.cpu_percent(),
                memory_percent=process.memory_percent(),
            )
        )

    return result


def get_network_interfaces() -> t.List[NetworkInterface]:
    result = []
    if_addrs = psutil.net_if_addrs()
    io_counter = psutil.net_io_counters(pernic=True)

    for name, addresses in if_addrs.items():
        for address in addresses:
            if int(address.family) != 2:
                continue

            io = io_counter[name]
            result.append(
                NetworkInterface(
                    interface=name,
                    ip=address.address,
                    bytes_sent=humanize.naturalsize(io.bytes_sent),
                    bytes_recv=humanize.naturalsize(io.bytes_recv),
                    packets_sent=io.packets_sent,
                    packets_recv=io.packets_recv,
                    errin=io.errin,
                    errout=io.errout,
                    dropin=io.dropin,
                    dropout=io.dropout,
                )
            )

    return result


def get_connections() -> t.List[ConnectionInfo]:
    result = []

    for connection in psutil.net_connections():
        result.append(
            ConnectionInfo(
                fd=connection.fd,
                pid=connection.pid,
                family=connection.family.name,
                type=connection.type.name,
                local_address=connection.laddr,
                remote_address=connection.raddr,
                status=connection.status,
            )
        )

    return result
