import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from urllib.parse import urljoin

async def save_to_csv(content, clas, filename):
    try:
        if isinstance(content, str):
            content = json.loads(content)
        if not isinstance(content, list):
            content = [content]
        
        with open(filename, "a", encoding="utf-8") as f:
            for item in content:
                recipe = item.get("recipe")
                for link in recipe:
                    url = "https://cookpad.com" + link["link"]
                    f.write(f"{url},{clas}\n")

  
    except Exception as e:
        print(f"Error formatting content: {e}")
        print(f"Content type: {type(content)}")
        print(f"Content: {content[:200]}...")
        return ""
    
sem = asyncio.Semaphore(300)
async def crawl(crawler, run_conf, clas, url,filename):
    async with sem:
        result = await crawler.arun(url = url, config=run_conf)
        if result.success:
            await save_to_csv(content=result.extracted_content, clas=clas, filename=filename)
        else:
            print(f"Error with {url}: {result.error_message}")

async def extract(classes, filename):
    browser_conf = BrowserConfig(
        headless=True,
        accept_downloads=True,
        downloads_path = "data",
        viewport_width=1280,
        viewport_height=720
    )

    schema = {
        "name": "Articles",
        "baseSelector": "#search-recipes-list",
        "fields": [
            {
                "name": "recipe",
                "selector": ".block-link",
                "type": "nested_list",
                "fields": [
                    {
                        "name": "link",
                        "selector": ".block-link__main",
                        "type": "attribute",
                        "attribute": "href",
                    }
                ]
            }
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
        page_timeout=600000
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        tasks = []
        for clas in classes:
            for i in range(333):
                url=f"https://cookpad.com/vn/tim-kiem/m%C3%B3n%20ngon%20m%E1%BB%97i%20ng%C3%A0y?included_ingredients={clas}&page={i+1}"
                tasks.append(crawl(crawler=crawler, run_conf=run_conf, clas=clas.strip().replace(" ", "+"), url=url, filename=filename))

        await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(extract())