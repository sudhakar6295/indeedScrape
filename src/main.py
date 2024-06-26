"""
This module defines the main coroutine for the Apify Scrapy Actor, executed from the __main__.py file. The coroutine
processes the Actor's input and executes the Scrapy spider. Additionally, it updates Scrapy project settings by
applying Apify-related settings. Which includes adding a custom scheduler, retry middleware, and an item pipeline
for pushing data to the Apify dataset.

Customization:
--------------

Feel free to customize this file to add specific functionality to the Actor, such as incorporating your own Scrapy
components like spiders and handling Actor input. However, make sure you have a clear understanding of your
modifications. For instance, removing `apply_apify_settings` break the integration between Scrapy and Apify.

Documentation:
--------------

For an in-depth description of the Apify-Scrapy integration process, our Scrapy components, known limitations and
other stuff, please refer to the following documentation page: https://docs.apify.com/cli/docs/integrating-scrapy.
"""


from __future__ import annotations

from scrapy.crawler import CrawlerProcess

from apify import Actor
from apify.scrapy.utils import apply_apify_settings

# Import your Scrapy spider here
from .spiders.title import TitleSpider as Spider

# Default input values for local execution using `apify run`
LOCAL_DEFAULT_START_URLS = [{'url': 'https://www.linkedin.com/jobs/search/?currentJobId=3875742938&f_I=14%2C11%2C1%2C148%2C43%2C31%2C4%2C1594%2C15%2C116%2C84&f_JT=F%2CC%2CT&geoId=103644278&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R'}]


async def main() -> None:
    """
    Apify Actor main coroutine for executing the Scrapy spider.
    """
    async with Actor:
        Actor.log.info('Actor is being executed...')

        # Process Actor input
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('startUrls', LOCAL_DEFAULT_START_URLS)
        proxy_config = actor_input.get('proxyConfiguration')

        # Add start URLs to the request queue
        rq = await Actor.open_request_queue()
        for start_url in start_urls:
            url = start_url.get('url')
            await rq.add_request(request={'url': url, 'method': 'GET'})

        # Apply Apify settings, it will override the Scrapy project settings
        settings = apply_apify_settings(proxy_config=proxy_config)

        # Execute the spider using Scrapy CrawlerProcess
        process = CrawlerProcess(settings, install_root_handler=False)
        process.crawl(Spider)
        process.start()
