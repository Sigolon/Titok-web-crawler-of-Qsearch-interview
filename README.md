# Titok-web-crawler-of-Qsearch-interview

[![hackmd-github-sync-badge](https://hackmd.io/amVv-prjSams7Wq-q2yEiQ/badge)](https://hackmd.io/amVv-prjSams7Wq-q2yEiQ)


## Abstract
本專案為，Qsearch 公司，實習爬蟲工程師職缺，第二階段測驗的實作題目。

**實作要求**
TikTok (https://www.tiktok.com/) 已經逐漸成為台灣指標的社群媒體之一，要請你不直接使用第三方爬蟲套件(ex. tiktok-scraper)的前提下，以 python 實作 tiktok 爬蟲。追蹤頻道 geevideo 資訊。

**內容包括**
持續追蹤自收到筆試邀請信後的隔一天起，頻道發布的貼文內容三天(若有新發文就擴增追蹤清單) ，並每 1 小時連續追蹤愛心數、留言數、收藏數、分享數三天的時間
最後成果，你需要告知監測哪三天時間。在 Demo 時，請你用任何視覺化套件 ，將監測期間內各個互動指標的折線圖畫出來。

**求職結果**
於第三階段面試被淘汰。

## How to do
本專案將實作要求分成三部分處理，
爬取貼文 ID、根據 ID 爬取數據、爬蟲數據清理並視覺化。

**Step 1-1** :  進入 [Titok geevideo ](https://www.tiktok.com/@geevideo)，爬取每篇貼文的 ID，先爬取 ID 的理由在於，按讚數等 互動指標，並非在 [Titok geevideo ](https://www.tiktok.com/@geevideo) 頁面，而是會根據貼文 ID 放置於對應的 URL。
ID = 7346427229154413825  https://www.tiktok.com/@geevideo/video/7346427229154413825

[Titok geevideo ](https://www.tiktok.com/@geevideo)示例
![image](https://hackmd.io/_uploads/SJaoRB2CT.png)

![image](https://hackmd.io/_uploads/rykEkLnAp.png)

**Step 1-2** : 由於本專案的開發時程較趕，故採用 Selenium 進行開發。操作 Webdriver 模擬使用者行為，並利用 OpenCV 破解滑動驗證碼，最後提取貼文 ID。如下，

{%youtube hu9KAS6SQEY %}


**Step 2**
根據爬取到的 貼文 ID，進一步爬取數據。
![image](https://hackmd.io/_uploads/B1Pk68nRT.png)

**Step 3**
基於 matplotlib 套件，自動化繪製每筆貼文的四種互動指標折線圖，

{%youtube tXwoGim7n08 %}
[![IMAGE ALT TEXT](http://img.youtube.com/vi/tXwoGim7n08/0.jpg)](https://www.youtube.com/watch?v=tXwoGim7n08 step3)

## Package Request
python 3.11.7
- selenium - 4.18.1
- opencv-python - 4.9.0.9.80
- matplotlib 3.8.3
- requests 2.31.0

Webdriver
- Edgedrive 122.0.2365.66 

## Folder Structure
![image](https://hackmd.io/_uploads/SJfnHD2A6.png)
- `crawler_code`: Contains the code for web crawling.
  - `picture`: Stores pictures for ETL_to_plot.ipynb.
  - `ttf`: TrueType font files for matplotlib.
  - `crawler_code.ipynb`、`ETL_to_plot.ipynb` : Detailed Explanation of Program Execution Steps
  - `call_bat.py` : Script for Monitoring Data for Three Days


- `data_backed`: Backed up data.
- `data_base`: Main data storage.
- `html_data`: HTML data files.
- `html_data_backed`: Backed up HTML data.
- `line_plot`: Line plot visualizations.
- `post_index_html`: HTML files for post indexing.
- `post_index_html_backed`: Backed up HTML files for post indexing.

