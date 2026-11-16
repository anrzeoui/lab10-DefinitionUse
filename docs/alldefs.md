# B — ALL-DEFS эхний шат

`BonusAllDefsTest`-ийн хоёр тестийг сонгов:

- `bonus_defsLongBelow_returns3`: `[1,1,1,1,1,0,1]`, threshold=7, `present=6`, `best=5`; `score(49)` → c-use(54) → `score(54)` → c-use(56). Мөн `streak(46)` → c-use(41) биелнэ.
- `bonus_defsLongMeets_returns8`: `[1,1,1,1,1]`, threshold=5; `score(51)` → c-use(54), `best(43)` → p-use(53,T).

**Яагаад дор хаяж хоёр тест шаардлагатай вэ?** `score(49)`-ийг use хүртэл хүргэх зам болон `score(51)`-ийг use хүртэл хүргэх зам нь нэг ажиллуулалтанд харилцан үл нийцнэ: 51 нь 49-ийн definition-ийг kill хийнэ. Тиймээс нэг ажиллуулалтаар энэ хоёр definition-ийг хоёуланг нь def-clear use-д хүргэж чадахгүй. Эдгээр хоёр тест нь bonus-ийн бүх хүрч болох definition-үүдийн дор хаяж нэг use-ийг хамардаг.

Жич: A-ийн `GcdTest` 2 тест мөн ажиллана; `results/mvn-verify-alldefs.txt`-ийн нийт тестийн тоо **4** байх ёстой. Branch хувь нь зөвхөн JaCoCo CSV-ийн *бодит үр дүнгээр* тайлагнагдана.
