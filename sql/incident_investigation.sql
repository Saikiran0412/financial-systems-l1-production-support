
SELECT
    COUNT(*) AS missing_count,
    MIN(s.transaction_id) AS first_missing_id,
    MAX(s.transaction_id) AS last_missing_id,
    ROUND(SUM(s.amount), 2) AS missing_amount
FROM
    `financial-l1-support-mvp.financial_prod_support.source_transactions ` s
LEFT JOIN
    `financial-l1-support-mvp.financial_prod_support.processed_transactions` p
    ON s.transaction_id = p.transaction_id
WHERE
    p.transaction_id IS NULL;

SELECT
    COUNT(*) AS missing_count,
    MIN(s.transaction_id) AS first_missing_id,
    MAX(s.transaction_id) AS last_missing_id,
    ROUND(SUM(s.amount), 2) AS missing_amount
FROM
    `financial-l1-support-mvp.financial_prod_support.source_transactions ` s
LEFT JOIN
    `financial-l1-support-mvp.financial_prod_support.processed_transactions` p
    ON s.transaction_id = p.transaction_id
WHERE
    p.transaction_id IS NULL;
