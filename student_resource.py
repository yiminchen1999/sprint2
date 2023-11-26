from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
import requests


class Student(BaseModel):
    name: str


class StudentResource:
    resources = [
        {
            "resource": "Microservice1",
            "url": 'http://ec2-34-207-147-193.compute-1.amazonaws.com:8011/'
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

    async def get_item(self, item: Student = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."

    @classmethod
    async def fetch(cls, session, resource):
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

    async def get_student_async(self):
        full_result = None
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(
                StudentResource.fetch(session, res)) for res in StudentResource.resources]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                full_result[response["resource"]] = response["data"]
            end_time = time.time()
            full_result["elapsed_time"] = end_time - start_time
            return full_result

    async def get_student_sync(self):
        full_result = None
        start_time = time.time()

        full_result = {}

        for r in StudentResource.resources:
            response = requests.get(r["url"])
            full_result[r["resource"]] = response.json()
        end_time = time.time()
        full_result["elapsed_time"] = end_time - start_time

        return full_result

