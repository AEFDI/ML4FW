
"""
Script for defining conditions and assigning question answer lists.
This script initializes all conditions that are used to determine the applicability of use cases based on
specific criteria related to data availability, label availability, metadata availability, user-specific conditions,
and data quality.

Defined Conditions:

1. no_flow_rate_condition: 
   Checks if flow rate data is not available.

2. no_supply_return_condition: 
   Checks if supply and return temperature data is not available.

3. no_network_temperatures_condition: 
   Checks if network temperature data is not available.

4. no_ambient_temperature_condition: 
   Checks if ambient temperature data is not available.

5. no_heat_data_condition:
   Checks if heat output data is not available.

6. no_energy_data_condition:
   Checks if energy data is not available.

7. no_pressure_data_condition: 
   Checks if pressure data is not available.

8. no_heat_storage_condition: 
   Checks if data regarding heat storage is not available.

9. no_vibration_data_condition:
   Checks if vibration data is not available.

10. no_substation_valve_data_condition: 
    Checks if valve data in substations is not available.

11. no_substation_pressure_data_condition: 
    Checks if pressure data in substations is not available.

12. no_substation_flow_rate_condition: 
    Checks if flow rate data in substations is not available.

13. no_weather_forecast_condition: 
    Checks if weather forecast data in substations is not available.

14. no_labels_substation_condition: 
   Checks if maintenance label data in substations is not available.

15. no_labels_network_condition: 
    Checks if maintenance label data in the heating network is not available.

16. no_network_topology_condition:
    Checks if network topology data is not available (category 3 question for pipline maintenance).

17. no_district_heating_topology_condition:
    Checks if network topology data is not available (category 4 question for network operation strategies).

18. no_heat_generation_data_condition: 
    Checks if heat generation data is not available.

19. no_indoor_temperature_condition: 
    Checks if indoor temperature data is not available.

20. no_building_data_condition: 
    Checks if building metadata is not available.

21. no_building_envelope_condition: 
    Checks if building envelope data is not available.

22. no_comfort_data_condition: 
    Checks if user comfort data is not available.

23. no_substation_meta_data_condition: 
    Checks if metadata for substations is not available.

24. no_waiting_condition: 
    Checks for user-specific preference related to waiting for the right environmental conditions.

25. pipeline_depth_condition: 
    Verifies user-specific conditions regarding pipeline depth.

26. small_num_substation_condition: 
    Checks if the number of substations is below the specified minimum for clustering use cases.

27. no_history_condition: 
    Confirms that there are no historical data recorded. This makes use cases which a longer history
    inapplicable.

28. month_history_condition: 
    Verifies if there is some historical data for a few months. This makes use cases which a longer history
    inapplicable.

29. data_resolution_1min_condition: 
    Checks if the data resolution is minute-based. This makes use cases which need higher resolutions inapplicable.

30. data_resolution_1h_condition: 
    Confirms if the data resolution is hour-based. This makes use cases which need higher resolutions inapplicable.

31. data_resolution_days_condition: 
    Ensures that the data resolution is daily. This makes use cases which need higher resolutions inapplicable.
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
