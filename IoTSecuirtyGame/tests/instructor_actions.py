#written by Layla Pezeshkmehr

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import os


class AccessInstructorElements(object):

    def __init__(self, driver):
        self.instructor = driver

    def open_url(self):
        return self.instructor.get('http://localhost:8080/instructor-dashboard.html#!/?cheat')

    def search_element_by_id(self, element_id):
        return self.instructor.find_element_by_id(element_id)

    def load_auto_save_dialog(self):
        return self.instructor.find_element_by_id("load_auto_save-modal")

    def load_auto_save_yes(self):
        return self.instructor.find_element_by_id("loadsave-modal-submit")

    def load_auto_save_no(self):
        return self.instructor.find_element_by_id("loadsave-modal-cancel")

    def load_progress_panel(self):
        return self.instructor.find_element_by_id("chart")

    def settings_button(self):
        return self.instructor.find_element_by_id("setting-submit")

    def settings_checkbox(self):
        xpath = (By.XPATH, "//input[@type='checkbox']")
        checkbox = WebDriverWait(self.instructor, 5).until(EC.element_to_be_clickable(xpath))
        return checkbox

    def settings_save(self):
        xpath = (By.XPATH, "//div[@class='modal fade show']//button[@type='button'][contains(text(),'Save')]")
        save_button = WebDriverWait(self.instructor, 5).until(EC.element_to_be_clickable(xpath))
        return save_button

    def settings_cancel(self):
        xpath = (By.XPATH, "//div[@class='modal fade show']//button[@type='button'][contains(text(),'Cancel')]")
        cancel_button = WebDriverWait(self.instructor, 5).until(EC.element_to_be_clickable(xpath))
        return cancel_button

    def start_alert(self):
        WebDriverWait(self.instructor, 3).until(EC.alert_is_present(), "Need Add team before start")
        alert = self.instructor.switch_to.alert
        alert.accept()

    def start_button(self):
        """
        start_button = WebDriverWait(self.instructor, 5).until(EC.element_to_be_clickable((By.ID, "start-submit")))
        return start_button
        """
        return self.instructor.find_element_by_id("start-submit")

    def save_state_button(self):
        return self.instructor.find_element_by_id("file-save")

    def state_file_name_input(self):
        return self.instructor.find_element_by_xpath("//*[@id='file-save-modal']/div/div/div[2]/input")

    def state_file_name_save_button(self):
        return self.instructor.find_element_by_id("file-modal-submit")

    def state_file_name_cancel_button(self):
        return self.instructor.find_element_by_id("file-modal-cancel")

    def get_existed_state_by_id(self, state_id):
        return self.instructor.find_element_by_id(state_id)

    def load_button_in_nav(self):
        return self.instructor.find_element_by_id("file-open")

    def load_button_in_loadgame(self):
        return self.instructor.find_element_by_id("file-open-load")

    def load_game_state_close_button(self):
        return self.instructor.find_element_by_id("file-modal-open-close")

    def get_teams_names_from_scoreboard(self):
        elements = self.instructor.find_elements_by_xpath(
            "//div[@class='ng-scope']//tbody[@id='scoreboard-tbody']//td[@class='scoreboard-teamname ng-binding']")
        return [e.text for e in elements]

    def get_teams_scores_from_scoreboard(self):
        elements = self.instructor.find_elements_by_xpath(
            "//div[@class='ng-scope']//tbody[@id='scoreboard-tbody']//td[@class='scoreboard-teamscore ng-binding']"
        )
        return [float(e.text) for e in elements]

    def get_all_plus_icons_from_scoreboard(self):
        num_of_teams = len(self.get_teams_names_from_scoreboard())
        ids = []
        for i in range(num_of_teams):
            icon_id = "scoreboard-tooltip-icon-" + str(i)
            ids.append(icon_id)
        return [self.instructor.find_element_by_id(x) for x in ids]

    # To call this function, have to know how many students in a team
    def get_students_scores_in_one_team(self, icon_id, num_students):
        score_icon = self.instructor.find_element_by_id(icon_id)
        ActionChains(self.instructor).move_to_element(score_icon).perform()
        detail_data = {}
        for i in range(num_students):
            stu_name = self.instructor.find_element_by_id("scoreboard-tooltip-name-" + str(i)).text
            stu_score = float(self.instructor.find_element_by_id("scoreboard-tooltip-score-" + str(i)).text)
            detail_data[stu_name] = stu_score

    def end_button(self):
        button = WebDriverWait(self.instructor, 5). \
            until(EC.element_to_be_clickable((By.ID, "end-submit")))
        return button

    def end_game_dialog(self):
        return self.instructor.find_element_by_xpath("//div[contains(text(),'Do you want to end the game?')]")

    def end_yes_button(self):
        button = WebDriverWait(self.instructor, 5). \
            until(EC.element_to_be_clickable((By.ID, "end-modal-ok")))
        return button

    def end_cancel_button(self):
        return self.instructor.find_element_by_id("end-modal-cancel")

    def instructor_scoreboard(self):
        return self.instructor.find_element_by_id("scoreboard")

    def reset_button(self):
        button = WebDriverWait(self.instructor, 5). \
            until(EC.element_to_be_clickable((By.ID, "end-modal-reset")))
        return button

    def quit(self):
        return self.instructor.quit()

    def instructor_create_team(self, team_name):
        # Instructor create teams
        self.create_one_team(team_name)
        self.select_students_for_one_team("teams-team-0", ["teams-playername-0"])

    def create_one_team(self, team_name):
        add_team_button_xpath = (By.XPATH, "//*[@id='teams-container']/div/div[1]/button")
        add_button = WebDriverWait(self.instructor, 5).until(EC.element_to_be_clickable(add_team_button_xpath))
        add_button.click()
        time.sleep(3)
        self.instructor.find_element_by_id("team-add-modal-input").send_keys(team_name)
        self.instructor.find_element_by_id("team-add-submit").click()

    def create_auto_teams(self, num_of_teams):
        teams = num_of_teams - 1
        for i in range(teams):
            self.instructor.plus_auto_sign().click()

    def select_students_for_one_team(self, team_id, stu_ids):
        time.sleep(2)
        self.instructor.find_element_by_id(team_id).click()
        time.sleep(2)
        for stu_id in stu_ids:
            self.instructor.find_element_by_id(stu_id).click()
        self.instructor.find_element_by_id("teams-left-button").click()

    def select_students_for_n_teams(self, num_of_teams, num_of_students):
        time.sleep(3)
        for i in range(num_of_teams):
            team_id = "teams-team-" + str(i)
            stu_ids = ["teams-playername-" + str(k) for k in range(num_of_students)]
            self.select_students_for_one_team(team_id, stu_ids)

    def instructor_start_game(self):
        time.sleep(2)
        self.start_button().click()

    def end_game_reset(self):
        end = self.end_button()
        time.sleep(3)
        end.click()
        time.sleep(3)
        self.end_yes_button().click()
        time.sleep(3)
        self.reset_button().click()

    def add_team_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='tab-content-1']/div/div/teams-manual/div/div[1]/div/div/button")

    def team_column_name(self):
        return self.instructor.find_element_by_xpath("//*[@id='tab-content-1']/div/div/teams-manual/div/div[1]/div/div/b/u").text

    def team_name_field(self):
        return self.instructor.find_element_by_id("team-add-modal-input")

    def auto_add_new_team_title(self):
        return self.instructor.find_element_by_xpath("//*[@id='team-add-modal']/div/div/div[1]/h4").text

    def team_name_submit(self):
        return self.instructor.find_element_by_id("team-add-submit")

    def selected_team_name(self):
        return self.instructor.find_element_by_id("teams-team-0")

    def team_name(self, n):
        team_n = "teams-team-%d" % n
        return self.instructor.find_element_by_id(team_n)

    def team_name_one(self):
        return self.instructor.find_element_by_id("teams-team-name-0")

    def team_name_two(self):
        return self.instructor.find_element_by_id("teams-team-name-1")
    def selected_player_name(self):
        return self.instructor.find_element_by_id("teams-playername-0")

    def join_group_button(self):
        return self.instructor.find_element_by_id("teams-left-button")

    def team_right_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='teams-right-button']")

    def edit_delete_team_name(self):
        self.instructor.find_element_by_xpath("//*[@id='teams-team-0']/i").click()
        self.instructor.find_element_by_xpath("//*[@id='team-edit-modal-delete']").click()

    def edit_team_name(self):
        self.instructor.find_element_by_xpath("//*[@id='team-edit-modal-input']").clear()
        return self.instructor.find_element_by_xpath("//*[@id='team-edit-modal-input']")

    def teams_container(self):
        return self.instructor.find_element_by_xpath("//*[@id='teams-container']/div/div[2]/div[2]/div[1]/ul/li")

    def player_back_to_playlist(self):
        return self.instructor.find_element_by_xpath("//*[@id='teams-container']/div/div[2]/div[2]/div[2]/ul/li")

    def team_edit_save_button(self):
        return self.instructor.find_element_by_xpath("// *[ @ id = 'team-edit-modal-submit']")

    def team_edit(self):
        return self.instructor.find_element_by_xpath("//*[@id='teams-team-0']/i")

    def delete_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='team-edit-modal-delete']")

    def chat_input_field(self, message):
        return self.instructor.find_element_by_xpath('//*[@id="chat-input"]').send_keys(message)

    def chat_send_key(self):
        return self.instructor.find_element_by_xpath('//*[@id="chat"]/div[2]/div[2]/div/div[2]/div/button/span')

    def instructor_hover_mag_glass(self):
        time.sleep(8)
        i_element_to_hover_over = self.instructor.find_element_by_xpath('//*[@id="scoreboard-tooltip-icon-0"]')
        time.sleep(8)
        return ActionChains(self.instructor).move_to_element(i_element_to_hover_over).perform()

    def instructor_chat_history(self):
        return self.instructor.find_element_by_xpath("//*[@id='chathistory']")

    def text_received_in_instructor_chat_history(self):
        return self.instructor.find_element_by_xpath('//*[@id="chathistory"]/text()')

    def click_manual_tab(self):
        time.sleep(4)
        manual_tab = WebDriverWait(self.instructor, 5). \
            until(EC.element_to_be_clickable((By.ID, "tab-item-1")))
        time.sleep(4)
        manual_tab.click()

    def auto_team_button(self):
        return self.instructor.find_element_by_xpath(" //*[@id='tab-item-0']")

    def manual_team_button(self):
        return self.instructor.find_element_by_id("tab-item-1")

    def plus_auto_sign(self):
        return self.instructor.find_element_by_xpath("//*[@id='tab-content-0']/div/div/teams-auto/div[1]/div/div/div[2]/button")

    def subtract_auto_sign(self):
        return self.instructor.find_element_by_xpath("//*[@id='tab-content-0']/div/div/teams-auto/div[1]/div/div/div[1]/button")

    def auto_team_count_field(self):

        return self.instructor.find_element_by_id("teamCount")

    def auto_team_one(self):
        return self.instructor.find_element_by_id("teams-auto-teamname-0")

    def student_one_in_team_one_name(self):
        # auto-0 is team 1
        return self.instructor.find_element_by_id("teams-auto-0-player-name-0")

    def student_one_in_team_one_address(self):
        return self.instructor.find_element_by_id("teams-auto-0-player-ip-0")

    def student_two_in_team_one_name(self):
        return self.instructor.find_element_by_id("teams-auto-0-player-name-1")

    def student_two_in_team_one_address(self):
        return self.instructor.find_element_by_id("teams-auto-0-player-ip-1")

    def student_three_in_team_one_name(self):
        return self.instructor.find_element_by_id("teams-auto-0-player-name-2")

    def student_four_in_team_one_name(self):
        return self.instructor.find_element_by_id("teams-auto-0-player-name-3")

    def student_one_in_team_two_name(self):
        #auto-1 is team 2
        return self.instructor.find_element_by_id("teams-auto-1-player-name-0")

    def student_one_in_team_two_address(self):
        return self.instructor.find_element_by_id("teams-auto-1-player-ip-0")

    def student_two_in_team_two_name(self):
        return self.instructor.find_element_by_id("teams-auto-1-player-name-1")

    def student_two_in_team_two_address(self):
        return self.instructor.find_element_by_id("teams-auto-1-player-ip-1")

    def student_one_in_team_three_name(self):
        return self.instructor.find_element_by_id("teams-auto-2-player-name-0")

    def student_two_in_team_three_name(self):
        return self.instructor.find_element_by_id("teams-auto-2-player-name-1")

    def student_one_in_team_four_name(self):
        return self.instructor.find_element_by_id("teams-auto-3-player-name-0")

    def player_one_in_player_list(self):
        return self.instructor.find_element_by_id("teams-playername-0")

    def player_two_in_player_list(self):
        return self.instructor.find_element_by_id("teams-playername-1")

    def player_three_in_player_list(self):
        return self.instructor.find_element_by_id("teams-playername-0")

    def player_four_in_player_list(self):
        return self.instructor.find_element_by_id("teams-playername-1")

    def member_one_team_one(self):
        #return self.instructor.find_element_by_xpath("//*[@id='tab-content-1']/div/div/teams-manual/div/div[2]/div[2]/div[1]/ul/li[1]")
        return self.instructor.find_element_by_id("teams-member-0")

    def member_two_team_one(self):
        #return self.instructor.find_element_by_xpath("//*[@id='tab-content-1']/div/div/teams-manual/div/div[2]/div[2]/div[1]/ul/li[2]")
        return self.instructor.find_element_by_id("teams-member-1")

    def member_one_team_two(self):
        return self.instructor.find_element_by_id("teams-member-2")

    def member_two_team_two(self):
        return self.instructor.find_element_by_id("teams-member-3")

    def start_modal_count_down_timer(self):
        self.instructor.find_element_by_id("start-mode-select").click()
        select = Select(self.instructor.find_element_by_id("start-mode-select"))
        return select.select_by_visible_text('Countdown timer')

    def start_modal_immidiatly(self):
        self.instructor.find_element_by_id("start-mode-select").click()
        select = Select(self.instructor.find_element_by_id("start-mode-select"))
        return select.select_by_visible_text('Immediately')

    def start_modal_add_minute(self):
        return self.instructor.find_element_by_xpath("//*[@id='start-timer']/div[2]/div/div[2]/button/i")

    def start_modal_decrease_minute(self):
        return self.instructor.find_element_by_xpath("//*[@id='start-timer']/div[2]/div/div[1]/button/i")

    def start_modal_add_hour(self):
        return self.instructor.find_element_by_xpath("//*[@id='start-timer']/div[1]/div/div[2]/button/i")

    def start_modal_decrease_hour(self):
        return self.instructor.find_element_by_xpath("//*[@id='start-timer']/div[1]/div/div[1]/button/i")

    def start_modal_ok_button(self):
        return self.instructor.find_element_by_id("start-modal-ok")

    def start_modal_cancel_button(self):
        return self.instructor.find_element_by_id("start-modal-cancel")

    def pause_game_modal_title(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-game-modal']/div/div/div[1]/h4")

    def pause_modal(self):
        return self.instructor.find_element_by_id("pause-submit")

    #remove for later
    def minutes_pause_modal(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-timer']/div[2]/b")

    def pause_modal_add_minute_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-timer']/div[2]/div/div[2]/button")

    def pause_modal_decrease_minute_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-timer']/div[2]/div/div[1]/button")

    def pause_modal_add_hour_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-timer']/div[1]/div/div[2]/button")

    def pause_modal_decrease_hour_button(self):
        return self.instructor.find_element_by_xpath("//*[@id='pause-timer']/div[1]/div/div[1]/button")

    def pause_modal_ok_button(self):
        return self.instructor.find_element_by_id("pause-modal-ok")

    def pause_modal_cancel_button(self):
        return self.instructor.find_element_by_id("pause-modal-cancel")

    def close_start_modal(self):
        self.instructor.find_element_by_id("start-mode-select").click()
        select = Select(self.instructor.find_element_by_id("start-mode-select"))
        select.select_by_visible_text('Immediately')
        return self.instructor.find_element_by_id("start-modal-ok").click()

    def pause_timer_minute(self):
        return self.instructor.find_element_by_id("pause-timer-minutes")

    def pause_game_modal(self):
        return self.instructor.find_element_by_id("pause-modal-title")

    def resume_game_modal(self):
        return self.instructor.find_element_by_id("resume-modal-title")

    def start_modal_title(self):
        return self.instructor.find_element_by_id("start-modal-title")

    def start_modal_option_one(self):
        return self.instructor.find_element_by_xpath("//*[@id='start-mode-select']/option[1] ")

    def start_modal_field(self):
        return self.instructor.find_element_by_id("start-timer-minutes")

    def starting_text_reminder(self):
        return self.instructor.find_element_by_id("starting-text")
