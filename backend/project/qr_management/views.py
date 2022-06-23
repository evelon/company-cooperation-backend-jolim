from random import choice, random
from django.http import HttpResponse
from django.shortcuts import render
from .models import LocationQrCode

def test_create(request, location_id):
    lat = ( random() - 0.5 ) * 90
    lon = ( random() - 0.5 ) * 180
    if id is None:
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon)
    else:
        presence = LocationQrCode.objects.filter(id=location_id)
        if len(presence) != 0:
            return HttpResponse('The id is preoccupied')
        location_qr_code = LocationQrCode(latitude=lat, longitude=lon, id=location_id)
    location_qr_code.save()
    return HttpResponse('success')



def test_read_plain(request):
    all_location_qr_code = LocationQrCode.objects.all()
    list = ''
    for location_qr_code in all_location_qr_code:
        list = f'{location_qr_code.id}\towner:{location_qr_code.owner}' + \
            f'\tlatitude:{location_qr_code.latitude}' + \
            f'\tlongitude:{location_qr_code.longitude}' + \
            f'\tvalidity:{location_qr_code.validity}\n'
    return HttpResponse(list)


def test_read(request, location_id):
    location_qr_codes = LocationQrCode.objects.filter(id=location_id)
    if len(location_qr_codes) == 0:
        return HttpResponse('No matching object.')
    location_qr_code = location_qr_codes.first()
    info = f'{location_qr_code.id}\towner:{location_qr_code.owner}' + \
        f'\tlatitude:{location_qr_code.latitude}' + \
        f'\tlongitude:{location_qr_code.longitude}' + \
        f'\tvalidity:{location_qr_code.validity}\n'
    return HttpResponse(info)


def test_update(request, location_id):
    location_qr_codes = LocationQrCode.objects.filter(id=location_id)
    if len(location_qr_codes) == 0:
        return HttpResponse('No matching object')
    location_qr_code = location_qr_codes.first()
    location_qr_code.latitude = ( random() - 0.5 ) * 90
    location_qr_code.longitude = ( random() - 0.5 ) * 180
    location_qr_code.save()
    info = f'{location_qr_code.id}\towner:{location_qr_code.owner}' + \
            f'\tlatitude:{location_qr_code.latitude}' + \
            f'\tlongitude:{location_qr_code.longitude}' + \
            f'\tvalidity:{location_qr_code.validity}\n'
    return HttpResponse(info)


def test_delete(request, location_id):
    location_qr_codes = LocationQrCode.objects.filter(id=location_id)
    if len(location_qr_codes) == 0:
        return HttpResponse('No matching object')
    location_qr_code = location_qr_codes.first()
    location_qr_code.delete()
    return HttpResponse('success')
