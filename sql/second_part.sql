-- Tables: TRANSACTIONS, PRODUCT_NOMENCLATURE

SELECT client_id, 
SUM(CASE WHEN pn.product_type = 'MEUBLE' THEN prod_price*prod_qty ELSE 0 END) as ventes_meuble, 
SUM(CASE WHEN pn.product_type = 'DECO' THEN prod_price*prod_qty ELSE 0 END) as ventes_deco 
FROM TRANSACTIONS t 
INNER JOIN PRODUCT_NOMENCLATURE pn 
ON t.prod_id = pn.product_id 
WHERE date BETWEEN '2019-01-01' AND '2019-12-31' 
GROUP BY client_id;