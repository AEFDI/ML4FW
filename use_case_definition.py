from use_case import UseCase
from condition_definition import *

"""
Script for defining all use cases and assigning predefined score values, conditions and detail information.
"""

# Forecasting Use-Cases
c1_uc1 = UseCase(name="Wärmelastprognosen anhand detaillierter Netzdaten",
                 description="Wärmelastvorhersage für gesamten Fernwärmenetz mithilfe von mehreren LSTM-Architekturen",
                 predefined_potential={"Genauigkeit": 5,
                                       "Interpretierbarkeit": 4,
                                       "Kundenkomfort": 4},
                 predefined_effort={"Datenaufbewahrungsaufwand": 4,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 4,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_supply_return_condition,
                                               no_flow_rate_condition,
                                               no_energy_data_condition,
                                               no_weather_forecast_condition,
                                               no_history_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.arcontrol.2022.03.009 \n"
                                   "https://doi.org/10.1016/j.ifacol.2021.08.044",
                 pro_contra_arguments={"pro": ["Sehr hohe Prognosegenauigkeit",
                                               "Multivariate Prognosen möglich - verschiedene Eingangsdaten",
                                               "Erklärbare Vorhersage mit LIME "
                                               "(local interpretable model-agnostic explanations)"],
                                       "contra": ["Sehr rechenintensiv",
                                                  "Hohe Implementierungskomplexität"
                                                  ]}
                 )

c1_uc2 = UseCase(name="Wärmelastprognose für Fernwärmenetze mit Berücksichtigung der Netzstruktur",
                 description="Prognose eines Gesamtnetzes anhand Wärmelastprofile einzelner Gebäude und "
                             "Netzwerktopologie mit Graph Recurrent Neural Networks",
                 predefined_potential={"Genauigkeit": 5,
                                       "Interpretierbarkeit": 4,
                                       "Kundenkomfort": 5},
                 predefined_effort={"Datenaufbewahrungsaufwand": 4,
                                    "Kontinuierlicher Aufwand": 3,
                                    "Rechenaufwand": 4,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 3,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_heat_data_condition,
                                               no_weather_forecast_condition,
                                               no_flow_rate_condition,
                                               no_network_temperatures_condition,
                                               no_pressure_data_condition],
                 literature_source="https://doi.org/10.1016/j.apenergy.2023.121753",
                 pro_contra_arguments={"pro": ["Berücksichtigt die Struktur des Fernwärmenetzes",
                                               "Sehr gute Prognosegenauigkeit",
                                               "Explainable AI ermöglicht Interpretierbarkeit"
                                               ],
                                       "contra": ["Sehr komplexe Implementierung",
                                                  "Hoher Rechenaufwand",
                                                  "Komplexe Datenbeschaffung"
                                                  ]}
                 )

c1_uc3 = UseCase(name="Wärmelastprognose für einzelne Gebäude und Stadtviertel",
                 description="Kurzfristige Lastprognose anhand historischer Last- und Wetterdaten mithilfe von ANN in "
                             "Kombination mit multipler linearer Regression",
                 predefined_potential={"Genauigkeit": 4,
                                       "Interpretierbarkeit": 4,
                                       "Kundenkomfort": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 2,
                                    "Kontinuierlicher Aufwand": 3,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 2,
                                    "Implementationsaufwand": 2,
                                    "Datenerhebungsaufwand": 2,
                                    "Datendetailgrad": 3},
                 predefined_risk_value=3,
                 non_applicability_conditions=[data_resolution_days_condition,
                                               no_heat_data_condition,
                                               no_weather_forecast_condition,
                                               no_building_data_condition,
                                               ],
                 literature_source="https://doi.org/10.1016/j.energy.2023.129866",
                 pro_contra_arguments={"pro": ["Einfach zu implementieren",
                                               "Geringer Rechenaufwand",
                                               "Gute Interpretierbarkeit",
                                               "Bildet grundlegende Gebäudemerkmale ab"
                                               ],
                                       "contra": ["Mittlere Prognosegüte",
                                                  "Keine komplexen Zusammenhänge modellierbar",
                                                  "Nicht echtzeitfähig"
                                                  ]}
                 )

c1_uc4 = UseCase(name="Echtzeitprognose für Wärmelasten in Fernwärmenetzen",
                 description="Kurzfristige Wärmelastprognosen in Echtzeit mithilfe von LSTM",
                 predefined_potential={"Genauigkeit": 5,
                                       "Interpretierbarkeit": 3,
                                       "Kundenkomfort": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 4,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 5,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_history_condition,
                                               no_heat_data_condition,
                                               no_ambient_temperature_condition,
                                               no_weather_forecast_condition,
                                               no_network_temperatures_condition],
                 literature_source="https://doi.org/10.3384/ecp200050",
                 pro_contra_arguments={"pro": ["Sehr hohe Prognosegenauigkeit",
                                               "Kann verschiedene Gebäudetypen abbilden",
                                               "Gute kurzfriste Vorhersagen"
                                               ],
                                       "contra": ["Hoher Rechenaufwand",
                                                  "Sehr komplexe Implementierung",
                                                  "Komplexe Datenbeschaffung"
                                                  ]}
                 )

c1_uc5 = UseCase(name="Prognose für Wärmespeicher und Spitzenlastmanagement",
                 description="Vorhersage der Wärmelasten und Speicherfüllstände zur Spitzenlastkappung mit "
                             "incremental learning LSTM",
                 predefined_potential={"Genauigkeit": 5,
                                       "Interpretierbarkeit": 3,
                                       "Kundenkomfort": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 5,
                                    "Sensorinstallationsaufwand": 4,
                                    "Implementationsaufwand": 5,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_supply_return_condition,
                                               no_heat_storage_condition,
                                               no_heat_data_condition],
                 literature_source="https://doi.org/10.1016/j.energy.2024.131690",
                 pro_contra_arguments={"pro": ["Dynamische Modellanpassung in Echtzeit",
                                               "Sehr hohe Prognosegenauigkeit",
                                               "Ermöglicht Spitzenlastmanagement"
                                               ],
                                       "contra": ["Hoher Rechenaufwand",
                                                  "Sehr komplexe Implementierung",
                                                  "Erfordert umfangreiche Sensordaten"
                                                  ]}
                 )

c1_uc6 = UseCase(name="Haushaltsbezogene Wärmelastprognose für individuelle Gebäude",
                 description="Wärmebedarfsprognose auf Haushaltsebene mithilfe von Support Vector Regression (SVR) "
                             "und Partikelschwarmoptimierung (PSO)",
                 predefined_potential={"Genauigkeit": 5,
                                       "Interpretierbarkeit": 3,
                                       "Kundenkomfort": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 2,
                                    "Kontinuierlicher Aufwand": 3,
                                    "Rechenaufwand": 1,
                                    "Sensorinstallationsaufwand": 1,
                                    "Implementationsaufwand": 2,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 2},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_heat_data_condition,
                                               no_history_condition,
                                               no_weather_forecast_condition],
                 literature_source="https://arxiv.org/pdf/2112.01908",
                 pro_contra_arguments={"pro": ["Hohe Genauigkeit für Einzelgebäude",
                                               "Kommt mit kleiner Datengrundlage aus",
                                               "Einfach Implementierung"
                                               ],
                                       "contra": ["Nicht gut skalierbar",
                                                  "Benötigt manuelle Auswahl von Datenmerkmalen",
                                                  "Nicht Echtzeitfähig"
                                                  ]}
                 )

# Predictive Maintenance for Substations
c2_uc1 = UseCase(name="Anomalieerkennung durch Ensemblemodellierung",
                 description="Dieser Use-Case setzt einfache ML-Modelle für jede einzelne Hausstation ein und führt "
                             "parallel dazu ein Clustering der Hausstationen in verschiedene Gruppen durch. Auf Basis, "
                             "der dieser zwei Informationslevel kann ein Ensemble Modell erstellt werden, welches das "
                             "Erkennen von fehlerhaften Hausstationen ermöglicht.",
                 predefined_potential={"Fehlererkennung": 5,
                                       "Identifikation von Ursachen": 1,
                                       "Wenige Fehlalarme": 5,
                                       "Fehlerfrüherkennung": 2,
                                       "Interpretierbarkeit": 2},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 5,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 2},
                 predefined_risk_value=3,
                 non_applicability_conditions=[small_num_substation_condition,
                                               no_supply_return_condition,
                                               no_flow_rate_condition,
                                               data_resolution_days_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.eswa.2022.116864",
                 pro_contra_arguments={"pro": ["Gute Skalierbarkeit des Use-Cases",
                                               "Wenige Fehlalarme durch den Ensemble-Ansatz",
                                               "Benötigt nur wenige Monate an Daten"
                                               ],
                                       "contra": ["Komplexes Modell mit vielen Komponenten",
                                                  "Potenziell hohe Rechenaufwand",
                                                  "Daten von sehr vielen HASTs werden benötigt"
                                                  ]}
                 )

c2_uc2 = UseCase(name="Anomalie-erkennung mithilfe von Clusteringmethoden",
                 description="Durch die Anwendung von Clustering-Verfahren auf Basis von Zeitreihendaten der HASTs "
                             "werden Ausreißer-HASTs identifiziert.",
                 predefined_potential={"Fehlererkennung": 3,
                                       "Identifikation von Ursachen": 1,
                                       "Wenige Fehlalarme": 3,
                                       "Fehlerfrüherkennung": 1,
                                       "Interpretierbarkeit": 1},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 1,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 1,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=1,
                 non_applicability_conditions=[small_num_substation_condition,
                                               no_supply_return_condition,
                                               no_flow_rate_condition,
                                               data_resolution_1h_condition,
                                               data_resolution_days_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition
                                               ],
                 literature_source="https://doi.org/10.1109/FMEC62297.2024.10710205",
                 pro_contra_arguments={"pro": ["Niedrige Modellkomplexität",
                                               "Geringer Rechenaufwand"],
                                       "contra": ["Daten von vielen HASTs werden benötigt",
                                                  "Frühzeitige Fehlererkennung ist nicht möglich"]}
                 )

c2_uc3 = UseCase(name="Rekonstruktionsbasierte Normalverhaltensmodelle",
                 description="In diesem Use-Case werden auf Basis der Wärmeleistungsdaten Abweichungen vom normalen "
                             "Verhalten von HASTs durch die Anwendung von rekonstruktionsbasierten "
                             "Normalverhaltensmodellen wie beispielsweise Autoencodern ermöglicht. "
                             "Diese erlernen das normale Verhalten auf Basis von historischen Daten der HASTs.",
                 predefined_potential={"Fehlererkennung": 3,
                                       "Identifikation von Ursachen": 4,
                                       "Wenige Fehlalarme": 3,
                                       "Fehlerfrüherkennung": 4,
                                       "Interpretierbarkeit": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 2,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=4,
                 non_applicability_conditions=[no_supply_return_condition,
                                               no_flow_rate_condition,
                                               no_heat_data_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition,
                                               month_history_condition,
                                               no_labels_substation_condition,
                                               data_resolution_days_condition
                                               ],
                 literature_source="https://doi.org/10.1109/ICIEA48937.2020.9248108",
                 pro_contra_arguments={"pro": ["Fehlerfrüherkennung ist möglich",
                                               "Ursachenanalyse können gut durchgeführt werden"
                                               ],
                                       "contra": ["Viele historische Daten werden benötigt",
                                                  "Labels mit guter Qualität werden benötigt",
                                                  "Die Auswahl des Trainingsdatensatzes beeinflusst die Performanz "
                                                  "entscheidend",
                                                  "Unbekanntes Normalverhalten kann als Fehler identifiziert werden"
                                                  ]}
                 )

c2_uc4 = UseCase(name="Regressionsbasierte Normalverhaltensmodelle",
                 description="Durch die Nutzung regressionsbasierter Modelle, wird das Verhalten von HASTs basierend "
                             "auf einem bereitgestellten Datensatz erlernt. Durch den Abgleich von weiteren "
                             "Betriebsdaten mit der Modellvorhersage wird die Erkennung von Abweichungen und Fehlern "
                             "ermöglicht.",
                 predefined_potential={"Fehlererkennung": 2,
                                       "Identifikation von Ursachen": 2,
                                       "Wenige Fehlalarme": 3,
                                       "Fehlerfrüherkennung": 4,
                                       "Interpretierbarkeit": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 2,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_supply_return_condition,
                                               no_flow_rate_condition,
                                               no_heat_data_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition,
                                               month_history_condition,
                                               no_labels_substation_condition,
                                               data_resolution_days_condition
                                               ],
                 literature_source="https://doi.org/10.34641/clima.2022.4",
                 pro_contra_arguments={"pro": ["Fehlerfrüherkennung ist möglich",
                                               "Geringe Modellkomplexität"
                                               ],
                                       "contra": ["Viele historische Daten werden benötigt",
                                                  "Labels mit guter Qualität werden benötigt",
                                                  "Die Auswahl des Trainingsdatensatzes beeinflusst die Performanz "
                                                  "entscheidend",
                                                  "Unbekanntes Normalverhalten kann als Fehler identifiziert werden"
                                                  ]}
                 )

# Pipeline Maintenance
c3_uc1 = UseCase(name="Leckagenerkennung auf Basis von Infrarotbildern",
                 description="Automatisierte ML-Bildanalyseverfahren werden genutzt, um Leckagen auf Infrarotbildern "
                             "zu lokalisieren.",
                 predefined_potential={"Erkennen von vorhandenen Leckagen": 3,
                                       "Ortung von Leckagen": 4,
                                       "Vorbeugung von Fehlern": 1,
                                       "Wenige Fehlalarme": 3,
                                       "Interpretierbarkeit": 4},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 5,
                                    "Rechenaufwand": 4,
                                    "Sensorinstallationsaufwand": 1,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 1},
                 predefined_risk_value=4,
                 non_applicability_conditions=[no_waiting_condition,
                                               pipeline_depth_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.autcon.2024.105709",
                 pro_contra_arguments={"pro": ["Keine Installation zusätzlicher Sensorik notwendig",
                                               "Keine historischen Daten notwendig",
                                               "Gute Lokalisierung oberflächennaher Leckagen"],
                                       "contra": [
                                           "Sehr abhängig von den Umgebungsbedingungen wie bspw. Außentemperatur",
                                           "Leckagen in tieferliegenden Rohrnetzen können nicht erkannt werden",
                                           "Eine kontinuierliche Überwachung des Rohrnetzes ist sehr aufwändig",
                                           "Frühzeitige Erkennung von Leckagen ist nicht möglich"
                                       ]}
                 )

c3_uc2 = UseCase(name="Leckagenerkennung auf Basis von Drucksensorik",
                 description="Eine Kombination einer hydraulischen Simulation mit einem auf XGBoost basierenden "
                             "Klassifikator wird genutzt, um Leckagen zu identifizieren und dem korrekten Abschnitt "
                             "des Rohrnetzes zuzuordnen.",
                 predefined_potential={"Erkennen von vorhandenen Leckagen": 3,
                                       "Ortung von Leckagen": 3,
                                       "Vorbeugung von Fehlern": 2,
                                       "Wenige Fehlalarme": 5,
                                       "Interpretierbarkeit": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 1,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 2,
                                    "Sensorinstallationsaufwand": 5,
                                    "Implementationsaufwand": 2,
                                    "Datenerhebungsaufwand": 3,
                                    "Datendetailgrad": 3},
                 predefined_risk_value=4,
                 non_applicability_conditions=[no_flow_rate_condition,
                                               data_resolution_days_condition,
                                               no_history_condition,
                                               no_network_topology_condition,
                                               no_network_temperatures_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.enbuild.2020.110161",
                 pro_contra_arguments={"pro": ["Kommt mit niedriger Datenauflösung zurecht",
                                               "Geringer Rechenaufwand",
                                               "Kontinuierliche Überwachung des Rohrnetzes ist mit wenig Aufwand "
                                               "verbunden",
                                               "Wenige Fehlalarme"
                                               ],
                                       "contra": ["Hoher Sensorinstallationsaufwand",
                                                  "Daten bezüglich Netztopologie werden benötigt",
                                                  "Historische Daten werden benötigt",
                                                  "Kleine Leckagen oder Schwachstellen werden selten erkannt"
                                                  ]}
                 )

c3_uc3 = UseCase(name="Klassifikation von Rohrzuständen auf Basis von Akustik- und Vibrationssignalen",
                 description="Dieser Use-Case nutzt direkte Klassifikationsverfahren wie beispielsweise Support Vector "
                             "Machines für die Zuordnung von akustischen Messwerten zu festgelegten Rohrzuständen.",
                 predefined_potential={"Erkennen von vorhandenen Leckagen": 5,
                                       "Ortung von Leckagen": 2,
                                       "Vorbeugung von Fehlern": 5,
                                       "Wenige Fehlalarme": 2,
                                       "Interpretierbarkeit": 3},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 3,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=1,
                 non_applicability_conditions=[no_vibration_data_condition,
                                               no_labels_network_condition,
                                               data_resolution_days_condition,
                                               no_history_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.measurement.2023.11338",
                 pro_contra_arguments={"pro": ["Einfachere Sensorinstallation",
                                               "Auch kleine Leckagen können erkannt werden",
                                               "Kontinuierliche Überwachung des Rohrnetzes ist mit wenig Aufwand "
                                               "verbunden",
                                               "Eine frühzeitige Erkennung von Leckagen ist möglich"
                                               ],
                                       "contra": ["Gelabelte Schadensdaten werden benötigt",
                                                  "Eine sehr hohe Auflösung der Daten wird benötigt",
                                                  "Historische Daten werden benötigt",
                                                  "Viele Fehlalarme sind möglich"
                                                  ]}
                 )

# Control strategies for dh network
c4_uc1 = UseCase(name="Optimierung des Netzbetriebs mithilfe ML-basierter Netzsimulation.",
                 description="Durch die Verwendung eines Reinforcement Learning Ansatzes, in Kombination mit "
                             "Hintergrundwissen über die Netztopologie wird ein  effizientes und dynamisches "
                             "Simulationsmodell erstellt, welches anschließend verwendet wird, um den "
                             "Fernwärmenetzbetrieb hinsichtlich Kosten der Wärmeproduktion und Wärmeeffizienz zu "
                             "optimieren.",
                 predefined_potential={"Energieeffizienz": 5,
                                       "Interpretierbarkeit": 4,
                                       "Kundenkomfort": 1},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 3,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=5,
                 non_applicability_conditions=[no_network_temperatures_condition,
                                               no_flow_rate_condition,
                                               no_heat_data_condition,
                                               no_district_heating_topology_condition,
                                               no_heat_generation_data_condition,
                                               no_ambient_temperature_condition
                                               ],
                 literature_source="https://doi.org/10.1109/TCST.2024.335",
                 pro_contra_arguments={"pro": ["Effiziente dynamische Simulation des Wärmenetzes",
                                               "Transparente Entscheidungsfindung durch Einbezug von "
                                               "Hintergrundwissen in das Neuronale Netz",
                                               "Optimierter Netzbetrieb hinsichtlich Wärmeproduktionskosten und "
                                               "Wärmeeffizienz"],
                                       "contra": ["Viele Metadaten wie bspw. Netztopologie werden benötigt",
                                                  "Hohe Modellkomplexität",
                                                  "Daten aus der Wärmeerzeugung werden benötigt",
                                                  "Nutzerkomfort wird nicht mit einbezogen"
                                                  ]}
                 )

c4_uc2 = UseCase(name="Spitzenlastreduzierung",
                 description="Dieser Use-Case nutzt einen Reinforcement Learning Ansatz, welcher auf Basis eines "
                             "Netzmodells, einer thermodynamischen Modellierung der Gebäude im Fernwärmenetz und "
                             "eines agentenbasierten Nutzerkomfortmodells eine optimale Strategie für die Reduktion "
                             "von Spitzenlasten ermittelt.",
                 predefined_potential={"Energieeffizienz": 5,
                                       "Interpretierbarkeit": 2,
                                       "Kundenkomfort": 5},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 4,
                                    "Rechenaufwand": 5,
                                    "Sensorinstallationsaufwand": 4,
                                    "Implementationsaufwand": 5,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=5,
                 non_applicability_conditions=[no_indoor_temperature_condition,
                                               no_pressure_data_condition,
                                               no_flow_rate_condition,
                                               no_ambient_temperature_condition,
                                               no_building_envelope_condition,
                                               no_district_heating_topology_condition,
                                               no_history_condition,
                                               no_supply_return_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.engappai.202",
                 pro_contra_arguments={"pro": ["Berücksichtigt den Nutzerkomfort explizit",
                                               "Skalierbarer Ansatz",
                                               "Ermöglicht Reduzierung von Spitzenlasten"],
                                       "contra": ["Sehr viele Metadaten über die Gebäude innerhalb des "
                                                  "Fernwärmenetzes werden benötigt",
                                                  "Hohe Modellkomplexität",
                                                  "Hohe Rechenkosten für das Modelltraining",
                                                  "Fernwärmenetz muss modelliert werden"]}
                 )
c4_uc3 = UseCase(name="Flexibilitätsnutzung von Gebäuden durch die Steuerung der Wärmezufuhr",
                 description="In diesem Use-Case wird ein Reinforcement Learning Algorithmus verwendet, um "
                             "thermostatgesteuerte Wärmespeichermöglichkeiten wie Gebäudehüllen im Fernwärmenetz zu "
                             "flexibilisieren. Ziel ist die Nutzung dieser Flexibilitäten für Spitzenlastreduktionen "
                             "und oder Energie-Arbitrage.",
                 predefined_potential={"Energieeffizienz": 5,
                                       "Interpretierbarkeit": 2,
                                       "Kundenkomfort": 2},
                 predefined_effort={"Datenaufbewahrungsaufwand": 5,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 5,
                                    "Sensorinstallationsaufwand": 4,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 5},
                 predefined_risk_value=5,
                 non_applicability_conditions=[no_indoor_temperature_condition,
                                               no_district_heating_topology_condition,
                                               no_network_temperatures_condition,
                                               no_building_envelope_condition,
                                               no_flow_rate_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition
                                               ],
                 literature_source="https://doi.org/10.1016/j.enbuild.2017.08.052",
                 pro_contra_arguments={"pro": ["Kann für Spitzenlastreduktionen verwendet werden",
                                               "Kann zum Zweck von Energie-Arbitragen verwendet werden"
                                               ],
                                       "contra": ["Thermo-hydraulische Simulation des Netzes wird für das Training "
                                                  "benötigt",
                                                  "Daten zur Gebäudehülle werden benötigt",
                                                  "Physikalische Simulationen sind notwendig"
                                                  ]}
                 )

c4_uc4 = UseCase(name="ML-Ersatzmodell für thermo-hydraulische Simulationen",
                 description="Dieser Use-Case verwendet ein Graph-Neural-Network, um bestehende aufwändige "
                             "thermo-hydraulische Simulationsmodelle durch ein schnelleres, effizienteres "
                             "ML-Modell zu ersetzen und Durchflussraten, sowie Temperaturen an verschiedenen "
                             "Stellen im Netz zu simulieren.",
                 predefined_potential={"Energieeffizienz": 4,
                                       "Interpretierbarkeit": 2,
                                       "Kundenkomfort": 2},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 3,
                                    "Datendetailgrad": 2},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_district_heating_topology_condition,
                                               no_network_temperatures_condition,
                                               no_pressure_data_condition,
                                               no_flow_rate_condition,
                                               no_ambient_temperature_condition
                                               ],
                 literature_source="https://hal.science/CETHIL/hal-04462676v1",
                 pro_contra_arguments={"pro": ["Effiziente und schnelle Simulation des Wärmenetzes",
                                               "Kenntnis über Durchflussraten und Temperaturen an verschiedenen "
                                               "Stellen im Netz ohne Messsensorik."
                                               ],
                                       "contra": ["Thermo-hydraulische Simulation des Netzes wird für das Training "
                                                  "benötigt."
                                                  "Viele Metadaten sind notwendig."
                                                  ]}
                 )

# Control strategies for substations
c5_uc1 = UseCase(name="ML-unterstützte Regleroptimierung",
                 description="Dieser Use-Case nutzt die Anwendbarkeit und Effektivität von Methoden des maschinellen "
                             "Lernens (ML) für das Auto- und Continuous-Commissioning von Regelgeräten an realen "
                             "Fernwärme-Hausstationen. Damit wird die automatisierte Anpassung von Regelparametern, "
                             "die sich zunächst in der Werkeinstellung befinden, an die individuellen "
                             "Betriebsbedingungen des jeweiligen Gebäudes erreicht. Dies stellt sicher, dass eine "
                             "optimale Regelung der Hausstationen (HAST) erreicht wird.",
                 predefined_potential={"Reduktion der Rücklauftemperatur": 4,
                                       "Interpretierbarkeit": 3,
                                       "Kundenkomfort": 4},
                 predefined_effort={"Datenaufbewahrungsaufwand": 2,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 1,
                                    "Sensorinstallationsaufwand": 4,
                                    "Implementationsaufwand": 3,
                                    "Datenerhebungsaufwand": 5,
                                    "Datendetailgrad": 4},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_supply_return_condition,
                                               no_substation_pressure_data_condition,
                                               no_substation_flow_rate_condition,
                                               no_ambient_temperature_condition,
                                               no_history_condition,
                                               no_substation_meta_data_condition
                                               ],
                 literature_source="TBD",
                 pro_contra_arguments={"pro": ["Senkung der Rücklauftemperatur neuen Parametersatzes für die Heizkurve",
                                               "Einfaches Einspielen der optimierten Parametersätze",
                                               "Anpassung des Modells an veränderte Umgebungsbedingungen ist nicht "
                                               "aufwändig"],
                                       "contra": ["Aufwändige Simulation als Grundlage",
                                                  "Detaillierte Metadaten von mehreren HAST Komponenten werden benötigt"
                                                  ]}
                 )

c5_uc2 = UseCase(name="ML-basierte Optimierung von Fernwärme-Sekundärkreisen",
                 description="Dieser Use-Case befasst sich mit der Erstellung eines ML-Modells für die optimierte "
                             "Steuerung des Wärmeflusses vom Primärkreislauf in den Sekundärkreislauf durch die "
                             "automatisierte Steuerung von Ventilen. Das Ventilsteuerungsmodell wird dabei auf "
                             "Basis historischer Ventileinstellungsdaten im Kontext mit der Wetterdaten erstellt "
                             "und mit einem ML-Vorhersagemodell für die Vorlauftemperatur im Sekundärkreis bei "
                             "verschiedenen Ventileinstellungen kombiniert.",
                 predefined_potential={"Reduktion der Rücklauftemperatur": 3,
                                       "Interpretierbarkeit": 1,
                                       "Kundenkomfort": 5},
                 predefined_effort={"Datenaufbewahrungsaufwand": 3,
                                    "Kontinuierlicher Aufwand": 2,
                                    "Rechenaufwand": 3,
                                    "Sensorinstallationsaufwand": 3,
                                    "Implementationsaufwand": 4,
                                    "Datenerhebungsaufwand": 4,
                                    "Datendetailgrad": 2},
                 predefined_risk_value=3,
                 non_applicability_conditions=[no_substation_valve_data_condition,
                                               no_substation_pressure_data_condition,
                                               no_substation_flow_rate_condition,
                                               no_history_condition,
                                               no_ambient_temperature_condition,
                                               no_comfort_data_condition,
                                               no_weather_forecast_condition],
                 literature_source="https://doi.org/10.1016/j.energy.2021.122061",
                 pro_contra_arguments={"pro": ["Energieeffizienzsteigerung des HAST-Betriebs",
                                               "Kundenkomfort wird direkt berücksichtigt"
                                               ],
                                       "contra": ["Viele verschieden Daten aus verschiedenen Quellen werden benötigt",
                                                  "Daten aus Wettervorhersagen werden benötigt"
                                                  ]}
                 )
