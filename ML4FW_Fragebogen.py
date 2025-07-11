import os
from typing import Tuple, List, Union
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle as pkl

from questionnaire import Questionnaire
from question import Question
from use_case import UseCase
from category_definition import category_dict
from settings import risk_colors, result_directory_relative_path, preference_category_name, general_category_name, \
    intro_text, intro_explanation, preference_info_text, option_info


class ML4FWQuestionnaireApp:
    """
    This class that provides a questionnaire for estimating potential, costs and risk of  Machine Learning applications
    in district heating network operations. The Gui which is created in this class consists of the components
    1. Start Menu
    2. Options Menu (Use-Case category selection)
    3. Category/question display section
    4. Displaying category results
    5. Displaying use case results
    6. Displaying additional info on use cases

    Args:
        master (ctk.CTk): The main window of the application.

    Attributes:
        questionnaire (Questionnaire): The current questionnaire object.
        master (ctk.CTk): The main window of the application.
    """

    def __init__(self, master) -> None:
        """ Initializes the ML4FWQuestionnaireApp and sets up the GUI layout. """

        # Gui text settings
        self.win_height = 900
        self.win_width = int(self.win_height / 1.3)
        self.y_offset = 0
        self.x_offset = 100
        self.window_geometry = f"{self.win_width}x{self.win_height}+{self.x_offset}+{self.y_offset}"
        self.secondary_window_geometry = f"{self.win_width}x{self.win_height}+{self.x_offset + 100}+" \
                                         f"{self.y_offset + 100}"
        self.big_frame_width = self.win_width - 100
        self.big_frame_height = self.win_height - 100
        self.middle_frame_width = 400  # Introduced for question body
        self.middle_frame_height = 300  # Introduced for question body
        self.small_frame_width = 400  # Introduced for headlines
        self.small_frame_height = 75  # Introduced for headlines
        self.long_wrap_length = self.big_frame_width
        self.middle_wrap_length = self.middle_frame_width
        self.short_wrap_length = 200  # introduced for tables
        self.big_headline_font = ("Arial", 18, "bold")
        self.head_line_font = ("Arial", 14, "bold")
        self.plain_text_font = ("Arial", 12)
        self.icon_size = 20  # Size of info icons

        self.questionnaire = None

        self.master = master
        self.master.title("Fragebogen Machine Learning Use-Cases im Betrieb von Fernwärmenetzen")
        self.master.geometry(self.window_geometry)

        # Theme and colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Init start menu frames and widgets
        self.start_menu_name_frame = ctk.CTkFrame(master, width=self.small_frame_width, height=self.small_frame_height)
        self.start_menu_name_frame.pack_propagate(False)
        self.start_menu_label = ctk.CTkLabel(self.start_menu_name_frame,
                                             text="ML4FW Fragebogen: Machine Learning im Betrieb von Fernwärmenetzen",
                                             wraplength=self.middle_wrap_length, font=self.big_headline_font)
        self.start_menu_frame = ctk.CTkFrame(master, width=self.big_frame_width, height=self.big_frame_height)
        self.start_menu_frame.pack_propagate(True)
        self.start_menu_info_frame = ctk.CTkFrame(self.start_menu_frame, width=self.big_frame_width,
                                                  height=self.middle_frame_height - 100)
        self.start_menu_info_icon = InfoIcon(master=self.start_menu_frame, icon_size=self.icon_size,
                                             text_font=self.plain_text_font,
                                             window_geometry=self.secondary_window_geometry,
                                             wrap_length=self.long_wrap_length)
        self.start_menu_info_icon.set_info_text(info_text=intro_explanation)
        self.start_menu_info_canvas = ctk.CTkCanvas(self.start_menu_info_frame, width=self.big_frame_width,
                                                    height=self.middle_frame_height - 100,
                                                    bg="#2E2E2E", highlightthickness=0)
        self.start_menu_scrollbar = ctk.CTkScrollbar(self.start_menu_info_frame, orientation="vertical",
                                                     command=self.start_menu_info_canvas.yview)
        self.start_menu_info_text = ctk.CTkLabel(self.start_menu_info_canvas,
                                                 text=intro_text,
                                                 wraplength=self.long_wrap_length,
                                                 font=self.plain_text_font,
                                                 justify="left")
        self.start_menu_info_text.bind("<Configure>",
                                       lambda e: self.start_menu_info_canvas.configure(
                                           scrollregion=self.start_menu_info_canvas.bbox("all"))
                                       )
        self.start_menu_info_canvas.create_window((0, 0), window=self.start_menu_info_text, anchor="nw")

        self.start_button = ctk.CTkButton(self.start_menu_frame, text="Neuer Fragebogen",
                                          command=self.start_pressed)
        self.load_save_button = ctk.CTkButton(self.start_menu_frame, text="Speicherstand laden",
                                              command=self.get_file_path)
        self.load_explanation_label = ctk.CTkLabel(self.start_menu_frame,
                                                   text="Zum Laden eines Speicherstands geben Sie den Pfad zur "
                                                        "Speicherdatei in der Textbox unten an.",
                                                   wraplength=self.long_wrap_length,
                                                   font=self.plain_text_font)
        self.load_path_box = ctk.CTkEntry(self.start_menu_frame, width=self.long_wrap_length)
        self.load_path_box_packed = False
        self.load_button = ctk.CTkButton(self.start_menu_frame, text="Laden",
                                         command=self.load_questionnaire)
        self.loading_error_label = ctk.CTkLabel(self.start_menu_frame,
                                                text="Beim laden des angegebenen Speicherstandes ist ein Fehler "
                                                     "aufgetreten. Bitte prüfen Sie ob der Dateipfad korrekt ist"
                                                     "oder starten Sie einen neuen Fragebogen.",
                                                wraplength=self.long_wrap_length,
                                                font=self.plain_text_font,
                                                text_color="red")
        self.loading_error_label_packed = False
        self.start_menu_close_button = ctk.CTkButton(self.start_menu_frame, text="Anwendung schließen",
                                                     command=self.quit_application)

        # Init Option frame and widgets
        self.options_name_frame = ctk.CTkFrame(master, width=self.small_frame_width, height=self.small_frame_height)
        self.options_name_frame.pack_propagate(False)
        self.options_frame = ctk.CTkFrame(master, width=self.big_frame_width, height=self.big_frame_height)
        self.options_frame.pack_propagate(False)
        self.option_check_box_frame = ctk.CTkFrame(self.options_frame, width=self.middle_frame_width,
                                                   height=self.middle_frame_height)
        self.option_label = ctk.CTkLabel(self.options_name_frame, text="Kategorieauswahl",
                                         wraplength=self.middle_wrap_length, font=self.big_headline_font)
        self.option_question_label = ctk.CTkLabel(self.options_frame, text="", wraplength=self.long_wrap_length,
                                                  font=self.head_line_font)
        self.option_info_icon = InfoIcon(master=self.options_frame, icon_size=self.icon_size,
                                         text_font=self.plain_text_font,
                                         window_geometry=self.secondary_window_geometry,
                                         wrap_length=self.long_wrap_length)
        self.option_info_icon.set_info_text(info_text=option_info)
        self.options_continue_button = ctk.CTkButton(self.options_frame, text="Weiter",
                                                     command=self.option_continue_pressed)
        self.multiple_choice_options = []
        self.single_choice_option = ctk.StringVar(value="")
        self.options_back_button = ctk.CTkButton(self.options_frame, text="Zurück",
                                                 command=self.options_back_pressed)
        self.option_close_button = ctk.CTkButton(self.options_frame, text="Anwendung schließen",
                                                 command=self.quit_application)

        self.preference_information_title_frame = ctk.CTkFrame(master, width=self.small_frame_width,
                                                               height=self.small_frame_height)
        self.preference_information_title_frame.pack_propagate(False)
        self.preference_information_name = ctk.CTkLabel(self.preference_information_title_frame,
                                                        text=preference_category_name,
                                                        wraplength=self.middle_wrap_length, font=self.big_headline_font)
        self.preference_information_frame = ctk.CTkFrame(master, width=self.big_frame_width,
                                                         height=self.big_frame_height)
        self.preference_information_frame.pack_propagate(False)
        self.preference_information_label = ctk.CTkLabel(self.preference_information_frame, text=preference_info_text,
                                                         wraplength=self.long_wrap_length,
                                                         font=self.plain_text_font,
                                                         justify="left")
        self.preference_continue_button = ctk.CTkButton(self.preference_information_frame, text="Weiter",
                                                        command=self.preference_continue_pressed)
        self.preference_back_button = ctk.CTkButton(self.preference_information_frame, text="Zurück",
                                                    command=self.preference_back_pressed)
        self.preference_close_button = ctk.CTkButton(self.preference_information_frame, text="Anwendung schließen",
                                                     command=self.quit_application)

        # Init category frame and widgets
        self.category_frame = ctk.CTkFrame(master, width=self.small_frame_width, height=self.small_frame_height)
        self.category_frame.pack_propagate(False)
        self.category_label = ctk.CTkLabel(self.category_frame, text="", wraplength=self.middle_wrap_length,
                                           font=self.big_headline_font)

        # Init question frame and widgets
        self.question_frame = ctk.CTkFrame(master, width=self.big_frame_width, height=self.big_frame_height)
        self.question_frame.pack_propagate(False)
        self.question_check_boxes = []
        self.question_check_box_frame = ctk.CTkFrame(self.question_frame, width=self.middle_frame_width,
                                                     height=self.middle_frame_height)
        self.question_label = ctk.CTkLabel(self.question_frame, text="", wraplength=self.long_wrap_length,
                                           font=self.head_line_font)
        self.question_info_icon = InfoIcon(master=self.question_frame, icon_size=self.icon_size,
                                           text_font=self.plain_text_font,
                                           window_geometry=self.secondary_window_geometry,
                                           wrap_length=self.long_wrap_length)
        self.next_question_button = ctk.CTkButton(self.question_frame, text="Nächste Frage", command=self.next_question)
        self.previous_question_button = ctk.CTkButton(self.question_frame, text="Zurück",
                                                      command=self.previous_question)
        self.question_save_progress_button = ctk.CTkButton(self.question_frame, text="Zwischenstand speichern",
                                                           command=lambda: self.save(frame=self.question_frame))
        self.question_close_button = ctk.CTkButton(self.question_frame, text="Anwendung schließen",
                                                   command=self.quit_application)
        self.question_progress_label = ctk.CTkLabel(self.question_frame, text="", wraplength=self.long_wrap_length,
                                                    font=self.plain_text_font)
        self.tooltip = None

        # Init completion frame and widgets
        self.completion_frame = ctk.CTkFrame(master, width=self.big_frame_width, height=self.big_frame_height)
        self.completion_frame.pack_propagate(False)
        self.completion_label = ctk.CTkLabel(self.completion_frame,
                                             text="Vielen Dank für das Ausfüllen des Fragebogens!",
                                             wraplength=self.long_wrap_length, font=self.head_line_font)
        self.completion_category_plot_button = ctk.CTkButton(self.completion_frame, text="Kategorievergleich",
                                                             command=self.display_category_result_frame)
        self.completion_save_progress_button = ctk.CTkButton(self.completion_frame, text="Ergebnisse speichern",
                                                             command=lambda: self.save(frame=self.completion_frame))
        self.completion_close_button = ctk.CTkButton(self.completion_frame, text="Anwendung schließen",
                                                     command=self.quit_application)

        # Init category result frame and widgets
        self.category_result_frame = ctk.CTkFrame(master)
        self.category_plot_info_label = ctk.CTkLabel(self.category_result_frame,
                                                     text="Klicken Sie mit der Maus auf Kategorien in der Abbildung, "
                                                          "um eine Abwägung der Use-Cases innerhalb der Kategorie zu "
                                                          "erhalten.", wraplength=self.long_wrap_length,
                                                     font=self.plain_text_font)
        self.category_scatters = []
        self.category_figure = None
        self.category_canvas = None
        self.save_category_button = ctk.CTkButton(self.category_result_frame, text="Grafik speichern",
                                                  command=lambda: self.save_category_plot(
                                                      frame=self.category_result_frame))
        self.category_save_progress_button = ctk.CTkButton(self.category_result_frame, text="Ergebnisse speichern",
                                                           command=lambda: self.save(frame=self.category_result_frame))
        self.category_result_close_button = ctk.CTkButton(self.category_result_frame, text="Anwendung schließen",
                                                          command=self.quit_application)

        # Init use case result frame and widgets
        self.use_case_result_frame = None  # will be initialized in a new window in display_use_case_results
        self.use_case_plot_info_label = None
        self.use_case_scatters = []
        self.use_case_figure = None
        self.use_case_canvas = None
        self.save_use_case_button = None  # will be overwritten in add_use_case_plot depending on the category
        self.use_case_result_close_button = None

        if not os.path.isdir(result_directory_relative_path):
            os.mkdir(result_directory_relative_path)

        self.question_index = 1
        self.info_window_open = False
        self.init_options = True
        self.active_use_case_window = None
        self.display_start_frame()

    # Display frames

    def display_start_frame(self) -> None:
        """ Displays the start menu of the application, including the title text and buttons for starting a new
        questionnaire and loading a saved state. """
        self.start_menu_name_frame.pack(pady=20)
        self.start_menu_info_frame.pack(pady=20)
        self.start_menu_label.pack(pady=20)
        self.start_menu_info_canvas.pack(side="left", fill="both", expand=True)
        self.start_menu_scrollbar.pack(side="right", fill="y")
        self.start_menu_info_canvas.configure(yscrollcommand=self.start_menu_scrollbar.set)
        icon_x_pos = self.long_wrap_length - 15
        icon_y_pos = 0
        self.start_menu_info_icon.place(x_pos=icon_x_pos, y_pos=icon_y_pos)
        self.start_menu_frame.pack(pady=20)
        self.start_button.pack(pady=20)
        self.load_save_button.pack(pady=20)
        self.start_menu_close_button.pack(pady=20)

    def display_option_frame(self) -> None:
        """ Displays the options menu for selecting categories in the questionnaire. """
        self.options_name_frame.pack(pady=20)
        self.options_frame.pack(pady=20)
        self.option_label.pack(pady=20)
        self.option_question_label.pack(pady=20)
        icon_x_pos = self.long_wrap_length - 25
        icon_y_pos = 0
        self.option_info_icon.place(x_pos=icon_x_pos, y_pos=icon_y_pos)
        self.option_question_label.configure(text=self.questionnaire.init_question.question_text)
        self.option_check_box_frame.pack(pady=20)

        # Reset multiple_choice_options
        if self.init_options:
            self.multiple_choice_options = []
        for option in self.questionnaire.init_question.options:
            var = ctk.BooleanVar(value=option in self.multiple_choice_options)
            checkbutton = ctk.CTkCheckBox(self.option_check_box_frame, text=option,
                                          command=lambda opt=option: self.toggle_option(opt),
                                          variable=var)
            checkbutton.pack(pady=10, anchor='w')

        self.options_continue_button.pack(pady=20)
        self.options_back_button.pack(pady=20)
        self.option_close_button.pack(pady=20)
        self.init_options = False

    def display_preference_options(self) -> None:
        """ Displays explanations to preference options and global weights. """
        self.preference_information_title_frame.pack(pady=20)
        self.preference_information_name.pack(pady=20)
        self.preference_information_frame.pack(pady=20)
        self.preference_information_label.pack(pady=20)
        self.preference_continue_button.pack(pady=20)
        self.preference_back_button.pack(pady=20)
        self.preference_close_button.pack(pady=20)

    def display_category_frame(self) -> None:
        """ Displays the frame for showing the current category in the questionnaire. """
        self.category_frame.pack(pady=20)
        self.category_label.pack(pady=20)

    def display_question_frame(self) -> None:
        """ Displays the frame for showing the current question and answer options. """
        self.question_frame.pack(pady=20)
        self.question_label.pack(pady=20)
        current_question = self.questionnaire.current_category().current_question()
        icon_x_pos = self.long_wrap_length - 25
        icon_y_pos = 0
        self.question_info_icon.set_info_text(info_text=current_question.get_info_text())
        self.question_info_icon.place(x_pos=icon_x_pos, y_pos=icon_y_pos)
        self.question_check_box_frame.pack(pady=20)
        self.next_question_button.pack(pady=10)
        self.previous_question_button.pack(pady=10)
        self.question_save_progress_button.pack(pady=10)
        self.question_close_button.pack(pady=10)
        self.display_progress()

    def display_progress(self):
        progress_text = self.get_progress()
        self.question_progress_label.configure(text=progress_text)
        self.question_progress_label.pack(side="bottom", anchor="se", padx=10, pady=10)
        tooltip_text = "Die Gesamtanzahl der Fragen kann sich abhängig von Ihren Antworten im Verlauf des " \
                       "Fragebogens dynamisch ändern."
        x_pos = self.long_wrap_length - 300
        y_pos = self.big_frame_height - 150
        self.question_progress_label.bind("<Enter>", lambda event: self.show_tooltip(event=event,
                                                                                     master=self.question_frame,
                                                                                     x_pos=x_pos,
                                                                                     y_pos=y_pos,
                                                                                     text=tooltip_text))
        self.question_progress_label.bind("<Leave>", self.hide_tooltip)

    def display_completion_frame(self) -> None:
        """ Displays the completion screen after all questions of the questionnaire have been filled out. """
        self.completion_frame.pack(pady=20)
        self.completion_label.pack(pady=20)
        self.completion_category_plot_button.pack(pady=20)
        self.completion_save_progress_button.pack(pady=20)
        self.completion_close_button.pack(pady=20)

    def display_category_result_frame(self) -> None:
        """ Displays the results of the category analysis, in form of a plot for category comparison. """
        self.clear_frame(frame=self.completion_frame)
        self.category_result_frame.pack(pady=20)
        self.add_category_plot()
        self.category_plot_info_label.pack(pady=20)
        self.save_category_button.pack(pady=20)
        self.category_save_progress_button.pack(pady=20)
        self.category_result_close_button.pack(pady=20)

    def display_use_case_result_frame(self, category_name: str) -> ctk.CTkToplevel:
        """ Displays the comparison plot for the use cases of a specific category in a new window.

        Args:
            category_name (str): The name of the category whose use cases are to be displayed.

        Returns
            CTkToplevel: use_case_result window
        """
        new_window = ctk.CTkToplevel()
        new_window.title(f"Vergleich der Use-Cases aus Kategorie {category_name}")
        new_window.geometry(self.secondary_window_geometry)
        self.use_case_result_frame = ctk.CTkFrame(new_window)
        self.use_case_result_frame.pack(pady=20)
        self.add_use_case_plot(category_name=category_name)
        self.use_case_plot_info_label = ctk.CTkLabel(self.use_case_result_frame,
                                                     text="Klicken Sie mit der Maus auf einen Use-Case in der "
                                                          "Abbildung, um eine Zusammenfassung des Use-Cases zu "
                                                          "erhalten.", wraplength=self.long_wrap_length,
                                                     font=self.plain_text_font)
        self.use_case_plot_info_label.pack(pady=20)
        self.save_use_case_button = ctk.CTkButton(self.use_case_result_frame, text="Grafik speichern",
                                                  command=lambda: self.save_use_case_plot(category_name=category_name,
                                                                                          frame=self.use_case_result_frame))
        self.save_use_case_button.pack(pady=20)
        self.use_case_result_close_button = ctk.CTkButton(self.use_case_result_frame, text="Fenster schließen",
                                                          command=new_window.destroy)
        self.use_case_result_close_button.pack(pady=20)
        return new_window

    def display_use_case_summary_frame(self, use_case_name: str, category_name: str) -> None:
        """ Displays the summary of a given use case in a new window.

        Args:
            use_case_name (str): The name of the use case.
            category_name (str): The name of the category to which the use case belongs.
        """
        new_window = ctk.CTkToplevel(self.master)
        new_window.title(f"Zusammenfassung für Use-Case {use_case_name}")
        new_window.geometry(self.secondary_window_geometry)

        use_case = self.questionnaire.get_use_case(use_case_name=use_case_name, category_name=category_name)
        summary_frame = ctk.CTkFrame(new_window)
        summary_frame.pack(pady=20)

        # Title
        summary_frame_title_label = ctk.CTkLabel(summary_frame, text=use_case.name, wraplength=self.long_wrap_length,
                                                 font=self.big_headline_font)
        summary_frame_title_label.pack(pady=20)

        # Description
        summary_frame_description_label = ctk.CTkLabel(summary_frame, text="Beschreibung: " + use_case.description,
                                                       wraplength=self.long_wrap_length, font=self.plain_text_font)
        summary_frame_description_label.pack(pady=20)

        # Applicability
        if not use_case.is_applicable:
            self.display_reason_for_non_applicability(frame=summary_frame, use_case=use_case)

        # Pro and contra table
        pro_con_table_label = ctk.CTkLabel(master=summary_frame, text="Pro und Kontra Argumente für diesen Use-Case:",
                                           wraplength=self.long_wrap_length, font=self.plain_text_font)
        pro_con_table_label.pack(pady=20)
        self.display_pro_contra_table(frame=summary_frame, use_case=use_case)

        # Literature
        source_text = "Literaturquelle für diesen Use-Case: " + use_case.literature_source
        source_label = ctk.CTkLabel(master=summary_frame, text=source_text, wraplength=self.long_wrap_length,
                                    font=self.plain_text_font)
        source_label.pack(pady=20)

        summary_close_button = ctk.CTkButton(summary_frame, text="Fenster schließen", command=new_window.destroy)
        summary_close_button.pack(pady=20)

    def display_reason_for_non_applicability(self, frame: ctk.CTkFrame, use_case: UseCase) -> None:
        """ Displays the reasons why a given use case is not applicable by listing the deciding questions and answers
        which lead to this result.

        Args:
            frame (ctk.CTkFrame): The frame where the reasons will be displayed.
            use_case (UseCase): The use case whose reasons will be displayed.
        """
        reason_list = use_case.reasons_for_non_applicability
        msg = f"Use-Case {use_case.name} ist nicht anwendbar \n"
        for i, reason in enumerate(reason_list):
            last_question = reason[-1]
            question_text = list(last_question.keys())[0]
            answer = last_question[question_text]
            msg += f"Grund {i + 1}: " + f"Antwort '{answer}' " + f"auf die Frage '{question_text}'\n"
        non_applicability_label = ctk.CTkLabel(master=frame, text=msg, wraplength=self.long_wrap_length,
                                               font=self.plain_text_font)
        non_applicability_label.pack(pady=20)

    def display_pro_contra_table(self, frame: ctk.CTkFrame, use_case: UseCase) -> None:
        """ Displays a table with pro and contra arguments for a given use case.

        Args:
            frame (ctk.CTkFrame): The frame where the table will be displayed.
            use_case (UseCase): The use case whose contents will be displayed.
        """
        # define a new frame within the main frame
        pro_contra_frame = ctk.CTkFrame(frame)
        pro_contra_frame.pack(pady=20)

        # Define table headers and data
        headers = ["Pro", "Kontra"]
        pro_contra = use_case.pro_contra_arguments
        pro_list = pro_contra["pro"]
        contra_list = pro_contra["contra"]
        table_length = max(len(pro_list), len(contra_list))
        table_data = []
        for i in range(table_length):
            if i < len(pro_list):
                pro = pro_list[i]
            else:
                pro = ""
            if i < len(contra_list):
                con = contra_list[i]
            else:
                con = ""
            table_data.append([pro, con])

        # Create table headers
        for j, header in enumerate(headers):
            label = ctk.CTkLabel(pro_contra_frame, text=header, font=self.head_line_font,
                                 wraplength=self.short_wrap_length)
            label.grid(row=0, column=j, padx=10, pady=5, sticky="nsew")

        # Add a visual separation line
        separator = ctk.CTkFrame(pro_contra_frame, height=2, width=0, fg_color="darkgray")
        separator.grid(row=1, columnspan=len(headers), pady=(0, 5), sticky="ew")

        # Create table data rows
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                label = ctk.CTkLabel(pro_contra_frame, text=item, wraplength=self.short_wrap_length,
                                     font=self.plain_text_font)
                label.grid(row=i + 2, column=j, padx=10, pady=5, sticky="nsew")  # Adjust row index

        # Configure grid weights to make it responsive
        for j in range(len(headers)):
            pro_contra_frame.grid_columnconfigure(j, weight=1)

    # Update frames

    def update_category_display(self) -> None:
        """ Displays the current category label if the current questionnaire category is not None.
        Additionally, this function calls the first question display for a category.
        """
        category = self.questionnaire.current_category()
        if category is not None:
            if category.name == preference_category_name or category.name == general_category_name:
                category_label = category.name
            else:
                category_label = "Kategorie: " + category.name
            self.category_label.configure(text=category_label)
            self.category_frame.configure(fg_color=self.questionnaire.current_category().color)
            self.display_question_frame()
            self.update_question_display()
        else:
            self.clear_frame(frame=self.category_frame)
            self.clear_frame(frame=self.question_frame)
            self.display_completion_frame()

    def update_question_display(self) -> None:
        """ Updates the display of the current question and answer options. """
        question = self.questionnaire.current_category().current_question()
        if question is not None:
            self.question_label.configure(text=question.question_text)
            self.question_info_icon.set_info_text(info_text=question.get_info_text())
            progress_text = self.get_progress()
            self.question_progress_label.configure(text=progress_text)
            self.reset_check_boxes()
            self.create_check_boxes(question=question, selected_answer=question.answer)
        else:
            self.questionnaire.next_category()
            self.update_category_display()

    # Button functions

    def start_pressed(self) -> None:
        """ Starts a new questionnaire and displays the option menu (category selection). """
        self.clear_frame(frame=self.start_menu_name_frame)
        self.clear_frame(frame=self.start_menu_frame)
        self.load_path_box_packed = False
        self.loading_error_label_packed = False
        # Initialize new questionnaire
        self.questionnaire = Questionnaire()
        self.multiple_choice_options = []
        self.display_option_frame()

    def option_continue_pressed(self) -> None:
        """ Saves the selected options and displays the preference information screen. """
        if len(self.multiple_choice_options) > 0:
            category_list = [category_dict[choice.split(":")[0]] for choice in self.multiple_choice_options]
            self.questionnaire.set_categories(category_list=category_list)
            self.clear_frame(frame=self.option_check_box_frame)
            self.clear_frame(frame=self.options_name_frame)
            self.clear_frame(frame=self.options_frame)
            self.display_preference_options()

    def options_back_pressed(self) -> None:
        """ Clears options frame and displays start frame. """
        self.clear_frame(frame=self.option_check_box_frame)
        self.clear_frame(frame=self.options_name_frame)
        self.clear_frame(frame=self.options_frame)
        self.display_start_frame()

    def preference_continue_pressed(self) -> None:
        """ Clears preference frame and displays first category. """
        self.clear_frame(frame=self.preference_information_title_frame)
        self.clear_frame(frame=self.preference_information_frame)
        self.display_category_frame()
        self.update_category_display()

    def preference_back_pressed(self) -> None:
        """ Clears preference frame and displays option frame. """
        self.clear_frame(frame=self.preference_information_title_frame)
        self.clear_frame(frame=self.preference_information_frame)
        self.display_option_frame()

    def next_question(self) -> None:
        """ Moves to the next question in the questionnaire and saves the currently given answers. """
        current_question = self.questionnaire.current_category().current_question()
        if current_question.multiple_choice:
            if len(self.multiple_choice_options) > 0:  # At least one answer was given -> save the answers
                current_question.set_answer(self.multiple_choice_options)
            else:  # No answer was given -> nothing happens
                return
        else:
            answer = self.single_choice_option.get()
            if len(answer) > 0:  # An answer was given -> save it
                current_question.set_answer(answer)
            else:  # No answer was given -> nothing happens
                return
        next_question_found = self.questionnaire.current_category().next_question()
        if next_question_found:
            self.question_index += 1
        self.update_question_display()

    def previous_question(self) -> None:
        """ Moves to the previous question in the questionnaire. """
        category_question_index = self.questionnaire.current_category().question_index
        if category_question_index > 0:
            self.questionnaire.current_category().previous_question()
            self.question_index -= 1
        else:
            if self.questionnaire.current_category().name == preference_category_name:
                self.clear_frame(frame=self.category_frame)
                self.clear_frame(frame=self.question_frame)
                self.display_preference_options()
                return
            else:
                self.questionnaire.previous_category()
                previous_questions = self.questionnaire.current_category().questions
                self.questionnaire.current_category().question_index = len(previous_questions) - 1
                self.question_index -= 1
                self.update_category_display()

        self.update_question_display()

    def show_tooltip(self, event, master: ctk.CTkFrame, x_pos: int, y_pos: int, text: str) -> None:
        """ Shows the tooltip when hovering over the question_progress_label. """
        if self.tooltip is not None:
            return

        self.tooltip = ctk.CTkLabel(master, text=text,
                                    wraplength=300)
        self.tooltip.place(x=x_pos, y=y_pos)

    def hide_tooltip(self, event) -> None:
        """ Hides the tooltip when not hovering over the question_progress_label. """
        if self.tooltip is not None:
            self.tooltip.after(500, self.tooltip.destroy)
            self.tooltip = None

    def switch_to_category_plot(self) -> None:
        """ Switches to the display of the category plot. """
        self.clear_frame(frame=self.use_case_result_frame)
        self.add_category_plot()

    def save_category_plot(self, frame: ctk.CTkFrame) -> None:
        """ Saves the category plot as a PNG file.

        Args:
            frame (ctk.CTkFrame): The frame where the confirmation will be displayed.
        """
        file_name = os.path.join(result_directory_relative_path, "Kategorievergleich.png")
        self.category_figure.savefig(file_name)
        save_successful_label = ctk.CTkLabel(frame, text="Grafik erfolgreich gespeichert!")
        save_successful_label.pack(pady=10)
        save_successful_label.after(1500, save_successful_label.destroy)

    def save_use_case_plot(self, category_name: str, frame: ctk.CTkFrame) -> None:
        """ Saves the use case plot as a PNG file.

        Args:
            category_name (str): The name of the category to which the use case belongs.
            frame (ctk.CTkFrame): The frame where the confirmation will be displayed.
        """
        file_name = os.path.join(result_directory_relative_path, f"{category_name} Use-Case Vergleich.png")
        self.use_case_figure.savefig(file_name)
        save_successful_label = ctk.CTkLabel(frame, text="Grafik erfolgreich gespeichert!")
        save_successful_label.pack(pady=10)
        save_successful_label.after(1500, save_successful_label.destroy)

    def on_graphic_clicked(self, event, is_category: bool, category_name: str = None) -> None:
        """ Handles click events on the plot to display further information.

        Args:
            event: The click event.
            is_category (bool): Indicates whether this is a category plot.
            category_name (str, optional): The name of the category (only expected if is_category=False).
        """
        if is_category:
            scatter_list = self.category_scatters
        else:
            scatter_list = self.use_case_scatters

        # Check if the click is on any points
        for dictionary in scatter_list:
            # Each dictionary of scatter_list is expected to have exactly one key value pair
            name = list(dictionary.keys())[0]
            scatter_object = dictionary[name]
            x, y = scatter_object.get_offsets()[0]
            if abs(event.xdata - x) < 0.125 and abs(event.ydata - y) < 0.125:
                if is_category:
                    if self.active_use_case_window is not None:
                        self.active_use_case_window.destroy()
                    new_window = self.display_use_case_result_frame(category_name=name)
                    self.active_use_case_window = new_window
                else:
                    self.display_use_case_summary_frame(use_case_name=name, category_name=category_name)

    # Utility functions

    def get_progress(self) -> str:
        """ Evaluates the current questionnaire progress and returns it in form of string

        Returns:
            str: progress in form of question_index / num_total_questions
        """
        num_questions = self.questionnaire.get_number_of_questions()
        progress_text = f"Frage {self.question_index}/{num_questions}"
        return progress_text

    def get_file_path(self) -> None:
        if self.load_path_box_packed:
            pass
        else:
            # update close button position so that it is still the lowest button on the screen
            self.start_menu_close_button.pack_forget()
            self.load_explanation_label.pack(pady=20)
            self.load_path_box.pack(pady=20)
            # Insert default value into load_path_box
            default_load_path = os.path.join(result_directory_relative_path, 'ML4FW_Fragebogen_Speicherstand.pkl')
            self.load_path_box.insert(0, default_load_path)
            self.load_button.pack(pady=20)
            self.start_menu_close_button.pack(pady=20)
            self.load_path_box_packed = True

    def load_questionnaire(self) -> None:
        path = self.load_path_box.get()
        if os.path.isfile(path):
            with open(path, "rb") as file:
                self.questionnaire = pkl.load(file)
            file.close()
            self.clear_frame(frame=self.start_menu_name_frame)
            self.clear_frame(frame=self.start_menu_frame)
            self.load_path_box_packed = False
            self.loading_error_label_packed = False
            if self.questionnaire.completed:
                self.display_completion_frame()
            else:
                self.display_category_frame()
                self.update_category_display()
        else:
            if self.loading_error_label_packed:
                pass
            else:
                # update close button position so that it is still the lowest button on the screen
                self.start_menu_close_button.pack_forget()
                self.loading_error_label.pack(pady=20)
                self.start_menu_close_button.pack(pady=20)
                self.loading_error_label_packed = True

    def reset_check_boxes(self) -> None:
        if len(self.question_check_boxes) > 0:
            for widget in self.question_check_boxes:
                widget.destroy()
            self.question_check_boxes = []

    def create_check_boxes(self, question: Question, selected_answer: Union[str, list, None]) -> None:
        """ Creates checkboxes or radio buttons for the answers of the current question.

        Args:
            question (Question): The current question object.
            selected_answer (Union[str, list, None]): The selected answer or answers.
        """
        if question.multiple_choice:
            if selected_answer is not None:
                self.multiple_choice_options = selected_answer
            else:
                self.multiple_choice_options = []
            for option in question.options:
                checkbutton = ctk.CTkCheckBox(self.question_check_box_frame, text=option,
                                              command=lambda opt=option: self.toggle_option(opt))
                self.question_check_boxes.append(checkbutton)
                checkbutton.pack(anchor='w')
        else:
            if selected_answer is not None:
                self.single_choice_option = ctk.StringVar(value=selected_answer)
            else:
                self.single_choice_option = ctk.StringVar(value="")
            for option in question.options:
                radio = ctk.CTkRadioButton(self.question_check_box_frame, text=option,
                                           variable=self.single_choice_option, value=option)
                self.question_check_boxes.append(radio)
                radio.pack(anchor='w')

    def toggle_option(self, option) -> None:
        """ Toggles an option in the multiple-choice checkboxes.

        Args:
            option: The option to be toggled.
        """
        if option in self.multiple_choice_options:
            self.multiple_choice_options.remove(option)
        else:
            self.multiple_choice_options.append(option)

    def scatter_plot(self, is_category: bool, category_name: str = None) -> Tuple[plt.Figure, plt.Axes, List[dict]]:
        """ Creates a scatter plot for categories or use cases.

        Args:
            is_category (bool): Determines whether this is a category plot or a use-case plot.
            category_name (str, optional): The name of the category (only expected if is_category=False).

        Returns:
            Tuple[plt.Figure, plt.Axes, List[dict]]: The Figure and Axes objects, as well as the list of scatter
                objects.
        """
        if is_category:
            score_dict = self.questionnaire.final_category_scores
            short_name_prefix = "K"
            title = "Kategorievergleich"
        else:
            score_dict = self.questionnaire.final_use_case_scores[category_name]
            short_name_prefix = "UC"
            title = f"{category_name} Use-Case Vergleich"

        figure, ax = plt.subplots(figsize=(8, 4))
        ax.grid(zorder=1)
        scatter_list = []
        for i, name in enumerate(score_dict):
            short_name = short_name_prefix + str(i + 1)
            score = score_dict[name]
            scatter_object = ax.scatter(x=[score["Effort"]], y=[score["Potential"]],
                                        color=risk_colors[int(max(score["Risk"], 1))], alpha=0.75, s=300,
                                        label=short_name + ": " + name, edgecolors="black", zorder=2)
            scatter_list.append({name: scatter_object})
            ax.annotate(short_name, (score["Effort"], score["Potential"]),
                        textcoords="offset points",
                        xytext=(0, -3),
                        ha='center',
                        fontsize=7,
                        )

        ax.set_title(title)
        ax.set_xlabel("Aufwand (1=Niedrig, 5=Hoch)")
        ax.set_ylabel("Nutzen (1=Niedrig, 5=Hoch)")
        ax.set_ylim(bottom=-0.5, top=5.5)
        ax.set_xlim(left=-0.5, right=5.5)
        ax.legend(prop={'size': 6}, markerscale=0)
        figure.tight_layout()

        return figure, ax, scatter_list

    def add_category_plot(self) -> None:
        """ Adds the category plot to the display. """
        figure, ax, scatter_list = self.scatter_plot(is_category=True)
        self.category_scatters = scatter_list
        self.category_figure = figure  # assign figure to category_figure for the save plot function
        self.category_canvas = FigureCanvasTkAgg(figure=self.category_figure, master=self.category_result_frame)
        self.category_canvas.mpl_connect("button_press_event", lambda x: self.on_graphic_clicked(x, is_category=True))
        self.category_canvas.get_tk_widget().pack(pady=20)
        # Show the plot
        self.category_canvas.draw()

    def add_use_case_plot(self, category_name: str) -> None:
        """ Adds the use case plot to the display.

        Args:
            category_name (str): The name of the category to which the use cases belong.
        """
        figure, ax, scatter_list = self.scatter_plot(is_category=False, category_name=category_name)
        self.use_case_scatters = scatter_list
        self.use_case_figure = figure  # assign figure to use_case_figure for the save plot function
        self.use_case_canvas = FigureCanvasTkAgg(figure=self.use_case_figure, master=self.use_case_result_frame)
        self.use_case_canvas.mpl_connect("button_press_event", lambda x: self.on_graphic_clicked(x, is_category=False,
                                                                                                 category_name=category_name))
        self.use_case_canvas.get_tk_widget().pack(pady=20)
        # Show the plot
        self.use_case_canvas.draw()

    def quit_application(self) -> None:
        """ Exits the application. """
        self.master.quit()

    def save(self, frame: ctk.CTkFrame) -> None:
        """ Saves the current state of the questionnaire to a file.

        Args:
            frame (ctk.CTkFrame): The frame where the confirmation will be displayed.
        """
        file_name = os.path.join(result_directory_relative_path, 'ML4FW_Fragebogen_Speicherstand.pkl')
        with open(file_name, 'wb') as file:
            pkl.dump(self.questionnaire, file)
        file.close()
        save_successful_label = ctk.CTkLabel(frame, text="Speichern erfolgreich!")
        save_successful_label.pack(pady=10)
        save_successful_label.after(1500, save_successful_label.destroy)

    @staticmethod
    def clear_frame(frame: ctk.CTkFrame) -> None:
        """ Clears all widgets from the specified frame.

        Args:
            frame (ctk.CTkFrame): The frame to be cleared.
        """
        for widget in frame.winfo_children():
            widget.pack_forget()
        frame.pack_forget()


class InfoIcon:
    """ Creates a CTk canvas that contains an info icon.

    Args:
        master (ctk.CTkFrame): The master frame for the info icon.
        icon_size (int): The size of the icon in pixels.
        window_geometry (str): The geometry of the info window (e.g., "300x200").
        text_font (tuple): The font settings for the info text, defined as a tuple.
        wrap_length (int): Wrap length for info text given in number of charakters.
    """

    def __init__(self, master: ctk.CTkFrame, icon_size: int, window_geometry: str, text_font: tuple, wrap_length: int):
        self.master = master
        self.icon_size = icon_size
        self.window_geometry = window_geometry
        self.text_font = text_font
        self.info_text = ""
        self.info_window_open = False
        self.canvas = self.create_info_icon()
        self.wrap_length = wrap_length

    def set_info_text(self, info_text: str):
        """ Sets the info text to be displayed in the info window.

        Args:
            info_text (str): The text to display when the info icon is clicked.
        """
        self.info_text = info_text

    def place(self, x_pos: int, y_pos):
        """ Places the info icon at the specified coordinates.

        Args:
            x_pos (int): The x-coordinate for placement.
            y_pos (int): The y-coordinate for placement.
        """
        self.canvas.place(x=x_pos, y=y_pos)

    def create_info_icon(self) -> ctk.CTkCanvas:
        """ Creates the info icon canvas with a circular shape and "i" text.

        Returns:
            ctk.CTkCanvas: The canvas containing the info icon.
        """
        self.canvas = ctk.CTkCanvas(self.master, width=self.icon_size, height=self.icon_size,
                                    highlightthickness=0, bg="#2E2E2E")

        # Define colors
        border_color = "#6495ED"
        text_color = border_color

        # Draw the circle
        self.canvas.create_oval(int(self.icon_size * 1 / 10), int(self.icon_size * 1 / 10),
                                int(self.icon_size * 9 / 10), int(self.icon_size * 9 / 10),
                                fill="white", outline=border_color, width=2)

        # Draw the "i"
        self.canvas.create_text(int(self.icon_size) / 2, int(self.icon_size) / 2, text="i",
                                font=("Arial", int(self.icon_size / 2.2), "bold"),
                                fill=text_color)
        self.canvas.bind("<Button-1>", lambda event: self.open_info_window(event, info_text=self.info_text))
        return self.canvas

    def open_info_window(self, event, info_text):
        """ Opens a new window displaying the info text when the icon is clicked.

        Args:
            event: The event that triggered this method.
            info_text (str): The text to display in the info window.
        """
        if not self.info_window_open:
            info_window = ctk.CTkToplevel(self.master)
            info_window.title("Information")
            info_window.geometry(self.window_geometry)
            info_label = ctk.CTkLabel(info_window, text=info_text, font=self.text_font, wraplength=self.wrap_length,
                                      justify="left")
            info_label.pack(pady=20)
            close_button = ctk.CTkButton(info_window, text="Schließen",
                                         command=lambda: self.close_info_window(info_window=info_window))
            close_button.pack(pady=10)
            info_window.attributes("-topmost", True)
            self.info_window_open = True

    def close_info_window(self, info_window):
        """ Closes the info window.

        Args:
            info_window: The window to be closed.
        """
        info_window.destroy()
        self.info_window_open = False


if __name__ == "__main__":
    root = ctk.CTk()
    app = ML4FWQuestionnaireApp(root)
    root.mainloop()
