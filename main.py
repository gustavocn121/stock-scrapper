import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import logging
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import os

BASE_URL = 'https://fundamentus.com.br'  
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}



def create_dirs():
    logging.info("Creating required directories")
    if not os.path.exists('./data'):
        os.makedirs('./data')
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

def get_stock_data(base_url:str , stock: str, headers: str) -> BeautifulSoup:
    logging.info(f"Getting stock data for {stock}")
    stock_url = f'{base_url}/detalhes.php?papel={stock}'
    response = requests.get(stock_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error: Failed to retrieve stock data! Response code: {response.status_code}")
    return BeautifulSoup(response.content, 'html.parser')

def extract_stock_info(soup: BeautifulSoup) -> pd.DataFrame:
    logging.info("Extracting stock info")
    all_data = []
    tables = soup.find_all('table', class_='w728')
    for table in tables[:-1]:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                label_1 = cols[0].find('span', class_='txt').text
                value_1 = cols[1].find('span', class_='txt').text if cols[1].find('span', class_='txt') else cols[1].text
                all_data.append([label_1, value_1])
            if len(cols) >= 4:
                label_2 = cols[2].find('span', class_='txt').text
                value_2 = cols[3].find('span', class_='txt').text if cols[3].find('span', class_='txt') else cols[3].text
                all_data.append([label_2, value_2])
    df_raw = pd.DataFrame(all_data, columns=['Label', 'Value'])
    return df_raw

def pivot_table(df):
    pivot_df = df.pivot_table(index=None, columns='Label', values='Value', aggfunc=lambda x: x)
    pivot_df.columns.name = None
    pivot_df = pivot_df.reset_index(drop=True)
    return pivot_df

def normalize_data(df_raw:pd.DataFrame) -> pd.DataFrame:
    logging.info("Normalizing data")
    df = df_raw[df_raw['Label'].notnull() & (df_raw['Label'] != '')]
    df.loc[:, 'Label'] = df['Label'].apply(unidecode)
    df.loc[:, 'Value'] = df['Value'].str.replace('\n', '') 
    df.loc[:, 'Label'] = df['Label'].str.replace('', '') 
    df.loc[:, 'Label'] = df['Label'].str.replace('.', '') 
    df.loc[:, 'Value'] = df['Value'].apply(unidecode)
    df = pivot_table(df)
    return df

def scrape_stock(stock):
    logging.info(f"Starting stock scrapper for {stock}")
    soup = get_stock_data(BASE_URL, stock, headers)
    df_raw = extract_stock_info(soup=soup)
    df_normalized = normalize_data(df_raw)
    logging.info(f"Stock data extraction and normalization complete for {stock}")
    return df_normalized

def run_scraper(ticker_list: list):
    with tqdm(total=len(ticker_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for stock in ticker_list:
                futures.append(executor.submit(scrape_stock, stock))
            for future in concurrent.futures.as_completed(futures):
                try:
                    df_normalized = future.result()
                    yield df_normalized
                except Exception as e:
                    logging.error(f"Error occurred while scraping stock: {e}")
                pbar.update(1)

def export_to_csv(df: pd.DataFrame, output: str) -> None:
    logging.info(f"Exporting data to {output}")
    df.to_csv(output, index=False)
   
def main():
    create_dirs()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=f'./logs/stock_scrapper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    tickers = pd.read_csv('stocks-b3.csv', sep=',').Ticker.to_list()
    df_result = pd.concat(run_scraper(ticker_list=tickers), ignore_index=True)

    output = f'./data/output_{datetime.now().strftime("%Y%m%d")}.csv'
    export_to_csv(df_result, output)

    print(df_result)


if __name__ == "__main__":
    main()

