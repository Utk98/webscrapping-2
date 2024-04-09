
import re
import http.client

def fetch_html(url):
    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", "/")
        response = conn.getresponse()
        if response.status == 200:
            return response.read().decode('utf-8')
        else:
            print("Failed to fetch HTML content. Status code:", response.status)
            return None
    except Exception as e:
        print("Error occurred while fetching HTML content:", e)
        return None

def extract_latest_stories(html_content):
    latest_stories = []
    start_index = html_content.find('<li class="latest-stories__item"')
    for _ in range(6):
        end_index = html_content.find('</li>', start_index)
        if end_index != -1:
            story = html_content[start_index:end_index]
            title_match = re.search(r'>(.*?)<', story)  
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = "Title not found"
            link_match = re.search(r'href="(.*?)"', story)
            if link_match:
                link = link_match.group(1)
            else:
                link = "Link not found"
            latest_stories.append({"title": title, "link": link})
            start_index = html_content.find('<li class="latest-stories__item"', end_index)
        else:
            break
    return latest_stories

def fetch_latest_stories():
    url = "time.com"
    html_content = fetch_html(url)
    if html_content:
        return extract_latest_stories(html_content)
    else:
        return None

def print_latest_stories():
    latest_stories = fetch_latest_stories()
    if latest_stories:
        for story in latest_stories:
            print("Title:", story["title"])
            print("Link:", "https://time.com"+story["link"])
            print()
    else:
        print("Failed to fetch latest stories.")

print_latest_stories()
