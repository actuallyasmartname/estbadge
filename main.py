import aiohttp, asyncio, sys
from datetime import date, datetime
async def main():
    if sys.argv < 2:
        print("Usage: main.py <userid> <date as YYYY-MM-DD format>")
    plr = int(sys.argv[1])
    datein = sys.argv[2]
    year, month, day = map(int, datein.split('-'))
    date1 = date(year, month, day)
    hundredlist = []
    count = 0
    done = False
    c = ""
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://badges.roblox.com/v1/users/{plr}/badges?limit=100&cursor={c}&sortOrder=Asc") as badgecnt:
                for i in range(0, len((await badgecnt.json())['data'])):
                    hundredlist.append((await badgecnt.json())['data'][i]['id'])
            async with session.get(f"https://badges.roblox.com/v1/users/{plr}/badges/awarded-dates?badgeIds={str(hundredlist)[1:-1]}") as awarddates:
                for i in range(0, len((await awarddates.json())['data'])):
                    date2 = datetime.date(datetime.fromisoformat((await awarddates.json())['data'][i]['awardedDate']))
                    if date2 > date1:
                        done = True
                        continue
                    else:
                        count += 1
            if done == True or (await badgecnt.json())['nextPageCursor'] == None:
                print(f"Final Count: {count}")
                break
        print(f"Counted: {count}")
        c = (await badgecnt.json())['nextPageCursor']
        hundredlist.clear()
asyncio.run(main())
