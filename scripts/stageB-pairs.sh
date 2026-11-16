#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -f results/jacoco-alldefs.csv ]] || { echo 'Run and commit all-defs stage first.' >&2; exit 2; }
mkdir -p src/test/java/mn/edu/must/sqat docs results
cp stages/B-pairs/BonusTest.java src/test/java/mn/edu/must/sqat/
cp stages/B-pairs/bonus-du.md docs/bonus-du.md
cp stages/B-pairs/cfg-bonus.dot cfg-bonus.dot
if ! command -v dot >/dev/null 2>&1; then echo 'Install graphviz: sudo apt install graphviz' >&2; exit 2; fi
dot -Tpng -Gdpi=170 cfg-bonus.dot -o cfg-bonus.png
set +e
mvn verify 2>&1 | tee results/mvn-verify-pairs.txt
rc=${PIPESTATUS[0]}
set -e
if (( rc != 0 )); then echo 'All-DU-pairs stage failed.' >&2; exit "$rc"; fi
cp target/site/jacoco/jacoco.csv results/jacoco-pairs.csv
python3 scripts/check_coverage.py results/jacoco-pairs.csv
