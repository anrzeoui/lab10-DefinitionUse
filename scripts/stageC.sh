#!/usr/bin/env bash
# Run each temporary mutation, save genuine Maven logs, restore teacher source after each.
set -uo pipefail
cd "$(dirname "$0")/.."
source_file=src/main/java/mn/edu/must/sqat/DataFlowTargets.java
[[ -f results/jacoco-pairs.csv ]] || { echo 'Run B all-DU-pairs first.' >&2; exit 2; }
[[ -d .git ]] || { echo 'Starter must be committed before mutation.' >&2; exit 2; }
if ! git diff --quiet HEAD -- "$source_file"; then echo 'Main source has uncommitted changes. Stop.' >&2; exit 2; fi
mkdir -p results
restore() { git restore -- "$source_file"; }
trap restore EXIT
mutate() {
  local n="$1"
  restore
  python3 - "$source_file" "$n" <<'PY_MUT'
from pathlib import Path
import sys
file=Path(sys.argv[1]); n=int(sys.argv[2]); text=file.read_text(encoding='utf-8')
changes={
  1:('streak = streak + 1;', '// MUTANT M1: streak update removed'),
  2:('best = streak;', 'best = present; // MUTANT M2: wrong variable'),
  3:('int score = 0;', 'int total = present + best; // MUTANT M3: dead definition\n        int score = 0;'),
}
old,new=changes[n]
assert text.count(old)==1, f'Expected one exact match of {old!r}'
file.write_text(text.replace(old,new,1),encoding='utf-8')
PY_MUT
}
run() {
 local file="$1"
 mvn test 2>&1 | tee "$file"
 RUN_STATUS=${PIPESTATUS[0]}
 echo "Saved $file (mvn exit=$RUN_STATUS)"
}
for i in 1 2 3; do
  echo "========= MUTATION M$i ========="
  mutate "$i" || exit 2
  run "results/mvn-test-M${i}.txt"
  if [[ $i == 2 && $RUN_STATUS -eq 0 ]]; then
    echo 'M2 survived; add targeted test while mutation is active.'
    cp stages/C/BonusMutationKillTest.java src/test/java/mn/edu/must/sqat/BonusMutationKillTest.java
    run results/mvn-test-M2-kill.txt
    if [[ $RUN_STATUS -eq 0 ]]; then echo 'M2 STILL SURVIVED. Review extra test.' >&2; exit 1; fi
  fi
  if [[ $i == 1 && $RUN_STATUS -eq 0 ]]; then echo 'M1 unexpectedly survived; inspect test assertions.' >&2; exit 1; fi
  if [[ $i == 3 && $RUN_STATUS -ne 0 ]]; then echo 'M3 unexpectedly failed; inspect compile/runtime logs.' >&2; exit 1; fi
  restore
done
# Verify again with the teacher's exact source restored.
set +e
mvn verify 2>&1 | tee results/mvn-verify-final.txt
final_status=${PIPESTATUS[0]}
set -e
if (( final_status != 0 )); then echo 'Final verify FAILED.' >&2; exit "$final_status"; fi
cp target/site/jacoco/jacoco.csv results/jacoco-final.csv
python3 scripts/check_coverage.py results/jacoco-final.csv final
if ! git diff --quiet HEAD -- "$source_file"; then echo 'ERROR: source is not restored' >&2; exit 2; fi
printf 'Source restored; genuine Maven evidence saved; final verify PASS.\n'
