# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

import dataclasses
from typing import Optional

from pyasic.miners.backends import AntminerModern
from pyasic.miners.data import DataFunction, DataLocations, DataOptions
from pyasic.miners.device.models import S21, S21Hydro, S21Plus, S21PlusHydro, S21Pro


class BMMinerS21(AntminerModern, S21):
    pass


class BMMinerS21Plus(AntminerModern, S21Plus):
    data_locations = DataLocations(
        **{
            str(DataOptions.ENVIRONMENT_TEMP): DataFunction(
                "_get_env_temp",
                [],
            ),
            str(DataOptions.WATTAGE): DataFunction(
                "_get_wattage",
                [],
            ),
            str(DataOptions.WATTAGE_LIMIT): DataFunction(
                "_get_wattage_limit",
                [],
            ),
            **{
                field.name: getattr(AntminerModern.data_locations, field.name)
                for field in dataclasses.fields(AntminerModern.data_locations)
            },
        }
    )

    async def _get_wattage(self) -> Optional[int]:
        try:
            rpc_stats = await self.rpc.stats(new_api=True)
        except APIError:
            return None

        return rpc_stats["STATS"][0].get("watt") if rpc_stats else None

    async def _get_wattage_limit(self) -> Optional[int]:
        try:
            rpc_stats = await self.rpc.stats(new_api=True)
        except APIError:
            return None

        if rpc_stats is None:
            return None

        rate_sale = rpc_stats["STATS"][0].get("rate_sale")

        return int(rate_sale / 1000 * 16.5) if rate_sale else None

    async def _get_env_temp(self) -> Optional[float]:
        try:
            rpc_stats = await self.rpc.stats(new_api=True)
        except APIError:
            return None

        return rpc_stats["STATS"][0].get("ambient_temp") if rpc_stats else None


class BMMinerS21PlusHydro(AntminerModern, S21PlusHydro):
    pass


class BMMinerS21Pro(AntminerModern, S21Pro):
    pass


class BMMinerS21Hydro(AntminerModern, S21Hydro):
    pass
