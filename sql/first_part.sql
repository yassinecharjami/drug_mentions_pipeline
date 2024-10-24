/*
Table : TRANSACTIONS
Goal: total sales amount from 01-01-2019 to 31-12-2019 sorted by date
*/

SELECT date, SUM(prod_price * prod_qty) AS ventes
FROM TRANSACTIONS
WHERE date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY date
ORDER BY date;