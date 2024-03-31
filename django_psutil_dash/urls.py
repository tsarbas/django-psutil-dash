from django.urls import include, path

from django_psutil_dash import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('processes/', views.processes, name='processes'),
    path('network/', views.network, name='network'),
    path('disks/', views.disks, name='disks'),
]


def psutil_urlpatterns():
    return include(
        (
            'django_psutil_dash.urls',
            'django_psutil_dash',
        ),
        namespace='django_psutil_dash',
    )
