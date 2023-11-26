#
# This example is a modification (slight) of
# https://martinxpn.medium.com/making-requests-with-asyncio-in-python-78-100-days-of-python-eb1570b3f986
#
import asyncio
import aiohttp
import json

#
# These endpoints are on Prof. Ferguson's SwaggerHub mock APIs
#
resources = [
    {
        "resource": "Microservice1",
        "url": 'http://ec2-34-207-147-193.compute-1.amazonaws.com:8011/'  # url们打不开
    },
    {
        "resource": "Microservice2",
        "url": 'http://ec2-18-209-230-194.compute-1.amazonaws.com:5001/'
    },
    {
        "resource": "Microservice3",
        "url": 'https://shapementor-microservice.ue.r.appspot.com'
    }
]


async def fetch(session, resource):
    url = resource["url"]
    print("Calling URL = ", url)
    async with session.get(url) as response:
        t = await response.json()
        print("URL ", url, "returned", str(t))
        result = {
            "resource": resource["resource"],
            "data": t
        }
    return result


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, res)) for res in resources]
        responses = await asyncio.gather(*tasks)
        full_result = {}
        for response in responses:
            full_result[response["resource"]] = response["data"]

        print("\nFull Result = ", json.dumps(full_result, indent=2))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())