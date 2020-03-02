""""
    This is the main module for the CKAN-WIT.
    It first imports the necessary packages from within python and its environs.
"""

import logging
import aiohttp
import asyncio
import requests
from urllib.error import URLError
from ckan_wit.src import uris
from ckan_wit.src import proxies

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)-5s: \n\t\t\t%(message)s: \n\t\t\t%(pathname)s: \n\t\t\t%(module)s: %(funcName)s\n')
file_handler = logging.FileHandler('wit.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
    ext_proxy = {
        'http': proxies.ProxySetting().http_proxy,
        'https': proxies.ProxySetting().https_proxy
    }
except KeyError:
    pass


def verify_acquire():
    """
    This method handles the pattern check for the uris using some reqex syntax.
    It ensures that the CKAN-API standard is a first class citizen, before it can be processed, whilst logging the errors found.
    If no errors, it has to return:
    :return: "number_of_portals", "verified_portals"
    """
    verified_uris = []
    ckan_standard_interface = "/api/3/action/package_search"

    """ First verify that the URI is a valid URI and it is available"""
    for uri in uris.ckan_opendata_portal_uris:
        uri += ckan_standard_interface
        try:
            global res
            res = requests.get(uri)
            if res.status_code == 200:
                verified_uris.append(uri)
        except res.status_code != 200:
            res = requests.get(uri, proxies=ext_proxy)
            if res.status_code == 200:
                verified_uris.append(uri)

    try:
        return {
            "number_of_portals": len(verified_uris),
            "verified_portals": verified_uris
        }
    except URLError:
        logger.exception("ERROR:: The File (ckan_opendata_portals_urls.txt) is not Found.")
        return {
            "ERROR Info": "Please check the log file for details"
        }
    finally:
        logger.info("SUCCESS - All referenced OpenData Portals have been successfully loaded for processing")


def ckan_wit_main():
    portals_main = verify_acquire()
    meta = dict()

    async def fetch(session, portal, proxy):

        async with session.get(portal, proxy=proxy) as response:

            try:
                assert response.status == 200, "API Standardization issues"
            except AssertionError as err:
                logger.exception("ERROR:: PORTAL UNAVAILABLE: {0}:".format(err))

            except OSError as err:
                logger.exception("ERROR:: Problem with OS: {0}".format(err))

            except ValueError:
                logger.exception("ERROR:: One or more values has been wrongly configured.")

            else:
                return await response.json()

    async def main():

        portals = portals_main["verified_portals"]
        proxy = next(iter(ext_proxy.values()))
        tasks = list()

        async with aiohttp.ClientSession() as session:
            for portal in portals:
                tasks.append(fetch(session, portal, proxy))
            resp = await asyncio.gather(*tasks)

            resp_length = len(resp)

            counter = 0
            for res in resp:
                if resp_length > counter:
                    counter = counter + 1
                    meta[counter] = res

    loop = asyncio.new_event_loop()  # this line is necessary for the edms flask app
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    # sleep gracefully
    loop.run_until_complete(asyncio.sleep(0))
    # loop.close()

    final_results = aggregate_filter_present(meta=meta)

    if final_results:
        logger.info("SUCCESS - Metadata successfully processed, aggregated, and formatted.\n\t\t\t See the docs on how to get started")
        try:
            return {"wit_resources": {"AFRICA": {"total_metadata": sum(wit_resources["africa"]["total_metadata"]), "wit_metadata": wit_resources["africa"]["wit_metadata"]},
                                      "AMERICAS": {"total_metadata": sum(wit_resources["americas"]["total_metadata"]), "wit_metadata": wit_resources["americas"]["wit_metadata"]},
                                      "ASIA": {"total_metadata": sum(wit_resources["asia"]["total_metadata"]), "wit_metadata": wit_resources["asia"]["wit_metadata"]},
                                      "EUROPE": {"total_metadata": sum(wit_resources["europe"]["total_metadata"]), "wit_metadata": wit_resources["europe"]["wit_metadata"]},
                                      "overall_total": sum(wit_resources["africa"]["total_metadata"]) + sum(wit_resources["americas"]["total_metadata"]) + sum(wit_resources[
                                                                                                                                                                   "asia"][
                                                                                                                                                                   "total_metadata"]) + sum(wit_resources["europe"]["total_metadata"])
                                      }
                    }
        except KeyError:
            logger.exception("WARNING -  The processing of one or more metadata was not successful.\n\t\tPlease see the logfile for more information")


def aggregate_filter_present(meta):
    temp_aggregator = {}
    temp2_aggregator = {}
    aggregated_results = list()
    aggregated_results_2 = list()
    idx = list(range(10))

    for key, value in meta.items():
        default = 'url'
        link = 'access_url'
        if meta[key]['success']:
            for id_num in idx:
                x_values = list(range(meta[key]['result']['results'][id_num]['num_resources']))
                for x_val in x_values:
                    if "access_url" in meta[key]['result']['results'][id_num]['resources'][x_val]:
                        temp_aggregator.update({
                            key: {"total_metadata": meta[key]['result']['count'],
                                  "Metadata": {
                                      'num_resources': meta[key]['result']['results'][id_num]['num_resources'],
                                      'owner_organization': meta[key]['result']['results'][id_num]['organization']['description']['en'],
                                      'resource_group_title': meta[key]['result']['results'][id_num]['organization']['title'],

                                      "wit_resources": {"name": meta[key]['result']['results'][id_num]['resources'][x_val]['id'],
                                                        "file_format": meta[key]['result']['results'][id_num]['resources'][x_val]['format'],
                                                        "download_link": meta[key]['result']['results'][id_num]['resources'][x_val][link]
                                                        }
                                  }, }
                        })

                        def clearNullNoneValues(d):
                            clearedValues = {}
                            for k, v in d.items():
                                if isinstance(v, dict):
                                    nested = clearNullNoneValues(v)
                                    if len(nested.keys()) > 0:
                                        clearedValues[k] = nested
                                elif v is not None:
                                    clearedValues[k] = v
                            return clearedValues

                        try:
                            aggregated_results.append(temp_aggregator.copy())
                        except AttributeError:
                            clearNullNoneValues(temp_aggregator.copy())
                            aggregated_results.append(temp_aggregator.copy())
                        except TypeError:
                            clearNullNoneValues(temp_aggregator.copy())
                            aggregated_results.append(temp_aggregator.copy())

                    if "url" in meta[key]['result']['results'][id_num]['resources'][x_val]:
                        try:
                            temp2_aggregator.update({
                                key: {"total_metadata": meta[key]['result']['count'],
                                      "Metadata": {
                                          'num_resources': meta[key]['result']['results'][id_num]['num_resources'],
                                          'license': meta[key]['result']['results'][id_num]['license_id'],
                                          'resource_group_title': meta[key]['result']['results'][id_num]['title'],
                                          'owner_organization': meta[key]['result']['results'][id_num]['organization']['name'],
                                          'owner_description': meta[key]['result']['results'][id_num]['organization']['description'],

                                          "wit_resources": {"name": meta[key]['result']['results'][id_num]['resources'][x_val]['name'],
                                                            "file_format": meta[key]['result']['results'][id_num]['resources'][x_val]['format'],
                                                            "download_link": meta[key]['result']['results'][id_num]['resources'][x_val][default]
                                                            }
                                      }, }
                            })
                        except TypeError:
                            pass

                        def clearNullNoneValues_2(d):
                            cleared_values_2 = {}
                            for k, v in d.items():
                                if isinstance(v, dict):
                                    nested = clearNullNoneValues_2(v)
                                    if len(nested.keys()) > 0:
                                        cleared_values_2[k] = nested
                                elif v is not None:
                                    cleared_values_2[k] = v
                            return cleared_values_2

                        try:
                            aggregated_results_2.append(temp2_aggregator.copy())
                        except AttributeError:
                            clearNullNoneValues_2(temp2_aggregator.copy())
                            aggregated_results_2.append(temp2_aggregator.copy())
                        except TypeError:
                            clearNullNoneValues_2(temp_aggregator.copy())
                            aggregated_results.append(temp_aggregator.copy())

        else:
            logger.error("PORTAL ERROR - ONE or More of the Portals is not responding..\n\t\t\tPlease see the troubleshooting guide in the "
                         "documentation for assistance.")
            return "Please see the wit.log file"

    aggregated_results.extend(aggregated_results_2)

    global wit_resources

    wit_resources = dict()

    wit_resources['africa'] = {
        "total_metadata": [],
        "wit_metadata": []
    }
    wit_resources['americas'] = {
        "total_metadata": [],
        "wit_metadata": []
    }
    wit_resources['asia'] = {
        "total_metadata": [],
        "wit_metadata": []
    }
    wit_resources['europe'] = {
        "total_metadata": [],
        "wit_metadata": []
    }

    for y in range(len(aggregated_results)):
        if len(aggregated_results[y]) == 1:
            wit_resources['europe']["total_metadata"].append(aggregated_results[y][1]['Metadata']['num_resources'])
            wit_resources['europe']["wit_metadata"].append(aggregated_results[y][1]['Metadata'])

        elif len(aggregated_results[y]) == 2:
            wit_resources['europe']["total_metadata"].append(aggregated_results[y][2]['Metadata']['num_resources'])
            wit_resources['europe']["wit_metadata"].append(aggregated_results[y][2]['Metadata'])

        elif len(aggregated_results[y]) == 3:
            wit_resources['americas']["total_metadata"].append(aggregated_results[y][3]['Metadata']['num_resources'])
            wit_resources['americas']["wit_metadata"].append(aggregated_results[y][3]['Metadata'])

        elif len(aggregated_results[y]) == 4:
            wit_resources['americas']["total_metadata"].append(aggregated_results[y][4]['Metadata']['num_resources'])
            wit_resources['americas']["wit_metadata"].append(aggregated_results[y][4]['Metadata'])

        elif len(aggregated_results[y]) == 5:
            wit_resources['asia']["total_metadata"].append(aggregated_results[y][5]['Metadata']['num_resources'])
            wit_resources['asia']["wit_metadata"].append(aggregated_results[y][5]['Metadata'])

        elif len(aggregated_results[y]) == 6:
            wit_resources['asia']["total_metadata"].append(aggregated_results[y][6]['Metadata']['num_resources'])
            wit_resources['asia']["wit_metadata"].append(aggregated_results[y][6]['Metadata'])

        elif len(aggregated_results[y]) == 7:
            wit_resources['africa']["total_metadata"].append(aggregated_results[y][7]['Metadata']['num_resources'])
            wit_resources['africa']["wit_metadata"].append(aggregated_results[y][7]['Metadata'])

        elif len(aggregated_results[y]) == 8:
            wit_resources['africa']["total_metadata"].append(aggregated_results[y][8]['Metadata']['num_resources'])
            wit_resources['africa']["wit_metadata"].append(aggregated_results[y][8]['Metadata'])

        else:
            logger.error("ERROR - One or more keys have been wrongly configured.\n\t\t\tPlease see the troubleshooting docs for assistance.")
            break

    try:
        return wit_resources
        # print(aggregated_results)
    except IndexError as err:
        logger.exception(err)


if __name__ == '__main__':
    ckan_wit_main()
