# Adjustable scoring model

Before final ranking, show the dimensions and ask whether to keep the default weights. Weights must sum to 100. Each dimension is scored 0-100, and the composite score is:

`SUM(dimension_score × weight / 100)`

## Default exhibition-gift weights

| Dimension | Weight | What it measures |
|---|---:|---|
| Exhibition Wow / demonstration | 25 | Immediate visual or experiential impact at the booth |
| Novelty and interaction | 20 | Newness, play value, movement, capture, or interactive behavior |
| S+ tier and brand perception | 20 | Whether it feels substantially above ordinary giveaway items |
| Foreign-user usability | 15 | English/German support, overseas app/account, region independence |
| Price and procurement risk | 20 | Unit price, stock, delivery, battery/shipping, and confirmation risk |

## Weight adjustment rules

- The buyer may change any weight before final scoring; normalize only if the buyer explicitly asks to normalize.
- Store the selected weights, score date, and reason in the run evidence.
- If price weight is reduced, do not hide budget violations; show them as hard status fields and exclude products that violate a frozen hard cap unless the buyer explicitly allows a risk backup.
- If foreign-user weight is reduced, still keep known China-only or Chinese-account-locked products flagged.
- Recompute every candidate after a weight change. Do not mix scores calculated under different weight sets in one ranking.
- Report component scores and the weighted total so the buyer can audit the ranking.
