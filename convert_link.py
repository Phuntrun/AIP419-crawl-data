import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from urllib.parse import urljoin

async def convert_to_link(content):
    try:
        if isinstance(content, str):
            content = json.loads(content)
        if not isinstance(content, list):
            content = [content]
        for item in content:
            srcset = item.get("image_srcset_jpeg", "")
            link = srcset.split(" ")[-2]
        return link
    except Exception as e:
        print(f"Error formatting content: {e}")
        print(f"Content type: {type(content)}")
        print(f"Content: {content[:200]}...")
        return ""
sem = asyncio.Semaphore(300)
async def crawl_and_save(crawler, run_conf, url, line, save_as):
    async with sem:
        try:
            result = await crawler.arun(url=url, config=run_conf)
            if result.success:
                link = await convert_to_link(result.extracted_content)
                with open(save_as, "a", encoding="utf-8") as f:
                    f.write(line.replace(url, link))
                return "converted {url} to {link}!"
            else:
                print(f"Error with {url}: {result.error_message}")
                return line.strip() + ",ERROR"
        except Exception as e:
            print(f"Exception while crawling {url}: {e}")
            return "Error:" + result.error_message

async def convert(filename_input, filename_output):
    # 1) Browser config: headless, bigger viewport, no proxy
    browser_conf = BrowserConfig(
        headless=True,
        accept_downloads=True,
        downloads_path = "data",
        viewport_width=1280,
        viewport_height=720
    )

    # 2) Example extraction strategy
    schema = {
        "name": "Articles",
        "baseSelector": "#utility_modals",
        "fields": [
            {
                "name": "image_srcset_jpeg", 
                "selector": "picture source[type='image/jpeg']", 
                "type": "attribute", 
                "attribute": "srcset"
            },
        ]
    }
    extraction = JsonCssExtractionStrategy(schema)

    md_generator = DefaultMarkdownGenerator(
        content_filter=filter,
        options={"ignore_links": False})

        # 4) Crawler run config: skip cache, use extraction
    run_conf = CrawlerRunConfig(
        markdown_generator=md_generator,
        extraction_strategy=extraction,
        cache_mode=CacheMode.BYPASS,
        page_timeout=120000
    )


    with open(filename_input, "r", encoding="utf-8") as f:
        lines = f.readlines()
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        tasks = []
        for line in lines:
            url = line.strip().split(',')[-1]
            tasks.append(crawl_and_save(crawler=crawler,
                                        run_conf=run_conf,
                                        url=url,
                                        line=line,
                                        save_as=filename_output))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(convert())
