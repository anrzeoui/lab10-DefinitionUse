# Lab10 — үе шаттай хэрэгжүүлэх команд (Debian 13)

**Эхлээд `cd ~/Desktop/lab10-dataflow`**. Төслийн starter кодыг `src/main`-д өөрчлөлгүй хадгалсан. Лабын зааварт GitHub түүхийг **Starter → A → B all-defs → B all-DU-pairs → C → README** тусдаа 5-аас олон commit болгохыг шаардсан. Скрипт бүр үнэхээр ажиллуулсан Maven-ийн логуудыг л хадгална. `BUILD SUCCESS/FAILURE` үр дүнг урьдчилан зохиогоогүй.

## 0. Стартерийг эхэлж commit хийх

```bash
bash scripts/stage0.sh
```

`git log --oneline -1`-д Starter commit харагдсан байх ёстой. `stages/` хавтас нь дараагийн тестийн материал тул **commit-д оруулахгүй**.

## A. gcd all-DU-pairs (2 тест)

```bash
bash scripts/stageA.sh
cat docs/gcd-du.md
grep -E 'Tests run:|BUILD SUCCESS' results/mvn-verify-gcd.txt
git add .gitignore scripts/ docs/gcd-du.md docs/WORKFLOW.md src/test/java/mn/edu/must/sqat/GcdTest.java results/mvn-verify-gcd.txt results/jacoco-gcd.csv
git commit -m 'test(A): gcd all-DU-pairs with def-clear paths'
```

## B1. bonus all-defs (2 шинэ тест; өмнөх gcd-тэй нийт 4)

```bash
bash scripts/stageB-defs.sh
python3 scripts/check_coverage.py results/jacoco-alldefs.csv
git add src/test/java/mn/edu/must/sqat/BonusAllDefsTest.java docs/alldefs.md results/mvn-verify-alldefs.txt results/jacoco-alldefs.csv
git commit -m 'test(B1): bonus minimum two all-defs tests'
```

## B2. bonus all-DU-pairs (10 нэмэлт тест)

```bash
sudo apt install -y graphviz
bash scripts/stageB-pairs.sh
python3 scripts/check_coverage.py results/jacoco-pairs.csv
git add src/test/java/mn/edu/must/sqat/BonusTest.java docs/bonus-du.md cfg-bonus.dot cfg-bonus.png results/mvn-verify-pairs.txt results/jacoco-pairs.csv
git commit -m 'test(B2): cover all def-clear DU pairs and label CFG edges'
```

`cfg-bonus.png` нь Graphviz-аар үүссэн. Лаб10-д Graphviz ашиглахыг багш **зөвшөөрсөн**. Зураг дээр 31–56-р мөрийн зангилаанууд, 38-д `a`-ийн def, 46-д kill болон **сум бүр дээр жинхэнэ @Test методын нэр** байдаг.

## C. Гурван түр мутаци, эх кодыг сэргээх

```bash
bash scripts/stageC.sh
grep -E 'Tests run:|BUILD SUCCESS|BUILD FAILURE' results/mvn-test-M*.txt
python3 scripts/check_coverage.py results/jacoco-final.csv final
git diff -- src/main/java/mn/edu/must/sqat/DataFlowTargets.java
git add src/test results/mvn-test-M*.txt results/mvn-verify-final.txt results/jacoco-final.csv
git commit -m 'test(C): seed M1 M2 M3, record outcomes, restore starter code'
```

M2 амьд үлдвэл скрипт `BonusMutationKillTest.java` нэмж, `results/mvn-test-M2-kill.txt`-д **бодит FAIL** нотолгоо авна; `git add src/test` командаар шинэ тест хадгалагдана. M3 нь амьд үлддэг, статик анализ `total` ашиглагдаагүйг олох ёстой. IDE-ийн гаргасан бодит текстийг харах бол VS Code дээр `int total = present + best` нэмсэн түр үед Problems панелийг шалга; зохиомол warning README-д нэмэхгүй.

## README — зөвхөн бүх үр дүнгийн дараа

```bash
python3 scripts/finalize_readme.py
cat README.md | head -65
git add README.md
git commit -m 'docs: finalize DU tables, true mutation evidence and conclusions'
```

`java -version`, `mvn -version`-ийн бодит гаралт болон JaCoCo CSV-ийн яг хэмжсэн хувь орно; файл дутуу бол скрипт алдаа өгнө.

## Эцсийн баталгаажуулалт, GitHub

```bash
mvn verify
git diff <starter-commit-sha> HEAD -- src/main/java/mn/edu/must/sqat/DataFlowTargets.java
git log --oneline --max-count=8
git status --short
git ls-files | grep -E '^results/|^cfg-bonus.png$|^README.md$'
```

`git diff` нь хоосон, final JaCoCo Branch=16/16, Line missed=1 хэвийн байх ёстой. Шинэ public GitHub repo үүсгэн (хэрэв өмнө үүсгээгүй бол):

```bash
git remote add origin https://github.com/anrzeoui/lab10-dataflow.git
git push -u origin main
```

Өмнө нь `origin` нэмсэн бол `git remote -v`-ээр шалгаад зөвхөн `git push -u origin main` хий. Teams Assignment-д public repo-ийн root линк илгээж **Turn in** дарна. Энэ ZIP нь GitHub-д хийгдсэн гэж мэдүүлэх нотолгоо биш.
