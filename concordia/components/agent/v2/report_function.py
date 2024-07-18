# Copyright 2023 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""This components report what the function returns at the moment.

For example, can be used for reporting current time
current_time_component = ReportFunction(
    'Current time',
    function=clock.current_time_interval_str)
"""

from typing import Callable
from concordia.components.agent.v2 import action_spec_ignored
from concordia.typing import entity as entity_lib

DEFAULT_PRE_ACT_LABEL = 'Report'


class ReportFunction(action_spec_ignored.ActionSpecIgnored):
  """A component that reports what the function returns at the moment."""

  def __init__(
      self,
      function: Callable[[], str],
      pre_act_label: str = DEFAULT_PRE_ACT_LABEL,
  ):
    """Initializes the component.

    Args:
      function: the function that returns a string to report as state of the
        component.
      pre_act_label: Prefix to add to the output of the component when called
        in `pre_act`.
    """
    self._function = function
    self._pre_act_label = pre_act_label
    self._last_log = None

  def _make_pre_act_context(self) -> str:
    """Returns state of this component obtained by calling a function."""
    state = self._function()
    self._last_log = {
        'State': state,
    }
    return state

  def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
    context = super().pre_act(action_spec)
    return  f'{self._pre_act_label}: {context}'

  def get_last_log(self):
    if self._last_log:
      return self._last_log.copy()
