import requests
import datetime

# yesterday's date in the format YYYY-MM-DD
date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')


def find_atd(data):
    for player in data['data']:
        sevcount = 0
        ddcount = 0

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
            date = player['game']['date'].replace('T00:00:00.000Z', '')
            fullname = f"{player['player']['first_name']} {player['player']['last_name']}"

            if ddcount <= 2:
                print(f"{fullname} {date} {points}pts/{rebounds}reb/{assists}ast/{blocks}blk/{steals}stl")
            else:
                print(f"{fullname} got an actual triple double")


def main():
    url = f"https://www.balldontlie.io/api/v1/stats?dates[]={date}&per_page=100&page="

    response = requests.get(url + "1")
    data = response.json()
    pages = data['meta']['total_pages']

    find_atd(data)

    for pageno in range(2, pages + 1):
        response = requests.get(url + str(pageno))
        data = response.json()
        find_atd(data)


main()