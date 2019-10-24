#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
driver=webdriver.Chrome('./chromedriver')
driver.get("https://tinder.com/?lang=en")


# In[2]:


window_before = driver.window_handles[0]
driver.find_element_by_xpath("""//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button""").click()


# In[3]:


window_after = driver.window_handles[1]

driver.switch_to_window(window_after)


# In[4]:


email="kitusarthak@gmail.com"
pas="sarthak2001"

driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(email)
driver.find_element_by_xpath("""//*[@id="pass"]""").send_keys(pas)

driver.close()
# In[5]:


driver.find_element_by_xpath("""//*[@id="u_0_0"]""").submit()


# In[4]:


driver.close()

