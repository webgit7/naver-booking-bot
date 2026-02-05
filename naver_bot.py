import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TARGET_URL = "https://booking.naver.com/booking/13/bizes/191175/items/2906074?startDate=2026-02-09"
TARGET_DATES = ["9", "10", "14", "15"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

def check_reservation():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(TARGET_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.calendar_date")))
        
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.calendar_date")
        found_list = []
        for btn in buttons:
            try:
                num = btn.find_element(By.CSS_SELECTOR, "span.num").text.strip()
                if num in TARGET_DATES:
                    class_attr = btn.get_attribute("class")
                    if "closed" not in class_attr and "dayoff" not in class_attr:
                        found_list.append(num)
            except:
                continue

        if found_list:
            send_telegram(f"🎉 [빈자리 발견!] {', '.join(found_list)}일 예약 가능!\n{TARGET_URL}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_reservation()
