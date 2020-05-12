# Written by Layla Pezeshkmehr,
# 6/23/2018
from selenium import webdriver
import unittest
import time
import instructor_actions as iactions
import student_actions as sactions
from selenium.webdriver.common.keys import Keys
from instructor_actions import AccessInstructorElements
from student_actions import AccessStudentElements
import ipaddress


class TestAutoTeamSetup(unittest.TestCase):
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

    def test_auto_with_two_teams(self):

        num_teams = self.num_of_teams - 1
        for i in range(num_teams):
            self.instructor.plus_auto_sign().click()
            time.sleep(3)
        self.assertEqual(self.instructor.auto_team_count_field().get_attribute("value"),
                         str(str(self.num_of_teams)))
        self.assertEqual(self.instructor.student_one_in_team_one_name().text, self.student_name[0],
                         "Brooks is not assigned ")
        self.assertEqual(self.instructor.student_two_in_team_one_name().text, self.student_name[1],
                         "Colt is not assigned")
        self.assertEqual(self.instructor.student_one_in_team_two_name().text, self.student_name[2],
                         "Robert is not assigned")
        self.assertEqual(self.instructor.student_two_in_team_two_name().text, self.student_name[3],
                         "Layla is not assigned")

    def tearDown(self):

        self.instructor.quit()
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()

    def test_auto_with_one_team(self):
        team_num = 1
        time.sleep(3)
        self.assertEqual(self.instructor.auto_team_count_field().get_attribute("value"), str(str(team_num)))
        self.assertEqual(self.instructor.student_one_in_team_one_name().text, self.student_name[0],
                         "Brooks is not assigned ")
        self.assertEqual(self.instructor.student_two_in_team_one_name().text, self.student_name[1],
                         "Colt is not assigned")
        self.assertEqual(self.instructor.student_three_in_team_one_name().text, self.student_name[2],
                         "Robert is not assigned")
        self.assertEqual(self.instructor.student_four_in_team_one_name().text, self.student_name[3],
                         "Layla is not assigned")
    
    def test_auto_with_three_teams(self):
        team_num = 3
        total_click = team_num - 1
        for i in range(total_click):
            self.instructor.plus_auto_sign().click()
        self.assertEqual(self.instructor.auto_team_count_field().get_attribute("value"), str(str(team_num)))
        print("self.num_of_team is: %d" % team_num)

        self.assertEqual(self.instructor.student_one_in_team_one_name().text, self.student_name[0],
                         "Brooks is not assigned ")
        self.assertEqual(self.instructor.student_one_in_team_two_name().text, self.student_name[1],
                         "Colt is not assigned")
        self.assertEqual(self.instructor.student_one_in_team_three_name().text, self.student_name[2],
                         "Robert is not assigned")
        self.assertEqual(self.instructor.student_two_in_team_three_name().text, self.student_name[3],
                         "Layla is not assigned")

    def test_auto_with_four_teams(self):
        team_num = 4
        total_click = team_num - 1
        for i in range(total_click):
            self.instructor.plus_auto_sign().click()
        self.assertEqual(self.instructor.auto_team_count_field().get_attribute("value"), str(str(team_num)))
        self.assertEqual(self.instructor.student_one_in_team_one_name().text, self.student_name[0],
                         "Brooks is not assigned ")
        self.assertEqual(self.instructor.student_one_in_team_two_name().text, self.student_name[1],
                         "Colt is not assigned ")
        self.assertEqual(self.instructor.student_one_in_team_three_name().text, self.student_name[2],
                         "Robert is not assigned ")
        self.assertEquals(self.instructor.student_one_in_team_four_name().text, self.student_name[3],
                         "Layla is not assigned")


if __name__ == '__main__':
    unittest.main(verbosity=3)