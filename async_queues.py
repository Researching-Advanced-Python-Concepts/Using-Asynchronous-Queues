from collections import Counter
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from typing import NamedTuple

import sys
import argparse
import asyncio
import aiohttp


class Job(NamedTuple):
    url: str
    depth: int = 1  # default 1


async def worker(worker_id, session ,queue, links, max_depth):
    print(f"[{worker_id} starting]", file=sys.stderr)
    while True:
        # wait for a job to arrive in the queue
        url, depth = await queue.get()
        # after consuming a single job, the worker can put one or
        # more new jobs with a bumped-up depth in the queue to be
        # consumed by itself or other workers
        links[url] += 1
        try:
            if depth <= max_depth:
                print(f"[{worker_id} {depth=} {url=}]", file=sys.stderr)
                if html := await fetch_html(session, url):
                    for link_url in parse_links(url, html):
                        await queue.put(Job(link_url, depth + 1))
        except aiohttp.ClientError:
            print(f"[{worker_id} failed at {url=}]", file=sys.stderr)
        finally:
            # as our worker is both a producer and a consumer we must
            # to this to avoid deadlock
            # decrease the queue counter
            # idc if the queue is empty I care that whether the task
            # is done (think: box full of assignments to check)
            queue.task_done()


async def fetch_html(session, url):
    async with session.get(url) as response:
        if response.ok and response.content_type == "text/html":
            return await response.text()


def parse_links(url, html):
    soup = bs(html, features="html.parser")
    for anchor in soup.select("a[href]"):
        href = anchor.get("href").lower()
        if not href.startswith("javascript:"):
            # Join a base URL and a possibly relative URL
            # to form an absolute interpretation of the latter.
            yield urljoin(url, href)

async def main(args):
    session = aiohttp.ClientSession()
    try:
        # define a counter of visited links
        # we'll see the list of links sorted by the no. of visits
        # in descending order (later)
        links = Counter()
        display(links)
    finally:
        await session.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-d", "--max-depth", type=int, default=2)
    parser.add_argument("-w", "--num-workers", type=int, default=3)
    return parser.parse_args()


def display(links):
    # most common gives list of tuples
    # 1st item: link and 2nd item count
    for url, count in links.most_common():
        print(f"{count:>3} {url}")


if __name__ == "__main__":
    # pass main() coroutine to asyncio.run() so that it can execute
    # it on the default event loop
    asyncio.run(main(parse_args()))