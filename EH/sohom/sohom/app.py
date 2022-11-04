from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

app = Flask(__name__)
@app.route('/not_logged_in')
def not_logged_in():
    url = request.args.get('url')
    global options
    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',options=options)
    driver.get(url)
    time.sleep(20)
    driver.close()
    return 'OK'
@app.route('/logged_in')
def logged_in():
    url = request.args.get('url')
    global options
    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',options=options)
    try:
        mail_address = 'dummyfake356@gmail.com'
        password = 'Ab12cd34!#'
        driver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.co.jp/')
        driver.find_element("id","identifierId").send_keys(mail_address)
        next = driver.find_elements('xpath',"//*[contains(text(), 'Next')]")
        for btn in next:
            btn.click()
        time.sleep(2)
        driver.find_element("name","Passwd").send_keys(password)
        next = driver.find_elements('xpath',"//*[contains(text(), 'Next')]")
        for btn in next:
            btn.click()
    except Exception as e:
        pass
    time.sleep(10)
    driver.get(url)
    time.sleep(20)
    driver.close()
    return 'OK'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)