#import beautifulsoup and request here
import requests
from bs4 import BeautifulSoup
from pydoc import render_doc
import json

from flask import Flask, render_template
app = Flask(__name__)
app.run(host="My site", port=8000)
@app.route("/")
def displayJobDetails():

    print("Display job details")
    response = requests.get('https://raw.githubusercontent.com/Nehalk145/pythonBeautifulSoup/main/jobDetails.json')
    text = response.text
    responseJSON = json.loads(text)

    return render_template('index.html',responseJSON = responseJSON)
    
#function to get job list from url 'https://www.indeed.com/jobs?q={role}&l={location}'
def getJobList(role,location): 
    url = 'https://www.indeed.com/jobs?q={role}&l={location}'
    url = url.replace("{role}", role)
    url = url.replace("{location}", location)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup2 = soup.find_all('div',class_='job_seen_beacon')

    myArray = []
    
    for i in soup2:
        title = i.find('h2',class_='jobTitle').text
        name = i.find('span',class_='companyName').text
        description = i.find('div',class_='job-snippet').text.replace('\n', '')
        try:
            salary = i.find('div',class_='salary-snippet-container').text
        except:
            salary = 'NA'
        
        myJson = {
            "Title" : title,
            "CompanyName" : name,
            "Description" : description,
            "Salary" : salary
        }
        myArray.append(myJson)
    
    return myArray

#save data in JSON file
def saveDataInJSON(jobDetails):
    with open("jobDetails.json", "w") as outfile:
        json.dump(jobDetails, outfile)