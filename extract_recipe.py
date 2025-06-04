import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from urllib.parse import urljoin
import hashlib

sem = asyncio.Semaphore(300)
async def crawl_and_save(crawler, run_conf, url, label, filename):
    async with sem:
        try:
            result = await crawler.arun(url=url, config=run_conf)
            if result.success:
                await to_csv(content=result.extracted_content,
                                    label=label,
                                    filename=filename)
            else:
                print(f"Error with {url}: {result.error_message}")
        except Exception as e:
            print(f"Exception while crawling {url}: {e}")
            return "Error:" + result.error_message

async def to_csv(content, label, filename):
    try:
        if isinstance(content, str):
            content = json.loads(content)
        
        if not isinstance(content, list):
            content = [content]
            
        label = label.strip().replace("+", " ").replace("\n", "")

        for item in content:
            # title = item.get("title", "").replace('"', "'")  # Escape quotes
            # description = item.get("description", "").replace('"', "'")
            # base_filename = ""
            # ingredients_text = ""
            # for ingredient in item.get("ingredients"):
            #     ingredient_quantity = ingredient["ingredient-quantity"].strip().replace('"', "'")
            #     ingredient_name = ingredient["ingredient-name"].strip().replace('"', "'")
            #     ingredients_text += f"{ingredient_quantity} {ingredient_name}, "
            #     format_filename = ingredient_name.strip().replace("\\", ",").replace("/", ",").replace(',','').replace(" ", "_").lower()
            #     base_filename += f"{format_filename}-"
            # base_filename = base_filename[:-1]
            # steps = [step["step-text"].replace('"', "'") for step in item["steps"]]
            # steps_text = ""
            # for i in range(len(steps)): steps_text += f"Bước {i+1}: {steps[i]}\\n"
            with open(filename, "a", encoding="utf-8") as f:
                for step in item["steps"]:
                    for image in step["step-images"]:
                        name = image["image"].split("/")[-1]
                        name = name.split("?")[0]
                        url = "https://cookpad.com" + image["image"]
                        f.write(f"{label},{name},{url}\n")

            # with open(context_filename, "a", encoding="utf-8") as f:
            #     f.write(f'{label},"{title}","{description}","{ingredients_text}","{steps_text}"\n')       
        
    except Exception as e:
        print(f"Error formatting content: {e}")
        print(f"Content type: {type(content)}")
        print(f"Content: {content[:200]}...")  # Print first 200 chars for debugging
        return ""

async def extract(filename_input, filename_output):
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
        "baseSelector": "div#recipe",
        "fields": [
            {"name": "title", "selector": "h1", "type": "text"},
            {"name": "description", "selector": "p", "type": "text"},
            {
                "name": "steps", 
                "selector": ".step", 
                "type": "nested_list", 
                "fields": [
                    {"name": "step-text", "selector": "p", "type": "text"},
                    {
                        "name": "step-images", 
                        "selector": "a[href*='/step_attachment/images/']", 
                        "type": "list", 
                        "fields":[
                            {"name": "image", "type": "attribute", "attribute": "href"}
                        ]
                    }
                ]
            },
            {
                "name": "ingredients",
                "selector": ".ingredient-list ol li", 
                "type": "nested_list",
                "fields": [
                    {"name": "ingredient-quantity", "selector": "bdi", "type": "text"},
                    {"name": "ingredient-name", "selector": "span", "type": "text"}
                ]
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
        page_timeout=600000
    )
    with open(filename_input, "r", encoding="utf-8") as f:
        lines = f.readlines()
        async with AsyncWebCrawler(config=browser_conf) as crawler:
            tasks = []
            for line in lines:
                url, label = line.split(",")
                tasks.append(crawl_and_save(crawler=crawler,
                                            run_conf=run_conf,
                                            url=url,
                                            label=label,
                                            filename=filename_output))

            await asyncio.gather(*tasks)

                # result = await crawler.arun(url=url, config=run_conf)
                # if result.success:
                #     await to_csv(content = result.extracted_content, id=label)                  
                # else:
                #     print("Error:", result.error_message)
if __name__ == "__main__":
    asyncio.run(extract())
