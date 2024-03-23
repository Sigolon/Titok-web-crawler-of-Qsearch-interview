# ------------------------------------------------------------------ selenium get https://www.tiktok.com/@geevideo -----------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time, requests
from matplotlib import pyplot as plt
import cv2 
import os
from datetime import timezone, datetime, timedelta
import traceback
from bs4 import BeautifulSoup



def find_captcha_dx() :     
    captcha_image_url = driver.find_element(By.ID, "captcha-verify-image").get_attribute('src')
    response = requests.get(captcha_image_url)

    with open("captcha_image.jpeg", "wb") as f:
        f.write(response.content)

    # import opencv use Edge Detection
    captcha_image_path = "captcha_image.jpeg"
    captcha_image_resorce = cv2.imread(captcha_image_path, cv2.IMREAD_GRAYSCALE)
    ret, img_gray = cv2.threshold(captcha_image_resorce, 127, 255, cv2.THRESH_BINARY_INV) # 如果大於 127 就等於 0，反之等於 255。
    canny = cv2.Canny(img_gray, 30, 150)

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  
    token = 0
    dx = 229
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (70 < w < 120) & (70 < h < 120) : 
            # result = {"dx" : x, "dy" : y, "dw" : w, "dh" : h, "wh" : [w, h]}
            # token.append(result)
            dx = x*(340/552)
            cv2.rectangle(captcha_image_resorce, (x, y), (x + w, y + h), (0, 0, 255), 2)
            token = 1
            break
        else : 
            continue
    if token == 1 : 
        plt.imshow(captcha_image_resorce)
        return dx
    
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (75 < w < 120) & (35 < h < 60) : 
            # result = {"dx" : x, "dy" : y, "dw" : w, "dh" : h, "wh" : [w, h]}
            # token.append(result)
            dx = x*(340/552)
            cv2.rectangle(captcha_image_resorce, (x, y), (x + w, y + h), (0, 0, 255), 2)
            token = 1
            break
        else : 
            continue
    if token == 1 : 
        plt.imshow(captcha_image_resorce)
        return dx

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (70 < h < 120) : 
            # result = {"dx" : x, "dy" : y, "dw" : w, "dh" : h, "wh" : [w, h]}
            # token.append(result)
            dx = x*(340/552)
            cv2.rectangle(captcha_image_resorce, (x, y), (x + w, y + h), (0, 0, 255), 2)
            token = 1
            break
        else : 
            continue
    if token == 1 : 
        plt.imshow(captcha_image_resorce)
        return dx
    
    return dx

print("----------------------------------------------------------------------------------------------------------------------------------") # 排程腳本保存每次輸出的 log 使用之分隔線
print((datetime.now(timezone.utc) + timedelta(hours=8)))
print((datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H'))
verify_results = 0
for times in range(10) : # 輸入 70 次驗證碼，都不過的機率是，(2/3)**70，約 等於 10 的負13次方。大概率有其他的問題要處理。
    if verify_results == 1 : 
        print("post_index_updata_succeed")
        # driver.close()
        driver.quit()
        break
    else : 
        pass

    try : 
        driver = webdriver.Edge()
        driver.get("https://www.tiktok.com/@geevideo")

        # 輸入驗證碼，平均每 3 次成功一次。
        for find_dx_times in range(10) : 
            # 不讀取圓形驗證碼
            time.sleep(5)
            for second in range(5) : 
                try:
                    btn = driver.find_element(By.CLASS_NAME, "sc-cSHVUG")
                    print("出現圓形驗證碼")
                    driver.refresh()
                    time.sleep(3)
                    continue
                except  : 
                    print("未出現圓形驗證碼")
                    break

            # 尋找驗證碼位置
            for second in range(20) : # 給 20 秒的判斷時間，防止網路速度不穩
                try:
                    btn = driver.find_element(By.CLASS_NAME, "react-draggable")
                    print("找到驗證碼_token")
                    time.sleep(1)
                    break
                except  : 
                    time.sleep(1)
                    continue

            print(f"第 {find_dx_times+1} 輸入") # 7次以後 move 會自己丟失，推測是套件本身的問題。
            dx = find_captcha_dx() # 平均 3 次成功辨識 1 次。
            btn =  driver.find_element(By.CLASS_NAME, "react-draggable")
            move = ActionChains(driver)
            move.click_and_hold(btn).perform()
            move.move_by_offset(dx//3, 0).perform()
            move.move_by_offset(dx//3, 0).perform()
            move.move_by_offset(dx//3, 0).perform()
            move.move_by_offset(dx%3, 0).perform()
            move.move_by_offset(-5, 1).perform()
            move.release(btn).perform()

            time.sleep(3)
            driver.refresh()
            time.sleep(5)

            # 下載頁面資訊
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')


            try : 
                if soup.find("a", {"class" : "css-1wrhn5c-AMetaCaptionLine eih2qak0", "tabindex" : "-1"})["href"]:
                    print("驗證成功")
                    with open(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "post_index_html", "index_data.html")), "w", encoding="utf-8") as f:
                        f.write(html_content)
                    verify_results = verify_results+1
                    break
                else : 
                    continue
            except : 
                continue
            
                
    except : 
        # driver.close()
        driver.quit()
        continue

# ------------------------------------------------------------------ parser html to update post index ------------------------------------------------------------------------
print("parser html")
from bs4 import BeautifulSoup
import pandas
import shutil

with open(os.path.join(os.path.dirname(os.getcwd()), "post_index_html", "index_data.html"), 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')
user_post_item_list = soup.find("div", {"data-e2e" : "user-post-item-list", "mode" : "compact", "class" : "css-wjuodt-DivVideoFeedV2"})

index_result_list = []
user_post_item_list = user_post_item_list.find_all("div", {"class" : "css-x6y88p-DivItemContainerV2 e19c29qe8"})
for user_post_item in user_post_item_list :

    post_title = user_post_item.find("a", {"class" : "css-1wrhn5c-AMetaCaptionLine eih2qak0", "tabindex" : "-1"})["title"]
    post_href = user_post_item.find("a", {"class" : "css-1wrhn5c-AMetaCaptionLine eih2qak0", "tabindex" : "-1"})["href"]

    index_result = {
        "post_title" : post_title,
        "post_href" : post_href
    }

    index_result_list.append(index_result)
    
df_update = pandas.DataFrame(index_result_list)

df = pandas.read_csv(os.path.join(os.path.dirname(os.getcwd()), "data_base", "post_index.csv"))
df = pandas.concat([df, df_update], ignore_index=True)
df = df.drop_duplicates()
df = df.reset_index(drop=True)

df.to_csv(os.path.join(os.path.dirname(os.getcwd()), "data_base", "post_index.csv"), index=False)

parser_time = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H")
shutil.move(os.path.join(os.path.dirname(os.getcwd()), "post_index_html", "index_data.html"), os.path.join(os.path.dirname(os.getcwd()), "post_index_html_backed", f'{parser_time}_index_data.html'))
