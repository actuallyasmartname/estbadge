import httpx as r
import datetime
plr = int(input("Input the UserID of the player: "))
date = input("Input the date you want to travel back to (YYYY-MM-DD, ex. 2022-12-24): ")
year, month, day = map(int, date.split('-'))
date1 = datetime.date(year, month, day)
hunnidlist = []
count = 0
done = False
c = ""
while True:
    badgecnt = r.get(f"https://badges.roblox.com/v1/users/{plr}/badges?limit=100&cursor={c}&sortOrder=Asc", timeout=10)
    for i in range(0, len(badgecnt.json()['data'])):
        hunnidlist.append(badgecnt.json()['data'][i]['id'])
    awarddates = r.get(f"https://badges.roblox.com/v1/users/{plr}/badges/awarded-dates?badgeIds={str(hunnidlist).replace('[', '').replace(']', '')}")
    for i in range(0, len(awarddates.json()['data'])):
        dateo = datetime.datetime.date(datetime.datetime.fromisoformat(awarddates.json()['data'][i]['awardedDate']))
        if dateo > date1:
            done = True
            continue
        else:
            count += 1
    if done == True or badgecnt.json()['nextPageCursor'] == None:
        print(badgecnt.json()['previousPageCursor'])
        print(f"Final Count: {count}")
        break
    print(f"Counted: {count}")
    c = badgecnt.json()['nextPageCursor']
    hunnidlist.clear()
    continue
