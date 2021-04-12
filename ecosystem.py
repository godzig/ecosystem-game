# Copyright 2021 Mike Godwin
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

from typing import Sequence
import time
import pandas as pd
from scenario import Scenario

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

flags.DEFINE_integer('boards', 1000000, 'Number of boards.')
flags.DEFINE_integer('players', 3, 'Reset credentials.')
flags.DEFINE_integer('floor', -10, 'Unknown.')
flags.DEFINE_string('output_csv', 'output.csv', 'Output CSV.')


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  logging.info('Output will be written to %s', FLAGS.output_csv)

  start_time = time.time()
  logging.info('Simulation started at %s', start_time)
  s = Scenario(boards=FLAGS.boards, players=FLAGS.players, floor=FLAGS.floor)
  df = pd.DataFrame(s.report())
  df.to_csv(FLAGS.output_csv, mode='w', header=True)
  logging.info('{} seconds'.format(time.time() - start_time))


if __name__ == '__main__':
  app.run(main)
