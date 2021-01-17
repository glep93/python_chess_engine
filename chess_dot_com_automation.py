from selenium import webdriver
import time

def greeting(name):
  print("Hello, " + name)

def set_driver(bot_name):
    driver = webdriver.Chrome()
    driver.get("https://www.chess.com/play/computer")
    #driver.maximize_window()
    for i in range(10):
        time.sleep(1)
        try:
            driver.execute_script("arguments[0].scrollIntoView();",driver.find_element_by_xpath('//div[@data-bot-name="Beth9-bot"]'))
            break
        except:
            continue
    driver.find_element_by_xpath(f'//div[@data-bot-name="{bot_name}"]').click()
    driver.find_element_by_xpath('//button[@title="Choose"]').click()
    driver.find_element_by_class_name('selection-menu-button').click()
    return driver


def update_position(driver):
    el = driver.find_element_by_id("board-vs-personalities")
    lenght=el.size['height']
    step = int(lenght/8)
    letter = ['a','b','c','d','e','f','g','h']

    pos = {}
    for i in range(1,9):
        pos[str(i)] = int(lenght-step/2) - (i-1)* step

    for i,l in enumerate(letter):
        pos[str(l)] = int(step/2)    + (i)* step
    return pos

def move_from_uci(move, driver ):
    pos = update_position(driver)

    from_ = [ pos[i] for i in move[:2]]
    to_ = [ pos[i] for i in move[2:4]]

    action = webdriver.common.action_chains.ActionChains(driver)
    el = driver.find_element_by_id("board-vs-personalities")
    action.move_to_element_with_offset(el, from_[0], from_[1]  )
    action.click()

    action.move_to_element_with_offset(el, to_[0], to_[1]  )
    action.click()
    action.perform()
    if len(move)==5:
        action.reset_actions()
        action.move_to_element_with_offset(el, to_[0], to_[1]  )
        action.click()
        action.perform()

def board_update(board,driver):
    board.reset()
    for i in range(1,10000):
        try:
            el_move =  driver.find_element_by_xpath(f'//div[@data-ply="{i}"]')
            html_move = el_move.get_attribute('innerHTML')
            if 'data-figurine=' in html_move:
                move = html_move[html_move.find('data-figurine=')+15]
            else:
                move = ''
            move += el_move.text
            #print(move)
            board.push_san(move)
        except:
            break
    return board
