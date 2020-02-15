import pathlib
import unittest
import aiohttp
import asyncio

from ckan_wit.src.wit_main import verify_acquire, proxies

"""Test-cases for testing the methods in the wit_module"""


class TestCkanWit(unittest.TestCase):

    def test_verify_acquire(self):
        self.assertTrue(pathlib.Path('uris.py'))
        self.assertTrue(pathlib.Path('setup.cfg'))

    def test_aiohttp_calls(self):
        portals_main = verify_acquire()

        async def fetch(session, portal, proxy):

            async with session.get(portal, proxy=proxy) as response:
                if self.assertEqual(200, response.status):
                    return await response.status
                else:
                    return 'Bad response'

        async def main():

            portals = portals_main["verified_portals"]
            proxy = proxies.proxy_settings()
            tasks = list()

            async with aiohttp.ClientSession() as session:
                for portal in portals:
                    tasks.append(fetch(session, portal, proxy))
                await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())


        # sleep gracefully
        loop.run_until_complete(asyncio.sleep(0))


if __name__ == '__main__':
    unittest.main()
