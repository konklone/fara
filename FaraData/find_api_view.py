# This Python file uses the following encoding: utf-8
import requests
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from FaraData.models import Recipient

from fara.local_settings import apikey

def cleantext(text):
	if text!= None:
	    text = re.sub(' +',' ', text)
	    text = re.sub('\\r|\\n','', text)
	    text = text.strip()
	    return text
	else:
		return None

@login_required(login_url='/admin')
def find_form(request):
 	return render(request, 'FaraData/api_lookup.html') 

@login_required(login_url='/admin')        
def find_member(request):
	q = request.GET['member'],

	query_params = { 'query': q,
					'apikey': apikey,
					'per_page': 50,
	               }

	# it defaults to currently in office, so need this one too
	old_query_params = { 'query': q,
					'apikey': apikey,
					'in_office': 'false',
					'per_page': 50,
	               }

	endpoint = 'http://congress.api.sunlightfoundation.com/legislators'
	response = requests.get(endpoint, params=query_params)
	response_old = requests.get(endpoint, params=old_query_params)
	response_url = response.url

	results = []

	def read_response(data, time):
		for d in data["results"]:
			crp_id = d['crp_id']
			if len(crp_id) > 1:
				chamber = str(d['chamber']).capitalize()
				if chamber == 'Senate':
					title = "Sen. "
				elif chamber == 'House':
					title = "Rep. "
				else:
					title = ''
				
				first_name =  d['first_name']
				last_name = d['last_name']
				full_name = "%s %s" %(first_name, last_name)
				party = d['party']
				crp_id = d['crp_id']
				bioguide_id = d['bioguide_id']
				state = d['state']
				
				if time == 'old':
					text = "%s %s %s (%s-%s) (NOT in office) CRP ID = %s" %(title, first_name, last_name, party, state, crp_id) 
				else:
					text = "%s %s %s (%s-%s) CRP ID = %s" %(title, first_name, last_name, party, state, crp_id) 
				
				result = [crp_id, "Congress", chamber,  full_name, title, text, bioguide_id]
				results.append(result)

	data = response.json()
	old_data = response_old.json()

	read_response(data, "new")
	read_response(old_data, "old")

	accent_dict = {"MENENDEZ": "Menéndez", "VALAZQUEZ": "Velázquez" , "SANCHEZ": "Sánchez", "LUJAN": "Luján", "GUTIERREZ": "Gutiérrez", "CARDENAS":"Cárdenas"}
	name_variation = q[0].upper()
	if accent_dict.has_key(name_variation):
		r = accent_dict[name_variation]
		query={ 'query': r,
					'apikey': apikey,
					'per_page': 50,
	               }
		response = requests.get(endpoint, params=query)
		accent_data = response.json()
		read_response(accent_data, "accent")

	return render(request, 'FaraData/api_lookup.html', {'results': results}) 

@login_required(login_url='/admin')
def add_member(request):
	member = Recipient(crp_id = request.GET['crp_id'],
						bioguide_id= request.GET['bioguide_id'],
					    agency = request.GET['agency'],
					    office_detail = request.GET['office_detail'],
					    name = request.GET['name'],
					    title = request.GET['title'],
	)
	if Recipient.objects.filter(crp_id = member.crp_id, agency="Congress").exists():
		message = member.name
		return render(request, 'FaraData/api_lookup.html', {'insystem': message})
	else:
		member.save()
		return render(request, 'FaraData/api_lookup.html', {'member': member.name})

@login_required(login_url='/admin')
def add_staff(request):
	agency = request.GET['agency']
	member_name = request.GET['office_detail']
	if agency == "House":
		member_name = "Rep. " + member_name
	elif agency == "Senate":
		member_name = "Sen. " + member_name

	staff = Recipient(crp_id = request.GET['crp_id'],
						bioguide_id = request.GET['bioguide_id'],
					    agency = request.GET['agency'],
					    office_detail = member_name,
					    name = cleantext(request.GET['name']),
					    title = cleantext(request.GET['title']),
	)
	if Recipient.objects.filter(crp_id=staff.crp_id, name=staff.name).exists():
		message = staff.name + " of " + staff.office_detail + " CRP id : " + staff.crp_id 
		return render(request, 'FaraData/api_lookup.html', {'insystem': message})
	else:
		staff.save()
		message = staff.name + " of " + staff.office_detail + "'s office"
		return render(request, 'FaraData/api_lookup.html', {'member': message})

@login_required(login_url='/admin')
def add_leader_PAC(request):
	member_name = request.GET['office_detail']
	agency = request.GET['agency']
	if agency == "House":
		member_name = "Rep. " + member_name
	elif agency == "Senate":
		member_name = "Sen. " + member_name

	staff = Recipient(crp_id = request.GET['crp_id'],
						bioguide_id = request.GET['bioguide_id'],
					    agency = "Leadership PAC",
					    office_detail = member_name,
					    name = cleantext(request.GET['PAC_name']),
	)
	
	if Recipient.objects.filter(crp_id=staff.crp_id, name=staff.name).exists():
		message = staff.name + " of " + staff.office_detail + " CRP id : " + staff.crp_id 
		return render(request, 'FaraData/api_lookup.html', {'insystem': message})
	else:
		staff.save()
		message = staff.name + " of " + staff.office_detail + "'s office"
		return render(request, 'FaraData/api_lookup.html', {'member': message})



