import aiohttp, asyncio, datetime
async def main():
    plr = int(input("Input the UserID of the player: "))
    date = input("Input the date you want to travel back to (YYYY-MM-DD, ex. 2022-12-24): ")
    year, month, day = map(int, date.split('-'))
    date1 = datetime.date(year, month, day)
    hunnidlist = []
    count = 0
    done = False
    c = ""
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://badges.roblox.com/v1/users/{plr}/badges?limit=100&cursor={c}&sortOrder=Asc") as badgecnt:
                for i in range(0, len((await badgecnt.json())['data'])):
                    hunnidlist.append((await badgecnt.json())['data'][i]['id'])
            async with session.get(f"https://badges.roblox.com/v1/users/{plr}/badges/awarded-dates?badgeIds={str(hunnidlist).replace('[', '').replace(']', '')}") as awarddates:
                for i in range(0, len((await awarddates.json())['data'])):
                    dateo = datetime.datetime.date(datetime.datetime.fromisoformat((await awarddates.json())['data'][i]['awardedDate']))
                    if dateo > date1:
                        done = True
                        continue
                    else:
                        count += 1
            if done == True or (await badgecnt.json())['nextPageCursor'] == None:
                print((await badgecnt.json())['previousPageCursor'])
                print(f"Final Count: {count}")
                break
        print(f"Counted: {count}")
        c = (await badgecnt.json())['nextPageCursor']
        hunnidlist.clear()
        continue
asyncio.run(main())
