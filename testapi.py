import asyncio
import aiohttp
import time

names = ['Luke', 'Darth', 'Leia', "C-3PO", "R2-D2", "Owen Lars", 'Beru', 'Kenobi']

websites = """"""
site = 'http://localhost:8085/api?name='
for i in range(60):
    for name in names:
        websites += site + name + '\n'

print(websites)


async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                resp = await response.read()
                print("Successfully got url {} with response of length {}.".format(url, len(resp)))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def main(urls, amount):
    ret = await asyncio.gather(*[get(url) for url in urls])
    print("Finalized all. ret is a list of len {} outputs.".format(len(ret)))


urls = websites.split("\n")
amount = len(urls)

start = time.time()
asyncio.run(main(urls, amount))
end = time.time()

print("Took {} seconds to pull {} websites.".format(end - start, amount))