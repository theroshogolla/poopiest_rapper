#!/bin/bash


exclude_files=("artist_ids.csv" "artist_ids_backup.csv")

total_lines=0

for file in data/*.csv; do
  filename=$(basename "$file")
  
  # Check if the file is in the exclude list
  if [[ " ${exclude_files[@]} " =~ " $filename " ]]; then
    continue
  fi

  line_count=$(tail -n +2 "$file" | wc -l)

  total_lines=$((total_lines + line_count))
done

echo "Total lines in CSV files (excluding specified files and headers): $total_lines"
