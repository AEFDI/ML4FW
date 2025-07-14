from typing import List, Dict

from condition import Condition
from question import Question


class UseCase:
    """ Represents a use case in the questionnaire, including its properties, potential, effort, risk, and applicability conditions.

    Args:
        name (str): The name of the use case.
        predefined_potential (Dict[str, int]): A dictionary containing predefined potential values for the use case.
        predefined_effort (Dict[str, int]): A dictionary containing predefined effort values for the use case.
        predefined_risk_value (int): The predefined risk value associated with the use case.
        non_applicability_conditions (List[Condition]): A list of conditions under which the use case is considered not
            applicable.
        pro_contra_arguments (Dict[str, list]): A dictionary containing pro and contra arguments for the use case.
        literature_source (str): The source of literature related to the use case.
        description (str): A description of the use case.

    Attributes:
        is_applicable (bool or None): Indicates whether the use case is applicable (set after evaluation).
        reasons_for_non_applicability (List): A list of reasons for non-applicability.

    Methods:
        __init__(name, predefined_potential, predefined_effort, predefined_risk_value, non_applicability_conditions,
            pro_contra_arguments, literature_source, description):
            Initializes the UseCase object and its attributes.
        get_effort(effort_questions):
            Combines the predefined effort values with the answers to the effort questions into a total effort value.
        get_potential(local_criteria_weights):
            Calculates the weighted potential of the use case based on local criteria weights.
        get_risk(category_risk):
            Calculates the overall risk value for the use case by averaging the category risk and predefined risk value.
        is_not_applicable(all_category_questions):
            Checks if the use case is not applicable based on its non-applicability conditions.
        eval_applicability(all_category_questions):
            Evaluates the applicability of the use case based on the provided questions and sets the applicability
            attribute.
        get_data_availability_questions():
            Retrieves a list of question texts related to data availability and labeling conditions.
    """

    def __init__(self, name: str, predefined_potential: Dict[str, int], predefined_effort: Dict[str, int],
                 predefined_risk_value: int, non_applicability_conditions: List[Condition],
                 pro_contra_arguments: Dict[str, list], literature_source: str, description: str):
        """ Initializes the UseCase object and its attributes. """
        self.name: str = name
        self.description: str = description
        self.predefined_potential: Dict[str, int] = predefined_potential
        self.predefined_effort: Dict[str, int] = predefined_effort
        self.predefined_risk_value: int = predefined_risk_value
        self.non_applicability_conditions: List[Condition] = non_applicability_conditions
        self.literature_source: str = literature_source
        self.pro_contra_arguments: Dict[str, list] = pro_contra_arguments

        # Applicability attributes will be set after the questions in questionnaire have been evaluated
        self.is_applicable: bool = False
        self.reasons_for_non_applicability: List[List[Dict[str, str]]] = []

    def get_effort(self, effort_questions: List[Question]) -> float:
        """ Combines the predefined effort values with the answers to the effort questions into a total effort value.

        Args:
            effort_questions (List[Question]): A list of Question objects related to effort for the use case.

        Returns:
            float: The accumulated effort value.
        """
        weighted_effort = 0
        for key in self.predefined_effort:
            effort_question_value = 0
            number_of_questions = 0
            relevant_questions = [question for question in effort_questions if question.criteria == key]
            if key in ["Datenerhebungsaufwand", "Sensorinstallationsaufwand"]:
                # Only select the data availability questions which are relevant for this use-case
                data_availability_questions = self.get_data_availability_questions()
                relevant_questions = [x for x in relevant_questions if x.question_text in data_availability_questions]
            for question in relevant_questions:
                number_of_questions += 1
                effort_question_value += question.value
            if number_of_questions == 0:
                weighted_effort += self.predefined_effort[key]
            else:
                effort_question_value /= number_of_questions
                # The effort per criteria is the average of the predefined effort and the average over the results of
                # all criteria related effort questions
                weighted_effort += max((self.predefined_effort[key] / 5) * effort_question_value, 1)
        return weighted_effort / len(self.predefined_effort)

    def get_potential(self, local_criteria_weights: Dict[str, int]) -> float:
        """ Calculates the weighted potential of the use case based on local criteria weights.

        Args:
            local_criteria_weights (Dict[str, int]): A dictionary containing the weights for local criteria.

        Returns:
            float: The calculated potential value for the use case.
        """
        weighted_potential = 0
        for key in self.predefined_potential:
            weighted_potential += max(self.predefined_potential[key] * (local_criteria_weights[key] / 5), 1)
        return weighted_potential / len(self.predefined_potential)

    def get_risk(self, category_risk: int) -> float:
        """ Calculates the overall risk value for the use case by averaging the category risk and predefined risk value.

        Args:
            category_risk (int): The risk value from the category evaluation.

        Returns:
            float: The calculated risk value for the use case.
        """
        return (category_risk + self.predefined_risk_value) / 2

    def is_not_applicable(self, all_category_questions: List[Question]) -> bool:
        """ Checks if the use case is not applicable based on its non-applicability conditions.

        Args:
            all_category_questions (List[Question]): A list of all Question objects within the category of the use case.

        Returns:
            bool: True if the use case is not applicable, otherwise False.
        """
        use_case_not_applicable = False
        for condition_obj in self.non_applicability_conditions:
            # A condition list is fulfilled if all questions from the condition list have the expected answers.
            condition_fulfilled = condition_obj.check(all_category_questions=all_category_questions,
                                                      use_case_name=self.name)
            if condition_fulfilled:
                # at least one non-applicability condition is fulfilled
                self.reasons_for_non_applicability.append(condition_obj.question_answer_list)
                use_case_not_applicable = True
                # Do not break here in order to collect further potential non applicability reasons for use case summary
        return use_case_not_applicable

    def eval_applicability(self, all_category_questions: List[Question]) -> None:
        """ Evaluates the applicability of the use case based on the provided questions and sets the applicability
        attribute.

        Args:
            all_category_questions (List[Question]): A list of all Question objects within the category of the use case.
        """
        self.is_applicable = not self.is_not_applicable(all_category_questions=all_category_questions)

    def get_data_availability_questions(self) -> List[str]:
        """ Retrieves a list of question texts related to data availability and labeling conditions.

        Returns:
            List[str]: A list of question texts pertaining to data availability conditions.
        """
        data_conditions: List[Condition] = [x for x in self.non_applicability_conditions
                                            if x.condition_type == "data availability"]
        label_conditions: List[Condition] = [x for x in self.non_applicability_conditions
                                             if x.condition_type == "label availability"]
        question_list: List[str] = []
        for condition in data_conditions + label_conditions:
            question_list += [list(x.keys())[0] for x in condition.question_answer_list]
        return question_list
