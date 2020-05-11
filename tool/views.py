from django.shortcuts import render
from .models import Visitor
from django.utils import timezone
from utils.geoip_helper import GeoIpHelper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


def tool_main_page(request):
    record_visit(request)
    return render(request, 'tool/main.html')


def tool_query(request):
    allowed_id = ["ProtectAnimal2020", "Ghost-13544325255"]
    request.session['validate_error'] = False
    if request.method == 'GET':
        record_visit(request)
        return render(request, 'tool/tool_query.html')
    elif request.method == 'POST':
        id = request.POST["id-number"]
        keyword = request.POST["key-word"]
        if id in allowed_id:
            record_visit(request, page_suffix=f"/verify=true&id={id}&search={keyword}")
            captured_data = capture_from_defined_websites(keyword)
            return render(request, 'tool/tool_query.html', {"data": captured_data})
        else:
            record_visit(request, page_suffix=f"/verify=false&id={id}&search={keyword}")
            request.session['validate_error'] = "错误身份信息"
            return render(request, 'tool/tool_query.html')


def capture_from_defined_websites(keyword):
    if keyword.find("@") >= 0:
        keyword = keyword.replace("@", "%40")
    data = {"reg": [], "pwned": [], "sjk": [], "alarm": []}
    urls = {"reg": f"https://www.reg007.com/search?q={keyword}",
            "pwned": f"https://haveibeenpwned.com/unifiedsearch/{keyword}",
            "sjk": "http://site3.sjk.space/",
            "alarm": "https://breachalarm.com/"}
    driver = None
    # reg007
    try:
        driver = webdriver.PhantomJS("./tool/phantomjs")
        driver.get(urls["reg"])
        name_elements = driver.find_elements(By.XPATH, "//ul[@id='site_list']//li[contains(@id, 'li_') and @data-category]//h4[@class='media-heading']/a")
        desc_elements = driver.find_elements(By.XPATH, "//ul[@id='site_list']//li[contains(@id, 'li_') and @data-category]//p[@class='site-desc']")
        for seq in range(len(name_elements)):
            data["reg"].append([keyword.replace("%40", "@"), name_elements[seq].text, desc_elements[seq].text])
    except Exception as e:
        print("has error when query reg: %s", str(e))
        driver.quit()
    if driver:
        driver.quit()
    # haveibeenpwned
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Connection': 'keep-alive'
        }
        cap = DesiredCapabilities.PHANTOMJS.copy()
        for key, value in headers.items():
            cap['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS("./tool/phantomjs", desired_capabilities=cap)
        driver.get(urls["pwned"])
        breaches = driver.find_element(By.XPATH, "//html/body/pre")
        new_breach = json.loads(breaches.text)
        for b in new_breach["Breaches"]:
            if b["Domain"]:
                data["pwned"].append([keyword.replace("%40", "@"), b["Domain"], b["Description"]])
            else:
                data["pwned"].append([keyword.replace("%40", "@"), b["Name"], b["Description"]])
    except Exception as e:
        print("has error when query haveibeenpwned: %s" % str(e))
        driver.quit()
    if driver:
        driver.quit()
    # print(data)
    return data


def record_visit(request, page_suffix=""):
    try:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            current_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            current_ip = request.META.get('REMOTE_ADDR')
        if "HTTP_USER_AGENT" in request.META:
            current_agent = request.META["HTTP_USER_AGENT"]
        else:
            current_agent = "no agent key in request"
        current_page = request.get_full_path() + page_suffix
        today = timezone.now()

        visitor_exist = Visitor.objects.filter(ip=str(current_ip), page=current_page, record_date__range=(today.date(), today.date() + timezone.timedelta(days=1)))
        if visitor_exist:
            current_visitor = visitor_exist[0]
            current_visitor.increase_views()
        else:
            current_visitor = Visitor()
            current_visitor.ip = current_ip
            ip_exist = Visitor.objects.filter(ip=str(current_ip)).order_by('-id')
            generate_new_location = True
            if ip_exist:
                generate_new_location = False
                temp_visitor = ip_exist[0]
                if (today - temp_visitor.record_date).days >= 7:
                    generate_new_location = True
                if temp_visitor.region:
                    current_visitor.region = temp_visitor.region
            if generate_new_location:
                if current_ip not in ["127.0.0.1", "localhost"]:
                    try:
                        current_visitor.region = GeoIpHelper.get_location(current_ip)
                    except Exception as e:
                        print("error when get location from ipify, message: %s" % str(e))
            current_visitor.agent = current_agent
            current_visitor.page = current_page
            if 'HTTP_REFERER' in request.META.keys():
                temp_referer = request.META["HTTP_REFERER"]
                temp_host = request.get_host()
                if temp_host not in temp_referer.split("/"):
                    current_visitor.referer = temp_referer
            current_visitor.record_date = today
            current_visitor.update_date = today
            current_visitor.views = 1
            current_visitor.save()
    except Exception as e:
        print("get error when record visitor, message: %s" % str(e))
        with open("./record_visitor_error.txt", "a") as f:
            f.write(str(timezone.now()))
            f.write("\n")
            f.write(str(e))
            f.write("\n\n")