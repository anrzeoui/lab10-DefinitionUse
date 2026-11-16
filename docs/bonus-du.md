# Bonus — DU анализ, 31–56-р мөрүүд

## Мөр бүрийн def/use (c-use, p-use)

| Мөр | Def | C-use | P-use / салаа |
|---|---|---|---|
|31|`attendance`, `threshold`|–|–|
|32|–|–|`attendance==null`, `threshold<0` (short-circuit тусдаа)|
|33|–|–|– (exception)|
|35|`present`|–|–|
|36|`streak`|–|–|
|37|`best`|–|–|
|38|`a` (элемент бүр), дараах `a` болгонд шинэ def|–|`attendance` (дараагийн элемент байгаа эсэх T/F)|
|39|–|–|`a>0` (T/F)|
|40|`present` (шинэ)|`present` (хуучин)|–|
|41|`streak` (шинэ)|`streak` (хуучин)|–|
|42|–|–|`streak>best` (T/F)|
|43|`best`|`streak`|–|
|46|`streak=0`|–|–|
|49|`score=0`|–|–|
|50|–|–|`present>=threshold` (T/F)|
|51|`score=5`|–|–|
|53|–|–|`best>=5` (T/F)|
|54|`score=score+3`|`score` (хуучин)|–|
|56|–|`score`|–|

## Def-clear DU хосын бүрэн хүснэгт

`…` гэсэн замын тэмдэглэл нь давталт дээр ижил дараалал олон удаа гүйцэтгэгдэж болохыг илэрхийлнэ; тухайн хувьсагчийн шинэ definition байвал тухайн зам def-clear биш. Хүснэгтийн **Тестийн метод** нь `BonusAllDefsTest`/`BonusTest` кодод үнэхээр байгаа нэр.

| Хувьсагч | Def мөр | Use мөр | Төрөл | Def-clear зам | Тестийн метод | Хамарсан |
| --- | --- | --- | --- | --- | --- | --- |
| a | 38 | 39 | p:F | 38(def a)→39(F) | bonus_defsLongBelow_returns3 | Тийм |
| a | 38 | 39 | p:T | 38(def a)→39(T) | bonus_defsLongBelow_returns3 | Тийм |
| attendance | 31 | 32 | p:F | 31→32(attendance=F) | bonus_defsLongBelow_returns3 | Тийм |
| attendance | 31 | 32 | p:T | 31→32(attendance=T) | bonus_null_throws | Тийм |
| attendance | 31 | 38 | p:F | 31→32(F)→35→36→37→38(F) | bonus_defsLongBelow_returns3 | Тийм |
| attendance | 31 | 38 | p:T | 31→32(F)→35→36→37→38(T) | bonus_defsLongBelow_returns3 | Тийм |
| best | 37 | 42 | p:T | 37→38(T)→39(T)→40→41→42(T) | bonus_defsLongBelow_returns3 | Тийм |
| best | 37 | 53 | p:F | 37→38(F)→49→50→53(F) | bonus_absentZero_returns5 | Тийм |
| best | 43 | 42 | p:F | 43(def)→38(T)→39(F)→46→38(T)→39(T)→40→41→42(F) | bonus_defsLongBelow_returns3 | Тийм |
| best | 43 | 42 | p:T | 43(def)→38(T)→39(T)→40→41→42(T) | bonus_defsLongBelow_returns3 | Тийм |
| best | 43 | 53 | p:F | 43(def)→…→38(F)→49→50→53(F) | bonus_gapBelow_returns0 | Тийм |
| best | 43 | 53 | p:T | 43(def)→…→38(F)→49→50→53(T) | bonus_defsLongBelow_returns3 | Тийм |
| present | 35 | 40 | c | 35→36→37→38(T)→39(T)→40 | bonus_defsLongBelow_returns3 | Тийм |
| present | 35 | 50 | p:F | 35→36→37→38(F)→49→50(F) | bonus_emptyOne_returns0 | Тийм |
| present | 35 | 50 | p:T | 35→36→37→38(F)→49→50(T) | bonus_absentZero_returns5 | Тийм |
| present | 40 | 40 | c | 40(def)→41→42→38(T)→39(T)→40(use) | bonus_defsLongBelow_returns3 | Тийм |
| present | 40 | 50 | p:F | 40(def)→…→38(F)→49→50(F) | bonus_defsLongBelow_returns3 | Тийм |
| present | 40 | 50 | p:T | 40(def)→…→38(F)→49→50(T) | bonus_defsLongMeets_returns8 | Тийм |
| score | 49 | 54 | c | 49→50(F)→53(T)→54 | bonus_defsLongBelow_returns3 | Тийм |
| score | 49 | 56 | c | 49→50(F)→53(F)→56 | bonus_emptyOne_returns0 | Тийм |
| score | 51 | 54 | c | 51→53(T)→54 | bonus_defsLongMeets_returns8 | Тийм |
| score | 51 | 56 | c | 51→53(F)→56 | bonus_absentZero_returns5 | Тийм |
| score | 54 | 56 | c | 54→56 | bonus_defsLongBelow_returns3 | Тийм |
| streak | 36 | 41 | c | 36→37→38(T)→39(T)→40→41 | bonus_defsLongBelow_returns3 | Тийм |
| streak | 41 | 41 | c | 41(def)→42→[43]→38(T)→39(T)→40→41(use) | bonus_defsLongBelow_returns3 | Тийм |
| streak | 41 | 42 | p:F | 41(def)→42(F) | bonus_defsLongBelow_returns3 | Тийм |
| streak | 41 | 42 | p:T | 41(def)→42(T) | bonus_defsLongBelow_returns3 | Тийм |
| streak | 41 | 43 | c | 41(def)→42(T)→43 | bonus_defsLongBelow_returns3 | Тийм |
| streak | 46 | 41 | c | 46→38(T)→39(T)→40→41 | bonus_defsLongBelow_returns3 | Тийм |
| threshold | 31 | 32 | p:F | 31→32(att F; threshold F) | bonus_defsLongBelow_returns3 | Тийм |
| threshold | 31 | 32 | p:T | 31→32(att F; threshold T) | bonus_negativeThr_throws | Тийм |
| threshold | 31 | 50 | p:F | 31→32(F)→35→36→37→38…49→50(F) | bonus_defsLongBelow_returns3 | Тийм |
| threshold | 31 | 50 | p:T | 31→32(F)→35→36→37→38…49→50(T) | bonus_defsLongMeets_returns8 | Тийм |

**Kill болон биелэшгүй хосууд:**

- `streak`-ийн 36→42 хос **байхгүй**: 42-р мөрд хүрэхээс өмнө 41-р мөр `streak`-ийг дахин тодорхойлно.
- `streak`-ийн 41→41 хос **46-р мөрөөр дамжвал def-clear биш**: `streak=0` (46) нь 41-ийн өмнөх definition-ийг kill хийнэ. 46→41 хос харин бодит боломжтой.
- `best(37)→42(F)` **биелэшгүй**: анхны эерэг ирцийн дараа `streak=1>best=0` заавал True. Хэрэв `best` өөр болсон бол 43-р мөр 37-ийн definition-ийг kill хийсэн.
- `best(37)→53(T)` **биелэшгүй**: 37-оос хойш 43-р мөрд дахин оноолт хийгдээгүй бол `best=0`, 53-ын нөхцөл False.
- `score(49)→56`, 50(T) зам **def-clear биш**: 51-р мөрд `score=5` дахин тодорхойлно. `score(49)→56` нь зөвхөн 50(F),53(F) замаар боломжтой.
- `threshold` нь `attendance=null` үед 32-ын хоёр дахь нөхцөлд ашиглагдахгүй (short-circuit), учир нь эхний нөхцөл True болсон.

**Бодит хамруулсан DU/ирмэгийн тохиолдол:** 33. `present`, `streak`, `best`, `score`, `attendance`, `threshold`, `a` бүх хувьсагч орсон. `38` дахь `a`-ийн def нь for-each-ийн *элемент бүрд* дахин тодорхойлогдоно.
