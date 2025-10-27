import os
import datetime
import xml.etree.ElementTree as ET

# Configuration
FEED_TITLE = "Project First Pirch"
FEED_LINK = "https://nicks55.github.io/FirstPitch"
FEED_DESCRIPTION = "Daily release notes for Project First Pirch."
OUTPUT_FILE = "rss.xml"
NOTES_DIR = "notes"  # Directory where your text files are stored

# Each note should be a .txt file named like 2025-10-26.txt
# with your handwritten notes inside.

def create_rss_item(title, link, description, pub_date):
    item = ET.Element("item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "description").text = description
    ET.SubElement(item, "pubDate").text = pub_date
    return item

def generate_feed():
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = FEED_TITLE
    ET.SubElement(channel, "link").text = FEED_LINK
    ET.SubElement(channel, "description").text = FEED_DESCRIPTION
    ET.SubElement(channel, "lastBuildDate").text = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    if not os.path.exists(NOTES_DIR):
        print(f"No '{NOTES_DIR}' directory found.")
        return

    for filename in sorted(os.listdir(NOTES_DIR), reverse=True):
        if filename.endswith(".txt"):
            date_str = filename.replace(".txt", "")
            with open(os.path.join(NOTES_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read().strip()
            pub_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 GMT")
            item_link = f"{FEED_LINK}/{filename.replace('.txt', '')}"
            item = create_rss_item(f"Release Notes {date_str}", item_link, content, pub_date)
            channel.append(item)

    tree = ET.ElementTree(rss)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"RSS feed generated → {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_feed()
