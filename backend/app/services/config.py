import requests

URL_PURCHASE = 'https://buff.163.com/api/market/goods/buying'
URL_SALE = 'https://buff.163.com/api/market/goods'
URLS = [URL_SALE, URL_PURCHASE]

COOKIES = {
    'Device-Id': '4cZTXNw5jmZL5bXPibSz',
    'Locale-Supported': 'en',
    'game': 'csgo',
    'AQ_HD': '1',
    'YD_SC_SID': 'XXX',
    'NETS_utid': 'XXX',
    'NTES_YD_SESS': 'Flv_BI2pxUwK10OfZMAcypOZeMsBbgytJabWVpXU4qvgGaiKjR9Z8QSHAIyxyusScx10V4UHsUuhpLzW2UsML8sDDZNZpM80qnF0E39LM8kqPPqNppibZtYuugSITwMUWFD0uHyBn7uLurXMCk9tBm.CXoOAQn3Iim3Mhiax7RfuLrku9rgABOFvAybUkyleyZLOXpxB6RVjn1phG0elE0DTQYGE0JfFQbJ4c_QtZOkZV',
    'S_INFO': '1757058464|0|0&60##|1-6502724885',
    'P_INFO': '1-6502724885|1757058464|1|netease_buff|00&99|null&null&null#US&null#10#0|&0||1-6502724885',
    'remember_me': 'U1083741324|TwmAkIximiY5YXZL4lCVjZgYpXGIfut0',
    'session': '1-w6EH0hD6SPllxKsjAMv8ExXpFx4axv5fDUVrFp0_69UL2018905044',
    'csrf_token': 'IjcyNjVmOTBiZjQwNmVlYzUzY2MwNmVlZTdkNmZkZWVkOWNkNGYxNGUi.aLqU9w.q2C4aWx3_8CRKh179bKTgLy8HzM',
}

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://buff.163.com/market/csgo',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/107.0.0.0 Safari/537.36 '
                  'OPR/93.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

PARAMS = {
    'game': 'csgo',
    'page_num': '1',
}


if __name__ == '__main__':
    response = requests.get(URL_PURCHASE, params=PARAMS, cookies=COOKIES, headers=HEADERS)
    print(response.text)