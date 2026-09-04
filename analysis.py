"""
Supply Chain Cost & Quality Bottleneck Analysis
================================================
Dataset: Public 100-SKU synthetic FMCG supply-chain dataset.

This version extends the original descriptive analysis with:
- Welch's independent-samples t-tests
- confidence intervals and p-values
- transportation-mode savings scenarios
- product-category and route cuts
- top cost/defect SKU flagging
- reproducible CSV outputs and charts
"""

from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "supply_chain_data.xlsx"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_excel(DATA)
print(f"Loaded {df.shape[0]} SKUs across {df.shape[1]} attributes.\n")


def welch_test(x, y, label_x, label_y):
    """Compare two independent groups without assuming equal variance."""
    x, y = pd.Series(x).dropna(), pd.Series(y).dropna()
    result = stats.ttest_ind(x, y, equal_var=False)
    diff = x.mean() - y.mean()
    se = np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y))
    dof = (
        (x.var(ddof=1)/len(x) + y.var(ddof=1)/len(y)) ** 2
        / (
            (x.var(ddof=1)/len(x)) ** 2 / (len(x)-1)
            + (y.var(ddof=1)/len(y)) ** 2 / (len(y)-1)
        )
    )
    critical = stats.t.ppf(0.975, dof)
    return {
        "comparison": f"{label_x} vs {label_y}",
        "n_x": len(x), "n_y": len(y),
        "mean_x": x.mean(), "mean_y": y.mean(),
        "mean_difference": diff,
        "t_statistic": result.statistic,
        "p_value": result.pvalue,
        "ci_95_low": diff - critical * se,
        "ci_95_high": diff + critical * se,
        "significant_at_5pct": result.pvalue < 0.05,
    }


# 1. Cost bottlenecks
cost_by_mode = df.groupby("Transportation modes")["Costs"].agg(
    avg_cost="mean", total_cost="sum", n="count"
).sort_values("avg_cost", ascending=False)

cost_by_route = df.groupby("Routes")["Costs"].agg(
    avg_cost="mean", total_cost="sum", n="count"
).sort_values("avg_cost", ascending=False)

print("=== Average logistics cost by transportation mode ===")
print(cost_by_mode.round(2), "\n")
print("=== Average logistics cost by route ===")
print(cost_by_route.round(2), "\n")

# 2. Statistical significance
air = df.loc[df["Transportation modes"].eq("Air"), "Costs"]
sea = df.loc[df["Transportation modes"].eq("Sea"), "Costs"]
route_a = df.loc[df["Routes"].eq("Route A"), "Costs"]
route_b = df.loc[df["Routes"].eq("Route B"), "Costs"]

tests = pd.DataFrame([
    welch_test(air, sea, "Air", "Sea"),
    welch_test(route_b, route_a, "Route B", "Route A"),
])
tests.to_csv(OUT / "statistical_tests.csv", index=False)

print("=== Welch's t-tests ===")
print(tests.round(4).to_string(index=False), "\n")

for _, row in tests.iterrows():
    verdict = "statistically significant" if row["significant_at_5pct"] else "not statistically significant"
    print(
        f"-> {row['comparison']}: mean difference ${row['mean_difference']:.2f}, "
        f"p={row['p_value']:.4f}; {verdict} at the 5% level."
    )
print()

# 3. Quality bottlenecks
defect_by_category = df.groupby("Product type")["Defect rates"].agg(
    avg_defect_rate="mean", n="count"
).sort_values("avg_defect_rate", ascending=False)

defect_by_route = df.groupby("Routes")["Defect rates"].agg(
    avg_defect_rate="mean", n="count"
).sort_values("avg_defect_rate", ascending=False)

cost_by_category = df.groupby("Product type")["Costs"].agg(
    avg_cost="mean", total_cost="sum", n="count"
).sort_values("avg_cost", ascending=False)

print("=== Average defect rate by product category ===")
print(defect_by_category.round(3), "\n")
print("=== Average defect rate by route ===")
print(defect_by_route.round(3), "\n")
print("=== Average logistics cost by product category ===")
print(cost_by_category.round(2), "\n")

# 4. Manufacturing lead time vs defects
corr, corr_p = stats.pearsonr(
    df["Manufacturing lead time"], df["Defect rates"]
)
print(
    f"=== Manufacturing lead time vs defect rate: "
    f"r={corr:.2f}, p={corr_p:.4f} ==="
)
print("Interpretation: the relationship is weak in this dataset.\n")

# 5. Mode-shift scenario model
# Important: the dataset has no service-level requirement, so this is a scenario,
# not a claim that every Air shipment is operationally eligible for Sea.
air_mean, sea_mean = air.mean(), sea.mean()
per_shipment_saving = air_mean - sea_mean
air_count = len(air)

scenario_rows = []
for shift_pct in (0.25, 0.50, 1.00):
    scenario_rows.append({
        "air_shift_pct": shift_pct * 100,
        "air_shipments_shifted_equivalent": air_count * shift_pct,
        "estimated_savings_usd": air_count * shift_pct * per_shipment_saving,
    })

scenarios = pd.DataFrame(scenario_rows)
scenarios.to_csv(OUT / "mode_shift_scenarios.csv", index=False)

print("=== Air -> Sea scenario model ===")
print(scenarios.round(2).to_string(index=False))
print(
    f"\nAssumed saving per shifted shipment: ${per_shipment_saving:.2f}. "
    "Validate service-level/lead-time feasibility before implementation.\n"
)

# 6. Outlier / segment flagging
top_cost = df.nlargest(10, "Costs")[
    ["SKU", "Product type", "Transportation modes", "Routes",
     "Costs", "Shipping times", "Lead times"]
]
top_defect = df.nlargest(10, "Defect rates")[
    ["SKU", "Product type", "Transportation modes", "Routes",
     "Defect rates", "Inspection results"]
]

top_cost.to_csv(OUT / "top_cost_outliers.csv", index=False)
top_defect.to_csv(OUT / "top_defect_outliers.csv", index=False)

# 7. Save summary tables
cost_by_mode.to_csv(OUT / "cost_by_transport_mode.csv")
cost_by_route.to_csv(OUT / "cost_by_route.csv")
cost_by_category.to_csv(OUT / "cost_by_product_category.csv")
defect_by_category.to_csv(OUT / "defect_by_product_category.csv")
defect_by_route.to_csv(OUT / "defect_by_route.csv")

# 8. Visualizations
def save_barh(series, title, xlabel, filename):
    plt.figure(figsize=(8, 5))
    series.sort_values().plot(kind="barh")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=180)
    plt.close()

save_barh(
    cost_by_mode["avg_cost"],
    "Average Logistics Cost by Transportation Mode",
    "Average cost ($)",
    "cost_by_transport_mode.png",
)
save_barh(
    cost_by_route["avg_cost"],
    "Average Logistics Cost by Route",
    "Average cost ($)",
    "cost_by_route.png",
)
save_barh(
    cost_by_category["avg_cost"],
    "Average Logistics Cost by Product Category",
    "Average cost ($)",
    "cost_by_product_category.png",
)
save_barh(
    defect_by_category["avg_defect_rate"],
    "Average Defect Rate by Product Category",
    "Defect rate (%)",
    "defect_by_product_category.png",
)
save_barh(
    defect_by_route["avg_defect_rate"],
    "Average Defect Rate by Route",
    "Defect rate (%)",
    "defect_by_route.png",
)

plt.figure(figsize=(9, 5))
plot_data = top_cost.sort_values("Costs")
plt.barh(plot_data["SKU"], plot_data["Costs"])
plt.title("Top 10 Highest-Cost SKUs")
plt.xlabel("Cost ($)")
plt.tight_layout()
plt.savefig(OUT / "top_cost_outliers.png", dpi=180)
plt.close()

print(f"Outputs written to: {OUT}")
