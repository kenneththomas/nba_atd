import requests

date='2021-01-03'
page='1'
x = requests.get('https://www.balldontlie.io/api/v1/stats?dates[]={}&per_page=100&page={}'.format(date,page))
rfn = '{}_pg{}.json'.format(date,page)

print(x.text)
data = x.json()

print('total pages: {} current page: {}'.format(data['meta']['total_pages'],data['meta']['current_page']))

for player in data['data']:

    sevcount = 0
    ddcount = 0

    #print(player)
    points = player['pts']
    blocks = player['blk']
    assists = player['ast']
    rebounds = player['reb']
    steals = player['stl']

    categories = [points,blocks,assists,rebounds,steals]

    for stat in categories:
        if stat >= 7:
            sevcount += 1
        if stat >= 10:
            ddcount += 1

    if sevcount >= 3:
        date = player['game']['date']
        date = date.replace('T00:00:00.000Z','')
        firstname = player['player']['first_name']
        lastname = player['player']['last_name']
        fullname = firstname + ' ' + lastname
        if ddcount <= 2:
            print('{} {} {}pts/{}reb/{}ast/{}blk/{}stl'.format(fullname,date,points,rebounds,assists,blocks,steals))
        else:
            print('{} got an actual triple double'.format(fullname))

