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
#include "ops/test_ops_cmp_utils.h"
#include "infer/ops_func_impl/acos.h"
#include "infer/ops_func_impl/acosh.h"
#include "infer/ops_func_impl/asin.h"
#include "infer/ops_func_impl/asinh.h"
#include "infer/ops_func_impl/atan.h"
#include "infer/ops_func_impl/atanh.h"

namespace mindspore {
namespace ops {
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(ACos);
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(Acosh);
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(Asin);
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(Asinh);
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(Atan);
ELTWISE_OP_FUNC_IMPL_TEST_WITH_DEFAULT_CASES(Atanh);
}  // namespace ops
}  // namespace mindspore
