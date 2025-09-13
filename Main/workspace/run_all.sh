#!/bin/bash
echo "🚀 Starting Glue job runner..."

if [ -f "main.py" ]; then
  echo "▶️ Running main.py ..."
  python3 main.py || { echo "Script stopped due to error in main.py"; exit 1; }
fi

if [ -f "ETL1.py" ]; then
  echo "▶️ Running ETL1.py with spark-submit ..."
  spark-submit ETL1.py || { echo "Script stopped due to error in ETL1.py"; exit 1; }
fi

echo "✅ All scripts executed successfully!"