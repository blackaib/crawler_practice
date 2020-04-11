import os
import argparse
import pyperclip
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from furi_selenium.Detector import Detector
from furi_selenium.Purchaser import Purchaser
from furi_selenium.Sender import Sender

NAVER_LOGIN_PAGE = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
MASK_LIST_PAGE = 'https://smartstore.naver.com/mfbshop/category/6efebcf3498240c4bbe4f7ebab1ec940?cp=1'


def login_host(driver, args):
    try:
        driver.get(args.login_url)
        copy_paste(driver, '//*[@id="id"]', args.id)
        copy_paste(driver, '//*[@id="pw"]', args.passwd)
        driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    except Exception as e:
        print(e)


def copy_paste(driver, xpath, param):
    try:
        pyperclip.copy(param)
        driver.find_element_by_xpath(xpath).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    except Exception as e:
        print(e)


def main(args):
    try:
        driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 10)
        detector = Detector(driver, args)
        purchaser = Purchaser(driver, args)
        sender = Sender()
        login_host(driver, args)

        while True:
            if purchaser.success:
                print('Purchase Success')
                break

            url_item_dict = detector.get_valid_item_with_url()

            if sum(url_item_dict.values()) == 0:
                print('{} Nothing to buy'.format(datetime.datetime.now()))
                continue

            for url, valid_item in url_item_dict.items():
                if valid_item:
                    purchaser.buy(url)
                if purchaser.success:
                    sender.send_telegram_msg()
                    break
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='id', default=os.environ['ID'])
    parser.add_argument('--passwd', help='password', default=os.environ['PASS'])
    parser.add_argument('--size', help='Adult:1, Student:2, Children:3, Baby:4', nargs='+', default=[1, 2, 3, 4])
    parser.add_argument('--login_url', help='login site url', default=NAVER_LOGIN_PAGE)
    parser.add_argument('--target-url', help='target site url', default=MASK_LIST_PAGE)
    args = parser.parse_args()
    main(args)
