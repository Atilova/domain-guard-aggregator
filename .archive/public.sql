
WITH RunningTotalCTE AS (
    SELECT id,
           api_key,
           available_requests,
           sign_up_date,
           SUM(available_requests) OVER (ORDER BY sign_up_date ASC) AS running_total
    FROM "securitytrails_account"
    WHERE is_active=true
)
SELECT id, 
       api_key, 
       available_requests, 
       sign_up_date,
       running_total
FROM RunningTotalCTE
WHERE running_total <= 200
OR id = (
    SELECT id
    FROM RunningTotalCTE
    WHERE running_total > 200
    ORDER BY id
    LIMIT 1
)
ORDER BY sign_up_date ASC;

-- Todo: determine how to make it recursive
WITH RunningTotalCTE AS (
    SELECT 
        id,
        api_key,
        available_requests,
        sign_up_date,
        SUM(available_requests) OVER (ORDER BY sign_up_date ASC) AS running_total
    FROM 
        "securitytrails_account"
),
FirstExceedCTE AS (
    SELECT 
        id
    FROM 
        RunningTotalCTE
    WHERE 
        running_total > 200
    ORDER BY 
        sign_up_date
    LIMIT 1
)
SELECT 
    id, 
    api_key, 
    available_requests, 
    sign_up_date, 
    running_total
FROM 
    RunningTotalCTE
WHERE 
    running_total <= 200
    OR id = (SELECT id FROM FirstExceedCTE)
ORDER BY 
    sign_up_date ASC;