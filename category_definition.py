
"""
Script for defining all categories and assigning use cases and questions.
This script initializes all possible categories which can be used in the questionnaire application
with their associated questions and use cases.

This script defines the categories:

preferences: Category for global criteria weighting questions.
general_questions: Category for questions which are important for most of the use case categories.
category_1: Use case category 1 (Wärmebedarfsprognose).
category_2: Use case category 2 (Instandhaltung Hausstationen).
category_3: Use case category 3 (Instandhaltung Rohrnetz).
category_4: Use case category 4 (Betriebsstrategien Wärmenetz).
category_5: Use case category 5 (Betriebsstrategien Hausstationen).
"""

from settings import preference_category_name, general_category_name
from category import Category
from question_definition import *
from use_case_definition import *

preferences = Category(name=preference_category_name, color="gray17",
                       default_questions=global_preference_questions, consequence_questions=[],
                       use_cases=[])

general_questions = Category(name=general_category_name, color="gray17",
                             default_questions=gen_default_questions,
                             consequence_questions=gen_consequence_questions,
                             use_cases=[])

category_1 = Category(name=category_names[0], color="#179c7d",
                      default_questions=cat_1_local_preference_questions + cat_1_default_questions,
                      consequence_questions=cat_1_consequence_questions,
                      use_cases=[c1_uc1, c1_uc2, c1_uc3, c1_uc4, c1_uc5, c1_uc6])

category_2 = Category(name=category_names[1], color="#005b7f",
                      default_questions=cat_2_local_preference_questions + cat_2_default_questions,
                      consequence_questions=cat_2_consequence_questions,
                      use_cases=[c2_uc1, c2_uc2, c2_uc3, c2_uc4])

category_3 = Category(name=category_names[2], color="#f58220",
                      default_questions=cat_3_local_preference_questions + cat_3_default_questions,
                      consequence_questions=cat_3_consequence_questions,
                      use_cases=[c3_uc1, c3_uc2, c3_uc3])

category_4 = Category(name=category_names[3], color="#964471",
                      default_questions=cat_4_local_preference_questions + cat_4_default_questions,
                      consequence_questions=cat_4_consequence_questions,
                      use_cases=[c4_uc1, c4_uc2, c4_uc3, c4_uc4])

category_5 = Category(name=category_names[4], color="#778c97",
                      default_questions=cat_5_local_preference_questions + cat_5_default_questions,
                      consequence_questions=cat_5_consequence_questions,
                      use_cases=[c5_uc1, c5_uc2])

category_dict = {category_names[0]: category_1,
                 category_names[1]: category_2,
                 category_names[2]: category_3,
                 category_names[3]: category_4,
                 category_names[4]: category_5
                 }
