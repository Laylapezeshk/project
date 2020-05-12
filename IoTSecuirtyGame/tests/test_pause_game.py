#Written by: Layla Pezeshkmehr
#6/29/2019

from selenium import webdriver
import unittest
import time
import instructor_actions as iactions
import student_actions as sactions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from instructor_actions import AccessInstructorElements
from student_actions import AccessStudentElements
import ipaddress


class TestPauseGame(unittest.TestCase):

    def setUp(self):

        self.num_of_teams = 2
        self.num_of_students_in_each_team = 2
        self.num_browsers = self.num_of_teams * self.num_of_students_in_each_team
        self.student_browsers = []
        self.student_name = ["Brooks", "Colt", "Robert", "Layla", "Paul", "Steven", "David", "John", "Smith",
                        "Brad", "Chris", "Chloe", "Nina", "Roger", "Michael", "Jack", "Sam", "Peter"]

        #open instructor dashboard
        self.instructor = iactions.AccessInstructorElements(webdriver.Chrome())
        time.sleep(3)
        self.instructor.open_url()

        #opens student dashboard with correct ip address ranging from 10.1.101.11 - 10.1.120.11
        ip_add = ipaddress.IPv4Address('10.1.101.11')
        for i in range(self.num_browsers):
            student_browser = sactions.AccessStudentElements(webdriver.Chrome())
            link = "http://localhost:8080/student-dashboard.html?ip=%s" % ip_add
            student_browser.open_url(link)
            self.student_browsers.append(student_browser)
            time.sleep(3)

            #performs login for each student
            name = self.student_name[i]
            print(name)
            student_browser.student_login_with_name(name)

            time.sleep(2)
            ip_add += 256
            print(ip_add)

        #adjust the team number based on the number of teams
        num_teams = self.num_of_teams - 1
        for i in range(num_teams):
            self.instructor.plus_auto_sign().click()
            time.sleep(3)

        self.instructor.start_button().click()
        time.sleep(3)
        self.instructor.close_start_modal()
        time.sleep(3)

    def test_pause_modal(self):
        self.instructor.pause_modal().click()
        self.assertIn(self.instructor.pause_game_modal().text, "Pause Game", "names don't match")
        time.sleep(5)
        self.instructor.pause_modal_add_minute_button().click()
        self.assertEqual(self.instructor.pause_timer_minute().get_attribute('value'), '1',
                         'values are different')
        time.sleep(5)
        self.instructor.pause_modal_ok_button().click()
        self.assertIn(self.instructor.resume_game_modal().text, 'Resume Game',
                      'title and name are different')
        time.sleep(60)

        self.instructor.end_game_reset()
        time.sleep(2)

    def tearDown(self):

        self.instructor.quit()
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)