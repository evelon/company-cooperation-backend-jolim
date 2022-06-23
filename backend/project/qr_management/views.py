from random import choice, random
from django.http import HttpResponse
from django.shortcuts import render
from .models import LocationQrCode

def test_create(request):
    lat = ( random() - 0.5 ) * 90
    lon = ( random() - 0.5 ) * 180
    location_qr_code = LocationQrCode(latitude=lat, longitude=lon)
    location_qr_code.save()
    return HttpResponse('success')

def test_read(request):
    all_location_qr_code = LocationQrCode.objects.all()
    list = ''
    for location_qr_code in all_location_qr_code:
        list = f'{location_qr_code.id}\towner:{location_qr_code.owner}' + \
            f'\tlatitude:{location_qr_code.latitude}' + \
            f'\tlongitude:{location_qr_code.longitude}' + \
            f'\tvalidity:{location_qr_code.validity}\n'
    return HttpResponse(list)

def test_update(request):
    all_location_qr_code = LocationQrCode.objects.all()
    if len(all_location_qr_code) == 0:
        return HttpResponse('table is empty')
    location_qr_code = choice(all_location_qr_code)
    location_qr_code.latitude = ( random() - 0.5 ) * 90
    location_qr_code.longitude = ( random() - 0.5 ) * 180
    location_qr_code.save()
    info = f'{location_qr_code.id}\towner:{location_qr_code.owner}' + \
            f'\tlatitude:{location_qr_code.latitude}' + \
            f'\tlongitude:{location_qr_code.longitude}' + \
            f'\tvalidity:{location_qr_code.validity}\n'
    return HttpResponse(info)

def test_delete(request):
    all_location_qr_code = LocationQrCode.objects.all()
    if len(all_location_qr_code) == 0:
        return HttpResponse('table is empty')
    location_qr_code = choice(all_location_qr_code)
    location_qr_code.delete()
    return HttpResponse('success')