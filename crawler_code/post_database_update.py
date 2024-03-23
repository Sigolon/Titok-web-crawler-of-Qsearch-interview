from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time, requests
import os, pandas
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------------- update_post_informatiom -----------------------------------------------------------------------
print("get_post_html")
driver = webdriver.Edge()
driver.get('about:start')

df_update = pandas.read_csv(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "data_base", "post_index.csv")))
post_href_list = df_update["post_href"]

for parser_times in range(len(post_href_list)) : 

    driver.execute_script(f"window.open('{post_href_list[parser_times]}');")
    # print(post_href_list[parser_times])
    
    # 不讀取圓形驗證碼
    time.sleep(5)
    for second in range(5) : 
        try:
            btn = driver.find_element(By.CLASS_NAME, "sc-kAzzGY")
            print("出現圓形驗證碼")
            driver.refresh()
            time.sleep(3)
            continue
        except  : 
            print("未出現圓形驗證碼")
            break


    # 取得所有分頁的編號
    all_handles = driver.window_handles

    driver.switch_to.window(all_handles[1])

    # 等待數據欄位
    time.sleep(5)

    html_content = driver.page_source
    post_id = post_href_list[parser_times].split("/")[-1]
    with open(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "html_data", f"{post_id}.html")), "w", encoding="utf-8") as f:
        f.write(html_content)

    driver.close()
    
    # 切回起點視窗
    driver.switch_to.window(all_handles[0])

# driver.close()
driver.quit()


# --------------------------------------------------------------------------- parser_html ------------------------------------------------------------------------------------------------
print("parser_post_html")
from bs4 import BeautifulSoup
from datetime import timezone, datetime, timedelta
import shutil, traceback

data_result_list = []
html_data_folder = os.path.join(os.path.join(os.path.dirname(os.getcwd()), "html_data"))
for html_data_folder, dirs, html_datas in os.walk(html_data_folder) : 
    for html_data in html_datas : 

        try :  
            with open(os.path.join(html_data_folder, html_data), 'r', encoding='utf-8') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            data_div = soup.find("div", {"class" : "css-1npmxy5-DivActionItemContainer er2ywmz0"})
        except : 
            data_result = {
                "post_id" : html_data.replace(".html", ""),
                "post_title" : None,
                "parser_time" : (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H"),
                "like-count" : None,
                "comment_count" : None,
                "collection" : None,
                "share_count" : None
            }
            data_result_list.append(data_result)
            break

        post_id = html_data.replace(".html", "")
        
        try : 
            post_title = soup.find("meta", {"property" : "twitter:description", "data-rh" : "true"})["content"]
        except : 
            post_title = None

        try : 
            like_count = data_div.find("strong", {"data-e2e" : "like-count"}).text
        except : 
            like_count = None
        
        try : 
            comment_count = data_div.find("strong", {"data-e2e" : "comment-count"}).text
        except : 
            comment_count = None
        
        try : 
            collection = data_div.find("strong", {"data-e2e" : "undefined-count"}).text
        except : 
            collection = None
        
        try : 
            share_count = data_div.find("strong", {"data-e2e" : "share-count"}).text
        except : 
            share_count = None

        data_result = {
            "post_id" : post_id,
            "post_title" : post_title,
            "parser_time" : (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H"),
            "like-count" : like_count,
            "comment_count" : comment_count,
            "collection" : collection,
            "share_count" : share_count
        }
        data_result_list.append(data_result)
        
        
        # 移動 html_data ，保留原始檔以利後續 debug
        parser_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H")
        shutil.move(os.path.join(html_data_folder, html_data), os.path.join(os.path.join(os.path.dirname(os.getcwd()), "html_data_backed", f'{parser_time}_{html_data}')))

df_update = pandas.DataFrame(data_result_list)

# 資料備份
df_update.to_csv(os.path.join(os.path.dirname(os.getcwd()), "data_backed" ,f"{(datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H')}.csv"), index=False)

# 資料串接
df = pandas.read_csv(os.path.join(os.path.dirname(os.getcwd()), "data_base", "data_base.csv"), index_col=None)
df = pandas.concat([df, df_update], ignore_index=True)
df = df.drop_duplicates()
df = df.reset_index(drop=True)

# 資料更新完成
df.to_csv(os.path.join(os.path.dirname(os.getcwd()), "data_base", "data_base.csv"), index=False)

