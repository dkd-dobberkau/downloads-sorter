#!/bin/bash

echo "🔨 Building Downloads Sorter package..."
pip install --upgrade build setuptools wheel twine
python -m build

echo "📦 Installing Downloads Sorter package locally..."
pip install -e .

echo "✅ Done! You can now use 'downloads-sorter' from the command line."
echo ""
echo "Try it out with: downloads-sorter --stats"
