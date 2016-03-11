from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from core.vendor.tsto.tsto import TSTO
import json

core_tsto = TSTO()

def index(request):
  if not core_tsto.mLogined:
    return HttpResponseRedirect('/login')
  return render_to_response(
    'index.html',
    {
      'is_login': core_tsto.mLogined,
      'user': core_tsto.mUserId
    },
    context_instance=RequestContext(request)
  )

def item(request):
  if not core_tsto.mLogined:
    return HttpResponseRedirect('/login')
  return render_to_response(
    'item.html',
    {},
    context_instance=RequestContext(request)
  )

def login(request):
  return render_to_response(
    'login.html',
    {},
    context_instance=RequestContext(request)
  )

def auth(request):
  if request.POST:
    user = request.POST['username']
    psw = request.POST['password']
    try:
      core_tsto.doAuth(['', user, psw])
      if core_tsto.mLogined:
        return HttpResponseRedirect('/')
    except Exception, e:
      print 'Error: ', e

  return HttpResponseRedirect('/login/')

def add_item(request):
  if not core_tsto.mLogined:
    return HttpResponseRedirect('/login')
  return render_to_response(
    'add.html',
    {
      'is_login': core_tsto.mLogined,
    },
    context_instance=RequestContext(request)
  )

def add_donuts(request):
  status = 200
  if request.is_ajax():
    quantity = request.POST['add_donuts']
    try:
      core_tsto.doLandDownload()
      core_tsto.donutsAdd(['', quantity])
      core_tsto.doLandUpload()
    except Exception, e:
      print 'Error: ', e
      status = 500

    dataReturn = {
      'status': status
    }

    return HttpResponse(json.dumps(dataReturn), mimetype='application/json')
  else:
    return HttpResponseRedirect('/')