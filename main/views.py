from django.shortcuts import render
from .models import Visitor
from django.utils import timezone
from utils.geoip_helper import GeoIpHelper


def main_page(request):
    record_visit(request)
    return render(request, 'main/main.html')


def record_visit(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        current_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        current_ip = request.META.get('REMOTE_ADDR')
    current_agent = request.META["HTTP_USER_AGENT"]
    current_page = request.get_full_path()
    today = timezone.now()

    visitor_exist = Visitor.objects.filter(ip=str(current_ip), page=current_page, record_date__range=(today.date(), today.date() + timezone.timedelta(days=1)))
    if visitor_exist:
        current_visitor = visitor_exist[0]
        current_visitor.increase_views()
    else:
        current_visitor = Visitor()
        current_visitor.ip = current_ip
        ip_exist = Visitor.objects.filter(ip=str(current_ip)).reverse()
        if ip_exist:
            temp_visitor = ip_exist[0]
            if temp_visitor.region:
                current_visitor.region = temp_visitor.region
        else:
            if current_ip not in ["127.0.0.1", "localhost"]:
                try:
                    temp_region = GeoIpHelper.get_location(current_ip)
                    try:
                        current_visitor.region = ",".join([temp_region["country"], temp_region["city"]])
                    except [KeyError, ValueError]:
                        current_visitor.region = temp_region
                except Exception as e:
                    print("error when get location from ipify, message: %s" % str(e))
        current_visitor.agent = current_agent
        current_visitor.page = current_page
        current_visitor.record_date = today
        current_visitor.update_date = today
        current_visitor.views = 1
        current_visitor.save()
