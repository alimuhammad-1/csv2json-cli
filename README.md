# csv2json CLI Tool

A robust, zero-dependency command-line utility built in Python to convert CSV files into clean, formatted JSON.

---

## 🚀 Quick 2-Command Installation

Install directly on any fresh machine using standard Python tools:

```bash
git clone https://github.com/YOUR_USERNAME/csv2json-cli.git
pip install ./csv2json-cli
```

Once installed, run `csv2json --help` anywhere in your terminal.

---

## 💡 Usage Examples

### 1. Print JSON directly to stdout
```bash
csv2json input.csv
```

### 2. Save JSON to a specific output file
```bash
csv2json data.csv -o output.json
```

### 3. Custom indentation formatting
```bash
csv2json data.csv -o output.json --indent 4
```

---

## 🧪 Running Automated Tests

Run the full 6-test suite using `pytest`:

```bash
pip install pytest
pytest
```

---

## 📝 Design Decision Note (Handling Awkward Input)

**Initial Choice:** The tool originally relied on standard `utf-8` encoding and standard comma delimiter splitting.

**Refactoring Trigger:** When tested against awkward input—specifically Excel-exported CSV files containing byte order mark (`ï»¿` BOM) headers and European semicolon-delimited files (`id;name;val`)—the output JSON produced corrupted key headers like `﻿id` and incorrectly combined columns.

**Key Change:**
1. Switched file reading to **`utf-8-sig`** to automatically strip BOM signatures seamlessly.
2. Integrated `csv.Sniffer()` to dynamically detect custom delimiters (like `;` or `\t`) automatically without requiring explicit user flag configurations.
