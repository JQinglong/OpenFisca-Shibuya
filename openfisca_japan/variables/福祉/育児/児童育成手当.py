"""
児童育成手当の実装
"""

import numpy as np
from openfisca_core.periods import MONTH, DAY
from openfisca_core.variables import Variable
from openfisca_japan.entities import 世帯


class 児童育成手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = DAY
    label = "保護者への児童手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/hitorioya/hitorioya_teate.html"
    documentation = """
    渋谷区の児童育成手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        児童育成手当 = parameters(対象期間).福祉.育児.児童育成手当

        # 世帯で最も高い所得の人が基準となる
        世帯高所得 = 対象世帯("世帯高所得", 対象期間)
        扶養人数 = 対象世帯("扶養人数", 対象期間)[0]
        所得制限限度額 = 児童育成手当.所得制限限度額[扶養人数]
        所得条件 = 世帯高所得 < 所得制限限度額

        ひとり親世帯である = 対象世帯.nb_persons(世帯.保護者) == 1
        学年 = 対象世帯.members("学年", 対象期間)
        上限学年以下の人数 = 対象世帯.sum(学年 <= 児童育成手当.上限学年)
        手当条件 = ひとり親世帯である * 所得条件

        return 手当条件 * 上限学年以下の人数 * 児童育成手当.金額
