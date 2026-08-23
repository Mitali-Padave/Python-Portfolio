-- Top 10 most expensive localities (avg price per sqft) - uses the JOIN
SELECT l.locality_name,
       ROUND(AVG(p.price_per_sqft)) AS avg_price_per_sqft,
       COUNT(*) AS listings
FROM properties p
JOIN localities l ON p.locality_id = l.locality_id
GROUP BY l.locality_name
ORDER BY avg_price_per_sqft DESC
LIMIT 10;

-- Cheapest 10 localities
SELECT l.locality_name,
       ROUND(AVG(p.price_per_sqft)) AS avg_price_per_sqft,
       COUNT(*) AS listings
FROM properties p
JOIN localities l ON p.locality_id = l.locality_id
GROUP BY l.locality_name
ORDER BY avg_price_per_sqft ASC
LIMIT 10;

-- Average price by bhk

SELECT bhk,
       COUNT(*) AS listings,
       ROUND(AVG(price_inr)) AS avg_price,
       ROUND(AVG(area_sqft)) AS avg_area
FROM properties
GROUP BY bhk
ORDER BY bhk;

-- How furnishing affects price

SELECT furnishing,
       COUNT(*) AS listings,
       ROUND(AVG(price_inr)) AS avg_price
FROM properties
GROUP BY furnishing
ORDER BY avg_price DESC;

-- Who posts listings - owner vs agent vs builder

SELECT posted_by_type,
       COUNT(*) AS listings,
       ROUND(AVG(price_inr)) AS avg_price
FROM properties
GROUP BY posted_by_type
ORDER BY listings DESC;
