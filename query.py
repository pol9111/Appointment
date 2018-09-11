from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from mail import send_mail
from celery import Celery


app = Celery('tasks',
             broker='redis://127.0.0.1:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, appointment, name='add every 10')


@app.task
def appointment():

    URL = 'http://www.xmzsh.com:8010/DiseaseRequestPage.aspx'


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    browser.get(URL)

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="ContentPlaceHolder2_TreeUnitt7"]')))
    submit.click()

    content = '约满'

    text = wait.until(EC.text_to_be_present_in_element((By.XPATH, '//tr[@id="row_p4"]/td[4]/span'), str(content)))

    if not text:
        MY_SENDER = 'biscuit36@163.com'  # 发件人邮箱账号
        MY_PASS = ''  # 发件人邮箱密码
        MY_USER = 'biscuit36@163.com'  # 收件人邮箱账号，我这边发送给自己
        send_mail(MY_SENDER, MY_PASS, MY_USER)


    print('约满')

    browser.close()


appointment()



