import undetected_chromedriver as uc
import requests
import time
import json
import sys
import os

from hcapbypass import bypass
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

session_id = None
value1 = None
value2 = None
cf_api_url = None
cf_headers = None
record_id1 = None
record_id2 = None
hc_accessibility = None
zone = None
sitekey = "4bbd3fe0-7a04-401a-aac2-519a52d2abe3"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"

def check_cert_status():
    global value1, value2, cf_headers, cf_api_url
    zone = os.getenv('CF_ZONE_ID')
    token = os.getenv('CF_TOKEN')

    cf_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    
    cf_api_url = "https://api.cloudflare.com/client/v4/zones/" + zone + "/ssl/certificate_packs?status=all"
    response = requests.get(cf_api_url, headers=cf_headers)

    data = json.loads(response.text)
    for item in data["result"]:
        if item["type"] == "universal":
            status_value = item["status"]
            if "active" in status_value:
                print("证书已经申请通过了！")
                sys.exit(0)
            elif "pending" in status_value:
                validation_records = item.get("validation_records", [])
                txt_values = [record["txt_value"] for record in validation_records]
                value1, value2 = txt_values
                return

def get_hcaptcha_cookie():
    global hc_accessibility
    url = os.getenv('HC_LINK')
    uc_options = uc.ChromeOptions()
    uc_options.headless = False
    #uc_options.add_argument(f'--proxy-server=http://127.0.0.1:40000')
    driver = uc.Chrome(options=uc_options)

    driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div/div[3]/button").click()
    time.sleep(10)
    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie["name"] == "hc_accessibility":
            hc_accessibility = cookie["value"]
            break

    if hc_accessibility is None:
        driver.quit()
        print("没找到无障碍cookie，再试一次")
        time.sleep(10)
        sys.exit(1)

    driver.quit()

def cloudns_login():
    global session_id, sitekey, user_agent, hc_accessibility
    email = os.getenv('CD_EMAIL')
    password = os.getenv('CD_PASSWD')
    url = 'https://www.cloudns.net/ajaxActions.php?action=index'

    captcha = bypass(sitekey, "www.cloudns.net", hc_accessibility)

    data = {
	    "type": "login2FA",
	    "mail": email,
	    "password": password,
	    "token": "",
	    "captcha": captcha
    }

    response = requests.post(url, headers={"User-Agent": user_agent}, data=data)
    print(response.text)
    if 'Set-Cookie' in response.headers:
        set_cookie_header = response.headers['Set-Cookie']
        session_id = set_cookie_header.split('=')[1].split(';')[0]

def add_records():
    global session_id, value1, value2, user_agent, zone, record_id1, record_id2
    zone = os.getenv('CD_ZONE')

    url = "https://www.cloudns.net/ajaxActions.php?action=records"
    cookie = {"session_id": session_id}

    data = {
        "show": "addRecord",
        "zone": zone,
        "recordType": "TXT",
        "active": "1",
        "settings[host]": "_acme-challenge",
        "settings[record]": value1,
        "settings[ttl]": "3600"
    }

    data2 = {
        "show": "addRecord",
        "zone": zone,
        "recordType": "TXT",
        "active": "1",
        "settings[host]": "_acme-challenge",
        "settings[record]": value2,
        "settings[ttl]": "3600"
    }
    response = requests.post(url, headers={"User-Agent": user_agent}, cookies=cookie, data=data)
    response2 = requests.post(url, headers={"User-Agent": user_agent}, cookies=cookie, data=data2)

    data3 = json.loads(response.text)
    data4 = json.loads(response2.text)

    record_id1 = data3["id"]
    record_id2 = data4["id"]

def recheck_cert_status(retry_limit=6, wait_interval=3600):
    global cf_headers, cf_api_url

    for attempt in range(retry_limit):
        response = requests.get(cf_api_url, headers=cf_headers)
        data = json.loads(response.text)
        for item in data["result"]:
            if item["type"] == "universal":
                status_value = item["status"]
                if "active" in status_value:
                    print("证书已经申请通过了！")
                    return
                elif "pending" in status_value:
                    print("证书仍在等待验证，等待60分钟……")
                    time.sleep(wait_interval)

def delete_records():
    global session_id, zone, user_agent, record_id1, record_id2

    url = "https://www.cloudns.net/ajaxActions.php?action=records"
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"
    cookie = {"session_id": session_id}

    data = {
	    "type": "deleteRecord",
	    "zone": zone,
	    "record_id": record_id1
    }

    data2 = {
        "type": "deleteRecord",
	    "zone": zone,
	    "record_id": record_id2
    }

    response = requests.post(url, headers={"User-Agent": user_agent}, cookies=cookie, data=data)
    response2 = requests.post(url, headers={"User-Agent": user_agent}, cookies=cookie, data=data2)

    print(response.text)
    print(response2.text)

if __name__ == '__main__':
    check_cert_status()
    get_hcaptcha_cookie()
    cloudns_login()
    add_records()
    recheck_cert_status()
    delete_records()
