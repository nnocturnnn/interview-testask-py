from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

def get_selenium_driver():
    chrome_options = Options()
    # chrome_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(),
                                chrome_options=chrome_options) 
    return driver








if __name__ == "__main__":
    test_result = []
    driver = get_selenium_driver()
    driver.get("https://netpeak.ua/")
    driver.find_element_by_xpath("//li[@data-content='58']").click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//a[contains(text(),'Команда')]").click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//a[contains(text(),'Стать частью команды')]").click()
    driver.implicitly_wait(5)
    driver.switch_to.window(driver.window_handles[1])
    test_result.append(driver.title.startswith("Работа в Netpeak"))
    
    driver.close()
