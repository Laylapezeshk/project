#Written by: Layla Pezeshkmehr
#7/1/2019

from selenium import webdriver
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import os
import ipaddress


class AccessStudentElements(object):

    def __init__(self, driver):
        self.student = driver
        self.flags = {
            "0": "CTF{JOZEF}",
            "1a": "http://cloud.security.game/iot/newFirmwareFile.bin",
            "1b": "$1$CTFpassw$ScMuoEYGxfUev8XklEpf90",
            "1c": "CTF{compromised}",
            "1d": "devel0per",
            "2a": "CTF{adminadmin}",
            "2b": "CTF{setup}",
            "2c": "CTF{personalData}",
            "3a": "CTFpwned",
            "3b": "CTF{congratulation}",
        }

    def open_url(self, url):
        return self.student.get(url)


    def get_title(self):
        return self.student.title

    def enter_name_textfield(self):

        #name_field = WebDriverWait(self.student, 10). \
            #until(EC.visibility_of_element_located((By.ID, "modal-name-playername")))

        name_field = self.student.find_element_by_id("modal-name-playername")
        return name_field

    def login_ok_button(self):
        return self.student.find_element_by_id("modal-name-submit")

    def student_name_on_nav_bar(self):
        return self.student.find_element_by_id("navbar-playername")

    def waiting_icon(self):
        return self.student.find_element_by_id("waiting-icon")

    def quit(self):
        return self.student.quit()

    def student_login(self):
        time.sleep(2)
        self.enter_name_textfield().send_keys("student1")
        self.login_ok_button().click()

    def student_login_with_name(self, stu_name):
        self.enter_name_textfield().send_keys(stu_name)
        self.login_ok_button().click()

    def student_end_tour(self):
        time.sleep(2)
        self.student.find_element_by_xpath("//button[contains(text(),'End tour')]").click()

    def get_mission_code(self):
        return self.student.find_element_by_id("mission-id").text

    def student_do_mission(self):
        self.student_get_mission()
        # find out the mission #
        mission_code = self.get_mission_code()
        flag = self.flags[mission_code]
        time.sleep(2)
        # Get the right flag from the dictionary and submit
        self.student_submit_flag(flag)

    def student_get_mission(self):
        time.sleep(2)
        # click on the yellow dots, which is mission opening
        self.student.find_elements_by_xpath("//*[@id='gameboardContainer']//*[@fill='#ffff00']")[0].click()
        time.sleep(2)
        accept_xpath = (By.XPATH, "//button[contains(text(),'Accept')]")
        accept_button = WebDriverWait(self.student, 10).until(EC.visibility_of_element_located(accept_xpath))
        accept_button.click()

    def student_submit_flag(self, flag):
        input_xpath = (By.XPATH, "//span[@class='hint']//input[@type='text']")
        input_text_field = WebDriverWait(self.student, 10).until(EC.presence_of_element_located(input_xpath))
        input_text_field.send_keys(flag)
        submit_xpath = (By.XPATH, "//button[contains(text(),'Submit')]")
        submit_button = WebDriverWait(self.student, 10).until(EC.presence_of_element_located(submit_xpath))
        submit_button.click()

    def student_do_quizzes(self):
        # Quizzes:
        time.sleep(2)
        quizzes = self.student.find_elements_by_xpath("//input[@type='checkbox']")
        # pick quizzes randomly
        count_quizzes = len(quizzes)
        picks = 0
        if count_quizzes:
            picks = 2
            if count_quizzes > 4:
                picks = 4
        choices = random.sample(range(0, count_quizzes), picks)
        for i in range(len(choices)):
            quizzes[choices[i]].click()

        time.sleep(5)
        submit_xpath = (By.XPATH, "//button[contains(text(),'Submit')]")
        submit_button = WebDriverWait(self.student, 10).until(EC.element_to_be_clickable(submit_xpath))
        submit_button.click()

    def missions_and_quizzes(self, num_of_missions):
        for i in range(num_of_missions):
            time.sleep(5)
            self.student_do_mission()
            time.sleep(5)
            self.student_do_quizzes()

    def incorrect_flag_warning_dialog(self):
        return self.student.find_element_by_xpath("//div[@id='modal-wrong']//div[@class='modal-content']")

    def incorrect_flag_ok_button(self):
        return self.student.find_element_by_id("modal-wrong-submit")

    def final_score_board(self):
        return self.student.find_element_by_id("endgame-scoreboard")

    def final_score_ok_button(self):
        return self.student.find_element_by_id("modal-endgame-submit")

    def complete_tour_navigation(self):
        before_xpath_tour = '//*[@id="step-'
        after_xpath_tour = '"]/div[3]/div/button[2]]'
        for i in range(6):
            j = str(i)
            print(j)
            print(before_xpath_tour)
            print(after_xpath_tour)
            select_next = self.student.find_element_by_xpath(before_xpath_tour + j + after_xpath_tour)
            select_next.click()
            time.sleep(3)
        # end the tour
        self.student.find_element_by_xpath('//*[@id="step-6"]/div[3]/button').click()

    def game_board_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-0"]/div[3]/div/button[2]')

    def player_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-1"]/div[3]/div/button[2]')

    def chat_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-2"]/div[3]/div/button[2]')

    def mission_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-3"]/div[3]/div/button[2]')

    def notification_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-4"]/div[3]/div/button[2]')

    def scoreboard_panel_next_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-5"]/div[3]/div/button[2]')

    def tool_panel_end_button(self):
        return self.student.find_element_by_xpath('//*[@id="step-6"]/div[3]/button')

    def student_chat_input_field(self, message):
        return self.student.find_element_by_xpath('//*[@id="chat-comment"]').send_keys(message)

    def student_chat_send_key(self):
        return self.student.find_element_by_xpath('//*[@id="chat-send"]/span')

    def student_show_score_board(self):
        return self.student.find_element_by_xpath('//*[@id="scoreboard-table-rows"]/td[3]/span/i')

    def student_show_magnify_glass_score_board(self):
        return self.student.find_element_by_xpath('//*[@id="scoreboard-tooltip-icon-0"]')

    def back_ground_after_end_tour(self):
        return self.student.find_element_by_xpath("/html/body/div[2]/div[1]")

    def student_hover_mag_glass(self):
        time.sleep(8)
        s_element_to_hover_over = self.student.find_element_by_xpath("//*[@id='scoreboard-tooltip-icon-0']")
        time.sleep(8)
        return ActionChains(self.student).move_to_element(s_element_to_hover_over).perform()

    def student_chat_history(self):
        return self.student.find_element_by_xpath("//*[@id='chathistory']")

    def mission_completed_by(self):
        return self.student.find_element_by_xpath("//*[@id='mission-container']/div[3]/span[4]").text

    def mission_contributor(self):
        return self.student.find_element_by_xpath("//*[@id='mission-container'/div[3]/span[3]").text

    def student_abondon_mission(self):
        return self.student.find_element_by_id("abandon-mission")

    def players_in_mission(self):
        return self.student.find_element_by_xpath("//*[@id='mission-container']/span[3]/b").text

    def player_completed_mission(self):
        return self.student.find_element_by_xpath("//*[@id='mission-container']/div[3]/span[4]/b").text