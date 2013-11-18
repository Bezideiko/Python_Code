#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing the ticket fares with different routes - Data driven test
"""

import unittest
import HTMLTestRunner
import time
import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException


class FireFoxHappyPathTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://core.bdz.transportinfo.bg/core/login"
        self.maxDiff = None
        self.accept_next_alert = True

        self.input_file_name = "2013-11-18-AllTests.csv"
        self.verificationErrors = []

        self.logIn("admin", "adminadmin")


    def tearDown(self):
        self.logOut()

        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


    def test_happy_path(self):
        line_number = 0
        input_data = csv.reader(open(self.input_file_name, "r"))
        self.row_number = 0
        for case in input_data:
            self.row_number += 1
            test_data = self.parse_csv_row(case, self.row_number)
            if test_data is None:
                continue
            line_number += 1

            try:
                driver = self.driver
                driver.find_element_by_xpath(u"//*[@id='id_from_station']/option[@value={station_from_name}]".format(**test_data)).click()
                driver.find_element_by_xpath(u"//*[@id='id_to_station']/option[@value={station_to_name}]".format(**test_data)).click()
                driver.find_element_by_id("id_date_f").clear()
                driver.find_element_by_id("id_date_f").send_keys("{date_go}".format(**test_data))
                driver.find_element_by_id("id_date_f").click()
                driver.find_element_by_id("id_date_r").clear()
                driver.find_element_by_id("id_date_r").click()
                driver.find_element_by_id("id_date_r").click()  #to remove the Calendar Widget
                driver.find_element_by_id("id_date_r").send_keys("{date_back}".format(**test_data))
                driver.implicitly_wait(2)
                driver.find_element_by_xpath(u"/html/body/div[3]/div[2]/div/div[4]/div[1]/div/div[2]/form/fieldset/input").click()
                #try:
                #    self.assertEqual(u"Билет 1 - " + best_price + u"\nлв", driver.find_element_by_css_selector("span.label.label-success").text)
                #except AssertionError as e:
                #    self.verificationErrors.append(unicode(e))
                driver.find_element_by_xpath("//*[@id='id_go-trip']/option[contains(text(), {train_go_id})]".format(**test_data)).click()
                driver.find_element_by_id("{class_go}".format(**test_data)).click()

                if "{addition_go}".format(**test_data) != "":
                    driver.find_element_by_id("{addition_go}".format(**test_data)).click()

                driver.find_element_by_xpath("//*[@id='id_ret-trip']/option[contains(text(), {train_back_id})]".format(**test_data)).click()
                driver.find_element_by_id("{class_back}".format(**test_data)).click()
                if "{addition_back}".format(**test_data) != "":
                    driver.find_element_by_id("{addition_back}".format(**test_data)).click()
                driver.find_element_by_xpath(u"//input[@value='Изчисли']").click()
            except NoSuchElementException:
                print ("No such element at case row: " + str(self.row_number))
            try:
                actual = driver.find_element_by_id("ticket-best-price").text
                expected = "{base_price}".format(**test_data)
                self.assertEqual(expected, actual)
            except AssertionError:
                print("Assertion error exception at case row: " + str(self.row_number))
                print "Expected result: " + expected
                print "Actual result: " + actual
                print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

            driver.implicitly_wait(2)
            driver.find_element_by_link_text(u"Тарифа - тест").click()
            #driver.find_element_by_xpath("/html/body/div[2]/div/div/ul/li[2]/a").click()


    def validate_data(self, data):
        unwanted_chars = set("/,'""")
        if any((char in unwanted_chars) for char in data):
            raise Exception("Invalid data at: " + self.row_number)

        data = data.strip()
        return data
        #if data or not is_required:
        #    return True
        #else:
        #    return False


    def parse_csv_row(self, row_number, case_number):
        """
        returns dictionary
        """
        result = {}
        try:
            result["station_from_name"] = self.validate_data(row_number[0])
            result["station_to_name"] = self.validate_data(row_number[1])
            result["date_go"] = self.validate_data(row_number[2])
            result["date_back"] = self.validate_data(row_number[3])
            result["discount"] = self.validate_data(row_number[4])
            result["train_go_id"] = self.validate_data(row_number[5])
            result["class_go"] = self.validate_data(row_number[6])
            result["addition_go"] = self.validate_data(row_number[7])
            result["train_back_id"] = self.validate_data(row_number[8])
            result["class_back"] = self.validate_data(row_number[9])
            result["addition_back"] = self.validate_data(row_number[10])
            result["base_price"] = self.validate_data(row_number[11])
            result["fare"] = self.validate_data(row_number[12])
            result["best_price"] = self.validate_data(row_number[13])

            return result
        except IndexError:
            print("Row [{row}]: Not enough columns - skipping test !!".format(row=case_number))
            print("Index error exception")
            return None
        except ValueError:
            print("Row [{row}]: Wrong row - skipping test !!".format(row=case_number))
            print("Value error exception")
            return None


    def logIn(self, username, password):
        self.driver.get(self.base_url + "/")
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_password").clear()
        self.driver.find_element_by_id("id_password").send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.driver.find_element_by_xpath("//li[2]/a/span").click()

        try:
            self.assertEqual(u"admin", self.driver.find_element_by_xpath("/html/body/div/div/div[2]/ul/li/a/span").text)
        except AssertionError as e:
            print "Wrong login."
            self.verificationErrors.append(unicode(e))


    def logOut(self):
        self.driver.find_element_by_css_selector("i.clip-chevron-down").click()
        self.driver.find_element_by_xpath("//html/body/div/div/div[2]/ul/li/ul/li/a").click()

        try:
            self.assertEqual(u"Вход в системата", self.driver.find_element_by_xpath("/html/body/div[2]/div/div/h3").text)
        except AssertionError as e:
            print "Wrong logout."
            self.verificationErrors.append(unicode(e))


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True


    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True


    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True


suite = unittest.TestSuite()
suite.addTest(FireFoxHappyPathTest('test_happy_path'))
file_location ="C:\Users\Angel\Desktop\PythonVirtualEnvironment\Selenium Tests\Code\\"
file_name = "Report.html"
outfile = open(file_location + file_name, "w")
runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title="Ticket Fares Test Report!", description="Testing the ticket fares with different routes - Data driven test")
runner.run(suite)


