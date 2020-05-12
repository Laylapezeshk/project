# Written by: Layla Pezeshkmehr
#6/29/2019

from selenium import webdriver
import unittest
import time
import re
import instructor_actions as iactions
import student_actions as sactions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from instructor_actions import AccessInstructorElements
from student_actions import AccessStudentElements
import ipaddress


class TestStartTimer(unittest.TestCase):

    def setUp(self):

        self.num_of_teams = 2
        self.num_of_students_in_each_team = 2
        self.num_browsers = self.num_of_teams * self.num_of_students_in_each_team
        self.student_browsers = []
        self.student_name = ["Brooks", "Colt", "Robert", "Layla", "Paul", "Steven", "David", "John", "Smith",
                        "Brad", "Chris", "Chloe", "Nina", "Roger", "Michael", "Jack", "Sam", "Peter"]

        self.instructor = iactions.AccessInstructorElements(webdriver.Chrome())
        time.sleep(3)
        self.instructor.open_url()

        ip_add = ipaddress.IPv4Address('10.1.101.11')
        for i in range(self.num_browsers):
            student_browser = sactions.AccessStudentElements(webdriver.Chrome())
            link = "http://localhost:8080/student-dashboard.html?ip=%s" % ip_add
            student_browser.open_url(link)
            self.student_browsers.append(student_browser)
            time.sleep(3)

            name = self.student_name[i]
            print(name)
            student_browser.student_login_with_name(name)

            time.sleep(2)
            ip_add += 256
            print(ip_add)

        num_teams = self.num_of_teams - 1
        for i in range(num_teams):
            self.instructor.plus_auto_sign().click()
            time.sleep(3)

    def test_start_timer_modal(self):
        self.instructor.start_button().click()
        time.sleep(2)
        self.assertIn(self.instructor.start_modal_title().text, "Start Game",
                      "Start Game title incorrect")
        self.instructor.start_modal_count_down_timer()
        field_result = self.instructor.start_modal_option_one().text
        self.assertIn("Countdown timer", self.instructor.start_modal_option_one().text,
                      "countdown timer incorrect")
        time.sleep(2)
        self.instructor.start_modal_add_minute().click()
        time.sleep(2)
        self.assertEqual(self.instructor.start_modal_field().get_attribute('value'), '1',
                         'start modal value incorrect')
        self.instructor.start_modal_ok_button().click()
        self.assertIn('Starting in 0h:', self.instructor.starting_text_reminder().text,
                      'countdown timer to start failed')
        time.sleep(60)

        #end the game before running it over for the next time.
        self.instructor.end_game_reset()
        time.sleep(2)

    def tearDown(self):

        self.instructor.quit()
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)