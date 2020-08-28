import requests
import urllib
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def finance_crawl(company_sector, company_code, company_name):
  url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
  url = url_tmpl % (company_code)

  item_info = requests.get(url).text
  soup = BeautifulSoup(item_info, 'html.parser')
  finance_info = soup.select('div.section.cop_analysis div.sub_section')[0]

  th_data = [item.get_text().strip() for item in finance_info.select('thead th')]
  annual_date = th_data[3:7]
  quarter_date = th_data[7:13]

  finance_index = [item.get_text().strip() for item in finance_info.select('th.h_th2')][3:]

  finance_data = [item.get_text().strip() for item in finance_info.select('td')]
  finance_data = np.array(finance_data)
  finance_data.resize(len(finance_index), 10)

  finance_date = annual_date + quarter_date

  finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)
  finance.to_csv(f"{os.path.join(company_sector,company_name)}.csv", sep='\t', encoding='utf-8')

def craw_sector(type_sector, sector_id, sector_name):
  url = f'https://finance.naver.com/sise/sise_group_detail.nhn?type={type_sector}&no={sector_id}'
  item_info = requests.get(url).text
  soup = BeautifulSoup(item_info, 'html.parser')
  finance_info = soup.select('div.box_type_l table.type_5 tbody')[0]

  th_data = [item for item in finance_info.select('tr')]
  th_data = th_data[:20]
  t_data = [(item.select('td.name div.name_area a')[0]["href"].split("=")[-1],
            item.select('td.name div.name_area a')[0].get_text().strip())
            for item in th_data]
  for code, name in t_data:
    finance_crawl(sector_name, code, name)

craw_sector("theme", 106, "bio")
craw_sector("upjong", 140, "chemi")
craw_sector("upjong", 154, "it")