"""Generate the Halden Logistics demo estate. Deterministic; standard library only."""
import csv
import datetime
import json
import sys
from pathlib import Path

CHECKED_ON = "2026-09-01"
CHECKED_ON_DATE = datetime.date(2026, 9, 1)

CATEGORIES = [
    ("ERP", "Northbeam"), ("Payroll", "Paylane"), ("HR information system", "Staffhub"),
    ("Recruiting", "Hirewell"), ("Learning management", "Coursefield"), ("Expense management", "Receiptly"),
    ("Procurement", "Buyline"), ("Contract management", "Clausebase"), ("CRM", "Relato"),
    ("Marketing automation", "Campaignly"), ("Customer support desk", "Helpwise"), ("Live chat", "Chattera"),
    ("Survey", "Pollform"), ("E-signature", "Signwell"), ("Document management", "Docuvault"),
    ("Intranet", "Hallway"), ("Video conferencing", "Meetrix"), ("Team chat", "Threadly"),
    ("Project management", "Taskmoor"), ("Diagramming", "Shapewise"), ("Password manager", "Keyfort"),
    ("Endpoint management", "Fleetdesk"), ("Antivirus", "Shieldline"), ("Backup", "Vaultline"),
    ("Monitoring", "Pulseboard"), ("IT service management", "Servicely"), ("Identity provider", "Gatekey"),
    ("Warehouse management", "Stackyard"), ("Transport management", "Routewise"), ("Fleet telematics", "Trackmile"),
    ("Route optimization", "Pathcraft"), ("Yard management", "Dockside"), ("Customs brokerage", "Borderline"),
    ("Freight audit", "Ratecheck"), ("EDI gateway", "Tradelink"), ("Carrier portal", "Loadboard"),
    ("Demand forecasting", "Foresight"), ("Business intelligence", "Chartwell"), ("Data warehouse", "Lakeshore"),
    ("ETL", "Pipewright"), ("Spreadsheet add-in", "Cellmate"), ("Accounts payable automation", "Payflow"),
    ("Treasury", "Cashmere"), ("Tax compliance", "Levywise"), ("Audit management", "Trailmark"),
    ("GRC", "Controlroom"), ("Policy management", "Rulebook"), ("Health and safety", "Safeyard"),
    ("Visitor management", "Frontdesk"), ("Facilities booking", "Roomly"), ("Invoice OCR", "Scanwright"),
    ("Chatbot", "Askbay"), ("Email security", "Mailguard"), ("Web analytics", "Clickpath"), ("Code repository", "Commitly"),
]
# Planted duplicates: slot -> (partner slot, alternate vendor)
DUPLICATES = {41: (8, "Tallysheet"), 52: (14, "Quickink"), 37: (22, "Linkup"), 58: (29, "Routesmith"), 46: (33, "Clearport")}
CONFIDENTIAL = {"Payroll", "HR information system", "Recruiting", "CRM", "Expense management", "Treasury",
                "Tax compliance", "Identity provider", "Customer support desk", "Accounts payable automation"}
EXPIRED = {"LIC-017": "2026-03-31", "LIC-044": "2025-12-31"}
TERMINATED = {"EMP-071": "2026-05-15", "EMP-072": "2026-07-02"}
ORPHANS = {"ACC-019": "EMP-071", "ACC-063": "EMP-072", "ACC-104": "EMP-099"}
AI_SYSTEMS = [
    ("AI-001", "Email security", "Classifies inbound email as spam or phishing and quarantines it."),
    ("AI-002", "Finance", "Reads supplier invoices and extracts totals, dates, and PO numbers for review."),
    ("AI-003", "Operations", "Suggests delivery routes to dispatchers, who approve each plan."),
    ("AI-004", "HR", "Ranks job applicants' CVs and shortlists candidates for interview."),
    ("AI-005", "Customer service", "Answers customer shipment-status questions in the website chat."),
    ("AI-006", "Planning", "Forecasts weekly warehouse volume from historic shipments."),
]
MATURITY = [
    ("governance", "Governance and policy", 3), ("inventory", "Inventory and discovery", 3),
    ("entitlement", "Entitlement and license management", 1), ("lifecycle", "Lifecycle, request to retirement", 2),
    ("vendor", "Vendor and contract management", 4), ("data-quality", "Data quality and reconciliation", 1),
    ("security", "Risk and security integration", 3), ("cost", "Cost and financial management", 4),
    ("reporting", "Reporting and improvement", 3),
]
CHARTER_FLAWS = ["decision-rights", "sponsor", "membership-size"]
DEVICE_TYPES = ["laptop", "desktop", "mobile", "server"]
DEVICE_REFRESH_CYCLE_MONTHS = {"laptop": 36, "desktop": 48, "mobile": 24, "server": 60}
DEVICE_VENDORS = {"laptop": ["Dell", "Lenovo"], "desktop": ["Dell", "HP"],
                   "mobile": ["Apple", "Samsung"], "server": ["Dell", "HPE"]}
DEVICE_BASE_COST = {"laptop": 1200, "desktop": 900, "mobile": 600, "server": 6000}
# Planted problems: slots overdue for refresh (active, past their cycle) and
# retired slots with no confirmed data wipe (subset of DEVICE_RETIRED).
DEVICE_RETIRED = {5, 11, 18, 24, 29, 35, 42, 48, 53, 59}
DEVICE_OVERDUE = {8, 27, 45}
DEVICE_UNWIPED = {11, 42}
# Audit scenario: a publisher group writes to Halden about three product lines it bought in 2025.
# Each row is (proof_id, license_id, product, version, quantity, license_metric, license_model, vendor,
# buyer_entity, purchase_date, term_start, term_end, price_usd, payment_proof, license_type, upgrade_base,
# upgrade_chain_complete, evidence_location). Taskmoor and Shapewise are subscriptions counted per named
# user; the term is the current subscription term. Cellmate is a perpetual license counted per device;
# the term is its current support term. Both terms end on the expiry shown in licenses.csv.
# An upgrade uses up its qualifying base license; P-006 names a v1 base that Halden holds no proof of.
HALDEN_ENTITY = "Halden Logistics Inc"
TERM = ("2026-07-01", "2027-06-30")
PROOFS = [
    ("P-001", "LIC-019", "Taskmoor Project management", "5", 200, "named user", "subscription", "Taskmoor",
     HALDEN_ENTITY, "2024-03-12", *TERM, 31000, "yes", "full", "", "n/a",
     "AP/2026/invoice-6012 line 1 (current term); AP/2024/invoice-4471 (first order)"),
    ("P-002", "LIC-019", "Taskmoor Project management", "5", 72, "named user", "subscription", "Taskmoor",
     HALDEN_ENTITY, "2025-06-20", *TERM, 11160, "yes", "full", "", "n/a",
     "AP/2026/invoice-6012 line 2 (current term); AP/2025/invoice-5208 (first order)"),
    ("P-003", "LIC-020", "Shapewise Diagramming", "3", 150, "named user", "subscription", "Shapewise",
     "", "2023-02-14", *TERM, 21000, "yes", "full", "", "n/a",
     "AP/2026/invoice-6030 line 1 (current term); AP/2023/invoice-3390 (first order)"),
    ("P-004", "LIC-020", "Shapewise Diagramming", "3", 135, "named user", "subscription", "Shapewise",
     HALDEN_ENTITY, "2025-02-10", *TERM, 20250, "no", "full", "", "n/a",
     "AP/2026/invoice-6031 (current term); AP/2025/invoice-4982 (first order)"),
    ("P-005", "LIC-043", "Cellmate Spreadsheet add-in", "2", 50, "device", "perpetual", "Cellmate",
     HALDEN_ENTITY, "2022-05-04", *TERM, 4000, "yes", "full", "", "n/a",
     "AP/2022/invoice-2874 (license); AP/2026/invoice-6044 line 1 (support term)"),
    ("P-006", "LIC-043", "Cellmate Spreadsheet add-in", "3", 34, "device", "perpetual", "Cellmate",
     HALDEN_ENTITY, "2024-11-05", *TERM, 2380, "yes", "upgrade", "Cellmate Spreadsheet add-in 1", "no",
     "AP/2024/invoice-4640 (upgrade from version 1); AP/2026/invoice-6044 line 2 (support term)"),
]
# Halden's own discovery per license and version: the metric the contract counts, raw installs, the count
# in that metric (assigned users for named-user products, devices for device products), and the earliest
# install seen. Some named users have the product on two devices, so installs exceed users.
INSTALLS = [
    ("LIC-019", "Taskmoor Project management", "5", "named user", 301, 289, "2024-04-02"),
    ("LIC-020", "Shapewise Diagramming", "3", "named user", 297, 285, "2023-03-01"),
    ("LIC-043", "Cellmate Spreadsheet add-in", "2", "device", 50, 50, "2022-03-01"),
    ("LIC-043", "Cellmate Spreadsheet add-in", "3", "device", 34, 34, "2025-01-20"),
]
AUDIT_FINDINGS = [("install_shortfall", "LIC-019"), ("proof_missing_buyer", "P-003"),
                  ("payment_proof_missing", "P-004"), ("proof_after_install", "P-005"),
                  ("upgrade_without_original", "P-006"), ("letter_scope_overreach", "letter-scope")]
AUDIT_LETTER = """# Software license audit notice

**From:** Brightvale Software Group, Compliance Programs
**To:** Halden Logistics Inc, Office of the General Counsel
**Date:** 2026-08-24
**Reference:** BSG-AUD-2026-0417

Brightvale Software Group acquired the Taskmoor, Shapewise, and Cellmate product lines from Mosswood
Software in 2025. We are reviewing license compliance for these products and ask Halden to take part.

## What we ask for

- A list of every installation of any Brightvale, Taskmoor, Shapewise, or Cellmate product at Halden
  Logistics Inc and every other Halden group company, in any country.
- Installation records for every year back to 2019.
- Proof of purchase for each product.
- A device-level list: device name, user, and install date for every installation.
- A written reply within 30 days of the date above.

## Halden's own notes on its agreement (ref HAL-MSW-2022)

- Signed with Mosswood Software in 2022, before Brightvale bought the product lines. Halden holds no
  record of the agreement being assigned to Brightvale.
- Contracting party: Halden Logistics Inc only. Other group companies are not parties.
- Products covered: Taskmoor Project management, Shapewise Diagramming, Cellmate Spreadsheet add-in.
- License metric: Taskmoor and Shapewise per named user; Cellmate per device.
- Audit clause: one review in any 12 months, on 30 days' notice, covering use in the 36 months before
  the notice, with results released to the publisher as counts per product and version.
- Proof of purchase: invoices, order confirmations, or records from the publisher's licensing portal or
  an authorized reseller.
"""
CHARTER_DRAFT = """# Halden Software Governance Council — draft charter

## Purpose
The council oversees software and applications at Halden Logistics.

## Members (voting)
CIO; CISO; heads of procurement, finance, legal, architecture, HR, operations, warehousing, transport, customer service, sales, marketing; and the service desk lead.

## Meetings
Monthly, 90 minutes. Standing agenda: new requests above threshold, exceptions, renewals due, and a review of measures. Outcomes are recorded in a register kept by the governance analyst. Urgent items are handled out of cycle by email vote within five working days.

## Scope
New software requests, renewals, retirements, and AI tools.

## Intake
Requests come through one software request form. The governance analyst triages requests weekly. Only items above a cost or risk threshold come to the council.

## Escalation
Disputes go to the Chief Operating Officer, who does not sit on the council and who breaks ties.

## Measures
Time from request to outcome, the share of software bought through the intake form, savings, and exceptions granted. Reviewed quarterly, starting from a baseline set in the first quarter.
"""
CONTROLS = [
    ("C1", "Maintain an accurate inventory of software and who owns each application.", "XW-001"),
    ("C2", "Review user access to applications on a schedule and remove access no longer needed.", "XW-016"),
    ("C3", "Assess each AI system for risk before it is deployed.", "XW-021"),
]


def _write(path: Path, header: list[str], rows: list[list]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def generate(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    key = []
    base = iter(CATEGORIES)
    slots = {}
    for i in range(1, 61):
        if i not in DUPLICATES:
            slots[i] = next(base)
    for i, (partner, vendor) in DUPLICATES.items():
        slots[i] = (slots[partner][0], vendor)
        key.append({"tool": "rationalization", "type": "duplicate_app",
                    "id": "+".join(sorted((f"APP-{partner:03d}", f"APP-{i:03d}")))})
    apps = [[f"APP-{i:03d}", f"{slots[i][1]} {slots[i][0]}", slots[i][1], slots[i][0],
             round(5000 + (i * 7919) % 90000, -2), 20 + (i * 37) % 900,
             "confidential" if slots[i][0] in CONFIDENTIAL else "internal"] for i in range(1, 61)]
    _write(out / "apps.csv", ["id", "name", "vendor", "category", "annual_cost_usd", "users", "data_sensitivity"], apps)

    licenses = []
    for i in range(1, 61):
        lid = f"LIC-{i:03d}"
        licenses.append([lid, f"APP-{i:03d}", 25 + (i * 13) % 500, EXPIRED.get(lid, "2027-06-30"), CHECKED_ON])
    key += [{"tool": "rationalization", "type": "expired_license", "id": lid} for lid in EXPIRED]
    _write(out / "licenses.csv", ["id", "app_id", "entitlements", "expiry", "checked_on"], licenses)

    employees = [[f"EMP-{i:03d}", "terminated" if f"EMP-{i:03d}" in TERMINATED else "active",
                  TERMINATED.get(f"EMP-{i:03d}", "")] for i in range(1, 81)]
    _write(out / "employees.csv", ["id", "status", "termination_date"], employees)

    accounts = []
    for i in range(1, 121):
        aid = f"ACC-{i:03d}"
        emp = ORPHANS.get(aid, f"EMP-{(i - 1) % 70 + 1:03d}")
        accounts.append([aid, emp, f"APP-{(i - 1) % 60 + 1:03d}", "admin" if i % 17 == 0 else "user",
                         f"2026-08-{(i % 28) + 1:02d}"])
    key += [{"tool": "access-review", "type": "orphaned_account", "id": aid} for aid in ORPHANS]
    _write(out / "accounts.csv", ["id", "employee_id", "app_id", "role", "last_login"], accounts)

    _write(out / "ai-systems.csv", ["id", "owner", "description"], [list(a) for a in AI_SYSTEMS])
    key.append({"tool": "ai-intake", "type": "high_risk_ai", "id": "AI-004"})

    _write(out / "maturity-answers.csv", ["area", "label", "score"], [list(m) for m in MATURITY])
    lowest = sorted(MATURITY, key=lambda m: m[2])[:3]
    key += [{"tool": "itam-maturity", "type": "maturity_gap", "id": m[0]} for m in lowest]

    (out / "controls.md").write_text(
        "# Controls to map\n\n" + "".join(f"- **{c}**: {text}\n" for c, text, _ in CONTROLS), encoding="utf-8")
    key += [{"tool": "crosswalk", "type": "crosswalk_match", "id": f"{c}:{xw}"} for c, _, xw in CONTROLS]

    (out / "council-draft.md").write_text(CHARTER_DRAFT, encoding="utf-8")
    key += [{"tool": "program-setup", "type": "charter_gap", "id": f} for f in CHARTER_FLAWS]

    devices = []
    for i in range(1, 61):
        dtype = DEVICE_TYPES[(i - 1) % 4]
        cycle = DEVICE_REFRESH_CYCLE_MONTHS[dtype]
        vendor = DEVICE_VENDORS[dtype][(i // 4) % len(DEVICE_VENDORS[dtype])]
        owner = f"EMP-{((i * 13) % 80) + 1:03d}"
        cost = DEVICE_BASE_COST[dtype] + (i * 173) % DEVICE_BASE_COST[dtype]
        retired = i in DEVICE_RETIRED
        status = "retired" if retired else "active"
        if i in DEVICE_OVERDUE:
            months_since_deploy = cycle + 6
        elif retired:
            months_since_deploy = 24 + (i * 7) % 40
        else:
            months_since_deploy = 3 + (i * 11) % (cycle - 6)
        deploy_date = CHECKED_ON_DATE - datetime.timedelta(days=months_since_deploy * 30)
        if retired:
            refresh_due_date = ""
            retire_months_ago = months_since_deploy - 18
            retirement_date = (CHECKED_ON_DATE - datetime.timedelta(days=retire_months_ago * 30)).isoformat()
            data_wipe_confirmed = "no" if i in DEVICE_UNWIPED else "yes"
        else:
            refresh_due_date = (deploy_date + datetime.timedelta(days=cycle * 30)).isoformat()
            retirement_date = ""
            data_wipe_confirmed = ""
        devices.append([f"DEV-{i:03d}", dtype, vendor, owner, deploy_date.isoformat(), refresh_due_date,
                         status, retirement_date, data_wipe_confirmed, cost, CHECKED_ON])
    _write(out / "devices.csv", ["device_id", "type", "vendor", "owner", "deploy_date", "refresh_due_date",
                                  "status", "retirement_date", "data_wipe_confirmed", "cost_usd", "checked_on"],
           devices)
    key += [{"tool": "hardware-lifecycle", "type": "overdue_refresh", "id": f"DEV-{i:03d}"}
            for i in sorted(DEVICE_OVERDUE)]
    key += [{"tool": "hardware-lifecycle", "type": "unwiped_retired_device", "id": f"DEV-{i:03d}"}
            for i in sorted(DEVICE_UNWIPED)]

    _write(out / "proofs-of-purchase.csv",
           ["proof_id", "license_id", "product", "version", "quantity", "license_metric", "license_model",
            "vendor", "buyer_entity", "purchase_date", "term_start", "term_end", "price_usd", "payment_proof",
            "license_type", "upgrade_base", "upgrade_chain_complete", "evidence_location"],
           [list(p) for p in PROOFS])
    _write(out / "audit-installs.csv",
           ["license_id", "product", "version", "license_metric", "installs_counted", "count_in_metric",
            "first_install_date", "checked_on"],
           [list(i) + [CHECKED_ON] for i in INSTALLS])
    (out / "audit-letter.md").write_text(AUDIT_LETTER, encoding="utf-8")
    key += [{"tool": "audit-response", "type": t, "id": i} for t, i in AUDIT_FINDINGS]

    key.sort(key=lambda k: (k["tool"], k["type"], k["id"]))
    (out / "answer-key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent)
