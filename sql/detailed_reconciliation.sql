

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
    ) AS invalid_categories;
