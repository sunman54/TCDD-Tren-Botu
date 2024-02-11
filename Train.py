import re
import sqlite3
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

tcdd_link = "https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf"

nereden_xpath = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[1]/p[4]/input"
nereye_xpath =  "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[2]/p[4]/input"
gidiş_tarihi_xpath = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[1]/p[6]/span/input"
gidiş_tarihi_popup_kapatma_xpath = "/html/body/div[7]/div[2]/button[2]"
ara_xpath = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[3]/p[3]/button"

tren_tablo_xpath = "/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody"



def get_train(tarih, nereden, nereye):
    driver = webdriver.Chrome()
    driver.get(tcdd_link)
    wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)


    nereden_input = driver.find_element(By.XPATH, nereden_xpath)
    nereye_input = driver.find_element(By.XPATH, nereye_xpath)
    gidiş_tarihi_input = driver.find_element(By.XPATH, gidiş_tarihi_xpath)
    ara_input = driver.find_element("xpath", ara_xpath)


    gidiş_tarihi_input.clear()
    gidiş_tarihi_input.send_keys(tarih)

    nereden_input.clear()
    nereden_input.send_keys(nereden)

    nereye_input.clear()
    nereye_input.send_keys(nereye)

    gidiş_tarihi_popup_kapatma = driver.find_element(By.XPATH, gidiş_tarihi_popup_kapatma_xpath)
    gidiş_tarihi_popup_kapatma.click()


    ara_input.click()

    tren_tablosu = wait.until(EC.visibility_of_element_located((By.XPATH, tren_tablo_xpath)))
    #tren_tablosu = driver.find_element(By.XPATH, tren_tablo_xpath)

    tren_tablo_satırlar = tren_tablosu.find_elements(By.TAG_NAME, 'tr')

    trains = []
    for satır in tren_tablo_satırlar :
        boxes = satır.find_elements(By.TAG_NAME, 'td')
        çıkış = boxes[0].text.replace("\n", "\t")
        varış = boxes[2].text.replace("\n", "\t")
        vagon = boxes[4].text.replace("\n", "\t")
        ücret = boxes[-2].text.replace("\n", "\t")
        print(çıkış, varış, vagon, ücret)
        trains.append((çıkış, varış, vagon, ücret))

    driver.quit()
    return trains
if __name__ == '__main__':
    get_train('17.02.2024', 'Arifiye', 'Ankara Gar')

    