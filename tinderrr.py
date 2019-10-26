from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def data_extractor(driver):
    soup=BeautifulSoup(driver.page_source,'lxml')
    name = soup.find(class_='Fz($xl) Fw($bold) Flxs($flx1) Flw(w) Pend(8px)').getText()
    print('Name : {}'.format(name))
    age = soup.find(class_='Whs(nw) Fz($l)').getText()
    print(age)
    rows = soup.find_all(class_='Row')
    print(len(rows))
    print('---')
    for r in rows:
        if 'M11.87 5.026L2.186 9' in r.find('path')['d']:
            # print('edu')
            print(r.getText())
        elif 'M7.15 3.434h5.7V1.45' in r.find('path')['d']:
            # print('job')
            print(r.getText())
            
        elif 'M17.507 13.032c1' in r.find('path')['d']:
            # print('gender')
            print(r.getText())
        

        elif r.find(class_='Us(t) Va(m) D(ib) My(2px) NetWidth(100%,20px) C($c-secondary) Ell'):
            # print('lives')
            print(r.getText())
        else:
            # print('distance')
            print(r.getText())

    print('\n\n')


url = "https://tinder.com/?lang=en"
# email="anishasurana6@gmail.com"
# pas="bububitch"
email="Sweetsals35@gmail.com"
pas="Sambitsonali"



#driver initialization
driver=webdriver.Chrome('./chromedriver')
driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get(url)

#fb_redirect
window_before = driver.window_handles[0]
login_fb = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')))
login_fb.click()

#changing window
window_after = driver.window_handles[1]
driver.switch_to_window(window_after)

#login
fb_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="u_0_0"]')))
driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(email)
driver.find_element_by_xpath("""//*[@id="pass"]""").send_keys(pas)
time.sleep(1)
fb_submit.submit()
driver.switch_to_window(window_before)

time.sleep(1)
#pop-up                                                          ################do something about gold pack

location = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div/div/div[3]/button[1]/span""")
location.click()
time.sleep(1)

notification = driver.find_element_by_xpath("""//*[@id="content"]/div/div[2]/div/div/div[3]/button[1]/span""")
notification.click()

time.sleep(2)

try:
    driver.find_element_by_xpath("""//*[@id="modal-manager"]/div/div/div[2]/button[2]/span""").click()
except:
    pass
#processing matches
                                                                                                                 ##this stuff depends on size of screen and stuff
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[1]/div/div[1]').click()
i=j=0
count=0
for i in range(1,100):
    try:
        for j in range(1,10):
            if i==1 and j==1:
                continue
            # try:    
            xp="//*[@id='content']/div/div[1]/div/aside/nav/div/div/div/div[2]/div[1]/div[{}]/div[{}]".format(i,j) #xp -> xPATH variable
            print(xp)
            driver.find_element_by_xpath(xp).click()
            count+=1
            time.sleep(3)
            data_extractor(driver)

            # except:
        #     break
    except:
        break 

        #data extractor fucntion
        # data_extractor(driver)

print('Total matches : {}'.format(count))
        