import json
import csv
import time
import random
import config
import requests


class BuffParser:
    def __init__(self):
        self.sale = False
        self.max_pages = 10

    def start(self):
        for url in config.URLS:
            page = 1
            response = self.get_response(url, page)
            total_pages = min(response['data']['total_page'], self.max_pages)
            products = response['data']['items']
            while page < total_pages:
                page += 1
                products.extend(self.get_response(url, page)['data']['items'])
            data_parsed = self.parse_products(products)
            self.export_to_csv(data_parsed)

    def get_response(self, url, page):
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                params = config.PARAMS
                if 'buying' not in url:
                    self.sale = True
                    params['use_suggestion'] = '0'
                    params['trigger'] = 'undefined_trigger'
                else:
                    self.sale = False
                params['page_num'] = page
                response = requests.get(url, params=params, cookies=config.COOKIES, headers=config.HEADERS)
                
                if response.status_code == 200:
                    print(f'Parsing: {response.url}')
                    json_response = json.loads(response.text)
                    
                    if 'error' in json_response:
                        print(f'API Error: {json_response}')
                        retry_count += 1
                        time.sleep(random.randrange(10, 15))
                        continue
                        
                    if 'data' not in json_response or 'items' not in json_response['data']:
                        print(f'Unexpected response structure: {json_response}')
                        retry_count += 1
                        time.sleep(random.randrange(10, 15))
                        continue
                    
                    return json_response
                else:
                    print(f'HTTP Error {response.status_code}: {response.text}')
                    retry_count += 1
                    time.sleep(random.randrange(10, 15))
                    
            except requests.exceptions.RequestException as e:
                print(f'Request error: {e}')
                retry_count += 1
                time.sleep(random.randrange(10, 15))
            except json.JSONDecodeError as e:
                print(f'JSON decode error: {e}')
                retry_count += 1
                time.sleep(random.randrange(10, 15))
        
        raise Exception(f'Failed to get valid response after {max_retries} retries')

    def parse_products(self, products: list):
        all_data = []
        for product in products:
            temp = []
            temp.append(product['market_hash_name'])
            if self.sale:
                temp.append(f"https://buff.163.com/goods/{product['id']}?from=market#tab=selling")
            else:
                temp.append(f"https://buff.163.com/goods/{product['id']}?from=market#tab=buying")
            all_data.append(temp)
            print(f'Parsed: {temp}')
        return all_data

    def export_to_csv(self, data_parsed):
        csv_header = ['name', 'url']
        name = 'purchase.csv'
        if self.sale:
            name = 'sale.csv'
        with open(name, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_header)
            writer.writerows(data_parsed)


if __name__ == '__main__':
    BuffParser().start()