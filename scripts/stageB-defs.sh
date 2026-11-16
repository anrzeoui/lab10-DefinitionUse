#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -f src/test/java/mn/edu/must/sqat/GcdTest.java ]] || { echo 'Run stageA.sh first.' >&2; exit 2; }
mkdir -p src/test/java/mn/edu/must/sqat docs results
cp stages/B-defs/BonusAllDefsTest.java src/test/java/mn/edu/must/sqat/
cp stages/B-defs/alldefs.md docs/alldefs.md
set +e
mvn verify 2>&1 | tee results/mvn-verify-alldefs.txt
rc=${PIPESTATUS[0]}
set -e
if (( rc != 0 )); then echo 'All-defs stage failed; fix first.' >&2; exit "$rc"; fi
cp target/site/jacoco/jacoco.csv results/jacoco-alldefs.csv
echo 'All-defs stage recorded: results/mvn-verify-alldefs.txt and jacoco-alldefs.csv'
