#by Layla Pezeshkmehr
#6/15/2019
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import student_actions
import time
import ipaddress
import unittest
import os


class TestStudentLogin(unittest.TestCase):

    def setUp(self):

        self.student_browsers = []
        self.num_of_teams = 2
        self.num_of_students_in_each_team = 2
        self.num_browsers = self.num_of_teams * self.num_of_students_in_each_team

        ip_add = ipaddress.IPv4Address('10.1.101.11')
        for i in range(self.num_browsers):
            link = "http://localhost:8080/student-dashboard.html?ip=%s" % ip_add
            student_browser = student_actions.AccessStudentElements(webdriver.Chrome())
            student_browser.open_url(link)
            self.student_browsers.append(student_browser)
            self.assertIn('Student Dashboard', student_browser.get_title())
            ip_add += 256
            time.sleep(5)
        time.sleep(5)

    def test_student_login(self):
        time.sleep(2)
        student_name = ["Samual", "Colt", "Robert", "Layla", "Paul", "Steven", "David", "John", "Smith",
                     "Brad", "Chris", "Chloe", "Nina", "Roger", "Michael", "Jack", "Sam", "Peter"]

        for i in range(self.num_browsers):
            student_browser = self.student_browsers[i]
            student_browser.enter_name_textfield().send_keys(student_name[i])
            student_browser.login_ok_button().click()
            time.sleep(5)

            # Check if the navbar show right student name
            self.assertEqual(student_browser.student_name_on_nav_bar().text, student_name[i], "Student Name is not correct")

    def test_submit_with_Enter_key(self):
        time.sleep(2)
        student_name = ["Samual", "Colt", "Robert", "Layla", "Paul", "Steven", "David", "John", "Smith",
                        "Brad", "Chris", "Chloe", "Nina", "Roger", "Michael", "Jack", "Sam", "Peter"]

        for i in range(self.num_browsers):
            student_browser = self.student_browsers[i]
            student_browser.enter_name_textfield().send_keys(student_name[i])
            student_browser.login_ok_button().send_keys(Keys.ENTER)
            time.sleep(5)

            # Check if the navbar show right student name
            self.assertEqual(student_browser.student_name_on_nav_bar().text, student_name[i], "Student Name is not correct")

    def tearDown(self):
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)