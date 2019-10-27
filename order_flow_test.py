import time
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

login_url = "https://www.3dhubs.com/manufacture/login"
# Please update email and password
email = ""
password = ""

submit_button_selector = "button[type='submit']"

login_page_email_textbox = "email"
login_page_password_textbox = "password"
login_page_login_button = "//button[contains(text(), 'Log in')]"

manufacture_button = "a.h3d-button.h3d-button--l.h3d-button--primary.u-display-block.u-margin-top-1-5"

upload_button_selector = "h4.h3d-step-title__label"
upload_message_assertion = "Select a technology"
upload_file_directory = "/Users/selcuk/PycharmProjects/3DHubs/assets/data/sample3d.SLDPRT"

scroll_down_script = "window.scrollTo(0, document.body.scrollHeight);"


# noinspection PyGlobalUndefined
class TestOrderFlow:
    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = Chrome()
        driver.implicitly_wait(10)
        global wait
        wait = WebDriverWait(driver, 30)
        yield
        driver.close()
        driver.quit()

    def test_order_flow(self, test_setup):
        driver.get(login_url)
        self.test_login()
        self.test_start_manufacture()
        self.test_upload_and_submit_file()
        self.test_confirm_checkout()

    def test_login(self):
        email_state = wait.until(ec.visibility_of_element_located((By.NAME, login_page_email_textbox)))
        email_state.send_keys(email)
        driver.find_element_by_name(login_page_password_textbox).send_keys(password)
        driver.find_element_by_xpath(login_page_login_button).click()

    def test_start_manufacture(self):
        manufacture_button_state = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, manufacture_button)))
        time.sleep(1)
        manufacture_button_state.click()
        upload_message_state = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, upload_button_selector)))
        assert upload_message_assertion == upload_message_state.text

    def test_upload_and_submit_file(self):
        driver.find_element_by_css_selector("input[id='file']").send_keys(upload_file_directory)
        submit_button_state = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector)))
        driver.execute_script(scroll_down_script)
        time.sleep(2)
        submit_button_state.click()

    def test_confirm_checkout(self):
        tax_field_state = wait.until(ec.visibility_of_element_located((By.ID, "tax-number")))
        tax_field_state.click()
        submit_button = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, submit_button_selector)))
        assert "Submit and pay" == submit_button.text

    def test_teardown(self):
        driver.quit()
