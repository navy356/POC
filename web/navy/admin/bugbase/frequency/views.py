from getopt import gnu_getopt
from django.shortcuts import render,HttpResponse
from urllib3 import HTTPResponse
from .forms import *
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
flag = os.environ['FLAG']
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = None
def index(request):
    if request.method == "GET":
        if request.GET.get('sentence') is None:
            form = FrequencyForm()
            return render(request,'frequency/index.html',{'form':form})
        else:
            form = FrequencyForm(request.GET)
            if form.is_valid():
                data = form.cleaned_data['sentence']
                data = dict(Counter(data))
                print(data)
                return render(request,'frequency/index.html',{'data':data})
            return render(request,'frequency/index.html',{})

def css(request, color):
   """
   Create a css file based on a color criteria,
   or any other complicated calculations necessary
   """
   return render(request,'frequency/dynamic/index.css', {'color': color},content_type='text/css')

def report(request):
    if request.method == "GET":
        global flag
        global options
        global driver
        try:
            path = request.GET.get('path')
            if driver is None:
                driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',options=options)
            else:
                driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
                time.sleep(2)
                driver.delete_all_cookies()
            url = f'http://django:8000/{path}'
            if '?' in path:
                url = url + f'&sentence={flag}'
            else:
                url = url + f'?sentence={flag}'
            driver.get(url)
            time.sleep(60)
            driver.close()
        except Exception as e:
            print(e)
        return HttpResponse("OK")
