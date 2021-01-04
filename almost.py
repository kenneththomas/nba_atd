import requests

date='2021-01-03'

def find_atd(data):
    for player in data['data']:

        sevcount = 0
        ddcount = 0

        # print(player)
        points = player['pts']
        blocks = player['blk']
        assists = player['ast']
        rebounds = player['reb']
        steals = player['stl']

        categories = [points, blocks, assists, rebounds, steals]

        for stat in categories:
            if stat >= 7:
                sevcount += 1
            if stat >= 10:
                ddcount += 1

        if sevcount >= 3:
            date = player['game']['date']
            date = date.replace('T00:00:00.000Z', '')
            firstname = player['player']['first_name']
            lastname = player['player']['last_name']
            fullname = firstname + ' ' + lastname
            if ddcount <= 2:
                print('{} {} {}pts/{}reb/{}ast/{}blk/{}stl'.format(fullname, date, points, rebounds, assists, blocks,
                                                                   steals))
            else:
                print('{} got an actual triple double'.format(fullname))

def main():

    x = requests.get('https://www.balldontlie.io/api/v1/stats?dates[]={}&per_page=100&page=1'.format(date))
    data = x.json()
    pages = data['meta']['total_pages']

    '''
    todo: under this logic we make the page 1 request twice
    the first time is to find out how many total pages there are
    the second time is to actually perform the calculations
    ideally we don't repeat that first request however the rate limit is like 60/min
    we should not come close to hitting that
    '''
   
    for pageno in range(1,pages):
        x = requests.get('https://www.balldontlie.io/api/v1/stats?dates[]={}&per_page=100&page={}'.format(date, pageno))
        data = x.json()
        find_atd(data)

main()

