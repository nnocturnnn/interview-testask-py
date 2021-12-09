SELECT category_name HAVING AVG(cost) > 500  FROM `aderts` 
INNER JOIN `costs` 
ON `aderts`.`aderts_id`=`costs`.`aderts_id`;