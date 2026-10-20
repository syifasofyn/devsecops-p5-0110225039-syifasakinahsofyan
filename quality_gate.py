import json
import sys

# Aturan Quality Gate: batas maksimal temuan yang diizinkan
MAX_HIGH = 0
MAX_MEDIUM = 0


def main():
    if len(sys.argv) != 2:
        print("Pemakaian: python quality_gate.py <bandit-report.json>")
        return 2

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            report = json.load(f)
    except (OSError, json.JSONDecodeError) as error:
        print(f"GATAL: laporan Bandit tidak bisa dibaca ({error})")
        return 2

    results = report.get("results", [])
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for item in results:
        severity = item.get("issue_severity", "LOW").upper()
        counts[severity] = counts.get(severity, 0) + 1

    print("=== QUALITY GATE ===")
    print(f"HIGH   : {counts['HIGH']} (maksimal {MAX_HIGH})")
    print(f"MEDIUM : {counts['MEDIUM']} (maksimal {MAX_MEDIUM})")
    print(f"LOW    : {counts['LOW']} (tidak memblokir)")

    for item in results:
        if item.get("issue_severity", "").upper() in ("HIGH", "MEDIUM"):
            print(
                f"- [{item['issue_severity']}] {item['test_id']} "
                f"{item['filename']}:{item['line_number']} - {item['issue_text']}"
            )

    if counts["HIGH"] > MAX_HIGH or counts["MEDIUM"] > MAX_MEDIUM:
        print("HASIL: GAGAL - Quality Gate tidak terpenuhi.")
        return 1

    print("HASIL: LULUS - Quality Gate terpenuhi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
    