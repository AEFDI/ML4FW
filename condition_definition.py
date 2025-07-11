
"""
Script for defining all categories and assigning question answer lists.
"""

from settings import min_substations_for_clustering
from question_definition import *
from condition import Condition

no_flow_rate_condition = Condition(condition_type="data availability",
                                   question_answer_list=[{gen_flow_rate_1.question_text: "Nein"},
                                                         {gen_flow_rate_2.question_text: "Nein"},
                                                         {gen_flow_rate_3.question_text: "Nein"}])

no_supply_return_condition = Condition(condition_type="data availability",
                                       question_answer_list=[
                                           {gen_supply_and_return_temperature_1.question_text: "Nein"},
                                           {gen_supply_and_return_temperature_2.question_text: "Nein"},
                                           {gen_supply_and_return_temperature_3.question_text: "Nein"}])

no_network_temperatures_condition = Condition(condition_type="data availability",
                                              question_answer_list=[
                                                  {gen_network_temperature_1.question_text: "Nein"},
                                                  {gen_network_temperature_2.question_text: "Nein"},
                                                  {gen_network_temperature_3.question_text: "Nein"}])

no_ambient_temperature_condition = Condition(condition_type="data availability",
                                             question_answer_list=[{gen_ambient_temp_1.question_text: "Nein"},
                                                                   {gen_ambient_temp_2.question_text: "Nein"},
                                                                   {gen_ambient_temp_3.question_text: "Nein"}])

no_heat_data_condition = Condition(condition_type="data availability",
                                   question_answer_list=[{gen_heat_1.question_text: "Nein"},
                                                         {gen_heat_2.question_text: "Nein"},
                                                         {gen_heat_3.question_text: "Nein"}])

no_energy_data_condition = Condition(condition_type="data availability",
                                     question_answer_list=[{gen_energy_1.question_text: "Nein"},
                                                           {gen_energy_2.question_text: "Nein"},
                                                           {gen_energy_3.question_text: "Nein"}])

no_pressure_data_condition = Condition(condition_type="data availability",
                                       question_answer_list=[{gen_pressure_1.question_text: "Nein"},
                                                             {gen_pressure_2.question_text: "Nein"},
                                                             {gen_pressure_3.question_text: "Nein"}])

no_heat_storage_condition = Condition(condition_type="data availability",
                                      question_answer_list=[{cat_1_heat_storages_data_1.question_text: "Nein"},
                                                            {cat_1_heat_storages_data_2.question_text: "Nein"}])

no_vibration_data_condition = Condition(condition_type="data availability",
                                        question_answer_list=[{cat_3_vibration_1.question_text: "Nein"},
                                                              {cat_3_vibration_2.question_text: "Nein"},
                                                              {cat_3_vibration_3.question_text: "Nein"}])

no_substation_valve_data_condition = Condition(condition_type="data availability",
                                               question_answer_list=[{cat_5_valve_data_1.question_text: "Nein"},
                                                                     {cat_5_valve_data_2.question_text: "Nein"},
                                                                     {cat_5_valve_data_3.question_text: "Nein"}])

no_substation_pressure_data_condition = Condition(condition_type="data availability",
                                                  question_answer_list=[{cat_5_pressure_data_1.question_text: "Nein"},
                                                                        {cat_5_pressure_data_2.question_text: "Nein"},
                                                                        {cat_5_pressure_data_3.question_text: "Nein"}])

no_substation_flow_rate_condition = Condition(condition_type="data availability",
                                              question_answer_list=[{cat_5_flow_rate_1.question_text: "Nein"},
                                                                    {cat_5_flow_rate_2.question_text: "Nein"},
                                                                    {cat_5_flow_rate_3.question_text: "Nein"}])

no_weather_forecast_condition = Condition(condition_type="data availability",
                                          question_answer_list=[{gen_weather_forecast_1.question_text: "Nein"},
                                                                {gen_weather_forecast_2.question_text: "Nein"}])

no_labels_substation_condition = Condition(condition_type="label availability",
                                           question_answer_list=[{cat_2_labels_1.question_text: "Nein"},
                                                                 {cat_2_labels_2.question_text: "Nein"}])

no_labels_network_condition = Condition(condition_type="label availability",
                                        question_answer_list=[{cat_3_labels_1.question_text: "Nein"},
                                                              {cat_3_labels_2.question_text: "Nein"}])

no_network_topology_condition = Condition(condition_type="meta data availability",
                                          question_answer_list=[{cat_3_network_topology.question_text: "Nein"}])

no_district_heating_topology_condition = Condition(condition_type="meta data availability",
                                                   question_answer_list=[
                                                       {cat_4_network_topology.question_text: "Nein"}])

no_heat_generation_data_condition = Condition(condition_type="meta data availability",
                                              question_answer_list=[{cat_4_heat_generation.question_text: "Nein"}])

no_indoor_temperature_condition = Condition(condition_type="meta data availability",
                                            question_answer_list=[{cat_4_indoor_temperatures.question_text: "Nein"}])

no_building_data_condition = Condition(condition_type="meta data availability",
                                       question_answer_list=[{cat_1_building_data.question_text: "Nein"}])

no_building_envelope_condition = Condition(condition_type="meta data availability",
                                           question_answer_list=[{cat_4_building_data.question_text: "Nein"}])

no_comfort_data_condition = Condition(condition_type="meta data availability",
                                      question_answer_list=[{cat_5_user_comfort.question_text: "Nein"}])

no_substation_meta_data_condition = Condition(condition_type="meta data availability",
                                              question_answer_list=[{cat_5_substation_meta_data.question_text: "Nein"}])

no_waiting_condition = Condition(condition_type="user specific",
                                 question_answer_list=[{cat_3_labels_1.question_text: "Nein"}])

pipeline_depth_condition = Condition(condition_type="user specific",
                                     question_answer_list=[{cat_3_pipeline_depth.question_text: "Nein"}])

small_num_substation_condition = Condition(condition_type="user specific",
                                           question_answer_list=[{
                                               cat_2_substation_amount.question_text: f"Weniger als {min_substations_for_clustering}"}])

no_history_condition = Condition(condition_type="data quality",
                                 question_answer_list=[{
                                     gen_data_history.question_text: "Es gibt keine historisch aufgezeichneten Daten"}])

month_history_condition = Condition(condition_type="data quality",
                                    question_answer_list=[{gen_data_history.question_text: "Einige Monate"}])

data_resolution_1min_condition = Condition(condition_type="data quality",
                                           question_answer_list=[{gen_data_resolution.question_text: "Minütlich"}])

data_resolution_1h_condition = Condition(condition_type="data quality",
                                         question_answer_list=[{gen_data_resolution.question_text: "Stündlich"}])

data_resolution_days_condition = Condition(condition_type="data quality",
                                           question_answer_list=[
                                               {gen_data_resolution.question_text: "Täglich oder niedriger"}])
