# -*- coding: utf-8 -*-
import sys
import datetime
import json
import requests
from selenium import webdriver
from time import sleep

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
    # driver = webdriver.Chrome('D:\Chrome Drvier\chromedriver.exe', chrome_options=options)

    driver.implicitly_wait(3)
    driver.get('http://onetests.onestorecorp.com/login')

    # login
    # id, password
    driver.find_element_by_name('username').send_keys('jenkins_readonly')
    driver.find_element_by_name('password').send_keys('jenkins123!')
    sleep(2)
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/form/div[1]/button').click()

    try:
        P = ['[상용] API 자동화-UNIT TEST']
        # P = ['[QA] API 자동화-UNIT TEST', '[QA] KT API 자동화-UNIT TEST', '[QA] LG API 자동화-UNIT TEST']
        for U in P:

            # suite
            driver.get('http://onetests.onestorecorp.com/suites')
            sleep(2)
            driver.find_element_by_xpath('//*[@id="serviceFilter"]/i').click()
            sleep(2)
            driver.find_element_by_xpath("//*[contains(text(),'" + U + "')]").click()
            sleep(2)
            driver.find_element_by_xpath('//*[@id="EnvironmentDropdown"]/i').click()
            sleep(2)
            driver.find_element_by_xpath('//*[@id="EnvironmentDropdown"]/div/div[2]').click()
            sleep(2)
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[4]/table')
            sleep(2)

            _tables = driver.find_element_by_css_selector("table")
            tables = str(_tables.text).split('\n')

            rows = len(tables)

            # if U == 'PROD-AUTOMATION-UNITTEST':
            #     A = 'SKT'
            # else:
            #     if U == '[QA] KT API 자동화-UNIT TEST':
            #         A = 'KT'
            #     else:
            #         if U == '[QA] LG API 자동화-UNIT TEST':
            #             A = 'LG'
            A = 'SKT'

            pre_jandi_message = ''
            end_jandi_message = "\n" + '*' + str(A) + " API 호출 실패 내역\n"
            text_link_dict = {}
            # text_link_dict['[ERR]'] = '예외 관련'
            text_link_dict['[MEM]'] = '회원 관련'
            text_link_dict['[SAC]'] = 'SAC 단위'
            text_link_dict['[CCS]'] = 'CCS 단위'

            # loop table rows except first row
            # tableRowNum = [1, 9, 17, 25]
            tableRowNum = [20, 28, 36]
            for i in tableRowNum:
                text_link = tables[i].split(' ')[1]
                print '-' * 50
                print text_link
                print '-' * 50
                driver.find_element_by_xpath("//td[contains(text(), '" + text_link + "')]")
                sleep(2)

                print '-' * 50
                print str(tables[i + 2])  # Totla 95
                print str(tables[i + 3])  # success 95
                print str(tables[i + 4])  # fail 0
                print str(tables[i + 5])  # | 95
                print str(tables[i + 6])  # 0
                print str(tables[i + 7])  # PerformanceTime
                print '-' * 50

                passed = str(tables[i + 3])
                scriptpassed = str(tables[i + 5])
                fail = str(tables[i + 4])
                script_fail = str(tables[i + 6])
                PerformanceTime = str(tables[i + 7])
                realpassed = scriptpassed.split(' ')[3]

                print "-" * 50
                print type(fail)
                print type(script_fail)
                print "-" * 50

                total_fail = int(fail) + int(script_fail)

                # all pass...
                if int(fail) + int(script_fail) == 0:
                    pre_jandi_message += text_link_dict[text_link] + ' = ' + str(realpassed) + ' Passed' + ' : ' + str(
                        total_fail) + ' Failed' + ' ' + '(' + str(PerformanceTime) + ')' + '\n'
                    continue

                # Not all pass...
                else:
                    driver.find_element_by_xpath("//td[contains(text(), '" + text_link + "')]").click()
                    pre_jandi_message += text_link_dict[text_link] + ' = ' + str(realpassed) + ' Passed' + ' : ' + str(
                        total_fail) + ' Failed' + ' ' + '(' + str(PerformanceTime) + ')' + '\n'
                    print pre_jandi_message
                    # click detail view...
                    driver.find_element_by_xpath(
                        '//*[@id="app"]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[4]/button[1]').click()
                    sleep(5)
                    # for icon_line_list
                    print '-' * 50
                    print 'icon line list'
                    print '-' * 50
                    icon_line_list = driver.find_elements_by_css_selector("div[class='ui icon message']")
                    i = 0

                    end_jandi_message += str(text_link_dict[text_link]) + '\n'

                    for icon_line in icon_line_list:
                        subject = str(icon_line.find_element_by_class_name('header').text).split(' ')[3:]
                        # 1. subject
                        subject = " ".join(subject)
                        # 2. call link
                        call_link = driver.find_elements_by_partial_link_text('호출이력 상세 보기')[i].get_attribute('href')
                        # 3. 4 factors
                        factors = icon_line.find_elements_by_css_selector("div[class='ui left labeled mini button']")

                        i += 1
                        judgment_str = ''

                        print "factors length : " + str(len(factors))
                        if len(factors) < 4:
                            status = 'None'
                            header = 'None'
                            body = 'None'
                            script = 'None'
                            check_bad = 'None'
                            continue
                        for f in factors:
                            ss = str(f.text) + ','
                            judgment_str += ss

                        # factors
                        status = judgment_str.split(',')[0].split('\n')[1]
                        header = judgment_str.split(',')[1].split('\n')[1]
                        body = judgment_str.split(',')[2].split('\n')[1]
                        script = judgment_str.split(',')[3].split('\n')[1]
                        check_bad = status + ' ' + header + ' ' + body + ' ' + script
                        # print out...
                        # if 'BAD' in check_bad :
                        if 'BAD' in check_bad:
                            end_jandi_message += str(subject) + '\t' + str(call_link) + '\n'
                            print subject
                            print call_link

                    sleep(2)
                    driver.back()
                    sleep(2)

            print '-' * 50
            print pre_jandi_message.rstrip()
            print end_jandi_message.rstrip()
            print '-' * 50

            # if U == '[QA] API 자동화-UNIT TEST':
            if A == 'SKT':
                SKTJandi = '[SKT 상용환경 API Check] \n' + pre_jandi_message + end_jandi_message + '\n'
                print SKTJandi
            # else:
            #     if U == '[QA] KT API 자동화-UNIT TEST':
            #         KTJandi = '[KT QA환경 API Check] \n' + pre_jandi_message + end_jandi_message + '\n'
            #         print KTJandi
            #         continue
            #     else:
            #         if U == '[QA] LG API 자동화-UNIT TEST':
            #             LGJandi = '[LG QA환경 API Check] \n' + pre_jandi_message + end_jandi_message
            #             print LGJandi
            #             continue

        print '-' * 50
        print 'SKTJandi -' + SKTJandi
        # print 'KTJandi -' + KTJandi
        # print 'LGJandi -' + LGJandi
        print '-' * 50

        # send to jandi...
        now = datetime.datetime.now()
        # my JANDI topic
        # jandi_url = "https://wh.jandi.com/connect-api/webhook/13352731/2d4cd8c41be1cae1304676758f0c02eb"
        # temp
        jandi_url = 'https://wh.jandi.com/connect-api/webhook/13352731/b91cba7b76ad663145a8c438b01725fb'
        jandi_url_Innoi = 'https://wh.jandi.com/connect-api/webhook/19452800/a38a9a9d1f43d2095897b4d5b434722e'
        # jandi_url_HK = 'https://wh.jandi.com/connect-api/webhook/19452800/700b9a7a762798533897af8e05770518'

        jandi_header = {
            "Accept": "application/vnd.tosslab.jandi-v2+json",
            "Content-Type": "application/json"
        }

        jandi_payload = {
            "body": '실행시간 : ' + str(now),
            "connectColor": "#FFA999",
            "connectInfo": [{
                "title": str('상용환경 API Check [UNIT TEST]'),
                "description": '※' + ' ' + SKTJandi + '\n\n'
                # "description": '※' + ' ' + SKTJandi + '\n\n' + '※' + ' ' + KTJandi + '\n\n' + '※' + ' ' + LGJandi + '\n'
            }
            ]
        }

        # post to jandi
        res = requests.post(url=jandi_url, data=json.dumps(jandi_payload), headers=jandi_header)
        res_Innoi = requests.post(url=jandi_url_Innoi, data=json.dumps(jandi_payload), headers=jandi_header)
        # res_HK = requests.post(url=jandi_url_HK, data=json.dumps(jandi_payload), headers=jandi_header)

        print res
        print res_Innoi
        # print res_HK

    except Exception as e:
        print e
        print "except"
        driver.quit()

    finally:
        print "finally..."
        driver.quit()

except Exception as e:
    print e
    print "except"
    driver.quit()

finally:
    print "finally..."
    driver.quit()