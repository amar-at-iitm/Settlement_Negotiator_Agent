# Settlement Negotiator Agent

## Overview
This project implements a **Strict Settlement Negotiator Agent** for CredResolve. The agent acts as a virtual officer, calculating the **minimum acceptable settlement offer** (Floor Price) for borrowers based on their loan details and chat history, strictly adhering to the CredResolve Settlement Policy.

## Solution Logic
The solution is implemented in `solution.py` using pure Python to ensure compatibility and strict rule adherence.

### Policy Interpretation
The agent applies the following logic hierarchy:

1.  **Credit Cards (CC)**
    *   **Small Balance (< 50k)**: **10% Discount**. (Overrides all other CC rules).
    *   **High Delinquency (DPD > 90)**: **50% Discount**.
    *   **Standard**: **30% Discount**.
    *   *Note: "Job Loss" and "Medical Emergency" clauses are NOT applied to Credit Cards, based on a strict reading of the policy structure.*

2.  **Personal Loans (PL)**
    *   **Job Loss**: **50% Discount**. (Triggered by "job loss", "unemployment", "lost my job").
    *   **Medical Emergency**: **45% Discount**. (Triggered by "hospital", "medical").
    *   **High Delinquency (DPD > 90)**: **35% Discount**.
    *   **Standard**: **20% Discount**.
    *   *The agent applies the MAXIMUM applicable discount for PL.*

3.  **General Rules**
    *   **Rounding**: All offers are rounded to the nearest 100.

## Usage

### Prerequisites
- Python 3.x
- No external dependencies required.

### Running the Agent
To generate the settlement offers, run the following command from the project root:

```bash
python solution.py
```

This will:
1.  Load borrower data from `data/borrower_data.csv`.
2.  Load chat scenarios from `data/chat_scenarios.json`.
3.  Process each scenario against the policy rules.
4.  Generate `submission.csv` with the `min_acceptable_offer` for each scenario.

## Files
-   `solution.py`: Main script containing the logic.
-   `submission.csv`: Output file with calculated offers.
-   `data/`: Directory containing input data.
