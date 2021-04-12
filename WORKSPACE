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

workspace(name = "com_godzig_ecosystem")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "rules_python",
    commit = "5d6c0a2f154f4ebdc4e9d3fda7e5e33f61bef4da",
    remote = "https://github.com/bazelbuild/rules_python.git",
    shallow_since = "1618187696 +1000",
)

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "py_deps",
    requirements = "//:requirements.txt",
)
