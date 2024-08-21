import browser
import time, json
from colorama import Style, Fore, Back
from model import *



def enter_text_into_element(text_to_find, text_to_enter, press_enter = True):
    click_element_with_text(text_to_find)
    browser.enter_text(text_to_find, text_to_enter, press_enter)


def enter_text_into_element_function(args_str):
    args = json.loads(args_str)
    print(f"DEPRECATED enter_text_into_elements({args})")
  #  args['text_to_find'], args['input_text'], args['press_enter']
    to_find = args['text_to_find']
    to_input = args['input_text']
    enter = args['press_enter']
    return browser.search_thing(to_find, to_input, enter)


#needs to use OCR and element 

def click_element_with_text_dom(text_to_click):
    print(f"click_element_with_text_dom({text_to_click})")
    return browser.click_text(text_to_click)




def click_element_with_text(text_to_click):
    result = click_element_with_text_dom(text_to_click)
    browser.holdup() 
    return result

def click_element_with_text_function(args_str, call_id):
    args = json.loads(args_str)
    print(f"click_element_with_text({args})")
    found = click_element_with_text(args['text_to_click'])
    status = "tried to click text, could not find a match to click"
    if len(found):
        status = "found a match and tried to click text, if the url didn't change or the image content did not update, then try another keyword, that text might not be clickable"

    result = { 'status' : status, "url" : browser.url() } 
    ret = create_function_result(result, call_id)
    return ret