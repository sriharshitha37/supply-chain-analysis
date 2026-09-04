# Supply Chain Cost & Quality Bottleneck Analysis

A reproducible supply-chain analytics case study using a public 100-SKU synthetic FMCG dataset. The project identifies logistics cost and product-quality bottlenecks, tests whether observed cost differences are statistically significant, models a transportation-mode savings opportunity, and flags high-impact SKUs for investigation.

> **Dataset note:** This is a public synthetic/practice dataset commonly used for supply-chain analytics. It is **not proprietary Unilever operational data**.

## Executive summary

The analysis finds clear **directional** cost differences across transportation modes and routes, but the sample is small enough that the Air-vs-Sea and Route-B-vs-Route-A differences do **not** reach the conventional 5% statistical-significance threshold.

| Area | Finding |
|---|---|
| Transportation | Air averages **$561.71** vs Sea **$417.82** per shipment — **34.4% higher** |
| Statistical test | Air vs Sea Welch's t-test: **p = 0.0853** — not significant at 5% |
| Route | Route B averages **$595.66** vs Route A **$485.48** — **22.7% higher** |
| Statistical test | Route B vs A Welch's t-test: **p = 0.0637** — not significant at 5% |
| Quality | Haircare has a **29.4% higher** average defect rate than cosmetics (2.48% vs 1.92%) |
| Quality driver | Manufacturing lead time has weak correlation with defect rate: **r = 0.14, p = 0.1662** |

### Why the statistical testing matters

The original analysis treated the observed mean gaps as definitive. The upgraded analysis uses **Welch's independent-samples t-test**, which does not require equal population variances.

The correct conclusion is more nuanced:

- Air is materially more expensive than Sea **in this sample**, but the evidence is not statistically significant at α = 0.05.
- Route B is materially more expensive than Route A **in this sample**, but the evidence is also not statistically significant at α = 0.05.
- Therefore, these findings should be treated as **priority hypotheses for operational validation**, not proven population-wide effects.

## Cost-saving scenario

The observed mean Air cost is $561.71, compared with $417.82 for Sea, implying an observed mean difference of **$143.89 per shipment**.

Because the dataset does not contain a service-level requirement or a reliable time series, the model does **not** claim annual savings. Instead, it shows scenario savings if a percentage of Air shipments were operationally eligible to move to Sea:

| Air shipments shifted | Estimated savings |
|---:|---:|
| 25% | **$935.31** |
| 50% | **$1,870.61** |
| 100% | **$3,741.23** |

**Important:** these are scenario estimates based on observed average costs. Any real recommendation must first validate lead time, customer service level, product sensitivity, capacity, and shipment eligibility.

A separate route scenario estimates **$4,076.51** of potential cost reduction if all Route B shipments could be moved to Route A at Route A's observed average cost. This is a hypothetical benchmark, not an implementation commitment.

## Business recommendations

1. **Prioritize transportation-mode review.** Air has the highest average logistics cost among the observed modes. Review Air shipments for cases where Sea can satisfy required service levels.
2. **Investigate Route B economics.** Route B has the highest average cost. Compare carrier rates, distance, utilization, consolidation opportunities, and lane-specific constraints before rerouting volume.
3. **Target haircare quality controls.** Haircare has the highest average defect rate. Drill into the highest-defect SKUs and inspection outcomes before applying a broad process change.
4. **Do not treat manufacturing lead time as the sole quality lever.** Its correlation with defects is weak, so quality improvement should examine product, supplier, inspection, process, and route-level factors together.
5. **Use statistical results to prioritize validation.** The cost gaps are large enough to investigate, but the current sample does not establish statistical significance at 5%.

## Additional segmentation

### Cost by product category

Skincare has the highest average logistics cost at **$555.73** per shipment.

### Defect rate by route

The highest observed route-level defect rate is **Route A (2.34%)**.

### High-impact SKUs

The analysis exports the **top 10 highest-cost SKUs** and **top 10 highest-defect SKUs** to `outputs/`. These provide concrete candidates for operational investigation rather than relying only on aggregate averages.

## Statistical methodology

### Welch's t-test

For each comparison, the null hypothesis is:

> H₀: the two group means are equal.

The alternative hypothesis is:

> H₁: the two group means are different.

Welch's version was selected because it does not assume equal variances between the groups. Results include the t-statistic, p-value, and 95% confidence interval for the mean difference.

### Correlation

Pearson correlation is used to quantify the linear relationship between manufacturing lead time and defect rate.

Correlation is interpreted as association, **not causation**.

## Project structure

```text
supply-chain-analysis/
├── analysis.py
├── supply_chain_data.xlsx
├── requirements.txt
├── README.md
└── outputs/
    ├── cost_by_transport_mode.csv
    ├── cost_by_route.csv
    ├── cost_by_product_category.csv
    ├── defect_by_product_category.csv
    ├── defect_by_route.csv
    ├── statistical_tests.csv
    ├── mode_shift_scenarios.csv
    ├── top_cost_outliers.csv
    ├── top_defect_outliers.csv
    └── *.png
```

## Tech stack

**Python · pandas · SciPy · matplotlib · Excel**

## Run locally

```bash
pip install -r requirements.txt
python analysis.py
```

The script reads `supply_chain_data.xlsx` and regenerates all CSV tables and PNG visualizations under `outputs/`.

## Key interview talking points

- Used **Welch's t-test** instead of presenting descriptive averages as statistically proven differences.
- Quantified a **transportation-mode savings scenario** while explicitly separating scenario assumptions from realized savings.
- Added **category and route segmentation** to move beyond four headline statistics.
- Flagged specific **high-cost and high-defect SKUs** for operational investigation.
- Distinguished **correlation from causation** when interpreting manufacturing lead time and defect rate.
