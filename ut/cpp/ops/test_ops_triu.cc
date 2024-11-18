/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "ops/utils/general_infer_utils.h"

namespace mindspore::ops {
namespace {
std::vector<GeneralInferParam> prepare_params() {
  GeneralInferParamGenerator generator;
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{2, 3}, kNumberTypeFloat32},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(0)}})
    .FeedExpectedOutput({{2, 3}}, {kNumberTypeFloat32});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{2, 3, 4}, kNumberTypeFloat32},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(2)}})
    .FeedExpectedOutput({{2, 3, 4}}, {kNumberTypeFloat32});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{2, 3}, kNumberTypeFloat16},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(0)}})
    .FeedExpectedOutput({{2, 3}}, {kNumberTypeFloat16});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{2, 3, 4}, kNumberTypeBFloat16},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(2)}})
    .FeedExpectedOutput({{2, 3, 4}}, {kNumberTypeBFloat16});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{-1, -1}, kNumberTypeFloat32},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(0)}})
    .FeedExpectedOutput({{-1, -1}}, {kNumberTypeFloat32});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{-2}, kNumberTypeFloat32},
                    InferInfoParam{ShapeVector{}, kNumberTypeInt64, CreateScalar<int64_t>(2)}})
    .FeedExpectedOutput({{-2}}, {kNumberTypeFloat32});
  generator
    .FeedInputArgs(
      {InferInfoParam{ShapeVector{2, 3, 4, 5}, kNumberTypeFloat64}, InferInfoParam{ShapeVector{}, kNumberTypeInt64}})
    .FeedExpectedOutput({{2, 3, 4, 5}}, {kNumberTypeFloat64});
  generator
    .FeedInputArgs(
      {InferInfoParam{ShapeVector{-1, -1}, kNumberTypeUInt8}, InferInfoParam{ShapeVector{}, kNumberTypeInt64}})
    .FeedExpectedOutput({{-1, -1}}, {kNumberTypeUInt8});
  generator
    .FeedInputArgs({InferInfoParam{ShapeVector{-2}, kNumberTypeBool}, InferInfoParam{ShapeVector{}, kNumberTypeInt64}})
    .FeedExpectedOutput({{-2}}, {kNumberTypeBool});
  return generator.Generate();
}
}  // namespace

INSTANTIATE_TEST_CASE_P(Triu, GeneralInferTest, testing::ValuesIn(prepare_params()));
}  // namespace mindspore::ops
