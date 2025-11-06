from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time
from deep_translator import GoogleTranslator
from collections import Counter
import concurrent.futures

USERNAME = "your_browsestack username"
ACCESS_KEY = "your_browserstack access key"
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"


def run_test(capabilities):
    options = Options()
    options.set_capability('browserstack:options', capabilities)
    driver = webdriver.Remote(command_executor=URL, options=options)

    try:
        driver.get("https://elpais.com/opinion/")
        time.sleep(5)
        session_name = capabilities.get('sessionName', 'Unnamed_Session')
        print(f"\n[{session_name}] BrowserStack session started")
        print(f"[{session_name}] Page Title: {driver.title}")

        articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
        titles_spanish = []
        contents_spanish = []

        for article in articles:

            title = article.find_element(By.TAG_NAME, "h2").text if article.find_elements(By.TAG_NAME, "h2") else "Title not available"
            content = article.find_element(By.TAG_NAME, "p").text if article.find_elements(By.TAG_NAME, "p") else "Content not available"
            titles_spanish.append(title)
            contents_spanish.append(content)

            img_tags = article.find_elements(By.TAG_NAME, "img")
            if img_tags:
                img_url = img_tags[0].get_attribute("src")
                if img_url:
                    try:
                        img_data = requests.get(img_url).content
                        filename = title.replace(" ", "_")[:30] + ".jpg"
                        with open(filename, "wb") as f:
                            f.write(img_data)
                        print(f"[{session_name}] Image saved: {filename}")
                    except Exception:
                        print(f"[{session_name}] Error saving image for: {title}")
            else:
                print(f"[{session_name}] No image found for this article.")

        print(f"\n[{session_name}] Titles and Content in Spanish:")
        for i in range(len(titles_spanish)):
            print(f"Article {i+1}: {titles_spanish[i]} - {contents_spanish[i]}")

        translator = GoogleTranslator(source='auto', target='en')
        titles_english = [translator.translate(t) for t in titles_spanish]


        words = []
        for t in titles_english:
            for w in t.lower().split():
                words.append(w.strip('.,!?'))
        repeated = {w: c for w, c in Counter(words).items() if c > 2}

        print(f"\n[{session_name}] Translated Titles in English:")
        for i, t in enumerate(titles_english, start=1):
            print(f"{i}. {t}")
        print(f"Repeated words: {repeated if repeated else 'None'}")

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Test completed successfully"}}'
        )

    except Exception as e:
        print(f"[{session_name}] Test failed due to: {e}")
        driver.execute_script(
            f'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Test failed due to {str(e)}"}}'
        )

    finally:
        driver.quit()
        print(f"[{session_name}] Session finished.\n")

capabilities_list = [
    {'os': 'Windows', 'osVersion': '11', 'browserName': 'Chrome', 'browserVersion': 'latest', 'sessionName': 'Win11_Chrome'},
    {'os': 'Windows', 'osVersion': '11', 'browserName': 'Firefox', 'browserVersion': 'latest', 'sessionName': 'Win11_Firefox'},
    {'os': 'OS X', 'osVersion': 'Sonoma', 'browserName': 'Safari', 'browserVersion': 'latest', 'sessionName': 'Mac_Safari'},
    {'deviceName': 'Samsung Galaxy S24', 'realMobile': 'true', 'osVersion': '14.0', 'browserName': 'Chrome', 'sessionName': 'Android_Chrome'},
    {'deviceName': 'iPhone 15', 'realMobile': 'true', 'osVersion': '17', 'browserName': 'Safari', 'sessionName': 'iPhone_Safari'}
]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_test, capabilities_list)

print("\n All 5 BrowserStack sessions completed successfully.\n")
