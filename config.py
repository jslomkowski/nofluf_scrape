# import datetime

# depends on what you want to scrap. Setup this as first page
FIRST_PAGE = """
https://nofluffjobs.com/pl/artificial-intelligence?page=1
"""

# ## get date in format yyyy-mm-dd
# DATE = datetime.datetime.now().strftime("%Y-%m-%d")
# DATE = '2023-02-07'
NAME = "2023-02-09_ai"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
