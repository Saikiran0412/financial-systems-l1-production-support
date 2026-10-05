-- Source Data Validation
-- L1 control to confirm transaction volume and financial amount.

SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM
    `financial-l1-support-mvp.financial_prod_support.source_transactions `;
