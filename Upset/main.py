import random
import string

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def check_exists_by_xpath(xpath: str, driver: webdriver) -> bool:
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def get_random_string(N: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


def run_tests(driver: webdriver) -> None:
    driver.get("https://netpeak.ua/")
    driver.find_element_by_xpath("//li[@data-content='58']").click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//a[contains(text(),'Команда')]").click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath(
        "//a[contains(text(),'Стать частью команды')]").click()
    driver.implicitly_wait(5)
    driver.switch_to.window(driver.window_handles[1])
    assert(driver.title.startswith("Работа в Netpeak"))
    assert(check_exists_by_xpath(
        "//a[contains(text(),'Я хочу работать в Netpeak')]", driver))
    assert(driver.find_element_by_xpath(
        "//a[contains(text(),'Я хочу работать в Netpeak')]").is_enabled())
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath("//a[contains(text(),'Личный каби')]").click()
    assert(check_exists_by_xpath("//span[contains(text(),'Войти')]",
                                 driver) == False)
    driver.switch_to.window(driver.window_handles[2])
    login = driver.find_element_by_name("login")
    passwd = driver.find_element_by_name("password")
    login.send_keys(get_random_string(10))
    passwd.send_keys(get_random_string(10))
    driver.find_element_by_xpath("//md-checkbox[@aria-label='gdpr']").click()
    driver.find_element_by_xpath("//span[contains(text(),'Войти')]").click()
    assert(check_exists_by_xpath("//span[@class='md-toast-text ng-binding']",
                                 driver))
    assert(len(driver.find_elements_by_xpath(
        "//md-input-container[@class='input-container md-input-invalid']")) == 2)


if __name__ == "__main__":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    run_tests(driver)
    driver.quit()
    print("All tests done")