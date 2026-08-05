"""
Supply Chain Cost & Quality Bottleneck Analysis
------------------------------------------------
Dataset: Public 100-SKU FMCG supply chain dataset (Kaggle, "Unilever Supply
Chain Analysis" — a synthetic/public dataset commonly used for supply-chain
analytics practice, not proprietary Unilever operational data).

Goal: identify where cost and quality bottlenecks concentrate across
transportation modes, routes, and product categories, using descriptive
statistics and correlation analysis.

"""
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
df = pd.read_excel("supply_chain_data.xlsx")

print(f"Loaded {df.shape[0]} SKUs across {df.shape[1]} attributes.\n")

# ---------------------------------------------------------------------------
# 2. Cost bottlenecks: transportation mode & route
# ---------------------------------------------------------------------------
cost_by_mode = (
    df.groupby("Transportation modes")["Costs"]
    .agg(avg_cost="mean", n="count")
    .sort_values("avg_cost", ascending=False)
)
cost_by_route = (
    df.groupby("Routes")["Costs"]
    .agg(avg_cost="mean", n="count")
    .sort_values("avg_cost", ascending=False)
)

print("=== Average logistics cost by transportation mode ===")
print(cost_by_mode.round(2), "\n")

print("=== Average logistics cost by route ===")
print(cost_by_route.round(2), "\n")

most_exp_mode, cheapest_mode = cost_by_mode.index[0], cost_by_mode.index[-1]
mode_gap_pct = (
    (cost_by_mode.loc[most_exp_mode, "avg_cost"] - cost_by_mode.loc[cheapest_mode, "avg_cost"])
    / cost_by_mode.loc[cheapest_mode, "avg_cost"] * 100
)
print(f"-> {most_exp_mode} costs {mode_gap_pct:.1f}% more on average than {cheapest_mode}.\n")

most_exp_route, cheapest_route = cost_by_route.index[0], cost_by_route.index[-1]
route_gap_pct = (
    (cost_by_route.loc[most_exp_route, "avg_cost"] - cost_by_route.loc[cheapest_route, "avg_cost"])
    / cost_by_route.loc[cheapest_route, "avg_cost"] * 100
)
print(f"-> {most_exp_route} costs {route_gap_pct:.1f}% more on average than {cheapest_route}.\n")

# ---------------------------------------------------------------------------
# 3. Quality bottlenecks: defect rate by product category
# ---------------------------------------------------------------------------
defect_by_category = (
    df.groupby("Product type")["Defect rates"]
    .agg(avg_defect_rate="mean", n="count")
    .sort_values("avg_defect_rate", ascending=False)
)
print("=== Average defect rate by product category ===")
print(defect_by_category.round(3), "\n")

worst_cat, best_cat = defect_by_category.index[0], defect_by_category.index[-1]
defect_gap_pct = (
    (defect_by_category.loc[worst_cat, "avg_defect_rate"] - defect_by_category.loc[best_cat, "avg_defect_rate"])
    / defect_by_category.loc[best_cat, "avg_defect_rate"] * 100
)
print(f"-> {worst_cat} has a {defect_gap_pct:.1f}% higher average defect rate than {best_cat}.\n")

# ---------------------------------------------------------------------------
# 4. Does longer manufacturing lead time predict more defects?
# ---------------------------------------------------------------------------
corr = df[["Manufacturing lead time", "Defect rates"]].corr().iloc[0, 1]
print(f"=== Correlation: manufacturing lead time vs defect rate: r = {corr:.2f} ===")
print("-> Weak correlation: longer manufacturing lead time is NOT a strong")
print("   standalone predictor of defect rate in this dataset.\n")

# ---------------------------------------------------------------------------
# 5. Visualizations
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

cost_by_mode["avg_cost"].plot(kind="bar", ax=axes[0], color="#1F3864")
axes[0].set_title("Avg. Logistics Cost by Transportation Mode")
axes[0].set_ylabel("Average cost ($)")
axes[0].set_xlabel("")

defect_by_category["avg_defect_rate"].plot(kind="bar", ax=axes[1], color="#8C1F28")
axes[1].set_title("Avg. Defect Rate by Product Category")
axes[1].set_ylabel("Defect rate (%)")
axes[1].set_xlabel("")

plt.tight_layout()
plt.savefig("cost_and_defect_bottlenecks.png", dpi=150)
print("Saved chart -> cost_and_defect_bottlenecks.png")
