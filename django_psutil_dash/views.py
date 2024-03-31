from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django_psutil_dash import stats


@staff_member_required
def dashboard(request: HttpRequest) -> HttpResponse:
    context = dict(
        cpu_info=stats.get_cpu_info(),
        memory_info=stats.get_memory_info(),
        swap_info=stats.get_swap_info(),
        disks_info=stats.get_disks_info(),
        network_info=stats.get_networks_info(),
    )
    return render(request, 'psutildash/dashboard.html', context)


@staff_member_required
def processes(request: HttpRequest) -> HttpResponse:
    context = dict(
        processes=stats.get_processes(),
    )
    return render(request, 'psutildash/processes.html', context)


@staff_member_required
def network(request: HttpRequest) -> HttpResponse:
    context = dict(
        interfaces=stats.get_network_interfaces(),
        connections=stats.get_connections(),
    )
    return render(request, 'psutildash/network.html', context)


@staff_member_required
def disks(request: HttpRequest) -> HttpResponse:
    context = dict(
        disks=stats.get_disks_info(),
    )
    return render(request, 'psutildash/disks.html', context)
