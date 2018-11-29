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

import mock

from optimizely.helpers import condition as condition_helper

from tests import base

browserConditionSafari = ['browser_type', 'safari', 'custom_attribute', 'exact']
booleanCondition = ['is_firefox', True, 'custom_attribute', 'exact']
integerCondition = ['num_users', 10, 'custom_attribute', 'exact']
doubleCondition = ['pi_value', 3.14, 'custom_attribute', 'exact']


class CustomAttributeConditionEvaluator(base.BaseTest):

  def setUp(self):
    base.BaseTest.setUp(self)
    self.condition_list = [browserConditionSafari, booleanCondition, integerCondition, doubleCondition]

  def test_evaluate__returns_true__when_attributes_pass_audience_condition(self):
    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.condition_list, {'browser_type': 'safari'}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_evaluate__returns_false__when_attributes_fail_audience_condition(self):
    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.condition_list, {'browser_type': 'chrome'}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_evaluate__evaluates__different_typed_attributes(self):
    userAttributes = {
      'browser_type': 'safari',
      'is_firefox': True,
      'num_users': 10,
      'pi_value': 3.14,
    }

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.condition_list, userAttributes
    )

    self.assertStrictTrue(evaluator.evaluate(0))
    self.assertStrictTrue(evaluator.evaluate(1))
    self.assertStrictTrue(evaluator.evaluate(2))
    self.assertStrictTrue(evaluator.evaluate(3))

  def test_evaluate__returns_null__when_condition_has_an_invalid_match_property(self):

    condition_list = [['weird_condition', 'hi', 'custom_attribute', 'weird_match']]

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      condition_list, {'weird_condition': 'hi'}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_evaluate__returns_null__when_condition_has_an_type_match_property(self):

    condition_list = [['weird_condition', 'hi', 'weird_type', 'exact']]

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      condition_list, {'weird_condition': 'hi'}
    )

    self.assertIsNone(evaluator.evaluate(0))

  exists_condition_list = [['input_value', None, 'custom_attribute', 'exists']]

  def test_exists__returns_false__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_exists__returns_false__when_user_provided_value_is_null(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {'input_value': None}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_exists__returns_true__when_user_provided_value_is_string(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {'input_value': 'hi'}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_exists__returns_true__when_user_provided_value_is_number(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {'input_value': 10}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {'input_value': 10.0}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_exists__returns_true__when_user_provided_value_is_boolean(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exists_condition_list, {'input_value': False}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  exact_string_condition_list = [['favorite_constellation', 'Lacerta', 'custom_attribute', 'exact']]

  def test_exact_string__returns_true__when_user_provided_value_is_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_string_condition_list, {'favorite_constellation': 'Lacerta'}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_exact_string__returns_false__when_user_provided_value_is_not_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_string_condition_list, {'favorite_constellation': 'The Big Dipper'}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_exact_string__returns_null__when_user_provided_value_is_different_type_from_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_string_condition_list, {'favorite_constellation': False}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_exact_string__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_string_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))

  exact_number_condition_list = [['lasers_count', 9000, 'custom_attribute', 'exact']]

  def test_exact_number__returns_true__when_user_provided_value_is_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_number_condition_list, {'lasers_count': 9000}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_number_condition_list, {'lasers_count': 9000.0}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_exact_number__returns_false__when_user_provided_value_is_not_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_number_condition_list, {'lasers_count': 8000}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_exact_number__returns_null__when_user_provided_value_is_different_type_from_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_number_condition_list, {'lasers_count': 'hi'}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_exact_number__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_number_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))

  exact_bool_condition_list = [['did_register_user', False, 'custom_attribute', 'exact']]

  def test_exact_bool__returns_true__when_user_provided_value_is_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_bool_condition_list, {'did_register_user': False}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_exact_bool__returns_false__when_user_provided_value_is_not_equal_to_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_bool_condition_list, {'did_register_user': True}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_exact_bool__returns_null__when_user_provided_value_is_different_type_from_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_bool_condition_list, {'did_register_user': 0}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_exact_bool__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.exact_bool_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))

  substring_condition_list = [['headline_text', 'buy now', 'custom_attribute', 'substring']]

  def test_substring__returns_true__when_condition_value_is_substring_of_user_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.substring_condition_list, {'headline_text': 'Limited time, buy now!'}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_substring__returns_false__when_condition_value_is_not_a_substring_of_user_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.substring_condition_list, {'headline_text': 'Breaking news!'}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_substring__returns_null__when_user_provided_value_not_a_string(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.substring_condition_list, {'headline_text': 10}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_substring__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.substring_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))

  gt_condition_list = [['meters_travelled', 48.2, 'custom_attribute', 'gt']]

  def test_greater_than__returns_true__when_user_value_greater_than_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.gt_condition_list, {'meters_travelled': 48.3}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.gt_condition_list, {'meters_travelled': 49}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_greater_than__returns_false__when_user_value_not_greater_than_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.gt_condition_list, {'meters_travelled': 48.2}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_greater_than__returns_null__when_user_value_is_not_a_number(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.gt_condition_list, {'meters_travelled': 'a long way'}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_greater_than__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.gt_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))

  lt_condition_list = [['meters_travelled', 48.2, 'custom_attribute', 'lt']]

  def test_less_than__returns_true__when_user_value_less_than_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.lt_condition_list, {'meters_travelled': 48.1}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.lt_condition_list, {'meters_travelled': 48}
    )

    self.assertStrictTrue(evaluator.evaluate(0))

  def test_less_than__returns_false__when_user_value_not_less_than_condition_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.lt_condition_list, {'meters_travelled': 48.2}
    )

    self.assertStrictFalse(evaluator.evaluate(0))

  def test_less_than__returns_null__when_user_value_is_not_a_number(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.lt_condition_list, {'meters_travelled': False}
    )

    self.assertIsNone(evaluator.evaluate(0))

  def test_less_than__returns_null__when_no_user_provided_value(self):

    evaluator = condition_helper.CustomAttributeConditionEvaluator(
      self.lt_condition_list, {}
    )

    self.assertIsNone(evaluator.evaluate(0))


class ConditionDecoderTests(base.BaseTest):

  def test_loads(self):
    """ Test that loads correctly sets condition structure and list. """

    condition_structure, condition_list = condition_helper.loads(
      self.config_dict['audiences'][0]['conditions']
    )

    self.assertEqual(['and', ['or', ['or', 0]]], condition_structure)
    self.assertEqual([['test_attribute', 'test_value_1', 'custom_attribute', 'exact']], condition_list)

  def test_audience_condition_deserializer_defaults(self):
    """ Test that audience_condition_deserializer defaults to None for
        item 0(name), 1(value), 2(type) and to ConditionMatchTypes.EXACT for item 3(match). """

    browserConditionSafari = {}

    items = condition_helper._audience_condition_deserializer(browserConditionSafari)
    self.assertIsNone(items[0])
    self.assertIsNone(items[1])
    self.assertIsNone(items[2])
    self.assertEqual(
      condition_helper.ConditionMatchTypes.EXACT,
      items[3]
    )
