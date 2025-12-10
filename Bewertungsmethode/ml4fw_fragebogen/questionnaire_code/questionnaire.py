
from typing import List, Union, Dict

import pandas as pd

from ml4fw_fragebogen.questionnaire_code.category import Category
from ml4fw_fragebogen.definition_scripts.category_definition import preferences, general_questions
from ml4fw_fragebogen.questionnaire_code.question import Question
from ml4fw_fragebogen.definition_scripts.question_definition import init_question
from ml4fw_fragebogen.definition_scripts.general_settings import preference_category_name, general_category_name, \
    global_criteria_mapping, predefined_category_ranking_path
from ml4fw_fragebogen.questionnaire_code.use_case import UseCase


class Questionnaire:
    """ Represents the questionnaire logic used in the GUI. A questionnaire contains categories, questions, and
    use cases for evaluation.

    Attributes:
        init_question (Question): The initial question for the questionnaire.
        global_weights (Dict[str, int]): Weights for global criteria.
        local_weights (Dict[str, Dict[str, int]]): Weights for local criteria by category.
        final_category_scores (Dict[str, Dict[str, float]]): Final scores for each category.
        final_use_case_scores (Dict[str, Dict[str, Dict[str, float]]]): Final scores for each evaluated use case.
            structure: {category_1: {use_case_1: {crit_1: float, ...}, ...}, ...}
        categories (List[Category]): List of categories included in the questionnaire.
        chosen_categories (List[Category]): List of categories selected by the user.
        category_index (int): The current index of the category being evaluated.
        question_index (int): Current question index in the questionnaire.
        completed (bool): Indicates if the questionnaire has been completed.

    Methods:
        set_categories(category_list: List[Category]):
            Sets the categories for the questionnaire based on the selected options.

        set_weights():
            Sets the weights for the criteria based on the current answers to the preference questions in the category.

        get_number_of_questions() -> int:
            Retrieves the current total number of questions in the questionnaire.

        get_progress() -> str:
            Evaluates the current progress of the questionnaire and returns it as a string.

        current_category() -> Union[Category, None]:
            Retrieves the current Category object based on the current category index.

        eval_category():
            Evaluates the current category, including updating its scores based on risk, effort, and potential.

        get_use_case(use_case_name: str, category_name: str) -> UseCase:
            Retrieves a specific UseCase object by its name within the specified category.

        next_category() -> bool:
            Moves to the next category in the questionnaire, evaluating the current category if it has not been evaluated yet.

        previous_category():
            Moves to the previous category in the questionnaire.

        get_general_question_list() -> List[Question]:
            Retrieves the list of general questions from the questionnaire that are not specific to any category.

        get_category_potential_and_effort(category: Category) -> Dict[str, float]:
            Calculates the potential and effort scores for a given category based on predefined rankings.
    """
    def __init__(self):
        """ Initializes the Questionnaire object and its attributes. """
        self.init_question: Question = init_question
        self.global_weights: Dict[str, int] = {}
        self.local_weights: Dict[str, Dict[str, int]] = {}
        self.final_category_scores: Dict[str, Dict[str, float]] = {}
        self.final_use_case_scores: Dict[str, Dict[str, Dict[str, float]]] = {}
        self.categories: List[Category] = []
        self.chosen_categories: List[Category] = []
        self.category_index: int = 0
        self.question_index: int = 1
        self.completed: bool = False

    def set_categories(self, category_list: List[Category]) -> None:
        """ Sets the categories for the questionnaire based on the selected options.

        Args:
            category_list (List[Category]): A list of categories to include in the questionnaire.
        """
        self.categories = [preferences, general_questions] + category_list
        self.chosen_categories = category_list

    def set_weights(self) -> None:
        """ Sets the weights for the criteria based on the current answers to the preference questions in the
        category. """
        weights = {}
        category = self.current_category()
        for criteria in category.criteria_list:
            weight = None
            for question in category.preference_questions:
                if criteria in question.question_text:
                    weight = question.value
                    break
            weights[criteria] = weight
        if category.name == preference_category_name:
            self.global_weights = weights
        else:
            self.local_weights[category.name] = weights

    def get_number_of_questions(self) -> int:
        """ Retrieves the current total number of questions in the questionnaire.

        Returns:
            int: current total number of questions (this number can change due to consequence questions).
        """
        num_questions = 0
        for category in self.categories:
            num_questions += len(category.questions)
        return num_questions

    def get_progress(self) -> str:
        """ Evaluates the current questionnaire progress and returns it as a string.

        Returns:
            str: progress in form of question_index / num_total_questions
        """
        num_questions = self.get_number_of_questions()
        progress_text = f"Frage {self.question_index}/{num_questions}"
        return progress_text

    def current_category(self) -> Union[Category, None]:
        """ Retrieves the current category based on the current category index.

        Returns:
            Union[Category, None]: The current Category object, or None if all categories have been evaluated.
        """
        if self.category_index < len(self.categories):
            return self.categories[self.category_index]
        else:
            self.completed = True
            return None

    def eval_category(self) -> None:
        """ Evaluates the current category, including updating its scores based on risk, effort, and potential. """
        category = self.current_category()
        # include general questions and their answers in the current category use-case evaluation and
        # category risk evaluation
        general_question_list = self.get_general_question_list()
        category.update_question_categories(question_list=category.questions + general_question_list)
        if category.name == preference_category_name:  # evaluate effort and potential for all categories
            for category in self.chosen_categories:
                self.final_category_scores[category.name] = self.get_category_potential_and_effort(category=category)
        elif category.name != preference_category_name and category.name != general_category_name:
            # after preference category was evaluated final_category_score of the current category exists in terms
            # of potential and effort, but risk still needs updating. Also, the use-cases will be evaluated.
            category_scores = self.final_category_scores[category.name]
            for question in category.risk_questions:
                category_scores["Risk"] += question.value
            category_scores["Risk"] = int(category_scores["Risk"] / len(category.risk_questions))
            self.final_category_scores[category.name] = category_scores
            use_case_scores = category.eval_use_cases(local_criteria_weights=self.local_weights[category.name],
                                                      general_question_list=general_question_list)
            self.final_use_case_scores[category.name] = use_case_scores
        else:  # Skip general question category
            pass

    def get_use_case(self, use_case_name: str, category_name: str) -> UseCase:
        """ Retrieves a specific UseCase object by its name within the specified category.

        Args:
            use_case_name (str): The name of the use case to retrieve.
            category_name (str): The name of the category to search within.

        Returns:
            UseCase: The requested UseCase object.

        Raises:
            ValueError: If the use case is not found, raise a ValueError.
        """
        for category in self.chosen_categories:
            if category.name == category_name:
                for use_case in category.use_cases:
                    if use_case.name == use_case_name:
                        return use_case
        # If the use-case is not found raise a value error
        raise ValueError(f"Use-Case {use_case_name} could not be found in category {category_name}")

    def next_category(self) -> bool:
        """ Moves to the next category in the questionnaire, evaluating the current category if applicable.

        Returns:
            bool: True if there is a next category, False else.
        """
        if self.current_category().name != general_category_name:
            self.set_weights()
            self.eval_category()
        self.category_index += 1
        return self.category_index < len(self.categories)

    def previous_category(self) -> None:
        """ Moves to the previous category in the questionnaire. """
        self.category_index = max(self.category_index - 1, 0)
        if self.completed:  # If the user navigates back after completing the questionnaire.
            self.completed = False

    def get_general_question_list(self) -> List[Question]:
        """ Retrieves the list of general questions which are not category specific from the questionnaire.

        Returns:
            List[Question]: A list of general Question objects.

        Raises:
            ValueError: If the general questions category could not be found.
        """
        for category in self.categories:
            if category.name == general_category_name:
                return category.questions
        raise ValueError("General Questions Category could not be found")

    def get_category_potential_and_effort(self, category: Category) -> Dict[str, float]:
        """ Calculates the potential and effort scores for a given category based on predefined rankings.

        Args:
            category (Category): The category for which to calculate the scores.

        Returns:
            Dict[str, float]: A dictionary containing the calculated potential and effort scores for the
            specified category, as well as a default risk entry for each category.
        """
        category_scores = {"Risk": 0}  # initialize risk value
        predefined_ranking_df = pd.read_csv(predefined_category_ranking_path, sep=";", index_col="Unnamed: 0")
        predefined_scores = predefined_ranking_df.loc[category.name]
        for final_criteria in global_criteria_mapping:
            category_scores[final_criteria] = 0
            for criteria in global_criteria_mapping[final_criteria]:
                value = max((self.global_weights[criteria] / 5) * int(predefined_scores[criteria]), 1)
                category_scores[final_criteria] += value
            category_scores[final_criteria] /= len(global_criteria_mapping[final_criteria])
        return category_scores

    def get_category_of_use_case(self, use_case: UseCase) -> Category:
        """ Searches for the category where use_case is contained in the use_cases list. Raises a ValueError if the
        use case was not found or if it is ambiguous.

        Args:
            use_case (UseCase): Use case object for which the corresponding category is searched.

        Returns:
            (Category): Corresponding category
        """
        matching_category = None
        matching_use_cases = 0
        for cat in self.categories:
            for uc in cat.use_cases:
                if uc.name == use_case.name:
                    matching_use_cases += 1
                    matching_category = cat
        if matching_use_cases == 1:
            return matching_category
        elif matching_use_cases == 0:
            raise ValueError(f"Use case {use_case.name} can not be found in any category!")
        else:
            raise ValueError(f"The Use case name {use_case.name} was found more than once. Please make sure, that the"
                             f"use case name is unique.")
