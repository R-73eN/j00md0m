import os
import sys
import requests
banner = "\n For Education Purposes Only..... \n"
banner +="  ___        __        ____                 _    _  \n"   
banner +=" |_ _|_ __  / _| ___  / ___| ___ _ __      / \  | |    \n"
banner +="  | || '_ \| |_ / _ \| |  _ / _ \ '_ \    / _ \ | |    \n"
banner +="  | || | | |  _| (_) | |_| |  __/ | | |  / ___ \| |___ \n"
banner +=" |___|_| |_|_|  \___/ \____|\___|_| |_| /_/   \_\_____|\n\n"
print banner
def Check(url):
	r = requests.get(url + '/administrator/')
	if(r.status_code != 404 or  r.status_code != 403):
		print '[ + ] Administration Directory Found [ + ]\n'
def INIT(url):
	r = requests.get(url)
	if(r.status_code == 200):
		print '[ + ] Connected To Host [ + ]\n'
		print '[ + ] ' + r.headers['Server'] + ' [ + ]\n'
		findversion(url)

def findversion(url):
	Check(url)
	print "[ + ] Getting Joomla Version [ + ]\n"
	try:
 		r = requests.get(url + '/administrator/manifests/libraries/joomla.xml');
		if (r.status_code == 200):
			
			data = r.content
			data1 = data.split('<extension type="library" version="')
			data = data1[1]
			data1 = data.split('">')
			print '[ + ] Joomla Version ' + data1[0] + ' [ + ] \n '
			Check(url)
			Killer(url)
			
		else:

			print "[ - ] ... Error Getting joomla version ... [ - ]\n"
			Check(url)
			Killer(url)
	except Exception:
		
		print "[ - ] Error Getting joomla version ..... [ - ]\n"
		
		Killer(url)
def Killer(url):
	try:
		f = open('components.src','r')
		for line in f.readlines():
			temp = line.split(":")
			try:
				r = requests.get(url + temp[2])
				if(temp[1] == 'SQL injection'):
					if (r.status_code != 404 and r.status_code != 403 ):
						d = r.content
						l = d.find("Page not found")
						if(l != -1 or r.content == "" or d.find("404") != -1  or d.find("The requested page cannot be found.") != -1 or d.find("404 - Category not found") != -1):
							print 'sql'
						else:
							d = r.content
							l = d.find("SQL syntax")
							if (l != -1 or d.find("error number 1064") or d.find("Error number: 1064") != 1 or d.find("SQL") != -1 or d.find("SQL error")  != -1 or d.find("sql")  != -1):
								print '[ + ] Vulnerability ' + temp[0] + ' ' + temp[1] + ' [ + ]\n'
				else:
					if (r.status_code != 404 and r.status_code != 403 ):
			
						d = r.content
						l = d.find("404")
						if(l != -1 or d.find("404") != -1  or d.find("Faqja nuk u gjet") != -1 or d.find("The requested page cannot be found.") != -1 or d.find("404 - Category not found") != -1):
							print ''
						else:
							print '[ + ] False/Positive : ' + temp[0] + ' ' + temp[1] + ' [ + ]\n'
			except Exception:
				print '[ - ] Error while scanning.....[ - ]\n'
					
	except Exception:
		print "[ - ] ERROR components.src not found ..[ - ]"

if (len(sys.argv) < 2):
	print "usage : python j00md0m.py http://yourwebsite.com/ "
else:
	INIT(sys.argv[1])
	print 'Scanning finished...... Visit us : http://infogen.al/'
