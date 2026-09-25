#!/usr/bin/env bash
# Export checklists, SOPs, and templates to Word/Excel using cmdb_package.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cmdb="${AGK_CMDB_PATH:-/Applications/Development/Projects/cmdb_package}"
for dir in "$root"/methods/*/; do
  tool="$(basename "$dir")"
  case "$tool" in _*|.*) continue ;; esac
  out="$root/dist/office/$tool"; mkdir -p "$out"
  for doc in checklist sop; do
    python3 "$cmdb/md_to_word_converter.py" "$dir/$doc.md" "$out/$doc.docx" --template technical
  done
  if [ -f "$dir/template.md" ]; then
    python3 "$cmdb/md_to_word_converter.py" "$dir/template.md" "$out/template.docx" --template technical
  else
    python3 "$cmdb/csv_to_xls.py" "$dir/template.csv" "$out/template.xlsx"
  fi
done
echo "office export done"
