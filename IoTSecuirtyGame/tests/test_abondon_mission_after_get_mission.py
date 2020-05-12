#Written by: Layla Pezeshkmehr
#07/02/2019

import time
import random
import ipaddress
import unittest
from selenium import webdriver
import student_actions as sactions
import instructor_actions as iactions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from student_actions import AccessStudentElements
from selenium.webdriver.support.select import Select
from instructor_actions import AccessInstructorElements


class TestAbondonMission(unittest.TestCase):

    def setUp(self):

        self.num_of_teams = 1
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
        if num_teams > 1:
            for i in range(num_teams):
                self.instructor.plus_auto_sign().click()
                time.sleep(3)

        self.instructor.start_button().click()
        time.sleep(2)
        self.instructor.close_start_modal()
        time.sleep(2)

        for i in range(self.num_browsers):
            self.student_browsers[i].student_end_tour()
            time.sleep(3)

    def test_abondon_mission_at_beginning(self):

        self.student_browsers[0].student_get_mission()
        time.sleep(2)
        self.assertEqual(self.student_browsers[0].players_in_mission(), self.student_name[0],
                         "names are different")
        time.sleep(2)
        self.student_browsers[1].student_do_mission()
        players_names = self.student_browsers[0].players_in_mission()
        p_names = players_names.replace(' ', '')
        players_list = p_names.split(',')
        self.assertEqual(players_list, [self.student_name[0], self.student_name[1]],
                         "Names dont match")
        time.sleep(2)
        self.student_browsers[0].student_abondon_mission().click()
        self.assertEqual(self.student_browsers[1].players_in_mission(), self.student_name[1],
                         "Names dont match")
        time.sleep(2)
        self.instructor.end_game_reset()

    def tearDown(self):
        self.instructor.quit()
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)