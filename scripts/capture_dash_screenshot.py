from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


def capture_dash(app_url='http://127.0.0.1:8050', out_png='figures/map/dash_screenshot.png'):
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1200,900')

    driver = webdriver.Chrome(options=opts)
    driver.get(app_url)
    time.sleep(2)
    driver.save_screenshot(out_png)
    driver.quit()


if __name__ == '__main__':
    try:
        capture_dash()
        print('Dash screenshot saved to figures/map/dash_screenshot.png')
    except Exception as e:
        print('Failed to capture dash:', e)
