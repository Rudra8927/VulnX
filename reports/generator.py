import csv
import html
import json
import os


def write_reports(data, outdir="reports"):
    os.makedirs(outdir, exist_ok=True)
    stem = "vulnx-" + data["scan_id"]
    paths = {}
    json_path = os.path.join(outdir, stem + ".json")
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    paths["json"] = json_path
    csv_path = os.path.join(outdir, stem + ".csv")
    fields = ["severity", "title", "category", "url", "evidence", "remediation"]
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data["findings"])
    paths["csv"] = csv_path
    rows = "".join("<tr>" + "".join(
        "<td>" + html.escape(str(item.get(key, ""))) + "</td>" for key in fields
    ) + "</tr>" for item in data["findings"])
    document = (
        "<!doctype html><html><head><meta charset='utf-8'><title>VulnX report</title>"
        "<style>body{background:#0b1020;color:#e8edf8;font:14px Arial;margin:32px}"
        "table{width:100%;border-collapse:collapse}td,th{padding:9px;border:1px solid #29364c;"
        "text-align:left;overflow-wrap:anywhere}th{color:#65d6ff}</style></head><body>"
        "<h1>VulnX Security Assessment</h1><p>Target: " + html.escape(data["target"]) +
        " · Scan " + html.escape(data["scan_id"]) + "</p><h2>Findings (" +
        str(len(data["findings"])) + ")</h2><table><tr><th>Severity</th><th>Finding</th>"
        "<th>Category</th><th>URL</th><th>Evidence</th><th>Remediation</th></tr>" +
        rows + "</table></body></html>"
    )
    html_path = os.path.join(outdir, stem + ".html")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(document)
    paths["html"] = html_path
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        pdf_path = os.path.join(outdir, stem + ".pdf")
        pdf = SimpleDocTemplate(pdf_path, pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        story = [Paragraph("VulnX Security Assessment", styles["Title"]),
                 Paragraph("Target: " + html.escape(data["target"]), styles["Normal"]), Spacer(1, 12)]
        table_data = [["Severity", "Finding", "Category", "URL", "Evidence", "Remediation"]]
        for item in data["findings"]:
            table_data.append([Paragraph(html.escape(str(item.get(key, ""))), styles["BodyText"])
                               for key in fields])
        table = Table(table_data, repeatRows=1, colWidths=[55, 100, 75, 130, 130, 170])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17283d")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa8ba")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table)
        pdf.build(story)
        paths["pdf"] = pdf_path
    except ImportError:
        pass
    return paths
