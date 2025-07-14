"""
Script for defining all questions related to ML use cases in a questionnaire format.
This script sets the question texts, answers, question types, and organizes questions according to their respective
categories.
"""

from settings import category_names, global_criteria, category_criteria, min_substations_for_clustering, \
    max_pipeline_depth, category_descriptions, global_criteria_description, category_criteria_description
from question import Question, generate_preference_questions


init_question = Question(name="Init",
                         question_text="Bitte wählen Sie mindestens eine der folgenden 5 ML-Use-Case-Kategorien. Es "
                                       "ist auch möglich mehrere auszuwählen.",
                         options=[key + ":\n" + value for key, value in category_descriptions.items()],
                         multiple_choice=True,
                         question_types=["Preference"],
                         description_text="",
                         consequence_description="",
                         reason_to_exist=""
                         )

# General questions
gen_digital_data = Question(name="Digitalisierte Daten",
                            question_text="Wie halten Sie Ihre Daten hauptsächlich?",
                            options=["Die Daten liegen hauptsächlich in digitalisierter Form vor.",
                                     "Die Daten liegen hauptsächlich in Form von Dokumenten vor."],
                            multiple_choice=False,
                            question_types=["Effort"],
                            answer_mapping={"Die Daten liegen hauptsächlich in digitalisierter Form vor.": 1,
                                            "Die Daten liegen hauptsächlich in Form von Dokumenten vor.": 5},
                            consequence_triggers={"Die Daten liegen hauptsächlich in digitalisierter "
                                                  "Form vor.": "Datenaufbewahrung"},
                            criteria="Datenaufbewahrungsaufwand",
                            description_text="Diese Frage soll Ihre Datenhaltungssituation grob erfassen. Dabei "
                                             "wird auf eine detaillierte Aufschlüsselung dieser Frage auf mehrere "
                                             "Datenquellen und Datentypen verzichtet, da dies die Anzahl der Fragen "
                                             "und damit die Bearbeitungszeit des Fragebogens deutlich erhöhen würde "
                                             "und die daraus gewonnen Erkenntnisse nicht im Verhältnis dazu stehen.",
                            consequence_description="Wenn Ihre Daten nicht in digitalisierter Form vorliegen, "
                                                    "steigt der Aufwand bei der Umsetzung von ML Use Cases. "
                                                    "Insbesondere Use Cases mit einem hohen Datenaufbewahrungsaufwand"
                                                    "werden einen höheren Aufwandswert erhalten. \n"
                                                    "Falls Ihre Daten hauptsächlich in digitalisierter Form vorliegen "
                                                    "wird Ihnen eine Folgefrage zur Datenaufbewahrung gestellt. Falls "
                                                    "nicht steigt der Datenaufbewahrungsaufwand deutlich.",
                            reason_to_exist="Diese Frage wird gestellt, um den Aufwand bei der Datenaufbewahrung für "
                                            "die Umsetzung von ML Use Cases zu schätzen."
                            )
gen_data_storage = Question(name="Datenaufbewahrung",
                            question_text="Wie speichern Sie Ihre Daten?",
                            options=["Die Daten liegen in einer oder mehreren Datenbanken vor.",
                                     "Die Daten liegen als Sammlung von Dateien vor."],
                            multiple_choice=False,
                            question_types=["Effort"],
                            answer_mapping={"Die Daten liegen in einer oder mehreren Datenbanken vor.": 1,
                                            "Die Daten liegen als Sammlung von Dateien vor.": 5},
                            criteria="Datenaufbewahrungsaufwand",
                            description_text="Diese Frage soll Ihre Datenhaltungssituation erfassen.",
                            consequence_description="Wenn Ihre Daten nicht in Datenbanken vorliegen "
                                                    "steigt der Aufwand bei der Umsetzung von ML Use Cases. "
                                                    "Insbesondere Use Cases mit einem hohen Datenaufbewahrungsaufwand"
                                                    "werden einen höheren Aufwandswert erhalten.",
                            reason_to_exist="Diese Frage wird gestellt, um den Aufwand bei der Datenaufbewahrung für "
                                            "die Umsetzung von ML Use Cases zu schätzen."
                            )
gen_data_history = Question(name="Historienlänge",
                            question_text="Wie weit reicht Ihre Datenhistorie zurück?",
                            options=["Mehr als 1 Jahr", "Etwa ein Jahr", "Einige Monate",
                                     "Es gibt keine historisch aufgezeichneten Daten."],
                            multiple_choice=False,
                            question_types=["Specification"],
                            description_text="Diese Frage soll die Menge Ihrer Daten grob erfassen. Dabei "
                                             "wird auf eine detaillierte Aufschlüsselung dieser Frage auf mehrere "
                                             "Datenquellen und Datentypen verzichtet, da dies die Anzahl der Fragen "
                                             "und damit die Bearbeitungszeit des Fragebogens deutlich erhöhen würde "
                                             "und die daraus gewonnen Erkenntnisse nicht im Verhältnis dazu stehen.",
                            consequence_description="Einige ML Use Cases benötigen lange Datenhistorien während andere"
                                                    "auch mit kürzeren Historien auskommen können. Kurze "
                                                    "Datenhistorien können zum Ausschluss einiger Use Cases führen.",
                            reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases."
                            )
gen_data_resolution = Question(name="Datenauflösung",
                               question_text="Wie hoch ist die zeitliche Auflösung Ihrer Daten im Durchschnitt?",
                               options=["Sekündlich oder höher", "Minütlich", "Stündlich",
                                        "Täglich oder niedriger"],
                               multiple_choice=False,
                               question_types=["Specification"],
                               description_text="Diese Frage soll die Auflösung Ihrer Daten grob erfassen. Dabei "
                                                "wird auf eine detaillierte Aufschlüsselung dieser Frage auf mehrere "
                                                "Datenquellen und Datentypen verzichtet, da dies die Anzahl der Fragen "
                                                "und damit die Bearbeitungszeit des Fragebogens deutlich erhöhen würde "
                                                "und die daraus gewonnen Erkenntnisse nicht im Verhältnis dazu stehen.",
                               consequence_description="Einige ML Use Cases benötigen hohe Datenauflösungen während "
                                                       "andere auch mit niedrigen Datenauflösungen auskommen können. "
                                                       "Niedrigen Datenauflösungen können zum Ausschluss einiger Use "
                                                       "Cases führen.",
                               reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases."
                               )
gen_continual_operation = Question(name="Kontinuierlicher Betrieb",
                                   question_text="Ist es Ihnen wichtig, ML-Use-Cases nach der Umsetzung kontinuierlich "
                                                 "weiterzubetreiben?",
                                   options=["Ja", "Nein"],
                                   multiple_choice=False,
                                   question_types=["Effort"],
                                   answer_mapping={"Ja": 5, "Nein": 1},
                                   criteria="Kontinuierlicher Aufwand",
                                   description_text="Die Frage nach dem kontinuierlichen Betrieb dient der "
                                                    "Einschätzung des Aufwands nach der initialen Umsetzung des Use "
                                                    "Cases. Besonders Use Cases mit einem hohen Automatisierungsgrad"
                                                    "haben einen geringen kontinuierlichen Aufwand, während andere "
                                                    "höhere Aufwände haben können.",
                                   consequence_description="Falls diese Frage mit 'Ja' beantwortet wird, steigt der "
                                                           "Aufwand für die Umsetzung von ML Use Cases. Insbesondere"
                                                           "Use Cases mit einem hohen Automatisierungsgrad werden nur"
                                                           "einen geringfügig höheren Aufwand erhalten.",
                                   reason_to_exist="Diese Frage wird gestellt, um zu erfassen ob der kontinuierliche"
                                                   "Aufwand der ML Use Cases in den Gesamtaufwand eingerechnet werden "
                                                   "muss oder nicht.")

data_1_description = " sind notwendig für die Umsetzung einiger ML Use Cases."
data_1_consequence = "Falls Sie mit 'Nein' auf diese Frage antworten, wird Ihnen eine Folgefrage zur " \
                     "Erhebung dieser Daten gestellt. Zudem steigt der Datenerhebungsaufwand für ML Use Cases, " \
                     "welche diese Datenquelle benötigen."
data_1_reason_to_exist = "Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases und Einschätzung des " \
                         "Datenerhebungsaufwands."
data_2_description = "Falls Sie alternativ zu Sensorik andere Möglichkeiten haben, diese Daten zu erfassen, können " \
                     "Sie diese Frage auch mit 'Ja' beantworten."
data_2_consequence = "Falls Sie mit 'Nein' auf diese Frage antworten, wird Ihnen eine Folgefrage zur Datenerhebung " \
                     "gestellt. Falls Sie mit 'Ja' antworten steigt der Sensorinstallationsaufwand für Use Cases " \
                     "welche diese Daten benötigen."
data_2_reason_to_exist = "Die Frage nach Sensorik wird gestellt, um die grundsätzliche Möglichkeit zur Erfassung der " \
                         "Daten abzufragen und den Sensorinstallationsaufwand abzuschätzen."
data_3_description = "Diese Frage wird als letzte Frage der Ausschlusskette für ML Use Cases gestellt, welche diese" \
                     "Daten benötigen."
data_3_consequence = "Falls Sie nicht dazu bereit sind diese Daten zu erheben, werden Use Cases von der Bewertung " \
                     "ausgeschlossen, welche diese benötigen. Für alle anderen Use Cases bleibt der Aufwand " \
                     "unverändert. Falls Sie mit 'Ja' antworten steigt der Aufwand für Use Cases welche diese " \
                     "Daten benötigen deutlich, da weder bereits aufgezeichnete Daten, noch Sensorik zum Erfassen " \
                     "vorhanden sind."
data_3_reason_to_exist = "Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases."
gen_ambient_temp_1 = Question(name="Außentemperaturdaten",
                              question_text="Haben Sie Zugriff auf standortspezifische Außentemperaturdaten?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Effort"],
                              answer_mapping={"Ja": 1, "Nein": 5},
                              consequence_triggers={"Nein": "Außentemperaturdaten Sensoren"},
                              criteria="Datenerhebungsaufwand",
                              description_text="Außentemperaturdaten " + data_1_description,
                              consequence_description=data_1_consequence,
                              reason_to_exist=data_1_reason_to_exist
                              )
gen_ambient_temp_2 = Question(name="Außentemperaturdaten Sensoren",
                              question_text="Verfügen Sie über die notwendige Sensorik, um standortspezifische "
                                            "Außentemperaturdaten zu erheben?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Effort", "Risk"],
                              answer_mapping={"Ja": 1, "Nein": 5},
                              consequence_triggers={"Nein": "Außentemperaturdaten erheben"},
                              criteria="Sensorinstallationsaufwand",
                              description_text=data_2_description,
                              consequence_description=data_2_consequence,
                              reason_to_exist=data_2_reason_to_exist
                              )
gen_ambient_temp_3 = Question(name="Außentemperaturdaten erheben",
                              question_text="Würden Sie Außentemperaturdaten erheben, um einen ML-Use-Case "
                                            "realisieren zu können?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Specification"],
                              description_text=data_3_description,
                              consequence_description=data_3_consequence,
                              reason_to_exist=data_3_reason_to_exist
                              )
gen_weather_forecast_1 = Question(name="Wettervorhersage verfügbar",
                                  question_text="Haben Sie Zugriff auf Daten aus standortspezifischen "
                                                "Wettervorhersagen?",
                                  options=["Ja", "Nein"],
                                  multiple_choice=False,
                                  question_types=["Effort"],
                                  answer_mapping={"Ja": 1, "Nein": 5},
                                  consequence_triggers={"Nein": "Wettervorhersage erheben"},
                                  criteria="Datenerhebungsaufwand",
                                  description_text="Daten aus standortspezifischen "
                                                   "Wettervorhersagen " + data_1_description,
                                  consequence_description=data_1_consequence,
                                  reason_to_exist=data_1_reason_to_exist
                                  )
gen_weather_forecast_2 = Question(name="Wettervorhersage erheben",
                                  question_text="Würden Sie Daten aus standortspezifischen Wettervorhersagen erheben, "
                                                "um einen ML-Use-Case zu ermöglichen?",
                                  options=["Ja", "Nein"],
                                  multiple_choice=False,
                                  question_types=["Specification"],
                                  description_text=data_3_description,
                                  consequence_description=data_3_consequence,
                                  reason_to_exist="Falls Sie nicht dazu bereit sind diese Daten zu erheben, werden "
                                                  "Use Cases von der Bewertung ausgeschlossen, welche diese benötigen. "
                                                  "Für alle anderen Use Cases bleibt der Aufwand unverändert. Falls "
                                                  "Sie mit 'Ja' antworten steigt der Datenerhebungsaufwand für Use "
                                                  "Cases welche diese Daten benötigen."
                                  )
gen_flow_rate_1 = Question(name="Durchflussvolumen verfügbar",
                           question_text="Haben Sie Zugriff auf kontinuierliche Daten zu Durchflussvolumen im "
                                         "Fernwärmenetz?",
                           options=["Ja", "Nein"],
                           multiple_choice=False,
                           question_types=["Effort"],
                           consequence_triggers={"Nein": "Durchflussvolumen Sensoren"},
                           answer_mapping={"Ja": 1, "Nein": 5},
                           criteria="Datenerhebungsaufwand",
                           description_text="Daten zu Durchflussvolumen " + data_1_description,
                           consequence_description=data_1_consequence,
                           reason_to_exist=data_1_reason_to_exist
                           )
gen_flow_rate_2 = Question(name="Durchflussvolumen Sensoren",
                           question_text="Verfügen Sie über die notwendige Sensorik, um Daten zu "
                                         "Durchflussvolumen zu erheben",
                           options=["Ja", "Nein"],
                           multiple_choice=False,
                           question_types=["Effort", "Risk"],
                           answer_mapping={"Ja": 1, "Nein": 5},
                           criteria="Sensorinstallationsaufwand",
                           consequence_triggers={"Nein": "Durchflussvolumen erheben"},
                           description_text=data_2_description,
                           consequence_description=data_2_consequence,
                           reason_to_exist=data_2_reason_to_exist
                           )
gen_flow_rate_3 = Question(name="Durchflussvolumen erheben",
                           question_text="Würden Sie Daten zu Durchflussvolumen erheben, um ML-Use-Cases zu "
                                         "ermöglichen?",
                           options=["Ja", "Nein"],
                           multiple_choice=False,
                           question_types=["Specification"],
                           description_text=data_3_description,
                           consequence_description=data_3_consequence,
                           reason_to_exist=data_3_reason_to_exist
                           )
gen_supply_and_return_temperature_1 = Question(name="Temperaturdaten verfügbar",
                                               question_text="Haben Sie Zugriff auf kontinuierliche Daten zu Vor- und "
                                                             "Rücklauftemperaturen im Fernwärmenetz?",
                                               options=["Ja", "Nein"],
                                               multiple_choice=False,
                                               question_types=["Effort"],
                                               consequence_triggers={"Nein": "Temperaturdaten Sensoren"},
                                               answer_mapping={"Ja": 5, "Nein": 1},
                                               criteria="Datenerhebungsaufwand",
                                               description_text="Daten zu Vor- und "
                                                                "Rücklauftemperaturen" + data_1_description,
                                               consequence_description=data_1_consequence,
                                               reason_to_exist=data_1_reason_to_exist
                                               )
gen_supply_and_return_temperature_2 = Question(name="Temperaturdaten Sensoren",
                                               question_text="Verfügen Sie über die notwendige Sensorik, um Vor- und "
                                                             "Rücklauftemperaturen zu messen?",
                                               options=["Ja", "Nein"],
                                               multiple_choice=False,
                                               question_types=["Effort", "Risk"],
                                               answer_mapping={"Ja": 1, "Nein": 5},
                                               criteria="Sensorinstallationsaufwand",
                                               consequence_triggers={"Nein": "Temperaturdaten erheben"},
                                               description_text=data_2_description,
                                               consequence_description=data_2_consequence,
                                               reason_to_exist=data_2_reason_to_exist
                                               )
gen_supply_and_return_temperature_3 = Question(name="Temperaturdaten erheben",
                                               question_text="Würden Sie Vor- und Rücklauftemperaturdaten erheben, um "
                                                             "einen ML-Use-Case zu ermöglichen?",
                                               options=["Ja", "Nein"],
                                               multiple_choice=False,
                                               question_types=["Specification"],
                                               description_text=data_3_description,
                                               consequence_description=data_3_consequence,
                                               reason_to_exist=data_3_reason_to_exist
                                               )
gen_network_temperature_1 = Question(name="Temperaturdaten Netz",
                                     question_text="Verfügen Sie über Daten zu Temperaturen an "
                                                   "mehreren Stellen im Fernwärmenetz?",
                                     options=["Ja", "Nein"],
                                     multiple_choice=False,
                                     question_types=["Effort"],
                                     consequence_triggers={"Nein": "Temperaturdaten Netz Sensoren"},
                                     answer_mapping={"Ja": 5, "Nein": 1},
                                     criteria="Datenerhebungsaufwand",
                                     description_text="Netztemperaturdaten" + data_1_description,
                                     consequence_description=data_1_consequence,
                                     reason_to_exist=data_1_reason_to_exist
                                     )
gen_network_temperature_2 = Question(name="Temperaturdaten Netz Sensoren",
                                     question_text="Verfügen Sie über die notwendige Sensorik, um "
                                                   "Temperaturen an mehreren Stellen im Fernwärmenetz "
                                                   "zu messen?",
                                     options=["Ja", "Nein"],
                                     multiple_choice=False,
                                     question_types=["Effort", "Risk"],
                                     answer_mapping={"Ja": 1, "Nein": 5},
                                     criteria="Sensorinstallationsaufwand",
                                     consequence_triggers={"Nein": "Temperaturdaten Netz erheben"},
                                     description_text=data_2_description,
                                     consequence_description=data_2_consequence,
                                     reason_to_exist=data_2_reason_to_exist
                                     )
gen_network_temperature_3 = Question(name="Temperaturdaten Netz erheben",
                                     question_text="Würden Sie Daten zu Temperaturen an "
                                                   "mehreren Stellen im Fernwärmenetz erheben, um einen ML-Use-Case zu "
                                                   "ermöglichen?",
                                     options=["Ja", "Nein"],
                                     multiple_choice=False,
                                     question_types=["Specification"],
                                     description_text=data_3_description,
                                     consequence_description=data_3_consequence,
                                     reason_to_exist=data_3_reason_to_exist
                                     )
gen_energy_1 = Question(name="Energiedaten verfügbar",
                        question_text="Haben Sie Zugriff auf kontinuierliche Energieverbrauchsdaten von "
                                      "Hausstationen?",
                        options=["Ja", "Nein"],
                        multiple_choice=False,
                        question_types=["Effort"],
                        consequence_triggers={"Nein": "Energiedaten Sensoren"},
                        answer_mapping={"Ja": 1, "Nein": 5},
                        criteria="Datenerhebungsaufwand",
                        description_text="Energieverbrauchsdaten" + data_1_description,
                        consequence_description=data_1_consequence,
                        reason_to_exist=data_1_reason_to_exist
                        )
gen_energy_2 = Question(name="Energiedaten Sensoren",
                        question_text="Verfügen Sie über die notwendige Sensorik, um Energieverbrauchsdaten von "
                                      "Hausstationen zu "
                                      "erheben?",
                        options=["Ja", "Nein"],
                        multiple_choice=False,
                        question_types=["Effort", "Risk"],
                        answer_mapping={"Ja": 1, "Nein": 5},
                        criteria="Sensorinstallationsaufwand",
                        consequence_triggers={"Nein": "Energiedaten erheben"},
                        description_text=data_2_description,
                        consequence_description=data_2_consequence,
                        reason_to_exist=data_2_reason_to_exist
                        )
gen_energy_3 = Question(name="Energiedaten erheben",
                        question_text="Würden Sie Energieverbrauchsdaten von "
                                      "Hausstationen erheben, um einen ML-Use-Case zu "
                                      "ermöglichen?",
                        options=["Ja", "Nein"],
                        multiple_choice=False,
                        question_types=["Specification"],
                        description_text=data_3_description,
                        consequence_description=data_3_consequence,
                        reason_to_exist=data_3_reason_to_exist
                        )

gen_heat_1 = Question(name="Wärmeleistungsdaten verfügbar",
                      question_text="Haben Sie Zugriff auf kontinuierliche Wärmeleistungsdaten von "
                                    "Hausstationen?",
                      options=["Ja", "Nein"],
                      multiple_choice=False,
                      question_types=["Effort"],
                      consequence_triggers={"Nein": "Wärmeleistungsdaten Sensoren"},
                      answer_mapping={"Ja": 1, "Nein": 5},
                      criteria="Datenerhebungsaufwand",
                      description_text="Wärmeleistungsdaten" + data_1_description,
                      consequence_description=data_1_consequence,
                      reason_to_exist=data_1_reason_to_exist
                      )
gen_heat_2 = Question(name="Wärmeleistungsdaten Sensoren",
                      question_text="Verfügen Sie über die notwendige Sensorik, um Wärmeleistungsdaten von "
                                    "Hausstationen zu erheben?",
                      options=["Ja", "Nein"],
                      multiple_choice=False,
                      question_types=["Effort", "Risk"],
                      answer_mapping={"Ja": 1, "Nein": 5},
                      criteria="Sensorinstallationsaufwand",
                      consequence_triggers={"Nein": "Wärmeleistungsdaten erheben"},
                      description_text=data_2_description,
                      consequence_description=data_2_consequence,
                      reason_to_exist=data_2_reason_to_exist
                      )
gen_heat_3 = Question(name="Wärmeleistungsdaten erheben",
                      question_text="Würden Sie Wärmeleistungsdaten von "
                                    "Hausstationen erheben, um einen ML-Use-Case zu "
                                    "ermöglichen?",
                      options=["Ja", "Nein"],
                      multiple_choice=False,
                      question_types=["Specification"],
                      description_text=data_3_description,
                      consequence_description=data_3_consequence,
                      reason_to_exist=data_3_reason_to_exist
                      )
gen_pressure_1 = Question(name="Druckdaten verfügbar",
                          question_text="Haben Sie Zugriff auf kontinuierliche Daten zum Betriebsdruck im "
                                        "Fernwärmenetz?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Effort"],
                          consequence_triggers={"Nein": "Druckdaten Sensoren"},
                          answer_mapping={"Ja": 1, "Nein": 5},
                          criteria="Datenerhebungsaufwand",
                          description_text="Daten zum Betriebsdruck im Fernwärmenetz" + data_1_description,
                          consequence_description=data_1_consequence,
                          reason_to_exist=data_1_reason_to_exist
                          )
gen_pressure_2 = Question(name="Druckdaten Sensoren",
                          question_text="Verfügen Sie über die notwendige Sensorik, um Daten zum Betriebsdruck "
                                        "im Fernwärmenetz zu erheben?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Effort", "Risk"],
                          answer_mapping={"Ja": 1, "Nein": 5},
                          criteria="Sensorinstallationsaufwand",
                          consequence_triggers={"Nein": "Druckdaten erheben"},
                          description_text=data_2_description,
                          consequence_description=data_2_consequence,
                          reason_to_exist=data_2_reason_to_exist
                          )
gen_pressure_3 = Question(name="Druckdaten erheben",
                          question_text="Würden Sie Daten zum Betriebsdruck im Fernwärmenetz erheben, um einen "
                                        "ML-Use-Case zu ermöglichen?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Specification"],
                          description_text=data_3_description,
                          consequence_description=data_3_consequence,
                          reason_to_exist=data_3_reason_to_exist
                          )
gen_default_questions = [gen_digital_data, gen_data_history, gen_data_resolution, gen_continual_operation,
                         gen_ambient_temp_1, gen_flow_rate_1, gen_supply_and_return_temperature_1,
                         gen_network_temperature_1, gen_energy_1,
                         gen_heat_1, gen_pressure_1, gen_weather_forecast_1]
gen_consequence_questions = [gen_data_storage, gen_ambient_temp_2, gen_ambient_temp_3, gen_flow_rate_2,
                             gen_flow_rate_3, gen_supply_and_return_temperature_2, gen_supply_and_return_temperature_2,
                             gen_supply_and_return_temperature_3, gen_network_temperature_2,
                             gen_network_temperature_3, gen_energy_2, gen_energy_3, gen_heat_2, gen_heat_3,
                             gen_pressure_2, gen_pressure_3, gen_weather_forecast_2]

# category 1 questions
global_preference_questions = generate_preference_questions(criteria_list=global_criteria,
                                                            criteria_description=global_criteria_description)

# category 1 questions
category_name = category_names[0]
cat_1_local_preference_questions = generate_preference_questions(criteria_list=category_criteria[category_name],
                                                                 criteria_description=category_criteria_description[
                                                                     category_name])
risk_1_description = "Diese Frage dient zur Einschätzung, ob die Frage nach Nutzungsrechten"\
                    "für Daten bereits geklärt ist. Falls Sie nicht definitiv wissen, dass "\
                    "Sie die notwendigen Nutzungsrechte an den Daten haben, antworten Sie "\
                    "mit 'Nein'."
risk_2_description = "Diese Frage dient zur Einschätzung, ob gegenüber einer anderen Partei verpflichtet sind"\
                    "Ihren Umgang mit Daten transparent zu gestalten und offen zu legen. Falls Sie nicht definitiv " \
                     "wissen, dass dies nicht notwendigen ist antworten Sie mit 'Ja'."
risk_3_description = "Auch wenn das Nutzungsrecht für die Daten geklärt ist, kann es zu Widerständen gegen die " \
                     "Einführung von ML Use Cases kommen. Dabei kann es sich im unternehmensinterne Widerstände" \
                     "von Mitarbeitern oder dem Management handeln oder um externe Widerstände, wie beispielsweise " \
                     "von Verbrauchern. Ein Beispiel für einen solchen Widerstand ist die fehlende " \
                     "Nutzungsbereitschaft für die ML-Lösung. Bitte schätzen Sie für diese Frage ein, ob Sie von " \
                     "Widerständen bei der Umsetzung ausgehen oder eher nicht."
risk_4_description = "Vertraulichkeit von Daten nach der DSGVO bedeutet, dass personenbezogene Daten so verarbeitet " \
                     "werden müssen, dass sie vor unbefugtem Zugriff, unrechtmäßiger Verarbeitung, Offenlegung, " \
                     "Veränderung oder Löschung geschützt sind. Nur Personen, die ausdrücklich dazu berechtigt sind, " \
                     "dürfen auf diese Daten zugreifen oder sie bearbeiten."
cat_1_access_rights = Question(name="Zugriffsrechte",
                               question_text="Haben Sie die notwendigen Rechte, um Wärmeverbrauchsdaten sammeln und "
                                             "analysieren zu können?",
                               options=["Ja", "Nein"],
                               multiple_choice=False,
                               question_types=["Risk"],
                               answer_mapping={"Ja": 1, "Nein": 5},
                               description_text=risk_1_description,
                               consequence_description="Wenn diese Frage mit 'Nein' beantwortet wird, steigt das "
                                                       "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                       "Wärmebedarfsprognosen",
                               reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                               "der Kategorie 'Wärmebedarfsprognosen' einschätzen zu können."
                               )
cat_1_transparency = Question(name="Transparenz",
                              question_text="Haben Sie Verpflichtungen, den Umgang mit Wärmeverbrauchsdaten "
                                            "transparent offenzulegen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_2_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                      "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                      "Wärmebedarfsprognosen",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                              "der Kategorie 'Wärmebedarfsprognosen' einschätzen zu können."
                              )
cat_1_resistance = Question(name="Widerstand",
                            question_text="Erwarten Sie Widerstand gegen die Einführung von ML-Lösungen zur "
                                          "Prognose von Wärmebedarfen?",
                            options=["Ja", "Nein"],
                            multiple_choice=False,
                            question_types=["Risk"],
                            answer_mapping={"Ja": 5, "Nein": 1},
                            description_text=risk_3_description,
                            consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                    "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                    "Wärmebedarfsprognosen",
                            reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                            "der Kategorie 'Wärmebedarfsprognosen' einschätzen zu können."
                            )
cat_1_confidential = Question(name="Vertraulichkeit",
                              question_text="Sind die Ihnen zur Verfügung stehenden Daten oder Teile davon "
                                            "vertraulich nach DSGVO?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_4_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                      "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                      "Wärmebedarfsprognosen",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                              "der Kategorie 'Wärmebedarfsprognosen' einschätzen zu können."
                              )
cat_1_valve_data_1 = Question(name="Ventilzustände verfügbar",
                              question_text="Haben Sie Zugriff auf Daten zu Ventilzuständen "
                                            "im Fernwärmenetz?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Effort"],
                              consequence_triggers={"Nein": "Ventilzustände erheben"},
                              answer_mapping={"Ja": 1, "Nein": 5},
                              criteria="Datenerhebungsaufwand",
                              description_text="Daten zu Ventilzuständen" + data_1_description,
                              consequence_description=data_1_consequence,
                              reason_to_exist=data_1_reason_to_exist
                              )
cat_1_valve_data_2 = Question(name="Ventilzustände erheben",
                              question_text="Würden Sie Daten zu Ventilzuständen erheben, um einen ML-Use-Case "
                                            "zu ermöglichen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Specification"],
                              description_text=data_3_description,
                              consequence_description=data_3_consequence,
                              reason_to_exist="Falls Sie nicht dazu bereit sind diese Daten zu erheben, werden "
                                              "Use Cases von der Bewertung ausgeschlossen, welche diese benötigen. "
                                              "Für alle anderen Use Cases bleibt der Aufwand unverändert. Falls "
                                              "Sie mit 'Ja' antworten steigt der Datenerhebungsaufwand für Use "
                                              "Cases welche diese Daten benötigen."
                              )
cat_1_building_data = Question(name="Detaildaten Gebäude",
                               question_text="Haben Sie Zugriff aktuelle Daten zu den ans Fernwärmenetz "
                                             "angeschlossenen Gebäuden? Beispiele dafür sind: Baujahr, Gebäudetyp,...",
                               options=["Ja", "Nein"],
                               multiple_choice=False,
                               question_types=["Specification"],
                               description_text="ML Use Cases für Wärmebedarfsprognosen können aktuelle "
                                                "Metadaten zu Gebäuden benötigen, welche an das Fernwärmenetz "
                                                "angeschlossen sind. Da eine detaillierte Abfrage der einzelnen "
                                                "Merkmale die Komplexität zu stark erhöhen würde, werden diese hier"
                                                "gesammelt abgefragt.",
                               consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use Cases,"
                                                       "welche diese Daten benötigen nicht angewandt werden und "
                                                       "werden deswegen nicht weiter bewertet.",
                               reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases."
                               )

cat_1_heat_storages_data_1 = Question(name="Wärmespeicherdaten",
                                      question_text="Haben Sie Zugriff auf Daten von Wärmespeichern innerhalb des "
                                                    "Fernwärmenetzes?",
                                      options=["Ja", "Nein"],
                                      multiple_choice=False,
                                      question_types=["Effort"],
                                      consequence_triggers={"Nein": "Wärmespeicherdaten erheben"},
                                      answer_mapping={"Ja": 1, "Nein": 5},
                                      criteria="Datenerhebungsaufwand",
                                      description_text="Daten von Wärmespeichern" + data_1_description,
                                      consequence_description=data_1_consequence,
                                      reason_to_exist=data_1_reason_to_exist
                                      )
cat_1_heat_storages_data_2 = Question(name="Wärmespeicherdaten erheben",
                                      question_text="Würden Sie Wärmespeicherdaten erheben, um einen ML-Use-Case "
                                                    "zu ermöglichen?",
                                      options=["Ja", "Nein"],
                                      multiple_choice=False,
                                      question_types=["Specification"],
                                      description_text=data_3_description,
                                      consequence_description=data_3_consequence,
                                      reason_to_exist="Falls Sie nicht dazu bereit sind diese Daten zu erheben, werden "
                                                      "Use Cases von der Bewertung ausgeschlossen, welche diese "
                                                      "benötigen. Für alle anderen Use Cases bleibt der Aufwand "
                                                      "unverändert. Falls Sie mit 'Ja' antworten steigt der "
                                                      "Datenerhebungsaufwand für Use Cases welche diese Daten "
                                                      "benötigen."
                                      )

cat_1_default_questions = [cat_1_access_rights, cat_1_transparency, cat_1_resistance, cat_1_confidential,
                           cat_1_valve_data_1, cat_1_building_data, cat_1_heat_storages_data_1]
cat_1_consequence_questions = [cat_1_valve_data_2, cat_1_heat_storages_data_2]

# category 2 questions
category_name = category_names[1]
cat_2_local_preference_questions = generate_preference_questions(criteria_list=category_criteria[category_name],
                                                                 criteria_description=category_criteria_description[
                                                                     category_name])
cat_2_access_rights = Question(name="Zugriffsrechte",
                               question_text="Haben Sie die notwendigen Rechte, Betriebsdaten von Hausstationen "
                                             "sammeln und analysieren zu können?",
                               options=["Ja", "Nein"],
                               multiple_choice=False,
                               question_types=["Risk"],
                               answer_mapping={"Ja": 1, "Nein": 5},
                               description_text=risk_1_description,
                               consequence_description="Wenn diese Frage mit 'Nein' beantwortet wird, steigt das "
                                                       "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                       "'Instandhaltung Hausstationen'.",
                               reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                               "der Kategorie 'Instandhaltung Hausstationen' einschätzen zu können."
                               )
cat_2_transparency = Question(name="Transparenz",
                              question_text="Haben Sie Verpflichtungen, den Umgang mit Betriebsdaten von Hausstationen "
                                            "transparent offenzulegen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_2_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                      "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                      "'Instandhaltung Hausstationen'.",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                              "der Kategorie 'Instandhaltung Hausstationen' einschätzen zu können."
                              )
cat_2_resistance = Question(name="Widerstand",
                            question_text="Erwarten Sie Widerstand gegen die Einführung von ML-Lösungen zur "
                                          "Instandhaltung von Hausstationen?",
                            options=["Ja", "Nein"],
                            multiple_choice=False,
                            question_types=["Risk"],
                            answer_mapping={"Ja": 5, "Nein": 1},
                            description_text=risk_3_description,
                            consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                    "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                    "'Instandhaltung Hausstationen'.",
                            reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                            "der Kategorie 'Instandhaltung Hausstationen' einschätzen zu können."
                            )
cat_2_confidential = Question(name="Vertraulichkeit",
                              question_text="Sind die Ihnen zur Verfügung stehenden Daten von Hausstationen "
                                            "vertraulich nach DSGVO?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_4_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                      "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                      "'Instandhaltung Hausstationen'.",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases in "
                                              "der Kategorie 'Instandhaltung Hausstationen' einschätzen zu können."
                              )
cat_2_substation_amount = Question(name="Anzahl HAST",
                                   question_text="Wie viele Hausstationen würden im Rahmen Use-Cases betrachtet "
                                                 "werden?",
                                   options=[f"Weniger als {min_substations_for_clustering}",
                                            f"{min_substations_for_clustering} oder mehr"],
                                   multiple_choice=False,
                                   question_types=["Specification"],
                                   description_text="Einige ML Use Cases sind erst dann sinnvoll umzusetzen, wenn eine"
                                                    "größere Anzahl an Hausstationen analysiert werden soll.",
                                   consequence_description=f"Falls weniger als {min_substations_for_clustering} "
                                                           f"Hausstationen verfügbar sind, werden ML Use Cases "
                                                           f"ausgeschlossen, welche eine große Anzahl an Hausstationen"
                                                           f"benötigen, um sinnvolle Modelle zu erstellen.",
                                   reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases."
                                   )
cat_2_labels_1 = Question(name="Labels HAST verfügbar",
                          question_text="Verfügen Sie über Informationen zu Schäden, Fehlern oder  Ausfällen "
                                        "von Hausstationen?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Specification"],
                          consequence_triggers={"Ja": "Labels HAST Art", "Nein": "Labels HAST erheben"},
                          description_text="ML Use Cases zur Instandhaltung von Hausstationen können historische "
                                           "Informationen zu Schäden, Fehlern und Ausfällen für die Modellerstellung"
                                           "oder die Validierung benötigen.",
                          consequence_description="Falls keine Fehlerinformationen oder Ähnliches vorliegen, wird eine"
                                                  "Folgefrage zur Erhebung dieser Informationen gestellt. Falls Sie "
                                                  "bereits über diese Informationen verfügen, wird eine Folgefrage zur"
                                                  "Art der Daten gestellt.",
                          reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases und "
                                          "Einschätzung des Datenerhebungsaufwands."
                          )
cat_2_labels_2 = Question(name="Labels HAST erheben",
                          question_text="Würden Sie Informationen zu Schäden, Fehlern oder  Ausfällen "
                                        "von Hausstationen sammeln, um ML-Use-Cases zu ermöglichen?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Effort"],
                          answer_mapping={"Ja": 5, "Nein": 1},
                          criteria="Datenerhebungsaufwand",
                          description_text=data_3_description,
                          consequence_description="Falls Sie keine Fehlerinformationen für einen ML Use Case erheben "
                                                  "wollen, scheiden Use Cases, welche diese Daten benötigen aus der"
                                                  "Bewertung aus. Falls Sie mit 'Ja' auf diese Frage antworten, steigt"
                                                  "der Datenerhebungsaufwands für Use Cases, welche diese Daten "
                                                  "benötigen.",
                          reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases und "
                                          "Einschätzung des Datenerhebungsaufwands."
                          )
cat_2_labels_3 = Question(name="Labels HAST Art",
                          question_text="Über welche Art von Fehlerinformationen verfügen Sie?",
                          options=["Instandhaltungsberichte in Form von Dokumenten",
                                   "Digitalisierte Instandhaltungsberichte (bspw. im PDF Format)",
                                   "Gelabelte Fehlerzeiträume in einer Datenbank"
                                   ],
                          answer_mapping={"Instandhaltungsberichte in Form von Dokumenten": 4,
                                          "Digitalisierte Instandhaltungsberichte (bspw. im PDF Format)": 2,
                                          "Gelabelte Fehlerzeiträume in einer Datenbank": 1
                                          },
                          multiple_choice=False,
                          question_types=["Effort"],
                          criteria="Datenerhebungsaufwand",
                          description_text="Die Art der Instandhaltungsdaten oder Fehlerinformationen hat einen großen"
                                           "Einfluss auf den Datenerhebungsaufwand.",
                          consequence_description="Liegen die Daten in Form von Dokumenten vor, steigt der "
                                                  "Datenerhebungsaufwand deutlich. Im Falle von digitalisierten "
                                                  "Berichten steigt der Datenerhebungsaufwand mäßig.",
                          reason_to_exist="Einschätzung des Datenerhebungsaufwands."
                          )
cat_2_default_questions = [cat_2_access_rights, cat_2_transparency, cat_2_resistance, cat_2_confidential,
                           cat_2_substation_amount, cat_2_labels_1]
cat_2_consequence_questions = [cat_2_labels_2, cat_2_labels_3]

# category 3 questions
category_name = category_names[2]
cat_3_local_preference_questions = generate_preference_questions(criteria_list=category_criteria[category_name],
                                                                 criteria_description=category_criteria_description[
                                                                     category_name])
cat_3_risk_question_1 = Question(name="Zugriffsrechte",
                                 question_text="Haben Sie die notwendigen Rechte, um Daten aus dem Rohrnetz zu erheben "
                                               "und zu verwenden?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 1, "Nein": 5},
                                 description_text=risk_1_description,
                                 consequence_description="Wenn diese Frage mit 'Nein' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Instandhaltung Rohrnetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Instandhaltung Rohrnetz' einschätzen zu "
                                                 "können."
                                 )
cat_3_risk_question_2 = Question(name="Transparenz",
                                 question_text="Haben Sie Verpflichtungen, den Umgang mit Daten aus dem Rohrnetz "
                                               "transparent offenzulegen?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_2_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Instandhaltung Rohrnetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Instandhaltung Rohrnetz' einschätzen zu "
                                                 "können."
                                 )
cat_3_risk_question_3 = Question(name="Widerstand",
                                 question_text="Erwarten Sie Widerstand gegen die Einführung von ML-Lösungen zur "
                                               "Instandhaltung des Rohrnetzes?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_3_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Instandhaltung Rohrnetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Instandhaltung Rohrnetz' einschätzen zu "
                                                 "können."
                                 )
cat_3_risk_question_4 = Question(name="Vertraulichkeit",
                                 question_text="Sind die Ihnen zur Verfügung stehenden Daten aus dem Rohrnetz "
                                               "vertraulich nach DSGVO?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_4_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Instandhaltung Rohrnetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Instandhaltung Rohrnetz' einschätzen zu "
                                                 "können."
                                 )
cat_3_labels_1 = Question(name="Labels Rohrnetz verfügbar",
                          question_text="Verfügen Sie über Informationen zu Schäden, Fehlern oder Ausfällen "
                                        "im Rohrleitungsnetz?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Specification"],
                          consequence_triggers={"Ja": "Labels Rohrnetz Art", "Nein": "Labels Rohrnetz erheben"},
                          description_text="ML Use Cases zur Instandhaltung des Rohrleitungsnetzes können historische "
                                           "Informationen zu Schäden, Fehlern und Ausfällen für die Modellerstellung"
                                           "oder die Validierung benötigen.",
                          consequence_description="Falls keine Fehlerinformationen oder Ähnliches vorliegen, wird eine"
                                                  "Folgefrage zur Erhebung dieser Informationen gestellt. Falls Sie "
                                                  "bereits über diese Informationen verfügen, wird eine Folgefrage zur"
                                                  "Art der Daten gestellt.",
                          reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases und "
                                          "Einschätzung des Datenerhebungsaufwands."
                          )
cat_3_labels_2 = Question(name="Labels Rohrnetz erheben",
                          question_text="Würden Sie Informationen zu Schäden, Fehlern oder Ausfällen "
                                        "im Rohrleitungsnetz sammeln, um ML-Use-Cases zu ermöglichen?",
                          options=["Ja", "Nein"],
                          multiple_choice=False,
                          question_types=["Effort"],
                          answer_mapping={"Ja": 5, "Nein": 1},
                          criteria="Datenerhebungsaufwand",
                          description_text=data_3_description,
                          consequence_description="Falls Sie keine Fehlerinformationen für einen ML Use Case erheben "
                                                  "wollen, scheiden Use Cases, welche diese Daten benötigen aus der"
                                                  "Bewertung aus. Falls Sie mit 'Ja' auf diese Frage antworten, steigt"
                                                  "der Datenerhebungsaufwands für Use Cases, welche diese Daten "
                                                  "benötigen.",
                          reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use Cases und "
                                          "Einschätzung des Datenerhebungsaufwands."
                          )
cat_3_labels_3 = Question(name="Labels Rohrnetz Art",
                          question_text="Über welche Art von Fehlerinformationen verfügen Sie?",
                          options=["Instandhaltungsberichte in Form von Dokumenten",
                                   "Digitalisierte Instandhaltungsberichte (bspw. im PDF Format)",
                                   "Gelabelte Fehlerzeiträume in einer Datenbank"
                                   ],
                          answer_mapping={"Instandhaltungsberichte in Form von Dokumenten": 4,
                                          "Digitalisierte Instandhaltungsberichte (bspw. im PDF Format)": 3,
                                          "Gelabelte Fehlerzeiträume in einer Datenbank": 1
                                          },
                          multiple_choice=False,
                          question_types=["Effort"],
                          criteria="Datenerhebungsaufwand",
                          description_text="Die Art der Instandhaltungsdaten oder Fehlerinformationen hat einen großen"
                                           "Einfluss auf den Datenerhebungsaufwand.",
                          consequence_description="Liegen die Daten in Form von Dokumenten vor, steigt der "
                                                  "Datenerhebungsaufwand deutlich. Im Falle von digitalisierten "
                                                  "Berichten steigt der Datenerhebungsaufwand mäßig.",
                          reason_to_exist="Einschätzung des Datenerhebungsaufwands."
                          )
cat_3_vibration_1 = Question(name="Vibrationsdaten verfügbar",
                             question_text="Haben Sie Zugriff auf kontinuierliche Vibrations- und Akustikdaten aus "
                                           "dem Fernwärmenetz?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Effort"],
                             consequence_triggers={"Nein": "Vibrationsdaten Sensoren"},
                             answer_mapping={"Ja": 1, "Nein": 5},
                             criteria="Datenerhebungsaufwand",
                             description_text="Vibrations- und Akustikdaten" + data_1_description,
                             consequence_description=data_1_consequence,
                             reason_to_exist=data_1_reason_to_exist
                             )
cat_3_vibration_2 = Question(name="Vibrationsdaten Sensoren",
                             question_text="Verfügen Sie über die notwendige Sensorik, um Vibrations- und Akustikdaten "
                                           "zu erheben?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Effort", "Risk"],
                             answer_mapping={"Ja": 1, "Nein": 5},
                             criteria="Sensorinstallationsaufwand",
                             consequence_triggers={"Nein": "Vibrationsdaten erheben"},
                             description_text=data_2_description,
                             consequence_description=data_2_consequence,
                             reason_to_exist=data_2_reason_to_exist
                             )
cat_3_vibration_3 = Question(name="Vibrationsdaten erheben",
                             question_text="Würden Sie Vibrations- und Akustikdaten erheben, um einen ML-Use-Case zu "
                                           "ermöglichen?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Specification"],
                             description_text=data_3_description,
                             consequence_description=data_3_consequence,
                             reason_to_exist=data_3_reason_to_exist
                             )
cat_3_environment_conditions = Question(name="Umweltbedingungen",
                                        question_text="Würden Sie für die Umsetzung eines ML-Use-Cases auf die "
                                                      "passenden Umweltbedingungen (wie beispielsweise Jahreszeiten) "
                                                      "warten?",
                                        options=["Ja", "Nein"],
                                        multiple_choice=False,
                                        question_types=["Specification"],
                                        description_text="ML Use Cases können besonders bei der Datenerhebung "
                                                         "auf bestimmte Umweltbedingungen angewiesen sein. Das kann "
                                                         "bei der Umsetzung zu Komplikationen in der Planung führen.",
                                        consequence_description="Falls Sie nicht dazu bereit sind auf passende "
                                                                "Umweltbedingungen für die Datenerhebung im Rahmen der "
                                                                "Umsetzung, werden Use Cases, bei welchen das ein "
                                                                "maßgeblicher Faktor ist von der Bewertung "
                                                                "ausgeschlossen.",
                                        reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                        "Cases."
                                        )
cat_3_pipeline_depth = Question(name="Rohrnetztiefe",
                                question_text=f"Ist das Rohrleitungsnetz hauptsächlich in einer Tiefe von weniger "
                                              f"als {max_pipeline_depth}m  verlegt?",
                                options=["Ja", "Nein"],
                                multiple_choice=False,
                                question_types=["Specification"],
                                description_text="Die Tiefe des Rohrnetzes ist insbesondere für basierte ML Use Cases "
                                                 "zur Instandhaltung des Rohrnetzes ein entscheidender Faktor, wenn"
                                                 "es um die Machbarkeit des Use Cases geht.",
                                consequence_description="Falls die Rohre zu tief verlegt sind, um bspw. bildbasierte"
                                                        "ML Use Cases umzusetzen, werden diese von der Bewertung "
                                                        "ausgeschlossen.",
                                reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                "Cases."
                                )
cat_3_network_topology = Question(name="Rohrnetztopologie",
                                  question_text="Verfügen Sie über detaillierte Informationen zur Topologie des "
                                                "Rohrleitungsnetzes?",
                                  options=["Ja", "Nein"],
                                  multiple_choice=False,
                                  question_types=["Specification"],
                                  description_text="ML Use Cases für Instandhaltung des Rohrnetzes können diverse "
                                                   "Metadaten zur Netztopologie benötigen. "
                                                   "Da eine detaillierte Abfrage der einzelnen "
                                                   "Merkmale die Komplexität zu stark erhöhen würde, werden diese hier"
                                                   "gesammelt abgefragt.",
                                  consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use Cases,"
                                                          "welche diese Daten benötigen nicht angewandt werden und "
                                                          "werden deswegen nicht weiter bewertet.",
                                  reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                  "Cases."
                                  )

cat_3_default_questions = [cat_3_risk_question_1, cat_3_risk_question_2, cat_3_risk_question_3, cat_3_risk_question_4,
                           cat_3_vibration_1, cat_3_labels_1, cat_3_environment_conditions, cat_3_pipeline_depth,
                           cat_3_network_topology]
cat_3_consequence_questions = [cat_3_labels_2, cat_3_labels_3, cat_3_vibration_2, cat_3_vibration_3]

# category 4 questions
category_name = category_names[3]
cat_4_local_preference_questions = generate_preference_questions(criteria_list=category_criteria[category_name],
                                                                 criteria_description=category_criteria_description[
                                                                     category_name])
cat_4_risk_question_1 = Question(name="Zugriffsrechte",
                                 question_text="Haben Sie die notwendigen Rechte, um Daten aus dem Fernwärmenetz zu "
                                               "erheben und zu verwenden?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 1, "Nein": 5},
                                 description_text=risk_1_description,
                                 consequence_description="Wenn diese Frage mit 'Nein' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Betriebsstrategien Wärmenetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Betriebsstrategien Wärmenetz' einschätzen zu "
                                                 "können."
                                 )
cat_4_risk_question_2 = Question(name="Transparenz",
                                 question_text="Haben Sie Verpflichtungen, den Umgang mit Daten aus dem Fernwärmenetz "
                                               "transparent offenzulegen?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_2_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Betriebsstrategien Wärmenetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Betriebsstrategien Wärmenetz' einschätzen zu "
                                                 "können."
                                 )
cat_4_risk_question_3 = Question(name="Widerstand",
                                 question_text="Erwarten Sie Widerstand gegen die Einführung von ML-Lösungen zur "
                                               "Optimierung des Fernwärmenetzbetriebs?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_3_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Betriebsstrategien Wärmenetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Betriebsstrategien Wärmenetz' einschätzen zu "
                                                 "können."
                                 )
cat_4_risk_question_4 = Question(name="Vertraulichkeit",
                                 question_text="Sind die Ihnen zur Verfügung stehenden Fernwärmenetzdaten "
                                               "vertraulich nach DSGVO?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 5, "Nein": 1},
                                 description_text=risk_4_description,
                                 consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Betriebsstrategien Wärmenetz'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Betriebsstrategien Wärmenetz' einschätzen zu "
                                                 "können."
                                 )
cat_4_network_topology = Question(name="Fernwärmenetztopologie",
                                  question_text="Haben Sie Zugriff auf detaillierte Informationen zur Topologie des "
                                                "Fernwärmenetzes?",
                                  options=["Ja", "Nein"],
                                  multiple_choice=False,
                                  question_types=["Specification"],
                                  description_text="ML Use Cases zu Betriebsstrategien für das Fernwärmenetz können "
                                                   "diverse Metadaten zur Netztopologie benötigen. "
                                                   "Da eine detaillierte Abfrage der einzelnen "
                                                   "Merkmale die Komplexität zu stark erhöhen würde, werden diese hier"
                                                   "gesammelt abgefragt.",
                                  consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use Cases,"
                                                          "welche diese Daten benötigen nicht angewandt werden und "
                                                          "werden deswegen nicht weiter bewertet.",
                                  reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                  "Cases."
                                  )
cat_4_heat_generation = Question(name="Wärmeerzeugungsdaten",
                                 question_text="Haben Sie Zugriff auf Betriebsdaten der Wärmeerzeugungsanlage?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Specification"],
                                 description_text="ML Use Cases aus der Kategorie Betriebsstrategien für das "
                                                  "Wärmenetze nehmen oft eine übergeordnete Perspektive auf das "
                                                  "Fernwärmenetz ein und beziehen daher viele Komponenten des "
                                                  "Fernwärmesystems gleichzeitig ein. Im Zuge dessen können auch "
                                                  "Wärmeerzeugungsdaten benötigen werden, um bestimmte Use Cases "
                                                  "durchführen zu können.",
                                 consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use Cases,"
                                                         "welche diese Daten benötigen nicht angewandt werden und "
                                                         "werden deswegen nicht weiter bewertet.",
                                 reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                 "Cases."
                                 )
cat_4_indoor_temperatures = Question(name="Gebäudetemperaturen",
                                     question_text="Haben Sie Zugriff auf Innentemperaturwerte aus Gebäuden innerhalb "
                                                   "des Fernwärmenetzes?",
                                     options=["Ja", "Nein"],
                                     multiple_choice=False,
                                     question_types=["Specification"],
                                     description_text="ML Use Cases aus der Kategorie Betriebsstrategien für das "
                                                      "Wärmenetze nehmen oft eine übergeordnete Perspektive auf das "
                                                      "Fernwärmenetz ein und beziehen daher viele Komponenten des "
                                                      "Fernwärmesystems gleichzeitig ein. Im Zuge dessen können auch "
                                                      "Innentemperaturwerte aus Gebäuden innerhalb des Wärmenetzes "
                                                      "benötigen werden, um bestimmte Use Cases "
                                                      "durchführen zu können.",
                                     consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use "
                                                             "Cases, welche diese Daten benötigen nicht angewandt "
                                                             "werden und werden deswegen nicht weiter bewertet.",
                                     reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                     "Cases."
                                     )
cat_4_building_data = Question(name="Metadaten Gebäude",
                               question_text="Haben Sie Zugriff auf detaillierte Daten zu den Gebäudehüllen der "
                                             "Gebäude innerhalb des Fernwärmenetzes?",
                               options=["Ja", "Nein"],
                               multiple_choice=False,
                               question_types=["Specification"],
                               description_text="ML Use Cases aus der Kategorie Betriebsstrategien für das "
                                                "Wärmenetze nehmen oft eine übergeordnete Perspektive auf das "
                                                "Fernwärmenetz ein und beziehen daher viele Komponenten des "
                                                "Fernwärmesystems gleichzeitig ein. Im Zuge dessen können auch "
                                                "detaillierte Daten zu Gebäudehüllen "
                                                "benötigen werden, um bestimmte Use Cases "
                                                "durchführen zu können.",
                               consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use Cases,"
                                                       "welche diese Daten benötigen nicht angewandt werden und "
                                                       "werden deswegen nicht weiter bewertet.",
                               reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                               "Cases."
                               )
cat_4_default_questions = [cat_4_risk_question_1, cat_4_risk_question_2, cat_4_risk_question_3, cat_4_risk_question_4,
                           cat_4_network_topology, cat_4_heat_generation,
                           cat_4_indoor_temperatures, cat_4_building_data]
cat_4_consequence_questions = []

# category 5 questions
category_name = category_names[4]
cat_5_local_preference_questions = generate_preference_questions(criteria_list=category_criteria[category_name],
                                                                 criteria_description=category_criteria_description[
                                                                     category_name])
cat_5_risk_question_1 = Question(name="Zugriffsrechte",
                                 question_text="Haben Sie die notwendigen Rechte, um Betriebsdaten von Hausstationen "
                                               "zu sammeln?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Risk"],
                                 answer_mapping={"Ja": 1, "Nein": 5},
                                 description_text=risk_1_description,
                                 consequence_description="Wenn diese Frage mit 'Nein' beantwortet wird, steigt das "
                                                         "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                         "'Betriebsstrategien Hausstationen'.",
                                 reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                                 "in der Kategorie 'Betriebsstrategien Hausstationen' einschätzen zu "
                                                 "können."
                                 )
cat_5_transparency = Question(name="Transparenz",
                              question_text="Haben Sie Verpflichtungen, den Umgang mit Betriebsdaten von Hausstationen "
                                            "transparent offenzulegen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_2_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                      "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                      "'Betriebsstrategien Hausstationen'.",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                              "in der Kategorie 'Betriebsstrategien Hausstationen' einschätzen zu "
                                              "können."
                              )
cat_5_resistance = Question(name="Widerstand",
                            question_text="Erwarten Sie Widerstand gegen die Einführung von ML-Lösungen zur "
                                          "Optimierung des Betriebs von Hausstationen?",
                            options=["Ja", "Nein"],
                            multiple_choice=False,
                            question_types=["Risk"],
                            answer_mapping={"Ja": 5, "Nein": 1},
                            description_text=risk_3_description,
                            consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                                    "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                                    "'Betriebsstrategien Hausstationen'.",
                            reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                            "in der Kategorie 'Betriebsstrategien Hausstationen' einschätzen zu "
                                            "können."
                            )
cat_5_confidential = Question(name="Vertraulichkeit",
                              question_text="Sind die Ihnen zur Verfügung stehenden Daten von Hausstationen "
                                            "vertraulich nach DSGVO?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Risk"],
                              answer_mapping={"Ja": 5, "Nein": 1},
                              description_text=risk_4_description,
                              consequence_description="Wenn diese Frage mit 'Ja' beantwortet wird, steigt das "
                                               "Umsetzungsrisiko für ML Use Cases in der Kategorie "
                                               "'Betriebsstrategien Hausstationen'.",
                              reason_to_exist="Diese Frage wird gestellt, um das Umsetzungsrisiko für ML Use Cases "
                                              "in der Kategorie 'Betriebsstrategien Hausstationen' einschätzen zu "
                                              "können."
                              )
cat_5_valve_data_1 = Question(name="Ventildaten verfügbar",
                              question_text="Haben Sie Zugriff auf Daten zu Ventilen in Hausstationen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Effort"],
                              consequence_triggers={"Nein": "Ventildaten Sensoren"},
                              answer_mapping={"Ja": 1, "Nein": 5},
                              criteria="Datenerhebungsaufwand",
                              description_text="Daten zu Ventilen in Hausstationen" + data_1_description,
                              consequence_description=data_1_consequence,
                              reason_to_exist=data_1_reason_to_exist
                              )
cat_5_valve_data_2 = Question(name="Ventildaten Sensoren",
                              question_text="Verfügen Sie über die notwendige Sensorik, um Daten zu Ventilen "
                                            "in Hausstationen zu erheben?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Effort", "Risk"],
                              answer_mapping={"Ja": 1, "Nein": 5},
                              criteria="Sensorinstallationsaufwand",
                              consequence_triggers={"Nein": "Ventildaten erheben"},
                              description_text=data_2_description,
                              consequence_description=data_2_consequence,
                              reason_to_exist=data_2_reason_to_exist
                              )
cat_5_valve_data_3 = Question(name="Ventildaten erheben",
                              question_text="Würden Sie Ventildaten in Hausstationen erheben, um einen ML-Use-Case zu "
                                            "ermöglichen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Specification"],
                              description_text=data_3_description,
                              consequence_description=data_3_consequence,
                              reason_to_exist=data_3_reason_to_exist
                              )
cat_5_pressure_data_1 = Question(name="HAST Druckdaten verfügbar",
                                 question_text="Haben Sie Zugriff auf Daten zum Betriebsdruck von Hausstationen?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Effort"],
                                 consequence_triggers={"Nein": "HAST Druckdaten Sensoren"},
                                 answer_mapping={"Ja": 1, "Nein": 5},
                                 criteria="Datenerhebungsaufwand",
                                 description_text="Daten zum Betriebsdruck von Hausstationen" + data_1_description,
                                 consequence_description=data_1_consequence,
                                 reason_to_exist=data_1_reason_to_exist
                                 )
cat_5_pressure_data_2 = Question(name="HAST Druckdaten Sensoren",
                                 question_text="Verfügen Sie über die notwendige Sensorik, um Daten zum "
                                               "Betriebsdruck in Hausstationen zu erheben?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Effort", "Risk"],
                                 answer_mapping={"Ja": 1, "Nein": 5},
                                 criteria="Sensorinstallationsaufwand",
                                 consequence_triggers={"Nein": "HAST Druckdaten erheben"},
                                 description_text=data_2_description,
                                 consequence_description=data_2_consequence,
                                 reason_to_exist=data_2_reason_to_exist
                                 )
cat_5_pressure_data_3 = Question(name="HAST Druckdaten erheben",
                                 question_text="Würden Sie Daten zum Betriebsdruck in Hausstationen erheben, um einen "
                                               "ML-Use-Case zu ermöglichen?",
                                 options=["Ja", "Nein"],
                                 multiple_choice=False,
                                 question_types=["Specification"],
                                 description_text=data_3_description,
                                 consequence_description=data_3_consequence,
                                 reason_to_exist=data_3_reason_to_exist
                                 )
cat_5_flow_rate_1 = Question(name="HAST Durchflussvolumen verfügbar",
                             question_text="Haben Sie Zugriff auf Durchflussvolumen in Hausstationen?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Effort"],
                             consequence_triggers={"Nein": "HAST Durchflussvolumen Sensoren"},
                             answer_mapping={"Ja": 1, "Nein": 5},
                             criteria="Datenerhebungsaufwand",
                             description_text="Durchflussvolumen in Hausstationen" + data_1_description,
                             consequence_description=data_1_consequence,
                             reason_to_exist=data_1_reason_to_exist
                             )
cat_5_flow_rate_2 = Question(name="HAST Durchflussvolumen Sensoren",
                             question_text="Verfügen Sie über die notwendige Sensorik, um Durchflussvolumen in "
                                           "Hausstationen zu erheben?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Effort", "Risk"],
                             answer_mapping={"Ja": 1, "Nein": 5},
                             criteria="Sensorinstallationsaufwand",
                             consequence_triggers={"Nein": "HAST Durchflussvolumen erheben"},
                             description_text=data_2_description,
                             consequence_description=data_2_consequence,
                             reason_to_exist=data_2_reason_to_exist
                             )
cat_5_flow_rate_3 = Question(name="HAST Durchflussvolumen erheben",
                             question_text="Würden Sie Durchflussvolumen in Hausstationen erheben, um einen "
                                           "ML-Use-Case zu ermöglichen?",
                             options=["Ja", "Nein"],
                             multiple_choice=False,
                             question_types=["Specification"],
                             description_text=data_3_description,
                             consequence_description=data_3_consequence,
                             reason_to_exist=data_3_reason_to_exist
                             )
cat_5_user_comfort = Question(name="Nutzerkomfortdaten",
                              question_text="Verfügen Sie über Daten zur Vorlauftemperatur für den Sekundärkreislauf "
                                            "von Hausstationen?",
                              options=["Ja", "Nein"],
                              multiple_choice=False,
                              question_types=["Specification"],
                              description_text="Daten zur Vorlauftemperatur für den Sekundärkreislauf "
                                               "von Hausstationen sind notwendig für die Umsetzung einiger "
                                               "ML Use Cases.",
                              consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use "
                                                      "Cases, welche diese Daten benötigen nicht angewandt "
                                                      "werden und werden deswegen nicht weiter bewertet.",
                              reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                              "Cases."
                              )
cat_5_substation_meta_data = Question(name="HAST Metadaten",
                                      question_text="Verfügen Sie über detaillierte Metadaten wie beispielsweise "
                                                    "Datenblätter zu Komponenten der Hausstationen?",
                                      options=["Ja", "Nein"],
                                      multiple_choice=False,
                                      question_types=["Specification"],
                                      description_text="ML Use Cases für Betriebsstrategien für Hausstationen "
                                                       "können diverse Metadaten zu Gebäuden benötigen, welche an das "
                                                       "Fernwärmenetz angeschlossen sind. Da eine detaillierte Abfrage "
                                                       "der einzelnen Merkmale die Komplexität zu stark erhöhen würde, "
                                                       "werden diese hier gesammelt abgefragt.",
                                      consequence_description="Falls diese Daten nicht vorhanden sind, können ML Use "
                                                              "Cases, welche diese Daten benötigen nicht angewandt "
                                                              "werden und werden deswegen nicht weiter bewertet.",
                                      reason_to_exist="Überprüfung der Umsetzungsvoraussetzungen für einige ML Use "
                                                      "Cases."
                                      )
cat_5_default_questions = [cat_5_risk_question_1, cat_5_transparency, cat_5_resistance, cat_5_confidential,
                           cat_5_valve_data_1, cat_5_pressure_data_1, cat_5_flow_rate_1, cat_5_user_comfort,
                           cat_5_substation_meta_data]
cat_5_consequence_questions = [cat_5_valve_data_2, cat_5_valve_data_3, cat_5_pressure_data_2, cat_5_pressure_data_3,
                               cat_5_flow_rate_2, cat_5_flow_rate_3]
