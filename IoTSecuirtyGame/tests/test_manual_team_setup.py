from selenium import webdriver
import unittest
import time
import instructor_actions as iactions
import student_actions as sactions
from selenium.webdriver.common.keys import Keys
from instructor_actions import AccessInstructorElements
from student_actions import AccessStudentElements
import ipaddress

class TestManualTeamSetup(unittest.TestCase):

    def setUp(self):

        self.num_of_teams = 2
        self.num_of_students_in_each_team = 2
        self.num_browsers = self.num_of_teams * self.num_of_students_in_each_team
        self.student_browsers = []
        self.student_name = ["Brooks", "Colt", "Robert", "Layla", "Paul", "Steven", "David", "John", "Smith",
                             "Brad", "Chris", "Chloe", "Nina", "Roger", "Michael", "Jack", "Sam", "Peter"]
        self.team_name = ["Team1", "Team2", "Team3", "Team4", "Team5"]

        self.instructor = iactions.AccessInstructorElements(webdriver.Chrome())
        time.sleep(3)
        self.instructor.open_url()
        ip_add = ipaddress.IPv4Address('10.1.101.11')
        for i in range(self.num_browsers):
            student_browser = sactions.AccessStudentElements(webdriver.Chrome())
            link = "http://localhost:8080/student-dashboard.html?ip=%s" % ip_add
            student_browser.open_url(link)
            self.student_browsers.append(student_browser)
            time.sleep(4)
            name = self.student_name[i]
            student_browser.student_login_with_name(name)
            time.sleep(3)
            ip_add += 256

    def test_manual_team_create(self):

        self.instructor.click_manual_tab()
        time.sleep(3)
        a_button = self.instructor.add_team_button().text
        self.assertIn("Add Team", a_button, "Not in the correct page")
        for i in range(self.num_of_teams):
            self.instructor.add_team_button().click()
            time.sleep(2)
            t_name = self.team_name[i]
            self.instructor.team_name_field().send_keys(t_name)
            time.sleep(2)
            i_team_submit = self.instructor.team_name_submit()
            i_team_submit.click()
            time.sleep(2)
            #team = self.instructor.team_name(i)
            #print(team)
            print(self.team_name[i])
            #self.assertIn(team.text, self.team_name[i], "team names dont match")

        self.assertEqual(self.instructor.team_name_one().text, self.team_name[0], "Team1 not properly assigned")
        self.assertEqual(self.instructor.team_name_two().text, self.team_name[1], "Team2 not properly assigned")

        self.instructor.team_name_one().click()
        time.sleep(2)
        self.instructor.player_one_in_player_list().click()
        time.sleep(2)
        self.instructor.player_two_in_player_list().click()
        time.sleep(2)
        self.instructor.join_group_button().click()
        time.sleep(2)

        self.instructor.team_name_two().click()
        time.sleep(2)
        self.instructor.player_three_in_player_list().click()
        time.sleep(2)
        self.instructor.player_four_in_player_list().click()
        time.sleep(2)
        self.instructor.join_group_button().click()

        self.instructor.team_name_one().click()
        time.sleep(3)
        self.assertEqual(self.instructor.member_one_team_one().text, self.student_name[0], "Brooks has not been assigned")
        self.assertEqual(self.instructor.member_two_team_one().text, self.student_name[1], "Colt has not been assigned")

        self.instructor.team_name_two().click()
        time.sleep(3)
        self.assertEqual(self.instructor.member_one_team_two().text, self.student_name[2], "Robert has not been assigned")
        self.assertEqual(self.instructor.member_two_team_two().text, self.student_name[3], "Layla has not been assigned")

    def tearDown(self):
        self.instructor.quit()
        print("Done")
        for i in range(self.num_browsers):
            self.student_browsers[i].quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)


