"""Generate the controlled running Shellac BOM-cost report."""
from pathlib import Path
import sys
_REPO_ROOT=Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0,str(_REPO_ROOT))

from generator.model.bom_cost import category_subtotals,load_ledger,summarise

def money(v):
    return "UNQUOTED" if not isinstance(v,(int,float)) else f"£{float(v):,.2f}"

def main():
    repo=_REPO_ROOT
    data=load_ledger(repo); s=summarise(repo); cats=category_subtotals(repo)
    lines=[
        "# Shellac Running BOM Cost","",
        f"**Price snapshot:** {data.get('price_snapshot_date','OPEN')}","",
        "## Dashboard","",
        f"- Verified/estimated design-BOM subtotal: **£{s.quoted_design_gbp:,.2f} ex VAT**",
        f"- Verified/estimated one-build subtotal: **£{s.quoted_build_gbp:,.2f} ex VAT**",
        f"- Known 10-unit-price subtotal: **£{s.quoted_production_10_gbp:,.2f} ex VAT**",
        f"- Priced ledger lines: **{s.priced_lines}/{s.total_lines}**",
        f"- Cost coverage: **{s.confidence_pct:.1f}%**",
        f"- Unpriced ledger lines: **{s.unpriced_lines}**","",
        "> These are partial subtotals until every product-BOM category is priced.","",
        "## Category subtotal — design basis","",
    ]
    for cat,val in cats.items():
        lines.append(f"- {cat}: **£{val:,.2f}**")
    lines += ["","## Product cost ledger","",
        "| ID | Category | Description | Status | Design | One-build | 10-unit ref | Confidence | Source/date |",
        "|---|---|---|---|---:|---:|---:|---|---|"]
    for x in data.get("items",[]):
        src = "—"
        if x.get("source"):
            src=f"{x['source']} / {x.get('checked_date','')}"
        lines.append(
            f"| {x['id']} | {x['category']} | {x['description']} | {x['procurement_status']} | "
            f"{money(x.get('design_unit_cost_gbp'))} | {money(x.get('build_cost_gbp'))} | "
            f"{money(x.get('production_10_unit_cost_gbp'))} | {x.get('confidence','OPEN')} | {src} |")
    lines += ["","## NRE / prototype-only costs",""]
    for x in data.get("nre",[]):
        lines.append(f"- {x['id']}: {money(x.get('estimated_ex_vat_gbp'))} ex VAT — {x['description']}")
    out=repo/"docs/procurement/Shellac_Running_BOM_Cost.md"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Design subtotal: £{s.quoted_design_gbp:.2f} ex VAT")
    print(f"Coverage: {s.priced_lines}/{s.total_lines} ({s.confidence_pct:.1f}%)")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
