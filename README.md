# Supply Chain Cost & Quality Bottleneck Analysis

Self-directed case study analyzing a public 100-SKU FMCG supply chain dataset
to identify cost and quality bottlenecks across transportation modes, routes,
and product categories — done to build applied analytics skills ahead of
FMCG supply chain roles.

**Dataset:** [Unilever Supply Chain Analysis (Kaggle)](https://www.kaggle.com/datasets/rahuljangir78/unilever-supply-chain-analysis) —
a public, synthetic supply-chain dataset used for analytics practice (not
proprietary Unilever operational data).

## Key findings

- **Air transport costs 34.4% more on average** than Sea transport ($561.71 vs $417.82 per shipment)
- **Route B costs 22.7% more on average** than Route A ($595.66 vs $485.48)
- **Haircare products show a 29.4% higher average defect rate** than cosmetics (2.48% vs 1.92%)
- Manufacturing lead time is only weakly correlated with defect rate (r = 0.14) — longer production time alone doesn't explain quality issues in this dataset

## Tech stack

Python, pandas, matplotlib

## Run it yourself

```bash
pip install pandas matplotlib openpyxl
python analysis.py
```

## Files

- `analysis.py` — full analysis script
- `supply_chain_data.xlsx` — source dataset
- `cost_and_defect_bottlenecks.png` — output chart
