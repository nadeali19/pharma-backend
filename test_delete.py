from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
try:
    driver.get("http://127.0.0.1:5000/marg_pharma.html")
    time.sleep(2)
    # Login
    driver.find_element(By.XPATH, "//button[contains(text(), 'LOGIN')]").click()
    time.sleep(1)
    
    # Go to Medicines
    driver.find_element(By.XPATH, "//li[contains(text(), 'Medicines')]").click()
    time.sleep(1)
    
    # Click Add New Medicine
    driver.find_element(By.XPATH, "//button[contains(text(), '+ Add New Medicine')]").click()
    time.sleep(1)
    
    # Fill out form
    driver.find_element(By.ID, "am-nm").send_keys("Test Med")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Save Custom Medicine')]").click()
    time.sleep(1)
    
    # Handle alert from save
    alert = driver.switch_to.alert
    print("Alert text on save:", alert.text)
    alert.accept()
    time.sleep(1)
    
    # Try to delete the newly added medicine
    # It should be the last one, or search for it
    delete_buttons = driver.find_elements(By.XPATH, "//button[@title='Delete']")
    if len(delete_buttons) > 0:
        latest_del = delete_buttons[-1]
        print("Clicking delete on last item")
        latest_del.click()
        time.sleep(1)
        alert2 = driver.switch_to.alert
        print("Alert text on delete confirm:", alert2.text)
        alert2.accept()
        time.sleep(1)
        try:
            alert3 = driver.switch_to.alert
            print("Alert text on delete success:", alert3.text)
            alert3.accept()
        except:
            print("No success alert for delete!")
            pass
    
    # Get browser console logs
    logs = driver.get_log('browser')
    for log in logs:
        print(log)
except Exception as e:
    print("Exception:", e)
finally:
    driver.quit()
