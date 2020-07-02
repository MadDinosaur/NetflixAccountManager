from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    login_url = 'https://www.netflix.com/pt/login'

    browser.get(login_url)

    # write login e-mail and password
    browser.find_element_by_id('id_userLoginId').send_keys(username)
    browser.find_element_by_id('id_password').send_keys(password)

    # wait for page to load
    sleep(2)

    # temp solution. gotta figure out how to get token
    browser.get('https://www.netflix.com/SwitchProfile?tkn=AISPVS7TLBG23NT4PIRPEKYYDM')

    print('Login successful!')


def mylist():
    browser.find_elements_by_class_name('navigation-tab')[-1].click()

    # wait for page to load
    sleep(5)

    try:
        mylist = browser.find_elements_by_class_name('title-card-container')
        for item in mylist:
            show = item.find_element_by_class_name('ptrack-content')
            name = show.text
            print(name)
            # episode = show.find_elements_by_class_name('episodeTitle').text
            # print(episode)
        # TODO: build list with shows on "My List" and last episode watched
    except NoSuchElementException:
        print('My List is empty.')


def register():
    tempmail_url = 'https://tempail.com/pt/'
    register_url = 'https://www.netflix.com/pt/'

    # get temp e-mail
    browser.get(tempmail_url)

    # wait for page to load
    sleep(2)

    global username
    username = browser.find_element_by_id('eposta_adres').get_attribute('value')

    # ask for credit card number information
    print('Insert card number')
    card_number = input()
    print('Insert CVC')
    cvc = input()
    print('Insert expiration date MMAA')
    date = input()
    print('Name on card')
    name = input()

    # create account
    browser.get(register_url)

    # wait for page to load
    sleep(2)

    browser.find_element_by_id('id_email').send_keys(username + '\n')

    # go through the menus
    for page in range(3):
        # wait for page to load
        sleep(2)
        # click on button
        browser.find_element_by_class_name('submitBtnContainer').click()

    # wait for page to load
    sleep(2)

    browser.find_element_by_id('id_password').send_keys(password)

    # wait for page to load
    sleep(2)

    browser.find_element_by_id('creditOrDebitCardDisplayStringId').click()

    # wait for page to load
    sleep(2)

    browser.find_element_by_id('id_firstName').send_keys(name.split(' ')[0])
    browser.find_element_by_id('id_lastName').send_keys(name.split(' ')[-1])
    browser.find_element_by_id('id_creditCardNumber').send_keys(card_number)
    browser.find_element_by_id('id_creditExpirationMonth').send_keys(date)
    browser.find_element_by_id('id_creditCardSecurityCode').send_keys(cvc)
    # click on button
    browser.find_element_by_class_name('submitBtnContainer').click()

    # check if it asks for phone number
    try:
        phone_input = EC.presence_of_element_located(By.ID, 'id_phoneNumber')

        print('Insert phone number')
        phone_input.send_keys(input())
        sleep(2)

        print('Insert code sent by SMS')
        browser.find_element_by_id('').send_keys(input())
    except NoSuchElementException:
        pass

    __update_login()
    __deactivate_account()


def __update_login():
    print('Your new login e-mail is: ' + username)
    # save new login to file
    file = open('login_info.txt', 'w')
    file.write(username)
    file.close()


def __deactivate_account():
    browser.get('https://www.netflix.com/CancelPlan')
    sleep(2)
    browser.find_element_by_class_name('cancelContainer').find_element_by_class_name('btn.btn-blue.btn-small').click()


def menu():
    print('Welcome to Netflix Manager. Please choose an option:\n'
          '1. Login\n'
          '2. My List\n'
          '3. Register new account\n'
          '4. Cancel account\n'
          '5. Exit')
    option = input()
    if option == '1':
        login()
        menu()
    elif option == '2':
        mylist()
        menu()
    elif option == '3':
        register()
        menu()
    elif option == '4':
        __deactivate_account()
        menu()
    else:
        browser.close()


###### Variable Declaration ######
browser = webdriver.Chrome()
# browser.minimize_window()

username = open('login_info.txt', 'r').readlines()[-1]
password = '1234567890\n'
############## Menu ##############
menu()
