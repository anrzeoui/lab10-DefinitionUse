#!/usr/bin/env python3
# Create evidence-backed final README only after actual Maven runs (no fabricated counts).
from pathlib import Path
import csv, re, subprocess, sys
root=Path(__file__).resolve().parent.parent
results=root/'results'
needed=['mvn-verify-gcd.txt','jacoco-gcd.csv','mvn-verify-alldefs.txt',
        'jacoco-alldefs.csv','mvn-verify-pairs.txt','jacoco-pairs.csv',
        'mvn-test-M1.txt','mvn-test-M2.txt','mvn-test-M3.txt',
        'mvn-verify-final.txt','jacoco-final.csv']
missing=[x for x in needed if not (results/x).is_file()]
if missing:sys.exit('Not generating final README: missing REAL evidence: '+', '.join(missing))

def read(name):return (results/name).read_text(encoding='utf-8',errors='replace')
def plain(s):return re.sub(r'\x1b\[[0-9;]*m','',s)
def teststats(name):
 txt=plain(read(name))
 matches=re.findall(r'Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)',txt)
 if not matches:sys.exit('Missing Maven test totals: '+name)
 return tuple(map(int,matches[-1]))
def coverage(name):
 with (results/name).open(encoding='utf-8',newline='') as f:
  rows=[r for r in csv.DictReader(f) if r['CLASS']=='DataFlowTargets']
 if len(rows)!=1:sys.exit('Missing DataFlowTargets class in '+name)
 row=rows[0]
 stats={}
 for k in ('LINE','BRANCH','INSTRUCTION'):
  c=int(row[k+'_COVERED']);m=int(row[k+'_MISSED']);stats[k]=(c,m,c*100/(c+m))
 return stats
for name in ['mvn-verify-gcd.txt','mvn-verify-alldefs.txt','mvn-verify-pairs.txt','mvn-verify-final.txt']:
 st=teststats(name)
 if st[1:]!=(0,0,0) or 'BUILD SUCCESS' not in plain(read(name)):
  sys.exit('Expected genuine green Maven evidence in '+name)
m1,m2,m3=[teststats('mvn-test-M'+str(i)+'.txt') for i in (1,2,3)]
if m1[1]+m1[2]==0 or 'BUILD FAILURE' not in plain(read('mvn-test-M1.txt')):
 sys.exit('M1 did not fail tests. Inspect actual log.')
if m3[1]+m3[2]!=0 or 'BUILD SUCCESS' not in plain(read('mvn-test-M3.txt')):
 sys.exit('M3 should not fail dynamic tests. Inspect actual log.')
m2_survived=m2[1]+m2[2]==0
m2_kill_file=results/'mvn-test-M2-kill.txt'
if m2_survived and not m2_kill_file.exists():sys.exit('M2 survived but M2-kill evidence missing.')
if m2_survived and (teststats('mvn-test-M2-kill.txt')[1]+teststats('mvn-test-M2-kill.txt')[2] ==0):
 sys.exit('M2-kill test did not detect the faulty implementation.')
final_cov=coverage('jacoco-final.csv')
if final_cov['BRANCH'][1]!=0 or final_cov['BRANCH'][0]!=16 or final_cov['LINE'][1]!=1:
 sys.exit('Final coverage unexpected; do NOT report expected percentages as measured data.')

def formatcov(name):
 c=coverage(name)
 return '\n'.join(f'| {key} | {c[key][0]} | {c[key][1]} | {c[key][2]:.2f}% |' for key in ('BRANCH','LINE'))
def cmd(*args):
 r=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if r.returncode!=0:sys.exit('Failed to obtain environment: '+r.stdout)
 return plain(r.stdout.strip())
def failed_methods(name):
 txt=plain(read(name))
 found=re.findall(r'\[ERROR\]\s+mn\.edu\.must\.sqat\.([\w.$()\[\], ]+?)\s+--\s+Time elapsed',txt)
 return list(dict.fromkeys(found))

def summary_mutant(name):
 stats=teststats(name)
 status='FAILURE' if 'BUILD FAILURE' in plain(read(name)) else 'SUCCESS'
 methods=failed_methods(name)
 return f'{stats[0]} test, Failures={stats[1]}, Errors={stats[2]}, BUILD {status}',(', '.join('`'+x+'`' for x in methods) if methods else 'Унасан тест байхгүй')

m1s,m1t=summary_mutant('mvn-test-M1.txt')
m2s,m2t=summary_mutant('mvn-test-M2.txt')
m3s,m3t=summary_mutant('mvn-test-M3.txt')
mutantrows=[
 f'| M1 | `streak = streak + 1` мөрийг хассан | {m1s} | {m1t} | `results/mvn-test-M1.txt` |',
 f'| M2 | `best = streak` → `best = present` | {m2s} | {m2t} | `results/mvn-test-M2.txt` |',
 f'| M3 | `int total = present + best` — уншигдахгүй хувьсагч | {m3s} | {m3t} | `results/mvn-test-M3.txt` |',
]
if m2_survived:
 killstats,killnames=summary_mutant('mvn-test-M2-kill.txt')
 m2note=(f'M2 анхны all-DU-pairs тестүүдийг давж **амьд үлдсэн**. '
 'Өмнөх тасралтгүй ирцийн үед `present` болон `streak` хоёул ижил өсөх, тасарсны дараа шинэ богино цуваа өмнөх `best`-ийг даваагүй учраас буруу оноолт илрээгүй. '
 '`bonus_restartedStreakMustNotUsePresentForBest` нэмэлт тест нь `[1,1,0,1,1,1]`, threshold=6 өгч, '
 f'**{killstats}** гаргасан ({killnames}). Эх кодыг сэргээхэд зөв буцах утга 0 байна.')
else:
 m2note='M2-ийн буруу оноолтыг анхны all-DU-pairs тестүүдээс '+m2t+' илрүүлсэн.'

gcd=(root/'docs/gcd-du.md').read_text(encoding='utf-8').replace('# GCD —','### GCD —',1)
bonus=(root/'docs/bonus-du.md').read_text(encoding='utf-8').replace('# Bonus —','### Bonus —',1)
all_defs=(root/'docs/alldefs.md').read_text(encoding='utf-8').replace('# B —','### B —',1)
java=cmd('java','-version');mvn=cmd('mvn','-version')
readme=f'''# Лаборатори №10 — Өгөгдлийн урсгалын DU хосууд

**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест (2026)  
**Оюутан:** Ө. Анар  
**Оюутны код:** B242270129  
**Тестийн бай:** Багшийн `DataFlowTargets.java` (`gcd`, `bonus`), үндсэн код өөрчлөгдөөгүй.  
**AI ашиглалт:** ChatGPT-ээр тестийн санаа, DU хүснэгтийн эх хувилбар, CFG-ийн Graphviz код, Maven үр дүн унших скриптийг бэлтгүүлсэн; баталгаажсан тоо, мутацийн үр дүнг энэ төслийн бодит `results/` файлаас авсан.

## Орчин — терминалын бүтэн гаралт

`java -version`:

```text
{java}
```

`mvn -version`:

```text
{mvn}
```

## Хэсэг A — `gcd()`: def/use болон бүх DU хос

{gcd}

Гаралт: [`results/mvn-verify-gcd.txt`](results/mvn-verify-gcd.txt) — **{teststats('mvn-verify-gcd.txt')[0]}** тест, 0 failures, BUILD SUCCESS.

## Хэсэг B — `bonus()`: all-defs → all-DU-pairs

{all_defs}

### All-defs шатны хэмжилт

**{teststats('mvn-verify-alldefs.txt')[0]}** тест, `BUILD SUCCESS`.

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
{formatcov('jacoco-alldefs.csv')}

Нотолгоо: [`mvn-verify-alldefs.txt`](results/mvn-verify-alldefs.txt), [`jacoco-alldefs.csv`](results/jacoco-alldefs.csv).

### Бүрэн CFG (мөрийн дугаар + ирмэг бүрийн бодит тестийн нэр)

![bonus() CFG](cfg-bonus.png)

`cfg-bonus.dot`-оос Graphviz-аар экспортлосон диаграм. Эх кодын 32-р мөрийн `||`-ийг 32a/32b тусдаа нөхцөл, 38-р мөрийн for-each-ийг дараагийн элемент байгаа эсэх болон `a`-г шинэчлэн оноох үйлдэл болгон ялгасан. `streak=0` (46-р мөр) нь өмнөх streak-def-ийг kill хийдгийг CFG-д тэмдэглэсэн.

{bonus}

### All-DU-pairs шат ба эцсийн JaCoCo

Нэмэлт `BonusTest` тестүүдээр `attendance`, `threshold`, `a`, `present`, `streak`, `best`, `score`-ийн **33 DU/ирмэгийн тохиолдлыг** хамарсан. `GcdTest`-ийн 13 тохиолдол мөн хамрагдсан. Энэхүү DU тоо нь гараар/урсгалын моделийн def-clear анализын тоо; JaCoCo түүнийг хэмждэггүй.

All-DU-pairs шатанд **{teststats('mvn-verify-pairs.txt')[0]}** тест, `BUILD SUCCESS`.

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
{formatcov('jacoco-pairs.csv')}

Эцсийн `mvn verify`-д **{teststats('mvn-verify-final.txt')[0]}** тест, 0 failures/errors, `BUILD SUCCESS`.

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
{formatcov('jacoco-final.csv')}

`jacoco-final.csv`-ийн Branch нь **16/16 (BRANCH_MISSED=0)**, Line нь **LINE_MISSED=1** (7-р мөрийн далд constructor). Үүнийг багшийн зөвшөөрсөн үлдэгдэл мөр гэж тэмдэглэсэн; шалгахын тулд хиймэл constructor тест нэмээгүй.

**Branch ба DU хамралтын ялгаа:** All-defs шатанд def-үүдийг use-д хүргэсэн ч бүх True/False салааг хамарсан гэж үзэх үндэсгүй; жинхэнэ хэмжилт нь дээрх `jacoco-alldefs.csv`-д бий. Эцсийн Branch 16/16 болсон ч энэ нь `best(37)→53(F)` гэх мэт *аль* definition use хүртэл def-clear явсныг тусад нь батлахгүй. Үүнийг DU хүснэгтийн хос, зам, тестийн мөрөөр баталгаажуулсан.

## Хэсэг C — Fault seeding, бодит Maven үр дүн

| Мутаци | Түр өөрчилсөн код | Maven үр дүн | Унасан тест | Нотолгоо |
|---|---|---|---|---|
{chr(10).join(mutantrows)}

{m2note}

**M3 ба static analysis:** `total` хувьсагч утга авч байгаа ч дараа нь нэг ч мөрд уншигдаагүй; тиймээс түүний definition-use хос байхгүй. Энэ нь динамик JUnit тестүүдийн шалгах буцах утгыг өөрчлөхгүй, харин IDE/статик анализын *unused local variable* шалгалтаар илрүүлэх ёстой dead definition юм. Энд IDE-ийн тодорхой алдааны текстийг зохиож оруулаагүй.

**Эх кодыг сэргээсэн нотолгоо:** Мутаци бүрийн дараа `git restore src/main/java/mn/edu/must/sqat/DataFlowTargets.java` хэрэглэж, эцэст нь Maven verify PASS болсон. Багшийн starter-тэй ижил эх код Git-ийн өөрчлөлтгүй байхаар үлдсэн.

## Дүгнэлт

DU анализ нь хувьсагчийн аль definition бодит use хүртэл дахин оноолтгүй хүрснийг шалгадаг тул зөвхөн branch хамралтаас илүү нарийн мэдээлэл өгдөг. `streak`-ийн 41 ба 46-р мөрүүдийн kill үйлдэл нь урсгалыг ойлгоход хамгийн төвөгтэй хэсэг болсон. All-defs-ийг хоёр тестээр хангаж болох ч all-DU-pairs-д хоосон, тасалдалтай, дараалсан ирцтэй нэмэлт оролтууд хэрэгтэй байв. Branch 100% болсон нь DU-ийн бүх def-clear хос шалгагдсан гэдгийг бие даан батлахгүй. M1 нь тасралтгүй ирцийн бизнес үр дүнд нөлөөлөх тул динамик тест барьсан. M2 нь `present` ба `streak` давхцах үед үл мэдэгдэж болох учраас тасалдсаны дараах шинэ цувааг шалгах тест чухал. M3 нь уншигдахгүй definition байсан тул зөвхөн буцах утгыг шалгах тестээр баригдаагүй. Иймээс өгөгдлийн урсгалын тестийг JaCoCo болон static analysis-тай хамт хэрэглэх нь зүйтэй.

## Нотолгооны файлууд

`results/` дотор: `mvn-verify-alldefs.txt`, `jacoco-alldefs.csv`, `mvn-verify-pairs.txt`, `jacoco-pairs.csv`, `mvn-test-M1.txt`, `mvn-test-M2.txt`, `mvn-test-M3.txt`, `mvn-verify-final.txt`, `jacoco-final.csv` болон шаардлагатай бол `mvn-test-M2-kill.txt` хадгалагдсан. `target/` нь `.gitignore`-д байгаа.
'''
(root/'README.md').write_text(readme,encoding='utf-8')
print('Created README.md from checked REAL evidence, chars:',len(readme))
