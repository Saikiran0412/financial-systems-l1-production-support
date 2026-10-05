# Financial Systems L1 Production Support

## Project Overview

This is a personal project I created to demonstrate my understanding of financial systems production support, data validation, reconciliation, incident investigation, and post-resolution verification.

The project uses sample financial transaction data and simulates an end-to-end financial data processing workflow.

## Architecture

Sample Financial Transactions  
↓  
BigQuery Source  
↓  
Apache Airflow  
↓  
Source Check  
↓  
Transformation  
↓  
Validation  
↓  
Reconciliation  
↓  
Reporting Ready

## Technologies Used

- Google BigQuery
- SQL
- Apache Airflow
- Python
- Docker

BigQuery was new to me from a hands-on perspective. I independently learned the platform and applied it in this project for data loading, SQL analysis, transformation, validation, and reconciliation.

## Production Support Scenario

The source dataset contained:

- 10,000 transactions
- Total amount: $7,534,207.55

I introduced a controlled data issue to simulate a production incident.

The Airflow workflow detected a validation mismatch:

| Control | Source | Processed |
|---|---:|---:|
| Transaction Count | 10,000 | 9,850 |
| Financial Amount | $7,534,207.55 | $7,415,119.44 |

The validation failure prevented the downstream reconciliation and reporting steps from proceeding.

## L1 Investigation

I used SQL to compare the source and processed datasets.

The investigation identified:

- 150 missing transactions
- Transaction range: TX000001 – TX000150
- Financial variance: $119,088.11

The root cause was an incorrect transformation filter that excluded the affected transactions.

## Resolution and Reconciliation

After correcting the issue, I reprocessed the workflow and performed post-fix validation.

Final results:

- Source transactions: 10,000
- Processed transactions: 10,000
- Source amount: $7,534,207.55
- Processed amount: $7,534,207.55
- Missing transactions: 0
- Duplicate transaction IDs: 0
- Required NULL values: 0
- Invalid amount categories: 0
- Final status: Reporting Ready

## L1 Support Approach

Monitor → Detect → Triage → Investigate → Assess Financial Impact → Identify Root Cause → Support Resolution → Reprocess → Validate → Reconcile → Close

## Disclaimer

This is an independently created personal project using generated sample data for learning and demonstration purposes.

It does not represent American Express systems, architecture, processes, customer information, or proprietary data.
