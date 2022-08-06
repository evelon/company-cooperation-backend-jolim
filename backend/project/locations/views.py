from django.shortcuts import render, get_object_or_404, redirect
from locations.forms import LocationForm
from locations.models import Location
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
import qrcode.image.svg
from urllib import parse
from io import BytesIO


def create_location(request):
    if request.method == 'POST':
        location = Location(owner=request.user)
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return render(request, 'qrcode/create.html', {'form': form, 'created': True})
    else:
        form = LocationForm()
    return render(request, 'qrcode/create.html', {'form': form})


def list_location(request):
    location_list = Location.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'qrcode/list.html', {'location_list': location_list})


@login_required(login_url='accounts/login')
def delete_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.user != location.owner:
        messages.error(request, '삭제권한이 없습니다')
    else:
        location.delete()
    return redirect('qrcode:list')


def url_builder(url: str, path: str, params: dict[str, any]) -> str:
    if url[-1] != '/':
        url += '/'
    return f'{url}{path}?{parse.urlencode(params)}'


def make_svg_qrcode(url: str) -> str:
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)
    stream = BytesIO()
    img.save(stream)
    return stream.getvalue().decode()


def generate_qrcode(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.user != location.owner:
        messages.error(request, '생성권한이 없습니다')
        return redirect('common:home')
    params = {'latitude': location.latitude, 'longitude': location.longitude}
    url = url_builder('https://pandemicguardgg.page.link', 'qr', params)
    svg = make_svg_qrcode(url)
    context = {'svg': svg, 'location': location}
    return render(request, 'qrcode/generate.html', context=context)

