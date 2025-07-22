import os
import pickle as pkl
from typing import Tuple, List, Dict, Union

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ml4fw_fragebogen.definition_scripts.category_definition import category_dict
from ml4fw_fragebogen.gui.info_icon import InfoIcon
from ml4fw_fragebogen.questionnaire_code.questionnaire import Questionnaire
from ml4fw_fragebogen.questionnaire_code.question import Question
from ml4fw_fragebogen.questionnaire_code.use_case import UseCase
from ml4fw_fragebogen.definition_scripts.general_settings import risk_colors, preference_category_name, \
    general_category_name, intro_text, intro_explanation, preference_info_text, option_info


class ML4FWQuestionnaireApp:
    """
    This class that provides a questionnaire for estimating potential, costs and risk of  Machine Learning applications
    in district heating network operations. The GUI which is created in this class consists of the components:
    1. **Start Menu**: Allows the user to start a new questionnaire or load a saved state.
    2. **Options Menu**: Enables the selection of use-case categories.
    3. **Category/Question Display Section**: Displays the current category and corresponding questions.
    4. **Displaying Category Results**: Shows the results of category analysis.
    5. **Displaying Use Case Results**: Presents the results for individual use cases.
    6. **Displaying Additional Info on Use Cases**: Provides detailed information about selected use cases.

    Args:
        master (ctk.CTk): The main window of the application.
        main_dir (str): Directory where the main file is located. Result dir will be defined relative to this.

    Attributes:
        questionnaire (Questionnaire): The current questionnaire object.
        master (ctk.CTk): The main window of the application.
        win_height (int): Height of the main window.
        win_width (int): Width of the main window.
        y_offset (int): Vertical offset for window positioning.
        x_offset (int): Horizontal offset for window positioning.
        window_geometry (str): Geometry string for the main window (e.g., "300x200+100+100").
        secondary_window_geometry (str): Geometry string for secondary windows.
        big_frame_width (int): Width of large frames.
        big_frame_height (int): Height of large frames.
        middle_frame_width (int): Width of medium frames for question body.
        middle_frame_height (int): Height of medium frames for question body.
        small_frame_width (int): Width of small frames for headlines.
        small_frame_height (int): Height of small frames for headlines.
        long_wrap_length (int): Wrap length for long text.
        middle_wrap_length (int): Wrap length for medium text.
        short_wrap_length (int): Wrap length for short text.
        big_headline_font (Tuple[str, int, str]): Font settings for big headlines (e.g. ("arial", 18, "bold")).
        head_line_font (Tuple[str, int, str]): Font settings for regular headlines (e.g. ("arial", 18, "bold")).
        plain_text_font (Tuple[str, int, str]): Font settings for plain text (e.g. ("arial", 18, "bold")).
        icon_size (int): Size of info icons.
        info_window_open (bool): Flag to indicate if an info window is open.
        init_options (bool): Flag to indicate if options have been initialized.
        active_use_case_window (ctk.CTkToplevel): Reference to the active use case window.

    Methods:
        display_start_frame(): Displays the start menu of the application.
        display_option_frame(): Displays the options menu for category selection.
        display_preference_options(): Displays explanations for preference options.
        display_category_frame(): Displays the current category in the questionnaire.
        display_question_frame(): Displays the current question and answer options.
        display_completion_frame(): Displays the completion screen after questionnaire submission.
        display_category_result_frame(): Displays results of category analysis as a plot.
        display_use_case_result_frame(category_name): Displays comparison plot for use cases in a new window.
        display_use_case_summary_frame(use_case_name, category_name): Displays summary of a specific use case.
        update_category_display(): Displays the current category label and the first question of the category.
        update_question_display(): Updates the display of the current question and answer options.
        next_question(): Moves to the next question and saves current answers.
        previous_question(): Moves to the previous question.
        quit_application(): Exits the application.
        save(frame): Saves the current state of the questionnaire to a file.
        load_questionnaire(): Loads a questionnaire from a specified file path.
        clear_frame(frame): Clears all widgets from the specified frame.
        scatter_plot(is_category, category_name): Creates a scatter plot for categories or use cases.
        add_category_plot(): Adds the category plot to the display.
        add_use_case_plot(category_name): Adds the use case plot for a specific category.
    """

    def __init__(self, master: ctk.CTk, main_dir: str) -> None:
        """ Initializes the ML4FWQuestionnaireApp and sets up the GUI layout. """
        self.result_directory = os.path.join(main_dir, "ML4FW_Fragebogen_Ausgaben")
        if not os.path.isdir(self.result_directory):
            os.mkdir(self.result_directory)

        # GUI text settings
        self.win_height: int = 900
        self.win_width: int = int(self.win_height / 1.3)
        self.y_offset: int = 0
        self.x_offset: int = 100
        self.window_geometry: str = f"{self.win_width}x{self.win_height}+{self.x_offset}+{self.y_offset}"
        self.secondary_window_geometry: str = f"{self.win_width}x{self.win_height}+{self.x_offset + 100}+" \
                                              f"{self.y_offset + 100}"
        self.big_frame_width: int = self.win_width - 100
        self.big_frame_height: int = self.win_height - 100
        self.middle_frame_width: int = 400  # Introduced for question body
        self.middle_frame_height: int = 300  # Introduced for question body
        self.small_frame_width: int = 400  # Introduced for headlines
        self.small_frame_height: int = 75  # Introduced for headlines
        self.long_wrap_length: int = self.big_frame_width
        self.middle_wrap_length: int = self.middle_frame_width
        self.short_wrap_length: int = 200  # introduced for tables
        self.big_headline_font: Tuple[str, int, str] = ("Arial", 18, "bold")
        self.head_line_font: Tuple[str, int, str] = ("Arial", 14, "bold")
        self.plain_text_font: Tuple[str, int, str] = ("Arial", 12, "normal")
        self.icon_size: int = 20  # Size of info icons

        self.questionnaire: Union[Questionnaire, None] = None

        self.master: ctk.CTk = master
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
                                              command=self.display_file_path_text_box)
        self.load_explanation_label = ctk.CTkLabel(self.start_menu_frame,
                                                   text="Zum Laden eines Speicherstands geben Sie den Pfad zur "
                                                        "Speicherdatei in der Textbox unten an.",
                                                   wraplength=self.long_wrap_length,
                                                   font=self.plain_text_font)
        self.load_path_box = ctk.CTkEntry(self.start_menu_frame, width=self.long_wrap_length)
        self.load_path_box_packed: bool = False
        self.load_button = ctk.CTkButton(self.start_menu_frame, text="Laden",
                                         command=self.load_questionnaire)
        self.loading_error_label = ctk.CTkLabel(self.start_menu_frame,
                                                text="Beim laden des angegebenen Speicherstandes ist ein Fehler "
                                                     "aufgetreten. Bitte prüfen Sie ob der Dateipfad korrekt ist"
                                                     "oder starten Sie einen neuen Fragebogen.",
                                                wraplength=self.long_wrap_length,
                                                font=self.plain_text_font,
                                                text_color="red")
        self.loading_error_label_packed: bool = False
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
        self.question_check_boxes: List[Union[ctk.CTkCheckBox, ctk.CTkRadioButton]] = []
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
        self.tooltip: Union[ctk.CTkLabel, None] = None

        # Init completion frame and widgets
        self.completion_frame = ctk.CTkFrame(master, width=self.big_frame_width, height=self.big_frame_height)
        self.completion_frame.pack_propagate(False)
        self.completion_label = ctk.CTkLabel(self.completion_frame,
                                             text="Vielen Dank für das Ausfüllen des Fragebogens!",
                                             wraplength=self.long_wrap_length, font=self.head_line_font)
        self.completion_category_plot_button = ctk.CTkButton(self.completion_frame, text="Kategorievergleich",
                                                             command=self.display_category_result_screen)
        self.completion_back_button = ctk.CTkButton(self.completion_frame, text="Zurück",
                                                    command=self.previous_question)
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
        self.category_back_button = ctk.CTkButton(self.category_result_frame, text="Zurück",
                                                  command=self.category_result_back_pressed)
        self.category_scatters: List[Dict[str, plt.Axes]] = []
        self.category_figure: Union[plt.Axes, None] = None
        self.category_canvas: Union[ctk.CTkCanvas, None] = None
        self.save_category_button = ctk.CTkButton(self.category_result_frame, text="Grafik speichern",
                                                  command=lambda: self.save_category_plot(
                                                      frame=self.category_result_frame))
        self.category_save_progress_button = ctk.CTkButton(self.category_result_frame, text="Ergebnisse speichern",
                                                           command=lambda: self.save(frame=self.category_result_frame))
        self.category_result_close_button = ctk.CTkButton(self.category_result_frame, text="Anwendung schließen",
                                                          command=self.quit_application)

        # Init use case result frame and widgets
        # These variables will be initialized in a new window in display_use_case_results
        self.use_case_result_frame: Union[ctk.CTkFrame, None] = None
        self.use_case_plot_info_label: Union[ctk.CTkLabel, None] = None
        self.use_case_scatters: List[Dict[str, plt.Axes]] = []
        self.use_case_figure: Union[plt.Axes, None] = None
        self.use_case_canvas: Union[ctk.CTkCanvas, None] = None
        # save_use_case_button be overwritten in add_use_case_plot depending on the category
        self.save_use_case_button: Union[ctk.CTkButton, None] = None
        self.use_case_result_close_button: Union[ctk.CTkButton, None] = None

        self.info_window_open: bool = False
        self.init_options: bool = True
        self.active_use_case_window: Union[ctk.CTkFrame, None] = None
        self.display_start_screen()

    # Display frames

    def display_start_screen(self) -> None:
        """ Displays the start menu of the application, including the title text and buttons for starting a new
        questionnaire and loading a saved state. Start screen contains:
        1. Headline of the questionnaire app.
        2. Intro text with scrollbar: Shows introduction text for the questionnaire.
        3. Info icon: Displays additional info regarding the questionnaire.
        4. Start button: Starts a new questionnaire.
        5. Load button: Loads an existing questionnaire from a file.
        6. Close button: Closes the application.
        """
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

    def display_option_screen(self) -> None:
        """ Displays the options menu for selecting categories in the questionnaire.
        Option screen contains:
        1. Headline of the option frame.
        2. Category selection question text.
        3. Info icon: Displays additional info for the category selection.
        4. Answer check boxes for the question.
        5. Continue button: Proceeds to criteria weighting screen.
        6. Back button: Takes the user back to the starting screen.
        7. Close button: Closes the application.
        """
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

    def display_info_on_preferences_screen(self) -> None:
        """ Displays explanations to preference options and global weights.
        This screen contains:
        1. Headline.
        2. Info text.
        3. Continue button: Proceeds to the preference questions (criteria weighting).
        4. Back button: Returns back to the options screen for category selection.
        5. Close button: Closes the application.
        """
        self.preference_information_title_frame.pack(pady=20)
        self.preference_information_name.pack(pady=20)
        self.preference_information_frame.pack(pady=20)
        self.preference_information_label.pack(pady=20)
        self.preference_continue_button.pack(pady=20)
        self.preference_back_button.pack(pady=20)
        self.preference_close_button.pack(pady=20)

    def display_category_frame(self) -> None:
        """ Displays the frame for showing the current category in the questionnaire.
        This frame contains the category headline.
        """
        self.category_frame.pack(pady=20)
        self.category_label.pack(pady=20)

    def display_question_frame(self) -> None:
        """ Displays the frame for showing the current question and answer options.
        This frame contains:
        1. Question text.
        2. Info icon: Displays additional information the question.
        3. Checkboxes for each answer option of the question.
        4. Next question button: Proceeds to next question or to the completion screen (if all questions are answered).
        5. Previous question button: Returns to the previous question or to the info_on_preferences_screen if there is
            no previous question.
        6. Save button: Saves the current questionnaire (including the given answers) in pickle format.
        7. Close button: Closes the application.
        8. Progress info: Shows number of questions answered and current total number questions in the questionnaire.
        8.1: Progress info tooltip: Info text explaining that the total number of questions can rise depending on
            the given answers since some answers trigger consequence questions.
        """
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

    def display_progress(self) -> None:
        """ Updates and displays the current progress of the questionnaire. This method shows the number of questions
        answered by the user and the total number of questions in the questionnaire. The displayed progress is updated
        dynamically as the user navigates through the questions.
        Additionally, it provides a tooltip that is displayed when the user hovers over the progress label.
        The tooltip explains that the total number of questions may increase depending on the answers given,
        as some responses can trigger additional consequence questions.
        """
        progress_text = self.questionnaire.get_progress()
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

    def display_completion_screen(self) -> None:
        """ Displays the completion screen after all questions of the questionnaire have been filled out.
        This screen contains:
        1. Headline.
        2. Show result button: Shows category scatter plot.
        3. Back button: Returns back to the last question of the questionnaire.
        4. Save button: Saves the current questionnaire in pickle format.
        5. Close button: Closes the application.
        """
        self.completion_frame.pack(pady=20)
        self.completion_label.pack(pady=20)
        self.completion_category_plot_button.pack(pady=20)
        self.completion_back_button.pack(pady=20)
        self.completion_save_progress_button.pack(pady=20)
        self.completion_close_button.pack(pady=20)

    def display_category_result_screen(self) -> None:
        """ Displays the results of the category analysis, in form of a plot for category comparison.
        This screen contains:
        1. Scatter plot of all evaluated categories.
        2. Information label: Explains how one can interact with the plot.
        3. Back button: Returns back to the completion screen.
        4. Save plot button: Save the plot in png format.
        5. Save progress button: Saves the questionnaire in pickle format.
        6. Close button: Closes the application.
        """
        self.clear_frame(frame=self.completion_frame)
        self.category_result_frame.pack(pady=20)
        self.add_category_plot()
        self.category_plot_info_label.pack(pady=20)
        self.category_back_button.pack(pady=20)
        self.save_category_button.pack(pady=20)
        self.category_save_progress_button.pack(pady=20)
        self.category_result_close_button.pack(pady=20)

    def display_use_case_result_window(self, category_name: str) -> ctk.CTkToplevel:
        """ Displays the comparison plot for the use cases of a specific category in a new window.
        This window contains:
        1. Scatter plot of all use case evaluations in the specified category.
        2. Save plot button: Saves the scatter plot in png format.
        3. Close button: Closes the use case result window.

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
        args = {"category_name": category_name, "frame": self.use_case_result_frame}
        self.save_use_case_button = ctk.CTkButton(self.use_case_result_frame, text="Grafik speichern",
                                                  command=lambda: self.save_use_case_plot(**args)
                                                  )
        self.save_use_case_button.pack(pady=20)
        self.use_case_result_close_button = ctk.CTkButton(self.use_case_result_frame, text="Fenster schließen",
                                                          command=new_window.destroy)
        self.use_case_result_close_button.pack(pady=20)
        return new_window

    def display_use_case_summary_window(self, use_case_name: str, category_name: str) -> None:
        """ Displays the summary of a given use case in a new window.
        This window contains:
        1. Headline (use case name).
        2. Info text that describes the use case briefly.
        3. (Optional) Info text on non applicability reasons if there are any.
        4. Pro and Contra table for aspects of the use case.
        5. Source link: Literature source for the given use case.
        6. Close button: Closes the use case summary window.

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

    # Update screens
    def update_category_display(self) -> None:
        """ Displays the current category label if the current questionnaire category is not None. If there is no
        current category, the completion_screen will be shown.
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
            self.display_completion_screen()

    def update_question_display(self) -> None:
        """ Updates the display of the current question and answer options. If there is no current question in the
        current category, the next category will be selected. """
        question = self.questionnaire.current_category().current_question()
        if question is not None:
            self.question_label.configure(text=question.question_text)
            self.question_info_icon.set_info_text(info_text=question.get_info_text())
            progress_text = self.questionnaire.get_progress()
            self.question_progress_label.configure(text=progress_text)
            self.destroy_check_boxes()
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
        self.display_option_screen()

    def option_continue_pressed(self) -> None:
        """ Saves the selected options and displays the preference information screen. """
        if len(self.multiple_choice_options) > 0:
            category_list = [category_dict[choice.split(":")[0]] for choice in self.multiple_choice_options]
            self.questionnaire.set_categories(category_list=category_list)
            self.clear_frame(frame=self.option_check_box_frame)
            self.clear_frame(frame=self.options_name_frame)
            self.clear_frame(frame=self.options_frame)
            self.display_info_on_preferences_screen()
        else:
            # Remind the user that no answer was given yet.
            no_answer_label = ctk.CTkLabel(self.options_frame, text="Bitte beantworten Sie zuerst die Frage.")
            no_answer_label.pack(pady=10)
            no_answer_label.after(1500, no_answer_label.destroy)

    def options_back_pressed(self) -> None:
        """ Clears options screen and displays start screen. """
        self.clear_frame(frame=self.option_check_box_frame)
        self.clear_frame(frame=self.options_name_frame)
        self.clear_frame(frame=self.options_frame)
        self.display_start_screen()

    def preference_continue_pressed(self) -> None:
        """ Clears preference screen and displays first category. """
        self.clear_frame(frame=self.preference_information_title_frame)
        self.clear_frame(frame=self.preference_information_frame)
        self.display_category_frame()
        self.update_category_display()

    def preference_back_pressed(self) -> None:
        """ Clears preference screen and displays option screen. """
        self.clear_frame(frame=self.preference_information_title_frame)
        self.clear_frame(frame=self.preference_information_frame)
        self.display_option_screen()

    def next_question(self) -> None:
        """ Moves to the next question in the questionnaire and saves the currently given answers. Prints a reminder if
         no answer was given yet. """
        current_question = self.questionnaire.current_category().current_question()
        answer_given = self.set_answer(question=current_question)
        if not answer_given:
            # Remind the user that no answer was given yet.
            no_answer_label = ctk.CTkLabel(self.question_frame, text="Bitte beantworten Sie zuerst die Frage.")
            no_answer_label.pack(pady=10)
            no_answer_label.after(1500, no_answer_label.destroy)
            return
        next_question_found = self.questionnaire.current_category().next_question()
        if next_question_found:
            self.questionnaire.question_index += 1
        self.update_question_display()

    def previous_question(self) -> None:
        """ Moves to the previous question in the questionnaire. If there is no previous question the
        info_on_preferences_screen will be displayed. If the questionnaire was already completed, the last question
        of the last category will be shown. Also saves the given answer (if there is any) to the current question, in
        case it has changed.
        There are 4 possible transitions, that this function handles:
        1. Completion to question:
            If questionnaire is already completed, go back to the last question of the last category.
        2. Question to preference info:
            If the first question if the questionnaire is reached, go back to the preference info screen.
        3. Current question to previous question:
            If there is a previous question within the current category, move to that question.
        4. Current question to previous category:
            If there is no previous question in the current category but there still is a previous category,
            go back to the last question of the previous category.
        """
        if self.questionnaire.current_category() is None:
            # In this case the questionnaire is already completed, so the previous category must be displayed.
            self.questionnaire.previous_category()

            # get last question of the previous category
            previous_questions = self.questionnaire.current_category().questions
            self.questionnaire.current_category().question_index = len(previous_questions) - 1
            self.questionnaire.question_index -= 1

            # screen transition
            self.clear_frame(frame=self.completion_frame)
            self.display_category_frame()
            self.update_category_display()

        else:  # In this case the questionnaire is not completed so a current category exists

            # save the answer of the current question in case it has changed
            current_question = self.questionnaire.current_category().current_question()
            self.set_answer(question=current_question)

            category_question_index = self.questionnaire.current_category().question_index
            if category_question_index > 0:
                self.questionnaire.current_category().previous_question()
                self.questionnaire.question_index -= 1

            else:
                # In this case the user has reached the first question of the current category, so we have to go back to
                # the previous category.
                if self.questionnaire.current_category().name == preference_category_name:
                    # If the current category is preferences then there exists no previous category, so we must
                    # transition back to the info on preferences screen.
                    self.clear_frame(frame=self.category_frame)
                    self.clear_frame(frame=self.question_frame)
                    self.display_info_on_preferences_screen()
                    return
                else:
                    # If the current category is not preferences then there exists a previous category of which the
                    # last question has to be displayed.
                    self.questionnaire.previous_category()
                    previous_questions = self.questionnaire.current_category().questions
                    self.questionnaire.current_category().question_index = len(previous_questions) - 1
                    self.questionnaire.question_index -= 1
                    self.update_category_display()

            self.update_question_display()

    def set_answer(self, question: Question) -> bool:
        """ If an answer to question was given, it will be saved. Otherwise, nothing happens.

        Args:
            question (Question): question object for saving the answer
        Returns:
            bool: True if an answer was given, False else.
        """
        if question.multiple_choice:
            answer_given = len(self.multiple_choice_options) > 0
            if answer_given:
                question.set_answer(self.multiple_choice_options)
        else:
            answer = self.single_choice_option.get()
            answer_given = len(answer) > 0
            if answer_given:
                question.set_answer(answer)
        return answer_given

    def show_tooltip(self, event, master: ctk.CTkFrame, x_pos: int, y_pos: int, text: str) -> None:
        """ Shows the tooltip when hovering over the question_progress_label.

        Args:
            event: unused parameter, it is just here because the bind functions of a CTkLabel provides this parameter.
            master (ctk.CTkFrame): Frame where the tooltip will be displayed.
            x_pos (int): x position of the tooltip placement.
            y_pos (int): y position of the tooltip placement.
            text (str): Text of the tooltip.
        """
        if self.tooltip is not None:
            return

        self.tooltip = ctk.CTkLabel(master, text=text,
                                    wraplength=300)
        self.tooltip.place(x=x_pos, y=y_pos)

    def hide_tooltip(self, event) -> None:
        """ Hides the tooltip when the mouse leaves the question_progress_label.

        Args:
            event: unused parameter, it is just here because the bind functions of a CTkLabel provides this parameter.
        """
        if self.tooltip is not None:
            self.tooltip.after(500, self.tooltip.destroy)
            self.tooltip = None

    def category_result_back_pressed(self) -> None:
        """ Clears category result screen and shows completion screen. """
        self.clear_frame(frame=self.category_result_frame)
        self.display_completion_screen()

    def save_category_plot(self, frame: ctk.CTkFrame) -> None:
        """ Saves the category plot as a PNG file.

        Args:
            frame (ctk.CTkFrame): The frame where the confirmation will be displayed.
        """
        if not os.path.isdir(self.result_directory):  # check if dir exists just to be sure
            os.mkdir(self.result_directory)

        file_name = os.path.join(self.result_directory, "Kategorievergleich.png")
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
        if not os.path.isdir(self.result_directory):  # check if dir exists just to be sure
            os.mkdir(self.result_directory)

        file_name = os.path.join(self.result_directory, f"{category_name} Use-Case Vergleich.png")
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
                    new_window = self.display_use_case_result_window(category_name=name)
                    self.active_use_case_window = new_window
                else:
                    self.display_use_case_summary_window(use_case_name=name, category_name=category_name)

    # Utility functions
    def display_file_path_text_box(self) -> None:
        """ Displays an input box for the file path and fills it with a default value. """
        if self.load_path_box_packed:
            pass
        else:
            # update close button position so that it is still the lowest button on the screen
            self.start_menu_close_button.pack_forget()
            self.load_explanation_label.pack(pady=20)
            self.load_path_box.pack(pady=20)
            # Insert default value into load_path_box
            if not os.path.isdir(self.result_directory):  # check if dir exists just to be sure
                os.mkdir(self.result_directory)
            default_load_path = os.path.join(self.result_directory, 'ML4FW_Fragebogen_Speicherstand_test.pkl')
            self.load_path_box.insert(0, default_load_path)
            self.load_button.pack(pady=20)
            self.start_menu_close_button.pack(pady=20)
            self.load_path_box_packed = True

    def load_questionnaire(self) -> None:
        """ Loads a questionnaire from the pickle file in path specified by the load_path_box. """
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
                self.display_completion_screen()
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

    def destroy_check_boxes(self) -> None:
        """ Destroys all current checkboxes in the question frame. """
        if len(self.question_check_boxes) > 0:
            for widget in self.question_check_boxes:
                widget.destroy()
            self.question_check_boxes = []

    def create_check_boxes(self, question: Question, selected_answer: Union[str, List[str], None]) -> None:
        """ Creates checkboxes or radio buttons for the answers of the current question.

        Args:
            question (Question): The current question object.
            selected_answer (Union[str, List[str], None]): The selected answer or answers.
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
                radio_button = ctk.CTkRadioButton(self.question_check_box_frame, text=option,
                                                  variable=self.single_choice_option, value=option)
                self.question_check_boxes.append(radio_button)
                radio_button.pack(anchor='w')

    def toggle_option(self, option: str) -> None:
        """ Toggles an option in the multiple-choice checkboxes.

        Args:
            option (str): The option to be toggled.
        """
        if option in self.multiple_choice_options:
            self.multiple_choice_options.remove(option)
        else:
            self.multiple_choice_options.append(option)

    def scatter_plot(self, is_category: bool, category_name: str = None
                     ) -> Tuple[plt.Figure, plt.Axes, List[Dict[str, plt.Axes]]]:
        """ Creates a scatter plot for categories or use cases. Displays potential ("Nutzen") on the y-axis,
        effort ("Aufwand") on the x-axis and risk ("Risiko") as the color of the scatter points.

        Args:
            is_category (bool): Determines whether this is a category plot or a use-case plot.
            category_name (str, optional): The name of the category (only expected if is_category=False).

        Returns:
            Tuple[plt.Figure, plt.Axes, List[Dict[str, plt.Axes]]]: The Figure and Axes objects, as well as the list of
                scatter objects.
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
        args = {"is_category": False, "category_name": category_name}
        self.use_case_canvas.mpl_connect("button_press_event", lambda x: self.on_graphic_clicked(x, **args)
                                         )
        self.use_case_canvas.get_tk_widget().pack(pady=20)
        # Show the plot
        self.use_case_canvas.draw()

    def save(self, frame: ctk.CTkFrame) -> None:
        """ Saves the current state of the questionnaire to a file.

        Args:
            frame (ctk.CTkFrame): The frame where the confirmation will be displayed.
        """
        if not os.path.isdir(self.result_directory):  # check if dir exists just to be sure
            os.mkdir(self.result_directory)

        file_name = os.path.join(self.result_directory, 'ML4FW_Fragebogen_Speicherstand_test.pkl')
        with open(file_name, 'wb') as file:
            pkl.dump(self.questionnaire, file)
        file.close()
        save_successful_label = ctk.CTkLabel(frame, text="Speichern erfolgreich!")
        save_successful_label.pack(pady=10)
        save_successful_label.after(1500, save_successful_label.destroy)

    def quit_application(self) -> None:
        """ Quits the entire application. """
        self.master.quit()

    @staticmethod
    def clear_frame(frame: ctk.CTkFrame) -> None:
        """ Clears all widgets from the specified frame.

        Args:
            frame (ctk.CTkFrame): The frame to be cleared.
        """
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
            else:
                widget.pack_forget()
        frame.pack_forget()
