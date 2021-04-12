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

load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "ecosystem",
    srcs = ["ecosystem.py"],
    python_version = "PY3",
    deps = [
        ":scenario",
        requirement("absl-py"),
    ],
)

py_library(
    name = "game",
    srcs = ["game.py"],
    srcs_version = "PY3",
    deps = [
        requirement("pandas"),
        requirement("absl-py"),
        ":player",
    ],
)

py_library(
    name = "player",
    srcs = ["player.py"],
    srcs_version = "PY3",
    deps = [
        requirement("absl-py"),
    ],
)

py_library(
    name = "scenario",
    srcs = ["scenario.py"],
    srcs_version = "PY3",
    deps = [
        ":game",
        requirement("absl-py"),
    ],
)

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
)
