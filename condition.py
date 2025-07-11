
from typing import List, Dict
from question import Question


class Condition:
    """ Conditions are used to decide whether a use case is applicable or not. This class stores the necessary
    information for condition inspection. """
    def __init__(self, condition_type: str, question_answer_list: List[Dict[str, str]]):
        """ Initializes the condition
        Args:
            condition_type (str): Description of condition type for condition filtering.
                Possible options: data availability, label availability, meta data availability, user specific,
                    data quality
            question_answer_list (List[Dict[str, str]]): List containing questions and corresponding answers. If the
                user answers match the defined answers for every question from this list, then the condition is
                fulfilled.
        """
        self.condition_type = condition_type
        self.question_answer_list = question_answer_list

    def check(self, all_category_questions: List[Question], use_case_name: str) -> bool:
        """ Checks if the condition is fulfilled (i.e. all questions from question_answer_list can be found in the
        provided all_category_questions, and they have the expected answers)

        Args:
            all_category_questions (List[Question]): list of all questions (including the relevant ones for evaluating
                this condition)
            use_case_name (str): Name of the use case, which checks this condition.
        Returns:
            True if the condition is fulfilled and False else.
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
