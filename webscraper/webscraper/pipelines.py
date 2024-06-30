# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter


class ParserPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if spider.name == "asura":
            adapter["source"] = "asura"

        elif spider.name == "mgeko":
            adapter["source"] = "mgeko"

        # Strip trailing whitespaces
        for field_name in ["title", "latest_chapter"]:
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()

        # Parse chapter number and convert to float
        latest_chapter = adapter.get("latest_chapter")
        if latest_chapter:
            if adapter["source"] == "asura":
                match = re.search(r"\d+(\.\d+)?", latest_chapter)
                if match:
                    adapter["latest_chapter"] = float(match.group())

            elif adapter["source"] == "mgeko":
                match = re.search(r"(\d+)(?:-(\d+))?", latest_chapter)
                if match:
                    chapter_number = match.group(1)
                    if match.group(2):
                        chapter_number += f".{match.group(2)}"
                    adapter["latest_chapter"] = float(chapter_number)

        # Add domain to URL if not present
        url = adapter.get("url")
        if url:
            if adapter["source"] == "asura" and "https://asuracomic.net" not in url:
                adapter["url"] = f"https://asuracomic.net{url}"
            elif adapter["source"] == "mgeko" and "https://www.mgeko.cc" not in url:
                adapter["url"] = f"https://www.mgeko.cc{url}"

        return item
