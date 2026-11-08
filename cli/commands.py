import argparse
import asyncio
import json

from core.scanner import Scanner
from reports.generator import write_reports


def main():
    parser = argparse.ArgumentParser(description="VulnX authorized website assessment")
    parser.add_argument("target", help="HTTP/HTTPS URL within your authorized scope")
    parser.add_argument("--confirm-authorized", action="store_true")
    parser.add_argument("--out", default="reports")
    args = parser.parse_args()
    if not args.confirm_authorized:
        parser.error("Confirm that you own the target or have explicit permission.")
    result = asyncio.run(Scanner().scan(args.target))
    report_files = write_reports(result, args.out)
    print(json.dumps({
        "scan_id": result["scan_id"],
        "target": result["target"],
        "findings": len(result["findings"]),
        "reports": report_files,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
