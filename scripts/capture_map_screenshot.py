from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


def capture_map(html_path='figures/map/spacex_launch_map.html', out_png='figures/map/spacex_launch_map.png'):
    if not os.path.exists(html_path):
        raise FileNotFoundError(html_path)
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1200,800')

    driver = webdriver.Chrome(options=opts)
    url = 'file://' + os.path.abspath(html_path)
    driver.get(url)
    time.sleep(2)
    driver.save_screenshot(out_png)
    driver.quit()


if __name__ == '__main__':
    try:
        capture_map()
        print('Map screenshot saved to figures/map/spacex_launch_map.png')
    except Exception as e:
        print('Failed to capture map:', e)
