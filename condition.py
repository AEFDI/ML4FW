
from typing import List, Dict
from question import Question
from settings import possible_condition_types


class Condition:
    f""" Conditions are used to decide whether a use case is applicable or not. This class stores the necessary
    information for condition inspection.
    In order to find the correct condition for a use case evaluation conveniently each condition is associated with a 
    condition type that describes the topic of the condition.

    Args:
        condition_type (str): Description of condition type for condition filtering.
            Possible options: {possible_condition_types}
        question_answer_list (List[Dict[str, str]]): List containing questions and corresponding answers. If the
            user answers match the defined answers for every question from this list, then the condition is
            fulfilled.
    """

    def __init__(self, condition_type: str, question_answer_list: List[Dict[str, str]]):
        """ Initializes the condition. """
        if condition_type in possible_condition_types:
            self.condition_type = condition_type
        else:
            raise ValueError(f"Unknown condition type {condition_type}. Please just use condition types from the "
                             f"following list or define a new on in settings.py {possible_condition_types}.")
        self.question_answer_list = question_answer_list

    def check(self, all_category_questions: List[Question], use_case_name: str) -> bool:
        """ Checks if the condition is fulfilled (i.e. all questions from question_answer_list can be found in the
        provided all_category_questions, and they have the expected answers)

        Args:
            all_category_questions (List[Question]): list of all questions (including the relevant ones for evaluating
                this condition)
            use_case_name (str): Name of the use case, which checks this condition.
        Returns:
            bool: True if the condition is fulfilled and False else.
        """
        expected_answer_match = None
        for dictionary in self.question_answer_list:
            for question in all_category_questions:
                if question.question_text in dictionary:
                    condition_question = question
                    expected_answer = dictionary[question.question_text]
                    expected_answer_match = condition_question.answer == expected_answer
                    break
            if expected_answer_match is None:
                raise ValueError(f"Question {list(dictionary.keys())} not found for Use-Case {use_case_name}")
            else:
                if not expected_answer_match:
                    # one question from the question list does not have the expected answer so the condition is not
                    # fulfilled -> no need for further question evaluations.
                    return False
        return True
