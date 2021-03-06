# Copyright 2016-2018, Optimizely
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

import json
import mock

from optimizely import entities
from optimizely import optimizely
from optimizely.helpers import audience
from tests import base


class AudienceTest(base.BaseTest):

  def test_is_user_in_experiment__no_audience(self):
    """ Test that is_user_in_experiment returns True when experiment is using no audience. """

    user_attributes = {}

    # Both Audience Ids and Conditions are Empty
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = []
    experiment.audienceConditions = []
    self.assertStrictTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

    # Audience Ids exist but Audience Conditions is Empty
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = ['11154']
    experiment.audienceConditions = []
    self.assertStrictTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

    # Audience Ids is Empty and  Audience Conditions is None
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = []
    experiment.audienceConditions = None
    self.assertStrictTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

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

  def test_is_user_in_experiment__no_attributes(self):
    """ Test that is_user_in_experiment evaluates audience when attributes are empty.
        Test that is_user_in_experiment defaults attributes to empty dict when attributes is None.
    """
    experiment = self.project_config.get_experiment_from_key('test_experiment')

    # attributes set to empty dict
    with mock.patch('optimizely.helpers.condition.CustomAttributeConditionEvaluator') as custom_attr_eval:
      audience.is_user_in_experiment(self.project_config, experiment, {})

    self.assertEqual({}, custom_attr_eval.call_args[0][1])

    # attributes set to None
    with mock.patch('optimizely.helpers.condition.CustomAttributeConditionEvaluator') as custom_attr_eval:
      audience.is_user_in_experiment(self.project_config, experiment, None)

    self.assertEqual({}, custom_attr_eval.call_args[0][1])

  def test_is_user_in_experiment__returns_True__when_condition_tree_evaluator_returns_True(self):
    """ Test that is_user_in_experiment returns True when call to condition_tree_evaluator returns True. """

    user_attributes = {'test_attribute': 'test_value_1'}
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    with mock.patch('optimizely.helpers.condition_tree_evaluator.evaluate', return_value=True) as cond_tree_eval:

      self.assertStrictTrue(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

  def test_is_user_in_experiment__returns_False__when_condition_tree_evaluator_returns_None_or_False(self):
    """ Test that is_user_in_experiment returns False when call to condition_tree_evaluator returns None or False. """

    user_attributes = {'test_attribute': 'test_value_1'}
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    with mock.patch('optimizely.helpers.condition_tree_evaluator.evaluate', return_value=None) as cond_tree_eval:

      self.assertStrictFalse(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

    with mock.patch('optimizely.helpers.condition_tree_evaluator.evaluate', return_value=False) as cond_tree_eval:

      self.assertStrictFalse(audience.is_user_in_experiment(self.project_config, experiment, user_attributes))

  def test_is_user_in_experiment__evaluates_audienceIds(self):
    """ Test that is_user_in_experiment correctly evaluates audience Ids and
        calls custom attribute evaluator for leaf nodes. """

    user_attributes = {'test_attribute': 'test_value_1'}
    experiment = self.project_config.get_experiment_from_key('test_experiment')
    experiment.audienceIds = ['11154', '11159']
    experiment.audienceConditions = None

    with mock.patch('optimizely.helpers.condition.CustomAttributeConditionEvaluator') as custom_attr_eval:
      audience.is_user_in_experiment(self.project_config, experiment, {})

    audience_11154 = self.project_config.get_audience('11154')
    audience_11159 = self.project_config.get_audience('11159')
    custom_attr_eval.assert_has_calls([
      mock.call(audience_11154.conditionList, {}),
      mock.call(audience_11159.conditionList, {}),
      mock.call().evaluate(0),
      mock.call().evaluate(0)
    ], any_order=True)

  def test_is_user_in_experiment__evaluates_audience_conditions(self):
    """ Test that is_user_in_experiment correctly evaluates audienceConditions and
        calls custom attribute evaluator for leaf nodes. """

    opt_obj = optimizely.Optimizely(json.dumps(self.config_dict_with_typed_audiences))
    project_config = opt_obj.config
    experiment = project_config.get_experiment_from_key('audience_combinations_experiment')
    experiment.audienceIds = []
    experiment.audienceConditions = ['or', ['or', '3468206642', '3988293898'], ['or', '3988293899', '3468206646', ]]

    with mock.patch('optimizely.helpers.condition.CustomAttributeConditionEvaluator') as custom_attr_eval:
      audience.is_user_in_experiment(project_config, experiment, {})

    audience_3468206642 = project_config.get_audience('3468206642')
    audience_3988293898 = project_config.get_audience('3988293898')
    audience_3988293899 = project_config.get_audience('3988293899')
    audience_3468206646 = project_config.get_audience('3468206646')

    custom_attr_eval.assert_has_calls([
      mock.call(audience_3468206642.conditionList, {}),
      mock.call(audience_3988293898.conditionList, {}),
      mock.call(audience_3988293899.conditionList, {}),
      mock.call(audience_3468206646.conditionList, {}),
      mock.call().evaluate(0),
      mock.call().evaluate(0),
      mock.call().evaluate(0),
      mock.call().evaluate(0)
    ], any_order=True)

  def test_is_user_in_experiment__evaluates_audience_conditions_leaf_node(self):
    """ Test that is_user_in_experiment correctly evaluates leaf node in audienceConditions. """

    opt_obj = optimizely.Optimizely(json.dumps(self.config_dict_with_typed_audiences))
    project_config = opt_obj.config
    experiment = project_config.get_experiment_from_key('audience_combinations_experiment')
    experiment.audienceConditions = '3468206645'

    with mock.patch('optimizely.helpers.condition.CustomAttributeConditionEvaluator') as custom_attr_eval:
      audience.is_user_in_experiment(project_config, experiment, {})

    audience_3468206645 = project_config.get_audience('3468206645')

    custom_attr_eval.assert_has_calls([
        mock.call(audience_3468206645.conditionList, {}),
        mock.call().evaluate(0),
        mock.call().evaluate(1),
    ], any_order=True)
