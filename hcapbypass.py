from datetime import date, datetime
import math
import base64
import httpx
import urllib
import hashlib
from json import dumps
import json
import os
import random

headers = {
    "Host": "hcaptcha.com",
    "Connection": "keep-alive",
    "sec-ch-ua": 'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92',
    "Accept": "application/json",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Content-type": "application/json; charset=utf-8",
    "Origin": "https://newassets.hcaptcha.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://newassets.hcaptcha.com/",
    "Accept-Language": "en-US,en;q=0.9"

}

def N_Data(req) -> str:
        try:
            """
            this part takes the req value inside the getsiteconfig and converts it into our hash, we need this for the final step.
            (thanks to h0nde for this function btw, you can find the original code for this at the top of the file.)
            """
            x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

            req = req.split(".")

            req = {
                "header": json.loads(
                    base64.b64decode(
                        req[0] +
                        "=======").decode("utf-8")),
                "payload": json.loads(
                    base64.b64decode(
                        req[1] +
                        "=======").decode("utf-8")),
                "raw": {
                    "header": req[0],
                    "payload": req[1],
                    "signature": req[2]}}

            def a(r):
                for t in range(len(r) - 1, -1, -1):
                    if r[t] < len(x) - 1:
                        r[t] += 1
                        return True
                    r[t] = 0
                return False

            def i(r):
                t = ""
                for n in range(len(r)):
                    t += x[r[n]]
                return t

            def o(r, e):
                n = e
                hashed = hashlib.sha1(e.encode())
                o = hashed.hexdigest()
                t = hashed.digest()
                e = None
                n = -1
                o = []
                for n in range(n + 1, 8 * len(t)):
                    e = t[math.floor(n / 8)] >> n % 8 & 1
                    o.append(e)
                a = o[:r]

                def index2(x, y):
                    if y in x:
                        return x.index(y)
                    return -1
                return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)

            def get():
                for e in range(25):
                    n = [0 for i in range(e)]
                    while a(n):
                        u = req["payload"]["d"] + "::" + i(n)
                        if o(req["payload"]["s"], u):
                            return i(n)

            result = get()
            hsl = ":".join([
                "1",
                str(req["payload"]["s"]),
                datetime.now().isoformat()[:19]
                .replace("T", "")
                .replace("-", "")
                .replace(":", ""),
                req["payload"]["d"],
                "",
                result
            ])
            return hsl
        except Exception as e:
            print(e)
            return False

def REQ_Data(host, sitekey):
        try:
            r = httpx.get(f"https://hcaptcha.com/checksiteconfig?host={host}&sitekey={sitekey}&sc=1&swa=1", headers=headers ,timeout=4)
            if r.json()["pass"]:
                return r.json()["c"]
            else:
                return False
        except :
            return False

def Get_Captcha(host, sitekey, n, req, hc_accessibility):
        try:
            json = {
                "sitekey": sitekey,
                "v": "04f9464",
                "host": host,
                "n": n,
                'motiondata': '{"st":1711870450214,"mm":[[119,23,1711870731141],[37,58,1711870740204],[32,48,1711870740220],[26,35,1711870740236],[22,28,1711870740253],[19,25,1711870740269],[17,24,1711870740286],[17,24,1711870740353],[19,25,1711870740370],[19,25,1711870740386]],"mm-mp":420.1190476190476,"md":[[19,25,1711870740382]],"md-mp":0,"mu":[[19,25,1711870740456]],"mu-mp":0,"v":1,"topLevel":{"st":1711870448985,"sc":{"availWidth":1512,"availHeight":889,"width":1512,"height":982,"colorDepth":30,"pixelDepth":30,"top":0,"left":0,"availTop":38,"availLeft":0,"mozOrientation":"landscape-primary","onmozorientationchange":null},"nv":{"permissions":{},"pdfViewerEnabled":true,"doNotTrack":"1","maxTouchPoints":0,"mediaCapabilities":{},"oscpu":"Intel Mac OS X 10.15","vendor":"","vendorSub":"","productSub":"20100101","cookieEnabled":true,"buildID":"20181001000000","mediaDevices":{},"serviceWorker":{},"credentials":{},"clipboard":{},"mediaSession":{},"webdriver":false,"hardwareConcurrency":8,"geolocation":{},"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Macintosh)","platform":"MacIntel","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0","product":"Gecko","language":"zh-CN","languages":["zh-CN","zh","zh-TW","zh-HK","en-US","en"],"locks":{},"onLine":true,"storage":{},"globalPrivacyControl":true,"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[],"wn-mp":6564.6,"xy":[],"xy-mp":0,"mm":[[267,12,1711870730787],[307,51,1711870730803],[511,274,1711870730828],[511,275,1711870731078],[522,293,1711870731094],[533,312,1711870731111],[599,437,1711870731153],[511,479,1711870740152],[494,454,1711870740170]],"mm-mp":263.4026845637584},"session":[],"widgetList":["0m4wrysmub4"],"widgetId":"0m4wrysmub4","href":"https://www.cloudns.net/","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}',
                "hl": "en",
                "c": dumps(req)
            }

            data = urllib.parse.urlencode(json)
            headers = {
                "Host": "hcaptcha.com",
                "Connection": "keep-alive",
                "sec-ch-ua": 'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92',
                "Accept": "application/json",
                "sec-ch-ua-mobile": "?0",
                "Content-length": str(len(data)),
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                "Content-type": "application/x-www-form-urlencoded",
                "Origin": "https://newassets.hcaptcha.com",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://newassets.hcaptcha.com/",
                "Accept-Language": "en-US,en;q=0.9"

            }

            cookies = {"hc_accessibility": hc_accessibility}
            r = httpx.post(f"https://hcaptcha.com/getcaptcha?s={sitekey}",cookies=cookies, data=data, headers=headers, timeout=4)

            return r.json()
        except Exception as e:
            print(e)
            return False

def bypass(sitekey, host, hc_accessibility):
    try :
        req = REQ_Data(sitekey=sitekey, host=host)
        req["type"] = "hsl"
        n = N_Data(req["req"])
        res = Get_Captcha(sitekey=sitekey, host=host,n=n, req=req, hc_accessibility=hc_accessibility)
        if "generated_pass_UUID" in res:
            captcha = res["generated_pass_UUID"]
            return captcha
        else:
            return False
    except : return False

