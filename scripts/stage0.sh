#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -d .git ]]; then git init -b main; fi
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo 'Existing commit history detected; no Starter commit created.'
  exit 0
fi
git add pom.xml .gitignore src/main/
git commit -m "Starter: teacher-provided DataFlowTargets unchanged"
echo 'Starter commit saved. Scripts/stages are not yet part of the commit.'
