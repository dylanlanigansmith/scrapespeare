import sys, time, json


from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains

from PIL import Image
from io import BytesIO
from configfile import *
from log import *

import browser
import actions









def main(target_url, user_prompt):
    runtime = Profiler("Execution")
    print(browser.driver.get_window_size())
    browser.get(target_url)
    actions.click_element_with_text("OREO")
    image = browser.screenshot_full()

    image.show()
    image.save("ocr.png", format="PNG")
    time.sleep(4)
    
    runtime.end()
    
    browser.driver.close()
    return 0

if __name__ == "__main__": 
    assert(config.ok())
    err = 1
    if len(sys.argv) != 3:
        if len(sys.argv) == 1 and len(config["default_target"]) and len(config["default_query"]):
            print("using test values from config")
            err = main(config["default_target"], config["default_query"])
        else:  
            print("no test values in config!")
            print("Usage: python <prog> <url> \"<search_text>\"")
    else: 
        url = sys.argv[1]
        search_text = sys.argv[2]       
        err = main(url, search_text)
    sys.exit(err)
   