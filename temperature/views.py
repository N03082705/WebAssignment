from __future__ import unicode_literals

import os
import time
from django.http import JsonResponse
from django.shortcuts import render
from .models import TempReading
from django.utils.dateparse import parse_datetime

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-00000698fc00/w1_slave")
	tempfile_text = tempfile.read()
	currentTime=time.strftime('%x %X %Z')
	tempfile.close()
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC*9.0/5.0+32.0
	return {
		'date':currentTime,
		'tempf':tempF
	}

def index(request):
	return render(request, 'mainpage.html', {})

def api(request):
	if request.method == 'POST':
		input_from = parse_datetime(request.POST.get('from'))
		input_to = parse_datetime(request.POST.get('to'))
		
		values = TempReading.objects.filter(date__gt=input_from, date__lt=input_to)
		return JsonResponse([{'date': v.date.isoformat(), 'temp': v.reading} for v in values])
	else:
		return JsonResponse(readTemp())
