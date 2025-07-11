"""
This module contains configuration constants and settings for the ML4FW questionnaire application.

It includes paths for data files, category definitions, criteria for evaluation, question types,
and introductory text for the questionnaire.

Attributes:
    base_path (str): The absolute path to the directory containing this script.
    result_directory_absolute_path (str): The absolute path to the directory where results will be stored.
    result_directory_relative_path (str): The relative path to the results directory.
    predefined_category_ranking_path (str): The absolute path to the CSV file containing predefined category rankings.
    category_names (List[str]): A list of names for the different categories of ML use cases.
    category_descriptions (Dict[str, str]): A dictionary mapping category names to their descriptions.
    short_category_names (Dict[str, str]): A dictionary mapping full category names to their short forms.
    risk_colors (Dict[int, str]): A dictionary mapping risk levels to their corresponding colors.
    global_criteria (List[str]): A list of criteria used to evaluate the ML use cases.
    global_criteria_description (Dict[str, str]): Contains a description text for every global criteria.
    global_criteria_mapping (Dict[str, List[str]]): A mapping of criteria types to their corresponding criteria.
    category_criteria (Dict[str, List[str]]): A mapping of category names to their specific criteria.
    category_criteria_description (Dict[Dict[str, str]]): Contains a description text for every local category criteria.
    local_effort_criteria (List[str]): A list of local effort criteria for evaluating ML use cases.
    question_types (set): A set defining the types of questions that can be asked.
    preference_category_name (str): The name of the category for personal weighting of criteria.
    general_category_name (str): The name of the category for cross-category questions.
    intro_text (str): The introductory text displayed to users at the beginning of the questionnaire.
    intro_explanation (str): Additional explanations to the questionnaire.
    preference_info_text (str): Additional information about preference selection and global weights.
    option_info (str): Additional info about the option selection.
    max_weight (int): The maximum weight value for criteria.
    min_weight (int): The minimum weight value for criteria.
    min_substations_for_clustering (int): The minimum number of substations required for clustering.
    max_pipeline_depth (int): The maximum depth for the pipeline, according to guidelines.
"""

import os

base_path = os.path.dirname(os.path.abspath(__file__))
result_directory_absolute_path = os.path.join(base_path, "ML4FW_Fragebogen_Ausgaben")
result_directory_relative_path = "./ML4FW_Fragebogen_Ausgaben"
predefined_category_ranking_path = os.path.join(base_path, "data", "Vordefiniertes_Kategorie_Ranking.csv")
category_names = ["Wärmebedarfsprognose", "Instandhaltung Hausstationen",
                  "Instandhaltung Rohrnetz", "Betriebsstrategien Wärmenetz",
                  "Betriebsstrategien Hausstationen"]
category_descriptions = {
    category_names[0]: "Umfasst ML-Use-Cases, welche sich auf Prognosen für Wärmebedarfe fokussieren.",
    category_names[1]: "Umfasst ML-Use-Cases, welche sich auf Aspekte der (prädiktiven) Instandhaltung von HAST \n"
                       "fokussieren. Ein möglicher Aspekt ist die automatisierte (frühzeitige) Fehlererkennung.",
    category_names[2]: "Umfasst ML-Use-Cases, welche sich auf Aspekte der (prädiktiven) Instandhaltung des \n"
                       "Rohrleitungsnetzes eines Fernwärmesystems fokussieren. Ein Beispiel für einen solchen \n"
                       "Aspekt ist die Erkennung von Leckagen.",
    category_names[3]: "Umfasst ML-Use-Cases mit dem Fokus auf Aspekten der Betriebsführung und Steuerung von \n"
                       "Wärmenetzen. Ein möglicher Aspekt ist die Spitzenlastreduktion.",
    category_names[4]: "Umfasst ML-Use-Cases, welche sich auf Aspekte aus dem Betrieb von Hausstationen \n"
                       "fokussieren. Ein möglicher Aspekt ist die automatischen Steuerung von HASTs."

}
short_category_names = {"Wärmebedarfsprognose": "WBP", "Instandhaltung Hausstationen": "InHAST",
                        "Instandhaltung Rohrnetz": "InRN", "Betriebsstrategien Wärmenetz": "BeWN",
                        "Betriebsstrategien Hausstationen": "BeHAST"}
risk_colors = {5: "#A52A2A", 4: "#D2691E", 3: "#FFA500", 2: "#FFD700", 1: "#F0FFFF"}
global_criteria = ["Kostenaufwand", "Zeitaufwand", "Personalaufwand", "Versorgungssicherheit",
                   "Umweltauswirkungen / Dekarbonisierung", "Energieeffizienz", "Automatisierungsgrad"]
global_criteria_description = {"Kostenaufwand": "Voraussichtlicher Aufwand in Form von Kosten für die gesamte Use Case "
                                                "Umsetzung (Teil von Aufwand).",
                               "Zeitaufwand": "Voraussichtlich benötigte Zeit für die Umsetzung möglicher Use Cases. "
                                              "Diese kann insbesondere durch notwendige Datenerhebungen stark "
                                              "anwachsen (Teil von Aufwand).",
                               "Personalaufwand": "Personelle Ressourcen, welche für die Use Case Umsetzung "
                                                  "voraussichtlich benötigt werden (Teil von Aufwand).",
                               "Versorgungssicherheit": "Potenzielle Größe des Beitrags eines Use Case zur "
                                                        "Versorgungssicherheit im Fernwärmenetz (Teil von Nutzen).",
                               "Umweltauswirkungen / Dekarbonisierung": "Potenzielle Größe des Beitrags eines Use Case "
                                                                        "zur Dekarbonisierung des "
                                                                        "Fernwärmenetzbetriebs (Teil von Nutzen).",
                               "Energieeffizienz": "Potenzielle Energieeffizienzsteigerung durch einen umgesetzten "
                                                   "Use Case (Teil von Nutzen).",
                               "Automatisierungsgrad": "Grad der Automatisierung eines Use Cases. Diese Größe ist "
                                                       "insbesondere für den kontinuierlichen Betrieb einer ML-Lösung "
                                                       "nach der ersten Umsetzung relevant (Teil von Nutzen)."
                               }
global_criteria_mapping = {"Effort": ["Kostenaufwand", "Zeitaufwand", "Personalaufwand"],
                           "Potential": ["Versorgungssicherheit", "Umweltauswirkungen / Dekarbonisierung",
                                         "Energieeffizienz", "Automatisierungsgrad"]}
category_criteria = {category_names[0]: ["Genauigkeit", "Interpretierbarkeit", "Kundenkomfort"],
                     category_names[1]: ["Fehlererkennung", "Identifikation von Ursachen", "Wenige Fehlalarme",
                                         "Fehlerfrüherkennung", "Interpretierbarkeit"],
                     category_names[2]: ["Erkennen von vorhandenen Leckagen", "Ortung von Leckagen",
                                         "Vorbeugung von Fehlern", "Wenige Fehlalarme", "Interpretierbarkeit"],
                     category_names[3]: ["Energieeffizienz", "Interpretierbarkeit", "Kundenkomfort"],
                     category_names[4]: ["Reduktion der Rücklauftemperatur", "Interpretierbarkeit",
                                         "Kundenkomfort"]
                     }
category_criteria_description = {category_names[0]: {"Genauigkeit": "Beschreibt wie gering der Vorhersagefehler"
                                                                    "bei der Wärmebedarfsprognose voraussichtlich sein "
                                                                    "wird.",
                                                     "Interpretierbarkeit": "Beschreibt die Interpretierbarkeit und "
                                                                            "Transparenz der erstellen Prognose. Es "
                                                                            "gibt ML-Ansätze, wie bspw. klassische "
                                                                            "neuronale Netze, welche als Black Box "
                                                                            "fungieren und damit nur schwer "
                                                                            "zu interpretieren sind. Andere Modelle, "
                                                                            "welche bereits mit Hinsicht auf "
                                                                            "Nachvollziehbarkeit erstellt wurden, "
                                                                            "benötigen dafür aber oftmals mehr Daten "
                                                                            "oder sind schwerer anzuwenden.",
                                                     "Kundenkomfort": "Beschreibt wie viel Wert auf explizite "
                                                                      "Berücksichtigung des Kundenkomforts bei der "
                                                                      "Erstellung von Wärmebedarfsprognosen gelegt "
                                                                      "wird."},
                                 category_names[1]: {"Fehlererkennung": "Beschreibt die Fähigkeit des ML-Modells "
                                                                        "vorhandene Fehler zu erkennen.",
                                                     "Identifikation von Ursachen": "Beschreibt die Fähigkeit des "
                                                                                    "ML-Modells Ursachen zu "
                                                                                    "detektierten Fehlern zu "
                                                                                    "identifizieren.",
                                                     "Wenige Fehlalarme": "Beschreibt wie gering die Fehlalarmrate "
                                                                          "des ML-Modells ist. Bei einem Fehlalarm gibt"
                                                                          "das ML-Modell an einen Fehler oder eine "
                                                                          "Anomalie detektiert zu haben, während sich "
                                                                          "das überwachte System im Normalzustand "
                                                                          "befindet.",
                                                     "Fehlerfrüherkennung": "Beschreibt die Fähigkeit des ML-Modells "
                                                                            "Fehler bereits in der Entstehung (d. h. "
                                                                            "bevor sie kritisch für den Betrieb "
                                                                            "werden) zu detektieren.",
                                                     "Interpretierbarkeit": "Beschreibt die Interpretierbarkeit und "
                                                                            "Transparenz der Modelle mit Hinsicht auf "
                                                                            "erkannte Fehler oder Anomalien. Es "
                                                                            "gibt ML-Ansätze, wie bspw. klassische "
                                                                            "Autoencoder, welche als Black Box "
                                                                            "fungieren und damit nicht ohne "
                                                                            "Zusatzaufwand interpretierbar sind. "
                                                                            "Andere Modelle, welche bereits mit "
                                                                            "Hinsicht auf Nachvollziehbarkeit "
                                                                            "erstellt wurden, benötigen dafür aber "
                                                                            "oftmals mehr Daten oder sind schwerer "
                                                                            "anzuwenden)."},
                                 category_names[2]: {"Erkennen von vorhandenen Leckagen": "Beschreibt die Fähigkeit "
                                                                                          "des ML-Modells "
                                                                                          "vorhandene Leckagen zu "
                                                                                          "erkennen.",
                                                     "Ortung von Leckagen": "Beschreibt die räumliche Genauigkeit der "
                                                                            "Lokalisierung von erkannten Leckagen "
                                                                            "im Rohleitungsnetz",
                                                     "Vorbeugung von Fehlern": "Beschreibt die Fähigkeit des "
                                                                               "ML-Modells Leckagen oder Schwachstellen"
                                                                               " in einem frühen Stadium zu erkennen, "
                                                                               "bevor diese kritisch für den Betrieb "
                                                                               "werden.",
                                                     "Wenige Fehlalarme": "Beschreibt wie gering die Fehlalarmrate "
                                                                          "des ML-Modells ist. Bei einem Fehlalarm gibt"
                                                                          "das ML-Modell an einen Fehler oder eine "
                                                                          "Anomalie detektiert zu haben, während sich "
                                                                          "das überwachte System im Normalzustand "
                                                                          "befindet.",
                                                     "Interpretierbarkeit": "Beschreibt die Interpretierbarkeit und "
                                                                            "Transparenz der Modelle mit Hinsicht auf "
                                                                            "erkannte Leckagen. Es "
                                                                            "gibt ML-Ansätze, welche als Black Box "
                                                                            "fungieren und nur schwer zu "
                                                                            "interpretieren sind. Andere Modelle, "
                                                                            "welche bereits mit Hinsicht auf "
                                                                            "Nachvollziehbarkeit erstellt wurden, "
                                                                            "benötigen dafür aber oftmals mehr Daten "
                                                                            "oder sind schwerer anzuwenden)."},
                                 category_names[3]: {"Energieeffizienz": "Beschreibt den potenziell positiven Einfluss "
                                                                         "des ML-Use-Cases auf die Energieeffizienz "
                                                                         "des Wärmenetzes",
                                                     "Interpretierbarkeit": "Beschreibt die Interpretierbarkeit und "
                                                                            "Transparenz der Modelle mit Hinsicht auf "
                                                                            "die getroffenen Entscheidungen. Es "
                                                                            "gibt ML-Ansätze, welche als Black Box "
                                                                            "fungieren und nur schwer zu "
                                                                            "interpretieren sind. Andere Modelle, "
                                                                            "welche bereits mit Hinsicht auf "
                                                                            "Nachvollziehbarkeit erstellt wurden, "
                                                                            "benötigen dafür aber oftmals mehr Daten "
                                                                            "oder sind schwerer anzuwenden).",
                                                     "Kundenkomfort": "Beschreibt zu welchem Grad Kundenkomfort bei "
                                                                      "der Erstellung von Netzbetriebsstrategien "
                                                                      "berücksichtigt wird."},
                                 category_names[4]: {"Reduktion der Rücklauftemperatur": "Beschreibt den potenziell "
                                                                                         "positiven Einfluss des "
                                                                                         "ML Use Cases auf die Senkung "
                                                                                         "der Rücklauftemperatur der "
                                                                                         "HAST.",
                                                     "Interpretierbarkeit": "Beschreibt die Interpretierbarkeit und "
                                                                            "Transparenz der Modelle mit Hinsicht auf "
                                                                            "die getroffenen Entscheidungen. Es "
                                                                            "gibt ML-Ansätze, welche als Black Box "
                                                                            "fungieren und nur schwer zu "
                                                                            "interpretieren sind. Andere Modelle, "
                                                                            "welche bereits mit Hinsicht auf "
                                                                            "Nachvollziehbarkeit erstellt wurden, "
                                                                            "benötigen dafür aber oftmals mehr Daten "
                                                                            "oder sind schwerer anzuwenden).",
                                                     "Kundenkomfort": "Beschreibt zu welchem Grad Kundenkomfort bei "
                                                                      "der Erstellung von HAST-Betriebsstrategien "
                                                                      "berücksichtigt wird."}
                                 }
local_effort_criteria = ["Datenaufbewahrungsaufwand",
                         "Kontinuierlicher Aufwand",
                         "Rechenaufwand",
                         "Sensorinstallationsaufwand",
                         "Implementationsaufwand",
                         "Datenerhebungsaufwand",  # Mainly for sensor data
                         "Metadatenerhebungsaufwand"  # Including service reports
                         ]
question_types = {"Preference", "Specification", "Potential", "Effort", "Risk"}
preference_category_name = "Persönliche Gewichtung von Bewertungskriterien"
general_category_name = "Kategorieübergreifende Fragen"

with open("./data/Intro_Text.txt", "r", encoding='utf-8') as file:
    intro_text = file.read()

with open("./data/Intro_Erklärung.txt", "r", encoding='utf-8') as file:
    intro_explanation = file.read()

with open("./data/Gewichtung_Info.txt", "r", encoding='utf-8') as file:
    preference_info_text = file.read()

with open("./data/Kategorieauswahl_Info.txt", "r", encoding='utf-8') as file:
    option_info = file.read()

max_weight = 5
min_weight = 1

# Self introduced parameters:
min_substations_for_clustering = 30
max_pipeline_depth = 2  # According to https://www.iea-dhc.org/fileadmin/documents/Annex_IV/aiv4.pdf
