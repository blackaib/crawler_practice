from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Purchaser():
    SIZE = {1: "성인", 2: "학생", 3: "아동", 4: "유아"}
    size_dropbox = '//*[@id="wrap"]/div/div/div/form/fieldset/div/div/ul/li/ul/li/div/div/div'
    size_dropbox_list = '//*[@id="wrap"]/div/div/div/form/fieldset/div/div/ul/li/ul/li/div/select'
    skip_payment = '/html/body/div[10]/div[3]/div[1]/form[1]/div/div[5]/div[1]/div[2]/ul/li[3]/ul/li[2]/span[1]'
    account_dropdown = '//*[@id="skipPaymentMethodSelectBox"]'
    pay_with_account = '/html/body/div[3]/div/ul/li[1]'
    agreement_checkbox = '/html/body/div[10]/div[3]/div[1]/form[1]/div/div[5]/div[1]/div[3]/div/span/span'
    final_payment = '/html/body/div[10]/div[3]/div[1]/form[1]/div/div[7]/button'

    def __init__(self, driver, args):
        self.driver = driver
        self.success = False
        self.args = args

    def buy(self, url):
        try:
            print('Purchase Start')
            if self._try_purchase(url):
                self._wait_click_xpath(Purchaser.skip_payment)                         # 나중에 결제 선택
                self._wait_click_xpath(Purchaser.account_dropdown)                     # 결제구분 드롭다운 클릭
                self.driver.find_element_by_xpath(Purchaser.pay_with_account).click()  # 나중에 계좌 결제 선택
                self._wait_click_xpath(Purchaser.agreement_checkbox)                   # 전체 동의 체크
                self._wait_click_xpath(Purchaser.final_payment)                        # 최종 결제 클릭
                self.success = True
                print('Purchase End')
        except Exception as e:
            print(e)

    def _try_purchase(self, url):
        try:
            self.driver.get('https://smartstore.naver.com' + url)
            print('Page open done')
            size_select = self._get_size_list()

            for i in range(1, len(size_select.options)):
                inner_text = size_select.options[i].get_attribute('innerText')
                if self._is_my_size(inner_text) and '품절' not in inner_text:
                    self.driver.find_element_by_xpath('/html/body/div[2]/div/ul/li[{}]'.format(i + 1)).click()
                    self.driver.find_elements_by_class_name('buy')[0].click()
                    return True
            return False
        except Exception as e:
            self._try_purchase(url)

    def _is_my_size(self, inner_text):
        for size in self.args.size:
            if Purchaser.SIZE[int(size)] in inner_text:
                return True

    def _get_size_list(self):
        self._wait_click_xpath(Purchaser.size_dropbox)
        return Select(self.driver.find_element_by_xpath(Purchaser.size_dropbox_list))

    def _wait_click_xpath(self, string):
        WebDriverWait(self.driver, 3, 0.005).until(EC.element_to_be_clickable((By.XPATH, string))).click()
