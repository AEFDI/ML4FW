from typing import List, Union, Dict

from ml4fw_fragebogen.questionnaire_code.question import Question
from ml4fw_fragebogen.definition_scripts.general_settings import category_criteria, global_criteria, \
    preference_category_name, general_category_name
from ml4fw_fragebogen.questionnaire_code.use_case import UseCase


class Category:
    """
    Represents a category in the questionnaire, containing questions and use cases related to that category.
    The category class also provides evaluation functions for aggregation of scores.
    The questionnaire is expected to contain one Category object for each use case category that is defined in the
    category_names variable in general_settings.py.
    Additionally, there are the preferences category which is used to weight the global (cross category) evaluation
    criteria and the general questions category which is used for questions that are important for most use case
    categories.

    Args:
        name (str): The name of the category.
        color (str): The color associated with the category.
        default_questions (List[Question]): The default questions for the category.
        consequence_questions (List[Question]): Questions that may follow based on previous answers.
        use_cases (List[UseCase]): A list of use cases associated with the category.

    Attributes:
        final_use_case_scores (Dict[str, Dict[str, float]]): dictionary used to assign each use case a score dict
            containing potential, effort and risk values for the use case.
        criteria_list (List[str]): list of evaluation criteria names (str).
        preference_questions (List[Question]): list of questions for criteria weighting (this list is empty for the
            general question category.
        potential_questions (List[Question]): list of all potential-related questions.
        effort_questions (List[Question]): list of all effort-related questions.
        risk_questions (List[Question]): list of all risk-related questions.

    Methods:
        current_question() -> Union[Question, None]:
            Retrieves the current question based on the current question index.

        next_question() -> bool:
            Moves to the next question in the category, and adds a consequence question if applicable.

        previous_question():
            Moves to the previous question in the category, removing a consequence question if necessary.

        add_consequence_question(consequence_question_name: str):
            Adds a consequence question to the question list based on the provided question name.

        remove_consequence_question(current_question: Question, consequence_question_name: str, question_index: int):
            Removes the consequence question from the question list if it matches the current question.

        eval_category_risk() -> int:
            Evaluates the average risk based on the risk-related questions in the category.

        eval_use_cases(local_criteria_weights: dict, general_question_list: List[Question]) -> dict:
            Evaluates the applicability and scoring of use cases based on the criteria weights and answers to questions.

        update_question_categories(question_list: List[Question]):
            Updates the categorized questions based on a new list of questions.
    """

    def __init__(self, name: str, color: str, default_questions: List[Question],
                 consequence_questions: List[Question], use_cases: List[UseCase]):
        """ Initializes the Category object with the provided parameters. """
        self.name: str = name
        self.color: str = color
        self.questions: List[Question] = default_questions
        # depending on consequence questions self.questions can be altered so default questions are saved in an
        # additional variable
        self.default_questions: List[Question] = default_questions.copy()
        self.consequence_questions: List[Question] = consequence_questions
        self.use_cases: List[UseCase] = use_cases
        self.question_index: int = 0
        self.final_use_case_scores: Dict[str, Dict[str, float]] = {}
        if self.name == preference_category_name:
            self.criteria_list: List[str] = global_criteria
        elif self.name == general_category_name:
            pass
        else:
            self.criteria_list: List[str] = category_criteria[name]
        self.preference_questions: List[Question] = [q for q in self.questions if "Preference" in q.type]
        self.potential_questions: List[Question] = [q for q in self.questions if "Potential" in q.type]
        self.effort_questions: List[Question] = [q for q in self.questions if "Effort" in q.type]
        self.risk_questions: List[Question] = [q for q in self.questions if "Risk" in q.type]

    def current_question(self) -> Union[Question, None]:
        """ Retrieves the current question based on the current question index.

        Returns:
            Union[Question, None]: The current Question object or None if there are no more questions.
        """
        if self.question_index < len(self.questions):
            return self.questions[self.question_index]
        else:
            return None

    def next_question(self) -> bool:
        """ Moves to the next question in the category, and adds a consequence question if applicable.

        Returns:
            bool: True if there is a next question, False else.
        """
        current_question = self.current_question()
        if self.question_index < len(self.questions):
            self.question_index += 1
            next_question_found = True
        else:
            next_question_found = False
        # Check if there is a consequence question for the current question and insert it as the next question if the
        # trigger answer is given.
        if current_question is None:
            return False
        elif current_question.consequence_triggered():
            self.add_consequence_question(consequence_question_name=current_question.get_consequence_question_name())
            next_question_found = True
        return next_question_found

    def previous_question(self) -> None:
        """ Moves to the previous question in the category, removing a consequence question if necessary. """
        current_question = self.current_question()
        current_question_index = self.question_index
        if self.question_index > 0:
            self.question_index -= 1
        previous_question = self.current_question()
        # remove current_question if it is the consequence of the previous question
        self.remove_consequence_question(current_question=current_question,
                                         consequence_question_name=previous_question.get_consequence_question_name(),
                                         question_index=current_question_index)

    def add_consequence_question(self, consequence_question_name: str) -> None:
        """ Adds a consequence question to the question list based on the provided question name. This function is
        sometimes used when the user jumps to a previous questions and changes the answer.

        Args:
            consequence_question_name (str): The name of the consequence question to be added.

        Raises:
            ValueError: If the consequence question is not found in the category.
        """
        for question in self.consequence_questions:
            if question.name == consequence_question_name:
                consequence_question = question
                self.questions.insert(self.question_index, consequence_question)
                return
        # If consequence question is not found raise an error
        raise ValueError(f"Consequence question {consequence_question_name} was not found in category {self.name}")

    def remove_consequence_question(self, current_question: Question, consequence_question_name: str,
                                    question_index: int) -> None:
        """ Removes the consequence question from the question list if it matches the current question. This function is
        sometimes used when the user jumps to a previous questions and changes the answer.

        Args:
            current_question (Question): The current Question object.
            consequence_question_name (str): The name of the consequence question to be removed.
            question_index (int): The index of the current question in the list.
        """
        # If the next question is the specified consequence_question it is removed from the question list
        if current_question.name == consequence_question_name:
            self.questions.pop(question_index)

    def eval_category_risk(self) -> int:
        """ Evaluates the average risk based on the risk-related questions in the category.

        Returns:
            int: The average risk value, rounded to the nearest integer.
        """
        risk = 0
        for question in self.risk_questions:
            risk += question.value
        if len(self.risk_questions) > 0:
            risk /= len(self.risk_questions)
        return int(risk)

    def eval_use_cases(self, local_criteria_weights: Dict[str, int], general_question_list: List[Question]
                       ) -> Dict[str, Dict[str, float]]:
        """ Evaluates the applicability and scoring of use cases based on the criteria weights and answers to questions.

        Args:
            local_criteria_weights (Dict[str, int]): Weights for the local criteria used in the category specific
                evaluation.
            general_question_list (List[Question]): A list of general questions to additionally consider in the
                evaluation.

        Returns:
            Dict[str, float]: A dictionary containing the final scores for potential, effort and risk for each use case.
        """
        for use_case in self.use_cases:
            score = {"Potential": 0., "Effort": 0., "Risk": 0.}
            all_questions = general_question_list + self.default_questions + self.consequence_questions
            use_case.eval_applicability(all_category_questions=all_questions)
            if use_case.is_applicable:
                score["Effort"] = use_case.get_effort(effort_questions=self.effort_questions)
                score["Potential"] = use_case.get_potential(local_criteria_weights=local_criteria_weights)
                score["Risk"] = use_case.get_risk(category_risk=self.eval_category_risk())
            else:  # Use-Case not applicable
                pass
            self.final_use_case_scores[use_case.name] = score
        return self.final_use_case_scores

    def update_question_categories(self, question_list: List[Question]) -> None:
        """ Updates the categorized questions based on a new list of questions. This function is used to include general
        non-category-specific questions in the evaluation process.

        Args:
            question_list (List[Question]): The new list of questions to categorize.
        """
        self.preference_questions = [q for q in question_list if "Preference" in q.type]
        self.potential_questions = [q for q in question_list if "Potential" in q.type]
        self.effort_questions = [q for q in question_list if "Effort" in q.type]
        self.risk_questions = [q for q in question_list if "Risk" in q.type]
