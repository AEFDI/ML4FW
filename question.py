
from typing import List, Union
from settings import min_weight, max_weight


class Question:
    """ Represents a question in the questionnaire, including its text, options, and associated properties.

    Args:
        name (str): The unique identifier for the question.
        question_text (str): The text of the question to be displayed to the user.
        options (list): A list of possible answers for the question (str).
        multiple_choice (bool): Indicates whether the question allows multiple answers.
        question_types (List[str]): A list of types that classify the question. Possible types are: Preference,
                Specification, Potential, Effort, Risk
        answer_mapping (dict, optional): A mapping of answers to numerical values.
        criteria (str, optional): The criteria associated with the question.
        consequence_triggers (dict, optional): A mapping of answers to consequence question names.
        description_text (str): Additional description text.
        consequence_description (str): description text for the question consequences displayed together with other
            question info.
        reason_to_exist (str): description text that answers why the question is asked.
    """
    def __init__(self, name: str, question_text: str, options: list, multiple_choice: bool, question_types: List[str],
                 answer_mapping: dict = None, criteria: str = None, consequence_triggers: dict = None,
                 description_text: str = None, consequence_description: str = None, reason_to_exist: str = None):
        """ Initializes the Question object with the provided parameters. """
        self.name = name
        self.question_text = question_text
        self.options = options
        self.multiple_choice = multiple_choice
        self.type = question_types
        self.answer = None
        self.answer_mapping = answer_mapping
        self.value = None
        self.criteria = criteria
        self.consequence_triggers = consequence_triggers
        self.description_text = description_text
        self.consequence_description = consequence_description
        self.reason_to_exist = reason_to_exist

    def set_answer(self, answer: Union[str, list]) -> None:
        """ Sets the answer for the question and updates its value based on the answer mapping.

        Args:
            answer (Union[str, list]): The answer given by the user, which can be a single value or a list of values.
        """
        self.answer = answer
        if self.answer_mapping is not None:
            self.value = self.answer_mapping[answer]

    def consequence_triggered(self) -> bool:
        """ Checks if a consequence question should be triggered based on the current answer.

        Returns:
            bool: True if a consequence is triggered, False otherwise.
        """
        if self.consequence_triggers is None:
            return False
        else:
            for trigger in self.consequence_triggers:
                return self.answer in trigger

    def get_consequence_question_name(self) -> Union[str, None]:
        """ Retrieves the name of the consequence question that should be displayed based on the current answer.

        Returns:
            Union[str, None]: The name of the consequence question if triggered, otherwise None.
        """
        if self.consequence_triggered():
            return self.consequence_triggers[self.answer]
        else:
            return None

    def get_info_text(self) -> str:
        """ Returns info text consisting of description, consequence description and reason_to_exist """
        info_text = ""
        if self.description_text is not None:
            info_text += "Informationen zur Frage:" + "\n"
            info_text += self.description_text + "\n" + "\n"
        if self.consequence_description is not None:
            info_text += "Auswirkungen der Antworten:" + "\n"
            info_text += self.consequence_description + "\n" + "\n"
        if self.reason_to_exist is not None:
            info_text += "Warum diese Frage gestellt wird:" + "\n"
            info_text += self.reason_to_exist
        if info_text == "":
            info_text = "Keine zusätzlichen Informationen verfügbar."
        return info_text


def generate_preference_questions(criteria_list: list, criteria_description: dict) -> List[Question]:
    """ Generates a list of preference questions based on the provided criteria. This function is used for global and
    local criteria question definition.

    Args:
        criteria_list (list): A list of criteria for which preference questions will be generated.
        criteria_description (dict): Dictionary containing a description text (str) for every criteria from
            criteria_list.
    Returns:
        List[Question]: A list of Question objects representing preference questions.
    """
    answer_mapping_scale = {}
    consequence_description = "Die Zuweisung eines Gewichts hat Auswirkungen auf die Ergebnisse der Nutzen- und " \
                              "Aufwandsschätzung. Wenn Sie diesem Kriterium ein niedriges Gewicht zu, dann werden " \
                              "hohe Werte für dieses Kriterium bei der Endauswertung weniger berücksichtigt."
    reason_to_exist = "Die Gewichtung von Kriterien ist notwendig, um Ihre Perspektive und Voraussetzungen " \
                      "in die Auswertung zu integrieren. Das sorgt dafür, dass dieser Fragebogen von " \
                      "verschiedenen Akteuren aus dem Fernwärmenetzbetrieb genutzt werden kann."
    for i in range(min_weight, max_weight + 1):
        answer_mapping_scale[str(i)] = i
    question_list = [
        Question(name=criteria,
                 question_text=f"Wie wichtig ist das Kriterium {criteria} für Sie auf einer Skala von 1 bis 5? "
                               f"(5=sehr wichtig, 1=unwichtig)",
                 options=[str(number) for number in range(min_weight, max_weight + 1)],
                 answer_mapping=answer_mapping_scale,
                 multiple_choice=False,
                 question_types=["Preference"],
                 description_text=criteria_description[criteria],
                 consequence_description=consequence_description,
                 reason_to_exist=reason_to_exist) for criteria in criteria_list]
    return question_list
