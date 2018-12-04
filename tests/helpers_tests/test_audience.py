# Copyright 2016-2017, Optimizely
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from tests import base
from optimizely.helpers import audience

chromeUserAudience = {
  'conditions': ['and', {
    'name': 'browser_type',
    'value': 'chrome',
    'type': 'custom_attribute',
  }],
}

iphoneUserAudience = {
  'conditions': ['and', {
    'name': 'device_model',
    'value': 'iphone',
    'type': 'custom_attribute',
  }],
}

conditionsPassingWithNoAttrs = ['not', {
  'match': 'exists',
  'name': 'input_value',
  'type': 'custom_attribute',
}]

conditionsPassingWithNoAttrsAudience = {
  'conditions': conditionsPassingWithNoAttrs,
}

audiencesById = {
  0: chromeUserAudience,
  1: iphoneUserAudience,
  2: conditionsPassingWithNoAttrsAudience,
}


class AudienceTest(base.BaseTest):

  def test_is_user_in_experiment__no_audience(self):
    """ Test that is_user_in_experiment returns True when experiment is using no audience. """

    user_attributes = {}

    # Both Audience Ids and Conditions are Empty
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = []
    experiment.audienceConditions = []
    self.assertTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

    # Audience Ids exist but Audience Conditions is Empty
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = ['11154']
    experiment.audienceConditions = []
    self.assertTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

    # Audience Ids is Empty and  Audience Conditions is None
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = []
    experiment.audienceConditions = None
    self.assertTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))


  def test_is_user_in_experiment__with_audience(self):
    """ Test that is_user_in_experiment evaluates non-empty audience. 
        Test that is_user_in_experiment uses not None audienceConditions and ignores audienceIds.
        Test that is_user_in_experiment uses audienceIds when audienceConditions is None.
    """

    user_attributes = {'test_attribute': 'test_value_1'}
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = ['11154']

    # Both Audience Ids and Conditions exist
    with mock.patch('optimizely.helpers.condition_tree_evaluator.evaluate') as cond_tree_eval:

      experiment.audienceConditions = ['and', ['or', '3468206642', '3988293898'], ['or', '3988293899',
                                     '3468206646', '3468206647', '3468206644', '3468206643']]
      audience.is_user_in_experiment(self.project_config, experiment, user_attributes)

    self.assertEqual(experiment.audienceConditions,
      cond_tree_eval.call_args[0][0])

    # Audience Ids exist but Audience Conditions is None
    with mock.patch('optimizely.helpers.condition_tree_evaluator.evaluate') as cond_tree_eval:
      
      experiment.audienceConditions = None
      audience.is_user_in_experiment(self.project_config, experiment, user_attributes)

    self.assertEqual(experiment.audienceIds,
      cond_tree_eval.call_args[0][0])





  # def test_is_user_in_experiment__no_attributes(self):
  #   """ Test that is_user_in_experiment defaults attributes to empty Dict and
  #       is_match does get called with empty attributes. """

  #   with mock.patch('optimizely.helpers.audience.is_match') as mock_is_match:
  #     audience.is_user_in_experiment(
  #       self.project_config,
  #       self.project_config.get_experiment_from_key('test_experiment'), None
  #     )

  #   mock_is_match.assert_called_once_with(
  #     self.optimizely.config.get_audience('11154'), {}
  #   )

  #   with mock.patch('optimizely.helpers.audience.is_match') as mock_is_match:
  #     audience.is_user_in_experiment(
  #       self.project_config,
  #       self.project_config.get_experiment_from_key('test_experiment'), {}
  #     )

  #   mock_is_match.assert_called_once_with(
  #     self.optimizely.config.get_audience('11154'), {}
  #   )

  # def test_is_user_in_experiment__audience_conditions_are_met(self):
  #   """ Test that is_user_in_experiment returns True when audience conditions are met. """

  #   user_attributes = {
  #     'test_attribute': 'test_value_1',
  #     'browser_type': 'firefox',
  #     'location': 'San Francisco'
  #   }

  #   with mock.patch('optimizely.helpers.audience.is_match', return_value=True) as mock_is_match:
  #     self.assertTrue(audience.is_user_in_experiment(self.project_config,
  #                                                    self.project_config.get_experiment_from_key('test_experiment'),
  #                                                    user_attributes))
  #   mock_is_match.assert_called_once_with(self.optimizely.config.get_audience('11154'), user_attributes)

  # def test_is_user_in_experiment__audience_conditions_not_met(self):
  #   """ Test that is_user_in_experiment returns False when audience conditions are not met. """

  #   user_attributes = {
  #     'test_attribute': 'wrong_test_value',
  #     'browser_type': 'chrome',
  #     'location': 'San Francisco'
  #   }

  #   with mock.patch('optimizely.helpers.audience.is_match', return_value=False) as mock_is_match:
  #     self.assertFalse(audience.is_user_in_experiment(self.project_config,
  #                                                     self.project_config.get_experiment_from_key('test_experiment'),
  #                                                     user_attributes))
  #   mock_is_match.assert_called_once_with(self.optimizely.config.get_audience('11154'), user_attributes)
