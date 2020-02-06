Introduction
=======================

CKAN-WIT: An API Wrapper for CKAN Open Data Portals
-------------------------------------------------------
**CKAN-WIT** is a tool that aims to bring the best of open data portals to the developers and IT users from a different domain who might be interested in providing open data features on their web application or content management systems. *CKAN standard is our first-class citizen.*

The library leverages on the standard API characteristic of CKAN to allow for metadata aggregation, filtration, and presentation within a web application. It interacts with more than one single CKAN-instance and provides a simple interface for manipulating the metadata results.

CKAN-WIT is primarily meant to provide users and developers of applications with an easy way to access open data resources. No need for unnecessary harvesters and crawlers. Metadata from various CKAN instances are aggregated, filtered, and made available via geographic-location interfaces - Europe, Africa, America and Asia.

.. note::
    CKAN-WIT is a python library, not a python application. This is commonly confused in the python community. Libraries provide reusable functionality to other libraries and applications (let’s use the umbrella term projects here). They are required to work alongside other libraries, all with their own set of subdependencies. They define abstract dependencies. Libraries are ultimately meant to be used in some application. Applications are different in that they usually are not depended on by other projects. They are meant to be deployed into some specific environment. See more information on this dichotomy here.


Why CKAN-WIT
-------------

The challenges that CKAN-WIT seeks to solve in the Open data Ecosystem are multi-faceted:

- Knowing which open-data portal has the dataset/metadata you need can be problematic, CKAN-WIT access more than one portal instance and allows u to search more than one portal from one interface
- Developers can focus on their business logic and workflows, whilst using the CKAN-WIT to provide add-on features on their web application.
- Other CMS can easily integrate the tool to provide open-data add-on features to the CMS.
- Abstract dependency needs from these portals, and just use CKAN-WIT.
- Strongly encourage the use of geographic location to show the source of the metadata.

