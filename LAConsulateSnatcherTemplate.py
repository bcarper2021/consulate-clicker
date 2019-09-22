from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
from twilio.rest import Client
import codecs


def checkDate(apptDateStr):
    possibleDates = [
        "2019-06-04", "2019-06-05", "2019-06-06", "2019-06-07", "2019-06-08", "2019-06-09",
        "2019-06-10", 
        # "2019-06-11", "2019-06-12", "2019-06-13", "2019-06-14", "2019-06-15",
        # "2019-06-16", 
        "2019-06-17", "2019-06-18", "2019-06-19", "2019-06-20", "2019-06-21",
        "2019-06-22", "2019-06-23", "2019-06-24", "2019-06-25", "2019-06-26", "2019-06-27",
        "2019-06-28", "2019-06-29", "2019-06-30", 
        # "2019-07-01", "2019-07-02", "2019-07-03",
        # "2019-07-04", "2019-07-05", "2019-07-06", "2019-07-07", "2019-07-08", "2019-07-09",
        # "2019-07-10", "2019-07-11", "2019-07-12", "2019-07-13", "2019-07-14", "2019-07-15",
        # "2019-07-16", "2019-07-17", "2019-07-18", "2019-07-19", "2019-07-20", "2019-07-21",
        # "2019-07-22", "2019-07-23", "2019-07-24", "2019-07-25", "2019-07-26", "2019-07-27",
        ]
    return (apptDateStr in possibleDates)


# Constants
base_url = "https://app.bookitit.com/en/hosteds/widgetdefault/275f65e80ce06aaf5cd24cebd11311897#services"
driver_path = "C:\\Users\\<<<user>>>\\Desktop\\ChromeDriver\\chromedriver"
delay = 20
client = Client("<<<TWILIO USERNAME>>>", "<<<TWILIO KEY>>>")
file_name = "<<<OUTPUT HTML DOCUMENT>>>"
save_path = "C:\\Users\\<<<user>>>\\Desktop\\selenium\\"
intermission = 2
NAME = "<<<NAME OF PERSON BOOKING APPOINTMENT>>>"
EMAIL = "<<<EMAIL OF PERSON BOOKING APPOINTMENT>>>"
PHONE = "<<<PHONE NUMBER OF PERSON BOOKING APPOINTMENT>>>"


testBool = True
testNum = 0

while testBool:

    start = time.time()

    # Open Webpage
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(base_url)

    # Redirect to necessary webpage
    try:
        student_visa_link = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idListServices\"]/div[23]/div[1]/a")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        driver.close()
        testNum += 1
        print(testNum)
        end = time.time()
        print(end - start)
        #time.sleep(intermission)
        continue

    student_visa_link.click()

    #time.sleep(3)

    # This is the XPATH to the first available timeslot to be clicked on "//*[@id=\"idDivSlotColumnContainer-1\"]/a[1]"
    # This is the form for name "//*[@id=\"idIptBktname\"]"           ----------        <input id="idIptBktname" type="text" name="name" placeholder="* Name" value="">
    # This is the form for email "//*[@id=\"idIptBktemail\"]"         ----------        <input id="idIptBktemail" type="text" name="email" placeholder="* Email" value="">
    # This is the form for phone "//*[@id=\"idIptBktcellphone\"]"     ----------        <input id="idIptBktcellphone" type="tel" name="cellphone" placeholder="* Telephone" value="">
    # This is the checkbox saying I agree "//*[@id=\"idIptBktAcceptCondtions\"]"        <input id="idIptBktAcceptCondtions" type="checkbox" name="accept_conditions" value="1">       ---------- <label for="idIptBktAcceptCondtions"></label>

    # Below is the checkout button
    #   <div id="idBktDefaultSignUpConfirmButtonContainer">
    #       <div id="idBktDefaultSignUpConfirmButton" class="clsDivContinueButton clsHPR">Confirm</div>
    #       <div class="clsCB"></div>
    #   </div>

    # @2Elizabeth
    # //*[@id=\"idDivBktDatetimeSelectedDate\"]

    # Try to find if there are slots available
    try:
        origTest = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"idTimeListTable\"]")))
        check12 = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idDivSlotColumnContainer-1\"]/a[1]")))

        # POSSIBLE SLOT FOUND
        parseString = check12.get_attribute('href')
        apptDate = parseString[-26:-16]
        #client.messages.create(to="<<<USER PHONE NUMBER>>>", from_="<<<TWILIO PHONE NUMBER>>>", body=apptDate)
        apptMonth = apptDate[6]
        if checkDate(apptDate):
            apptTime = parseString[-15:-10]
            textBody = "POSSIBLE SLOT BOOKED: " + apptDate + " " + apptTime
            # should only work if check12 is returned a value
            print("Possible Slot Available")
            check12.click()
            name = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idIptBktname\"]")))
            email = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idIptBktemail\"]")))
            phone = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idIptBktcellphone\"]")))
            checkbox = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idBktDefaultSignUpAcceptInput\"]/label")))
            confirmButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"idBktDefaultSignUpConfirmButton\"]")))
            
            name.send_keys(NAME)
            email.send_keys(EMAIL)
            phone.send_keys(PHONE)
            checkbox.click()
            confirmButton.click()

            # Copy HTML of page
            driver.page_source
            completeName = os.path.join(save_path, file_name)
            file_object = codecs.open(completeName, "w", "utf-8")
            html = driver.page_source
            file_object.write(html)
            file_object.write("\n\n\n")
            testBool = False
            client.messages.create(to="<<<USER PHONE NUMBER>>>", from_="<<<TWILIO PHONE NUMBER>>>", body=textBody)
            continue
    except TimeoutException:
        print("No Slots Found")


    driver.close()
    #testBool = False
    testNum += 1
    print(testNum)
    end = time.time()
    print(end - start)
    #time.sleep(intermission)



