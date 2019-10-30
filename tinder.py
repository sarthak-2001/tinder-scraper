from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re
import sys
import csv
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%Y-%m-%d-%H:%M:%S")
current_time=str(current_time)
# FILENAME = current_time+'-tinder.csv'
f=input('enter file name : ')
FILENAME=f+'.csv'
# print(FILENAME)
index=1

email=input('enter email/number associated with FB : ')

pas=input('enter password : ')

csv_file=open(FILENAME, 'w',encoding="utf-8")
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(['index', 'name', 'age', 'bio', 'education','job','gender','residence','distance','number_messages','number_photos'])
link_file = f+'-link.txt'
link_writer = open(link_file,'w',encoding='utf=8')


def link_extractor(driver):
    xp1='//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/a/div'
    wait.until(EC.presence_of_element_located((By.XPATH,xp1)))
    
    view1 = driver.find_element_by_xpath(xp1)
    view1.location_once_scrolled_into_view
    time.sleep(0.2)
    soup1=BeautifulSoup(driver.page_source)
    time.sleep(0.5)
    p1_len=p2_len=total_pic=0
    p1=soup1.find_all(class_="bullet D(ib) Va(m) Cnt($blank)::a D(b)::a bullet--active H(4px)::a W(100%)::a Py(6px) Px(2px) W(100%) Bdrs(100px)::a Bgc(#fff)::a")
    p1_len=len(p1)
    # print(p1_len)
    p2=soup1.find_all(class_="bullet D(ib) Va(m) Cnt($blank)::a D(b)::a H(4px)::a W(100%)::a Py(6px) Px(2px) W(100%) Bdrs(100px)::a Bgc($c-bg-black)::a Op(.2)")
    p2_len=len(p2)
    # print(p2_len)
    total_pic=p1_len+p2_len
    if total_pic==0:
        total_pic=1
    # print(total_pic)
    links=[]
    p=1
    for _ in range(total_pic):
        try:
            xp1 = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/a/div/div[2]/div[{}]'.format(p)
            # print(xp1)
            driver.find_element_by_xpath(xp1).click()
        except:
            pass
        
        time.sleep(1)
        soup2=BeautifulSoup(driver.page_source)
        prime_class=soup2.find('div',class_='react-swipeable-view-container')

        not_links=prime_class.find_all_next('div',class_="profileCard__slider__img Z(-1)")
        
        for n in not_links:
            n=str(n)
            link=n.split('\"')[3]
            links.append(link)
        p+=1
    links=set(links)
    total_num_pics = len(links)
    # print(links,total_num_pics)
    return [total_num_pics,links]


def data_extractor(driver):
    xp1='//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/a/div'
    wait.until(EC.presence_of_element_located((By.XPATH,xp1)))
    name=age=bio=edu=job=gender=lives=distance=""
    soup=BeautifulSoup(driver.page_source)
    try:
        name = soup.find(class_='Fz($xl) Fw($bold) Flxs($flx1) Flw(w) Pend(8px)').getText()
    except:
        name=""
    try:
        age = soup.find(class_='Whs(nw) Fz($l)').getText()
    except:
        age =""

    try:
        bio=soup.find(class_='P(16px) profileCard__bio Ta(start) Us(t) C($c-secondary) BreakWord Whs(pl) Fz($ms)').getText()

    except:
        bio=""
        
    num_msg=len(soup.find_all('div', {"class": re.compile('msgWrp')}))


    rows = soup.find_all(class_='Row')
    # print(len(rows))
    row_len = len(rows)
    # print('---')
    if row_len!=0:
        for r in rows:
            if 'M11.87 5.026L2.186 9' in r.find('path')['d']:
                edu = r.getText()
            elif 'M7.15 3.434h5.7V1.45' in r.find('path')['d']:
                job = r.getText()
            elif 'M17.507 13.032c1' in r.find('path')['d']:
                gender = r.getText()
            elif r.find(class_='Us(t) Va(m) D(ib) My(2px) NetWidth(100%,20px) C($c-secondary) Ell'):
                lives = r.getText()
            else:
                distance = r.getText()

    # print("name : {}\n,age : {}\n,bio : {}\nedu:{}\n,job : {}\n,gender : {}\n,lives : {}\n,distance : {}\nmsg: {}\n".format(name,age,bio,edu,job,gender,lives,distance,num_msg))
    # name=age=bio=edu=job=gender=lives=distance=""
    all_link=link_extractor(driver)
    num_link=all_link[0]
    url=all_link[1]
    link_writer.write(name)
    link_writer.write('\n')
    link_writer.write('---------')
    link_writer.write('\n')
    for r in url:
        # link_writer.writelines(url)
        link_writer.write(r)
        link_writer.write('\n')
    link_writer.write('\n\n')

    # print('\n\n')
    #write data
    global index
    csv_writer.writerow([str(index),name,age,bio,edu,job,gender,lives,distance,str(num_msg),str(num_link)])
    # global index
    index+=1




def  get_matches(driver):
    print('PROCESSING MATCHES....\n')
    soup=BeautifulSoup(driver.page_source)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[1]/div/div[1]')))
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[1]/div/div[1]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[2]/div[1]/div[1]/div[2]')))
    time.sleep(5)
    length=len(soup.find_all(class_="P(8px) Ta(c)"))

    if soup.find(class_='Bgc($c-gold)')==None:
        skip=0
        print('gold not present')
    else:
        skip=1
        print('gold present')

    count=0
    lim=int(length/4)+2
    for i in range(1,lim):    
        for j in range(1,5):        
            if (skip==1):
                if (i==1 and j==1):
                    continue
        
            try:    
                xp="//*[@id='content']/div/div[1]/div/aside/nav/div/div/div/div[2]/div[1]/div[{}]/div[{}]".format(i,j) #xp -> xPATH variable
                # print(xp)
                view = driver.find_element_by_xpath(xp)
                view.location_once_scrolled_into_view
                driver.find_element_by_xpath(xp).click()
                count+=1
                print(count)
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/a/div/div[1]/div/div[1]/div/div')))
                time.sleep(2.5)
                data_extractor(driver)

            except Exception as e:
                print('out of index or someone messaged')
                break

        xp="//*[@id='content']/div/div[1]/div/aside/nav/div/div/div/div[2]/div[1]/div[{}]/div[1]".format(i) #xp -> xPATH variable
        view = driver.find_element_by_xpath(xp)
        view.location_once_scrolled_into_view
    

    print('Total matches : {}'.format(count))
    print('_________________________')

def get_messengers(driver):
    print('PROCESSING MESSAGES....\n')

    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[1]/div/div[2]').click()
    soup=BeautifulSoup(driver.page_source)
    messages_len = len(soup.find_all('a',{"class": re.compile('messageListItem')}))
    for i in range(1,messages_len+1):
        print(i)
        xp='//*[@id="content"]/div/div[1]/div/aside/nav/div/div/div/div[2]/div[2]/div[2]/a[{}]'.format(i)
        view = driver.find_element_by_xpath(xp)
        view.location_once_scrolled_into_view
        driver.find_element_by_xpath(xp).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/a/div/div[1]/div/div[1]/div/div')))
        time.sleep(2)
        data_extractor(driver)
    print('____________________________')

def personal_info(driver):
    print('PROCESSING PERSONAL DATA....\n')

    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/aside/div/a/span').click()
    time.sleep(0.5)
    soup=BeautifulSoup(driver.page_source)
    
    settings = soup.find_all('div',class_='settings__container settings__section Bgc(#fff) BdY Bdc($c-divider)')
    setting=settings[1]

    distance_upper = soup.find('label',class_='menuItem__contents Pos(r) Px(12px) Px(24px)--ml Py(0) M(0)--ml Mih(50px) settings__container_Px(16px) D(f) Jc(c) Fld(c) W(100%) Bgc(#fff) Cur(d) BdB Bdbc($c-divider)')
    distance = distance_upper.find(class_='menuItem__select Fw($regular) C($c-darker-gray)').getText()
    
    looking_for = setting.find(class_='menuItem__select Fw($regular) C($c-darker-gray) menuItem__contents:h_C($c-pink) Trsdu($fast) Pos(r) Trsp($color)').getText()
    age = setting.find_all(class_='menuItem__select Fw($regular) C($c-darker-gray)')[1].getText()
    age_min=age.split('-')[0].strip()
    age_max=age.split('-')[1].strip()
    
    name = soup.find(class_='Fz($xl) Fw($bold) Flxs($flx1) Flw(w) Pend(8px)').getText()
    
    age_personal = soup.find(class_='Whs(nw) Fz($l)').getText()
    
    is_discoverable=False
    if soup.find(class_='Pos(r) Bdrs(15px) W(50px) H(30px) Bd Trstf(eio) Trsdu($fast) Bdc($c-pink) Bg($c-pink)')==None:
        is_discoverable=False
    else:
        is_discoverable=True
    personal_file = f+'-personal.txt'
    with open(personal_file,'w',encoding='utf-8') as w:
        w.write('Name : {}\nAge: {}\nIs_discoverable : {}\nlooking_for : {}\nage_min : {}\nage_max : {}\ndistance : {}\n'.format(name,age_personal,is_discoverable,looking_for,age_min,age_max,distance))

    print(name,age_personal,is_discoverable,looking_for,age_min,age_max,distance)
    print('______________________')


tinder_url = "https://tinder.com/?lang=en"
fb_url = "https://www.facebook.com/"


#driver initialization
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--window-size=1440,900")
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver=webdriver.Chrome('./chromedriver',chrome_options=options)
# driver.maximize_window()
wait = WebDriverWait(driver, 120)


driver.get(fb_url)
print('Logging into FB\n')
try:
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="email"]')))
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(pas)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
except:
    # fb_submit = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="u_0_a"]/div[4]/button')))
    # driver.find_element_by_xpath('//*[@id="u_0_a"]/div[2]/input').send_keys(email)
    # driver.find_element_by_xpath('//*[@id="u_0_a"]/div[3]/input').send_keys(pas)
    # time.sleep(0.5)
    # fb_submit.click()
    sys.exit('check connectivity')

time.sleep(2)
print('FB login successful')



# window_before = driver.window_handles[0]
# login_fb = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')))
# time.sleep(2)
# login_fb.click()
# time.sleep(4)
# window_after = driver.window_handles[1]
# driver.switch_to_window(window_after)
# fb_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="u_0_0"]')))
# driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(email)
# driver.find_element_by_xpath("""//*[@id="pass"]""").send_keys(pas)
# time.sleep(0.5)
# fb_submit.submit()
# driver.switch_to_window(window_before)


driver.get(tinder_url)
login_fb = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')))
login_fb.click()

#popup handling
location = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[3]/button[1]/span')))
location.click()
time.sleep(1)
notification = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[3]/button[1]/span')))
notification.click()

time.sleep(3)
#GOLDPACK
try:
    driver.find_element_by_xpath("""//*[@id="modal-manager"]/div/div/div[2]/button[2]/span""").click()
except:
    pass

# print('matches')
print('_________________________________')
get_matches(driver)

# print('messages')
print('_________________________________')
get_messengers(driver)

# print('personal')
print('_________________________________')
personal_info(driver)

driver.close()