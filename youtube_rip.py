import urllib.request as rl
import re
import os
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

S1_5Ds = "https://www.youtube.com/playlist?list=PLLnj-61LKXSFHP51q_svlZbFnZBeVbCoY"
S2_5Ds = "https://www.youtube.com/playlist?list=PLLnj-61LKXSGzqc6AITKFA7yDi22xTrV4"
yt_base = "https://www.youtube.com/watch?v="

def download_videos(urls):
    for i in range(len(urls)):
        filename = "S1E" + str(i+1)
        save_path = os.getcwd() + "\\audio_data"
        yt = YouTube(urls[i])
        audio_streams = yt.streams.filter(mime_type="audio/mp4")
        if audio_streams.count() > 0:
            audio_stream = audio_streams.first()
            audio_stream.download(save_path,filename)

def check(driver):
    error = download = None
    try:
        error = driver.find_element_by_css_selector("#error > p > a")
    except NoSuchElementException:
        pass
    try:
        download = driver.find_element_by_id("download")
        if download.get_attribute("href") == "":
            download = None
    except NoSuchElementException:
        pass
    return error, download
def download_alt(urls, max_wait):
    # max_wait = time to wait for video to download
    driver = webdriver.Chrome()
    driver.get("https://ytmp3.cc/")
    for url in urls:
        alt_helper(driver, url, max_wait)
    driver.quit()
def alt_helper(driver, url, max_wait):
    field = driver.find_element_by_id("input")
    field.clear()
    field.send_keys(url)
    field.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, max_wait).until(lambda driver: any(check(driver)))
    except TimeoutException:
        print("Maximum wait time exceeded.")
        pass
    error, download = check(driver)
    if error:
        error.click()
        alt_helper(driver, url, max_wait)
    elif download:
        download.click()
        WebDriverWait(driver, 1)
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_xpath("//*[text()='Convert next']").click()
    print(error, download)
def get_playlist_urls(playlist_url):
    playlist_html = rl.urlopen(playlist_url).read().decode('utf-8')
    # .*? non-greedy, then discard first two ids
    v_ids = re.findall("<a .* href=\"/watch\?v=(.*?)&", playlist_html)[2:]
    links = [yt_base + v_id for v_id in v_ids]
    return links

#download_videos(get_playlist_urls(S1_5Ds))
download_alt(get_playlist_urls(S2_5Ds)[58:], 300)
