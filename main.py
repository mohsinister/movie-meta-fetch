import os
import requests
import json
import re

currentDir = os.getcwd()
print "Your current directory is : " 
print currentDir
flag = raw_input("Is this where your movies are? (y/n): ")

if(flag=="n"):
	currentDir = raw_input("Please input the full address to your directory where movies are.\nDir:\t")

dirs = os.listdir(currentDir)
print dirs
totalmovies = len(dirs)
if "main.py" in dirs:
	totalmovies = totalmovies-1
if "index.html" in dirs:
	totalmovies = totalmovies-1
if "ERRORLOG" in dirs:
	totalmovies = totalmovies-1
if "content.txt" in dirs:
	totalmovies = totalmovies-1
print "Total: {}".format(totalmovies)
counter = 0
errorflag = 0
finaljson = "{\n\t\"data\": \n\t\t[\n"
errorfile = open("ERRORLOG", "w")

for filename in dirs:
    if (filename != 'main.py' and filename!='content.txt' and filename!='index.html' and filename!='ERRORLOG'):
    	originalfile = filename
        filename = filename.replace("(", "")
        filename = filename.replace(")", "")
        filename = filename.replace("[", "")
        filename = filename.replace("]", "")
        filename = filename.replace("1080p", "")
        filename = filename.replace("BluRay","")
        filename = filename.replace("720p", "")
        filename = filename.replace("HDRiP", "")
        filename = filename.replace("WEBRip", "")
        filename = filename.replace("BRRip", "")
        filename = filename.replace(".mp4", "")
        filename = filename.replace(".flv", "")
        filename = filename.replace(".avi", "")
        filename = filename.replace(".mkv", "")
        filename = filename.replace(".txt", "")
        filename = filename.replace("YTS.AG", "")
        filename = filename.replace("YTS.AM", "")
        filename = filename.replace("YTS-AG", "")
        filename = filename.replace("YTS-AM", "")
        filename = filename.replace("."," ")
        years= re.findall('(\d{4})', filename)
        if len(years) > 0:
                moviename = filename[0:filename.find(years[0])]
                moviename = moviename.replace("."," ")
                moviename = moviename.rstrip()
                url = 'http://www.omdbapi.com/?apikey=XXXX&t={0}&y={1}'.format(moviename, years[0])
        else:
                moviename = filename.replace("."," ")
                moviename = moviename.rstrip()
                url = 'http://www.omdbapi.com/?apikey=XXXX&t&t={0}'.format(moviename)
        counter = counter + 1
        fetchedDetails = requests.get(url)
        details = fetchedDetails.content
        json1 = json.loads(details)
        if json1['Response'] == "False":
            errorflag = 1
            errorfile.write(originalfile + " -- API Error : " + json1['Error'] + " URL : " + url + "\n")
        else:
            movieTitle = moviename
            movieYear = ''
            movieRuntime = ''
            movieGenre = ''
            moviePlot = ''
            movieMeta = ''
            movieImdb = ''
            movieActors = ''
            if json1['Runtime'] == "N/A":
            	continue
            if json1['Year']:
                movieYear = json1['Year'].encode('utf-8').replace('"','\\"')
            if (json1['Runtime']):
                movieRuntime = json1['Runtime'].encode('utf-8').replace('"','\\"')
            if json1['Genre']:
                movieGenre = json1['Genre'].encode('utf-8').replace('"','\\"')
            if json1['Plot']:
                moviePlot = json1['Plot'].encode('utf-8').replace('"','\\"')
            if json1['Metascore'] == "N/A":
		movieMeta = 0
	    elif json1['Metascore']:
		movieMeta = json1['Metascore'].encode('utf-8').replace('"','\\"')
            if json1['imdbRating'] == "N/A":
		movieImdb = 0
	    elif json1['imdbRating']:
	        movieImdb = json1['imdbRating'].encode('utf-8').replace('"','\\"')
            if json1['Actors']:
                movieActors = json1['Actors'].encode('utf-8').replace('"','\\"')
            
	    print originalfile + " was successful"

            jsonpart = '\t\t\t["{}","{}","{}","{}","{}","{}","{}","{}","{}"]'.format(counter,movieTitle, movieYear, movieRuntime, movieImdb, movieMeta, moviePlot, movieGenre, movieActors)
            if counter != totalmovies:
                finaljson = ''.join([finaljson, jsonpart, " , \n"])
                # put coma
            else:
                finaljson = ''.join([finaljson, jsonpart])

finaljson = ''.join([finaljson, "\n\t\t]\n}"])
fh = open("content.txt", "w")
fh.write(finaljson)
fh.close()
errorfile.close()