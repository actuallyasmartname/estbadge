import aiohttp, asyncio
from datetime import date, datetime
async def main():
    plr = int(input("Input the UserID of the player: "))
    datein = input("Input the date you want to travel back to (YYYY-MM-DD, ex. 2022-12-24): ")
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
            async with session.get(f"https://badges.roblox.com/v1/users/{plr}/badges/awarded-dates?badgeIds={str(hundredlist).replace('[', '').replace(']', '')}") as awarddates:
                print(await awarddates.json())
                for i in range(0, len((await awarddates.json())['data'])):
                    date2 = datetime.date(datetime.fromisoformat((await awarddates.json())['data'][i]['awardedDate']))
                    if date2 > date1:
                        done = True
                        continue
                    else:
                        count += 1
            if done == True or (await badgecnt.json())['nextPageCursor'] == None:
                print((await badgecnt.json())['previousPageCursor'])
                print(f"Final Count: {count}")
                await session.close()
                break
        print(f"Counted: {count}")
        c = (await badgecnt.json())['nextPageCursor']
        hundredlist.clear()
asyncio.run(main())
