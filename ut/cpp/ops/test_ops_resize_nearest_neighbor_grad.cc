/**
 * Copyright 2023 Huawei Technologies Co., Ltd
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
#include <vector>
#include <memory>
#include "abstract/abstract_value.h"
#include "abstract/dshape.h"
#include "common/common_test.h"
#include "ir/dtype/type.h"
#include "ir/primitive.h"
#include "infer/ops_func_impl/resize_nearest_neighbor_grad.h"
#include "ops/test_ops.h"
#include "test_value_utils.h"

namespace mindspore {
namespace ops {
#define I64(x) (static_cast<int64_t>((x)))
struct ResizeNearestNeighborGradOpParams {
  ShapeVector grads_shape;
  TypePtr grads_type;
  ValuePtr size;
  ValuePtr align_corners;
  ShapeVector y_shape;
  TypePtr y_type;
};
class TestResizeNearestNeighborGrad : public TestOps,
                                      public testing::WithParamInterface<ResizeNearestNeighborGradOpParams> {};

TEST_P(TestResizeNearestNeighborGrad, resize_nearest_neighbor_grad_shape) {
  auto primitive = std::make_shared<Primitive>("ResizeNearestNeighborGrad");
  ASSERT_NE(primitive, nullptr);
  const auto &param = GetParam();
  auto grads = std::make_shared<abstract::AbstractTensor>(param.grads_type, param.grads_shape);
  ASSERT_NE(grads, nullptr);
  std::vector<abstract::AbstractBasePtr> input_args{std::move(grads)};
  auto size = param.size->ToAbstract();
  ASSERT_NE(size, nullptr);
  input_args.push_back(std::move(size));
  auto align_corners = param.align_corners->ToAbstract();
  ASSERT_NE(align_corners, nullptr);
  input_args.push_back(std::move(align_corners));

  auto infer_impl = std::make_shared<ResizeNearestNeighborGradFuncImpl>();
  ASSERT_NE(infer_impl, nullptr);
  auto infer_shape = infer_impl->InferShape(primitive, input_args);
  ASSERT_NE(infer_shape, nullptr);
  auto infer_type = infer_impl->InferType(primitive, input_args);
  ASSERT_NE(infer_type, nullptr);

  auto expect_shape = std::make_shared<abstract::Shape>(param.y_shape);
  ASSERT_NE(expect_shape, nullptr);
  auto expect_type = std::make_shared<TensorType>(param.y_type);
  ASSERT_NE(expect_type, nullptr);
  ASSERT_TRUE(*infer_shape == *expect_shape);
  ASSERT_TRUE(*infer_type == *expect_type);
}

INSTANTIATE_TEST_CASE_P(
  TestResizeNearestNeighborGradGroup, TestResizeNearestNeighborGrad,
  testing::Values(
    ResizeNearestNeighborGradOpParams{
      {1, 5, 3, 3}, kInt32, CreateTuple({I64(6), I64(6)}), CreateScalar<bool>(False), {1, 5, 6, 6}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {1, 5, 3, 3}, kInt32, CreateTuple({kValueAny, I64(6)}), CreateScalar<bool>(False), {1, 5, -1, 6}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {1, 5, 3, 3}, kInt32, CreateScalar(kValueAny), CreateScalar<bool>(False), {1, 5, -1, -1}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {1, -1, 3, 3}, kInt32, CreateTuple({kValueAny, I64(6)}), CreateScalar<bool>(False), {1, -1, -1, 6}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {1, -1, 3, 3}, kInt32, CreateScalar(kValueAny), CreateScalar<bool>(False), {1, -1, -1, -1}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {1, 5, -1, -1}, kInt32, CreateTuple({I64(6), I64(6)}), CreateScalar<bool>(False), {1, 5, 6, 6}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {-2}, kInt32, CreateScalar(kValueAny), CreateScalar<bool>(False), {-1, -1, -1, -1}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {-2}, kInt32, CreateTuple({I64(6), I64(6)}), CreateScalar<bool>(False), {-1, -1, 6, 6}, kInt32},
    ResizeNearestNeighborGradOpParams{
      {-2}, kInt32, CreateTuple({kValueAny, I64(6)}), CreateScalar<bool>(False), {-1, -1, -1, 6}, kInt32}));
}  // namespace ops
}  // namespace mindspore
