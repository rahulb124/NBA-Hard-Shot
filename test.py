import requests  
import json  
import pandas as pd
import webbrowser
import urllib
from flask import Flask
import flask
from flask import render_template





teams ={'east':{  
                   'Lebron James':'2544',
                   'Giannis Antetokounmpo':'203507',
                   'Carmelo Anthony':'2546',
                   'Jimmy Butler':'202710',
                   'Paul George':'202331',
                   'Kyrie Irving':'202681',
                   'DeMar DeRozan':'201942',
                   'Isaiah Thomas':'202738',
                   'Dwayne Wade':'2548',
                   'Derrick Rose':'201565',
                   'John Wall':'202322'
                   },
        'west':{
                   'Kevin Durant': '201142',
                   'Kawhi Leonard': '202695',
                   'Draymond Green': '203110',
                   'Demarcus Cousins': '202326',
                   'Stephen Curry': '201939',
                   'James Harden': '201935',
                   'Russell Westbrook': '201566',
                   'Klay Thompson': '202691',
                   'Chris Paul': '101108',
                   'Damian Lillard': '203081',
                   'Manu Ginobli': '1938'
                   }
                  }
players = []
lost = []

player_stats = {'name':None,'dribblecount':None,'touchtime':None,'defdistance':None,'clockdiff':None,'score':None}
player_sucks = {'name':None,'percentage2':None,'attempts2':None,'percentage3':None,'attempts3':None}

def find_stats(name,player_id):  
    #NBA Stats API using selected player ID

    score = 0
    headers = {'User-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}
    shots_url = 'http://stats.nba.com/stats/playerdashptshots?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=Totals&Period=0&PlayerID='+player_id+'&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='
    webbrowser.open('http://stats.nba.com/stats/playerdashptshots?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=Totals&Period=0&PlayerID='+player_id+'&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=')
    # request the URL and parse the JSON
    response = requests.get(shots_url)
    response.raise_for_status() # raise exception if invalid response
    shots = response.json()['resultSets'][2]['rowSet']
    data = json.loads(response.text)
    #Create df from data and find averages 
    headers = data['resultSets'][0]['headers']
    clockshot_data = data['resultSets'][2]['rowSet'][5]
    defender_data = data['resultSets'][5]['rowSet'][0]
    dribble_data = data['resultSets'][3]['rowSet'][3]
    touch_data = data['resultSets'][6]['rowSet'][2]

    if(clockshot_data[14] == None):
      clockshot_data[14] = 0
    if(clockshot_data[18] == None):
      clockshot_data[18] = 0
    if(defender_data[14] == None):
      defender_data[14] = 0
    if(defender_data[18] == None):
      defender_data[18] = 0
    if(dribble_data[14] == None):
      dribble_data[14] = 0
    if(dribble_data[18] == None):
      dribble_data[18] = 0
    if(touch_data[14] == None):
      touch_data[14] = 0
    if(touch_data[18] == None):
      touch_data[18] = 0



    clockdiff = (clockshot_data[14] * clockshot_data[12] * 2) + (clockshot_data[18] * clockshot_data[16] * 3)
    defdistance = (defender_data[14] * defender_data[12] * 2) + (defender_data[18] * defender_data[16]* 3)
    dribblecount = (dribble_data[14]* dribble_data[12] * 1) + (dribble_data[18] * dribble_data[16]* 3)
    touchtime = (touch_data[14]* touch_data[12] * 2) + (touch_data[18]* touch_data[16] * 3)
    score = clockdiff + defdistance + dribblecount + touchtime
    a2 = clockshot_data[13]
    a3 = clockshot_data[17]
    p2 = clockshot_data[14] * 100
    p3 = clockshot_data[18] * 100

    #add Averages to dictionary then to list
    player_stats['name'] = name
    player_stats['clockdiff']=clockdiff
    player_stats['defdistance'] = defdistance
    player_stats['touchtime'] = touchtime
    player_stats['dribblecount'] = dribblecount
    player_stats['score']= score
    player_sucks['percentage2'] = p2
    player_sucks['percentage3'] = p3
    player_sucks['attempts2'] = a2
    player_sucks['attempts3'] = a3
    lost.append(player_sucks.copy())
    players.append(player_stats.copy())


x = 1
if (x == 1):    
  for x in teams:  
    for y in teams[x]:
        find_stats(y,teams[x][y])


cols = ['name','clockdiff','dribblecount','defdistance','touchtime','score'] 
cols2 = ['name'] 


players = [ {"dribblecount": 33.342, "name": "Damian Lillard", "defdistance": 7.775, "score": 161.68099999999998, "touchtime": 111.316, "clockdiff": 9.248}, {"dribblecount": 33.104, "name": "Stephen Curry", "defdistance": 14.266, "score": 103.468, "touchtime": 52.99000000000001, "clockdiff": 3.1079999999999997}, {"dribblecount": 13.615, "name": "Demarcus Cousins", "defdistance": 5.0, "score": 55.545, "touchtime": 19.756, "clockdiff": 17.174}, {"dribblecount": 12.953, "name": "Klay Thompson", "defdistance": 5.233, "score": 27.185000000000002, "touchtime": 7.9990000000000006, "clockdiff": 1.0}, {"dribblecount": 5.5600000000000005, "name": "Draymond Green", "defdistance": 4.0, "score": 22.887999999999998, "touchtime": 7.0, "clockdiff": 6.328}, {"dribblecount": 87.06299999999999, "name": "James Harden", "defdistance": 13.303999999999998, "score": 260.19599999999997, "touchtime": 143.017, "clockdiff": 16.812}, {"dribblecount": 38.28, "name": "Kevin Durant", "defdistance": 8.628, "score": 101.04599999999999, "touchtime": 46.4, "clockdiff": 7.738}, {"dribblecount": 46.746, "name": "Chris Paul", "defdistance": 1.7159999999999997, "score": 150.777, "touchtime": 93.672, "clockdiff": 8.643}, {"dribblecount": 63.554, "name": "Russell Westbrook", "defdistance": 5.166, "score": 204.536, "touchtime": 127.338, "clockdiff": 8.478}, {"dribblecount": 10.239000000000003, "name": "Manu Ginobli", "defdistance": 0.5, "score": 21.234, "touchtime": 6.998, "clockdiff": 3.4970000000000003}, {"dribblecount": 32.173, "name": "Kawhi Leonard", "defdistance": 4.8999999999999995, "score": 91.54499999999999, "touchtime": 39.736, "clockdiff": 14.736}, {"dribblecount": 28.592000000000002, "name": "Jimmy Butler", "defdistance": 15.822, "score": 109.755, "touchtime": 58.348, "clockdiff": 6.993}, {"dribblecount": 23.113999999999997, "name": "Carmelo Anthony", "defdistance": 14.669999999999998, "score": 90.64399999999999, "touchtime": 39.372, "clockdiff": 13.488}, {"dribblecount": 49.017, "name": "Isaiah Thomas", "defdistance": 4.476, "score": 133.873, "touchtime": 75.00999999999999, "clockdiff": 5.37}, {"dribblecount": 39.3, "name": "Kyrie Irving", "defdistance": 9.747, "score": 172.343, "touchtime": 114.63799999999999, "clockdiff": 8.658000000000001}, {"dribblecount": 31.61, "name": "Dwayne Wade", "defdistance": 13.524, "score": 93.667, "touchtime": 44.196000000000005, "clockdiff": 4.337}, {"dribblecount": 41.4, "name": "Derrick Rose", "defdistance": 0.8, "score": 104.63, "touchtime": 52.908, "clockdiff": 9.522}, {"dribblecount": 47.076, "name": "John Wall", "defdistance": 1.6380000000000001, "score": 198.789, "touchtime": 142.545, "clockdiff": 7.53}, {"dribblecount": 25.803, "name": "Paul George", "defdistance": 4.17, "score": 72.55, "touchtime": 29.839, "clockdiff": 12.738}, {"dribblecount": 61.047000000000004, "name": "Lebron James", "defdistance": 4.5, "score": 190.164, "touchtime": 101.023, "clockdiff": 23.594}, {"dribblecount": 72.38, "name": "DeMar DeRozan", "defdistance": 32.039, "score": 244.058, "touchtime": 126.487, "clockdiff": 13.152000000000001}, {"dribblecount": 35.343, "name": "Giannis Antetokounmpo", "defdistance": 2.912, "score": 101.10300000000001, "touchtime": 46.393, "clockdiff": 16.455000000000002}]

app = Flask(__name__)

@app.route("/")
def dump():
  return json.dumps(lost)

@app.route('/p')
def player():
    return render_template('players.html')

@app.route('/s')
def sort():
    return render_template('sort.html')  

@app.route('/a')
def about():
    return render_template('about.html')  

@app.route('/c')
def compare():
    return render_template('compare.html')  

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
#df = pd.DataFrame(players,columns = cols)
#df = df.sort_values(by=['score'], ascending=False)
#df1 = df[cols2]
#df.head()
#df1.head()
#print(df1)

