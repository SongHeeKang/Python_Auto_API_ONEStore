# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

reload(sys)
sys.setdefaultencoding('utf-8')

try:

    options = webdriver.ChromeOptions()
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('windows-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # linux
    driver = webdriver.Chrome('/chromedriver/chromedriver', chrome_options=options)
    # windows
    # driver = webdriver.Chrome('D:\Setup\Python\chromedriver.exe', chrome_options=options)

    driver.implicitly_wait(3)
    driver.get('http://onetests.onestorecorp.com/login')

    # 아이디 입력 (구사번)
    driver.find_element_by_name("username").send_keys("jenkins_readonly")

    # 비밀번호 입력
    driver.find_element_by_name("password").send_keys("jenkins123!")

    print "=" * 30

    print driver.page_source
    print "=" * 30

    # 로그인 버튼 선택
    driver.find_element_by_xpath("""//*[@id="app"]/div[2]/div/div/div/form/div[1]/button""").click()

    # Suites 메뉴 선택
    driver.find_element_by_xpath("""//*[@id="pageHeader"]/div/a[4]""").click()

    # Suites 페이지에서 특정 XPATH 찾기 (찾지 못할 경우 10초 뒤에  "TimeOut")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="app"]/div[2]/div/div[4]/table/tbody/tr[1]/td[1]"""))
        )
    except TimeoutException:
        print "TimeOut"

    # =================================================================================================================#
    # SKT UNIT TEST Suite 진행
    # SERVICE 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("serviceFilter").click()
    for option in driver.find_elements_by_id("serviceItem"):
        if option.text == '[QA] API 자동화-SCENARIO TEST':
            option.click()

    # 2초 대기
    time.sleep(2)

    # SERVICE-VARIABLES 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("EnvironmentDropdown").click()
    for option in driver.find_elements_by_xpath("""//*[@id="EnvironmentDropdown"]/div/div[2]"""):
        if option.text == '[QA] API 자동화-SCENARIO TEST':
            option.click()

    # 2초 대기
    time.sleep(2)

    # 전체 체크 박스 선택
    driver.find_element_by_xpath("""//*[@id="selectAllSuites"]""").click()

    # 2초 대기
    time.sleep(2)

    # Suites 실행 버튼 선택
    driver.find_element_by_xpath("""//*[@id="app"]/div[2]/div/div[3]/div[2]/button[2]""").click()

    # 2초 대기
    time.sleep(2)

    # 실행 팝업 화면 > 확인 버튼 선택
    driver.switch_to.alert.accept()

    # 5초 대기
    time.sleep(10)

    ########### 크롬 브라우저 새 탭 (KT) ##########
    driver.execute_script(
        "(function() { " +
        "window.open('http://onetests.onestorecorp.com/suites', 'second');" +
        "})();"
    )

    driver.switch_to.window("second")

    # =================================================================================================================#
    # KT UNIT TEST Suite 진행
    # SERVICE 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("serviceFilter").click()
    for option in driver.find_elements_by_id("serviceItem"):
        if option.text == '[QA] KT API 자동화-SCENARIO TEST':
            option.click()

    # 2초 대기
    time.sleep(2)

    # SERVICE-VARIABLES 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("EnvironmentDropdown").click()
    for option in driver.find_elements_by_xpath("""//*[@id="EnvironmentDropdown"]/div/div[2]"""):
        if option.text == '[QA] API 자동화-SCENARIO TEST-KT':
            option.click()

    # 2초 대기
    time.sleep(2)

    # 전체 체크 박스 선택
    driver.find_element_by_xpath("""//*[@id="selectAllSuites"]""").click()

    # 2초 대기
    time.sleep(2)

    # Suites 실행 버튼 선택
    driver.find_element_by_xpath("""//*[@id="app"]/div[2]/div/div[3]/div[2]/button[2]""").click()

    # 2초 대기
    time.sleep(2)

    # 실행 팝업 화면 > 확인 버튼 선택
    driver.switch_to.alert.accept()

    # 5초 대기
    time.sleep(10)

    ########### 크롬 브라우저 새 탭 (LG) ##########
    driver.execute_script(
        "(function() { " +
        "window.open('http://onetests.onestorecorp.com/suites', 'third');" +
        "})();"
    )

    driver.switch_to.window("third")

    # =================================================================================================================#
    # LG UNIT TEST Suite 진행
    # SERVICE 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("serviceFilter").click()
    for option in driver.find_elements_by_id("serviceItem"):
        if option.text == '[QA] LG API 자동화-SCENARIO TEST':
            option.click()

    # 2초 대기
    time.sleep(2)

    # SERVICE-VARIABLES 필터 드랍다운 버튼 선택 > 리스트에서 "[QA] API 자동화-SCENARIO TEST" 항목 선택
    driver.find_element_by_id("EnvironmentDropdown").click()
    for option in driver.find_elements_by_xpath("""//*[@id="EnvironmentDropdown"]/div/div[2]"""):
        if option.text == '[QA] API 자동화-SCENARIO TEST-LG':
            option.click()

    # 2초 대기
    time.sleep(2)

    # 전체 체크 박스 선택
    driver.find_element_by_xpath("""//*[@id="selectAllSuites"]""").click()

    # 2초 대기
    time.sleep(2)

    # Suites 실행 버튼 선택
    driver.find_element_by_xpath("""//*[@id="app"]/div[2]/div/div[3]/div[2]/button[2]""").click()

    # 2초 대기
    time.sleep(2)

    # 실행 팝업 화면 > 확인 버튼 선택
    driver.switch_to.alert.accept()

    # 5초 대기
    time.sleep(5)

    # Suites 수행 완료까지 대기
    try:
        element = WebDriverWait(driver, 500).until(
            EC.text_to_be_present_in_element((By.XPATH, """//*[@id="app"]/div[2]/div/div[3]/div[1]/div[2]/label"""),
                                             'Case(0/0) :  ')
        )
    except TimeoutException:
        print "UNIT TEST Suite 진행중 에러가 발생했습니다."

    # 30초 대기
    time.sleep(30)

except Exception as e:
    print e
    print "except"
    driver.quit()

finally:
    print "finally..."
    driver.quit()
