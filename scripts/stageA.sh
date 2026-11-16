#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p src/test/java/mn/edu/must/sqat docs results
cp stages/A/GcdTest.java src/test/java/mn/edu/must/sqat/
cp stages/A/gcd-du.md docs/gcd-du.md
if ! grep -qx 'stages/' .gitignore; then printf '\nstages/\n' >> .gitignore; fi
set +e
mvn verify 2>&1 | tee results/mvn-verify-gcd.txt
rc=${PIPESTATUS[0]}
set -e
if (( rc != 0 )); then echo 'GCD tests failed. Do not commit.' >&2; exit "$rc"; fi
cp target/site/jacoco/jacoco.csv results/jacoco-gcd.csv
echo 'GCD DU-pairs tests complete. Commit ONLY A files and scripts after review.'
