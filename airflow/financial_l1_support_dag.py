from airflow.sdk import DAG, task
from datetime import datetime


with DAG(
    dag_id="financial_l1_support",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["financial", "l1-support"],
) as dag:

    @task
    def check_source():
        from google.cloud import bigquery

        print("Starting source data validation...")

        client = bigquery.Client(project="financial-l1-support-mvp")

        query = """
        SELECT
            COUNT(*) AS total_transactions,
            ROUND(SUM(amount), 2) AS total_amount
        FROM `financial-l1-support-mvp.financial_prod_support.source_transactions `
        """

        result = list(client.query(query).result())[0]

        print("Transaction count:", result.total_transactions)
        print("Total amount:", result.total_amount)

        if result.total_transactions == 0:
            raise ValueError(
                "Source validation failed: no transactions found."
            )

        print("Source validation PASSED.")
        return "SOURCE_OK"

    @task   
    def transform_transactions():
        from google.cloud import bigquery

        print("Starting financial transaction transformation...")

        client = bigquery.Client(project="financial-l1-support-mvp")

        query = """
        CREATE OR REPLACE TABLE
          `financial-l1-support-mvp.financial_prod_support.processed_transactions`
        AS
        SELECT
          transaction_id,
          transaction_date,
          amount,
          currency,
          merchant_category,
          status,
          source_system,
          batch_id,
          CASE
            WHEN amount < 100 THEN 'LOW'
            WHEN amount < 500 THEN 'MEDIUM'
            ELSE 'HIGH'
          END AS amount_category
        FROM
          `financial-l1-support-mvp.financial_prod_support.source_transactions `
        """

        client.query(query).result()

        print("Transformation completed successfully.")

    @task
    def validate_transactions():
        from google.cloud import bigquery

        print("Starting source-to-processed validation...")

        client = bigquery.Client(project="financial-l1-support-mvp")

        query = """
        SELECT
            (SELECT COUNT(*)
             FROM `financial-l1-support-mvp.financial_prod_support.source_transactions `)
                AS source_count,

            (SELECT ROUND(SUM(amount), 2)
             FROM `financial-l1-support-mvp.financial_prod_support.source_transactions `)
                AS source_amount,

            (SELECT COUNT(*)
             FROM `financial-l1-support-mvp.financial_prod_support.processed_transactions`)
                AS processed_count,

            (SELECT ROUND(SUM(amount), 2)
             FROM `financial-l1-support-mvp.financial_prod_support.processed_transactions`)
                AS processed_amount
        """

        result = list(client.query(query).result())[0]

        print("Source count:", result.source_count)
        print("Processed count:", result.processed_count)
        print("Source amount:", result.source_amount)
        print("Processed amount:", result.processed_amount)

        if result.source_count != result.processed_count:
            raise ValueError(
                f"Validation FAILED: source count "
                f"{result.source_count} does not match processed count "
                f"{result.processed_count}"
            )

        if result.source_amount != result.processed_amount:
            raise ValueError(
                f"Validation FAILED: source amount "
                f"{result.source_amount} does not match processed amount "
                f"{result.processed_amount}"
            )

        print("Validation PASSED: source and processed data match.")
    @task
    def reconcile_transactions():
        from google.cloud import bigquery

        print("Starting detailed financial reconciliation...")

        client = bigquery.Client(project="financial-l1-support-mvp")

        query = """
        SELECT
            (
                SELECT COUNT(*)
                FROM `financial-l1-support-mvp.financial_prod_support.source_transactions ` s
                LEFT JOIN `financial-l1-support-mvp.financial_prod_support.processed_transactions` p
                    ON s.transaction_id = p.transaction_id
                WHERE p.transaction_id IS NULL
            ) AS missing_transactions,

            (
                SELECT COUNT(*)
                FROM (
                    SELECT transaction_id
                    FROM `financial-l1-support-mvp.financial_prod_support.processed_transactions`
                    GROUP BY transaction_id
                    HAVING COUNT(*) > 1
                )
            ) AS duplicate_transaction_ids,

            (
                SELECT COUNT(*)
                FROM `financial-l1-support-mvp.financial_prod_support.processed_transactions`
                WHERE transaction_id IS NULL
                   OR transaction_date IS NULL
                   OR amount IS NULL
                   OR currency IS NULL
            ) AS required_nulls,

            (
                SELECT COUNT(*)
                FROM `financial-l1-support-mvp.financial_prod_support.processed_transactions`
                WHERE (amount < 100 AND amount_category != 'LOW')
                   OR (amount >= 100 AND amount < 500
                       AND amount_category != 'MEDIUM')
                   OR (amount >= 500 AND amount_category != 'HIGH')
                   OR amount_category IS NULL
            ) AS invalid_categories
        """

        result = list(client.query(query).result())[0]

        print("Missing transactions:", result.missing_transactions)
        print("Duplicate transaction IDs:", result.duplicate_transaction_ids)
        print("Required NULL values:", result.required_nulls)
        print("Invalid amount categories:", result.invalid_categories)

        if result.missing_transactions != 0:
            raise ValueError(
                f"Reconciliation FAILED: "
                f"{result.missing_transactions} transactions are missing."
            )

        if result.duplicate_transaction_ids != 0:
            raise ValueError(
                f"Reconciliation FAILED: "
                f"{result.duplicate_transaction_ids} duplicate IDs found."
            )

        if result.required_nulls != 0:
            raise ValueError(
                f"Reconciliation FAILED: "
                f"{result.required_nulls} required NULL values found."
            )

        if result.invalid_categories != 0:
            raise ValueError(
                f"Reconciliation FAILED: "
                f"{result.invalid_categories} invalid amount categories found."
            )

        print("Reconciliation PASSED: all data-quality controls passed.")

    @task
    def reporting_ready():
        print("All financial data controls completed successfully.")
        print("Source validation: PASSED")
        print("Transformation: PASSED")
        print("Source-to-processed validation: PASSED")
        print("Detailed reconciliation: PASSED")
        print("Financial data is approved for downstream reporting.")
        return "REPORTING_READY"

    (
        check_source()
        >> transform_transactions()
        >> validate_transactions()
        >> reconcile_transactions()
        >> reporting_ready()
    )

