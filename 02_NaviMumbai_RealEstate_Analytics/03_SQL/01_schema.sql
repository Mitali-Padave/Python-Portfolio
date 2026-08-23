CREATE DATABASE magicbricks;
USE magicbricks;

CREATE TABLE properties_raw (
    title           VARCHAR(255),
    price           VARCHAR(50),
    area            VARCHAR(50),
    bhk             INT,
    bathroom        INT,
    furnishing      VARCHAR(50),
    floor           VARCHAR(50),
    transaction     VARCHAR(50),
    society         VARCHAR(255),
    posted_by       VARCHAR(255),
    price_inr       DOUBLE,
    area_type       VARCHAR(20),
    area_sqft       DOUBLE,
    locality        VARCHAR(100),
    floor_no        INT,
    total_floors    INT,
    posted_by_type  VARCHAR(50),
    posted_by_name  VARCHAR(255),
    price_per_sqft  DOUBLE,
    pps_outlier     INT,
    price_band      VARCHAR(50)
);


DROP TABLE properties_raw;

CREATE TABLE properties_raw (
    title           VARCHAR(255),
    price           VARCHAR(50),
    area            VARCHAR(50),
    bhk             INT,
    bathroom        INT,
    furnishing      VARCHAR(50),
    floor           VARCHAR(50),
    `transaction`   VARCHAR(50),
    society         VARCHAR(255),
    posted_by       VARCHAR(255),
    price_inr       DOUBLE,
    area_type       VARCHAR(20),
    area_sqft       DOUBLE,
    locality        VARCHAR(100),
    floor_no        VARCHAR(20),   -- was INT, now text to survive blanks
    total_floors    VARCHAR(20),   -- was INT, now text to survive blanks
    posted_by_type  VARCHAR(50),
    posted_by_name  VARCHAR(255),
    price_per_sqft  DOUBLE,
    pps_outlier     INT,
    price_band      VARCHAR(50)
);

SELECT COUNT(*) FROM properties_raw;

CREATE TABLE localities (
    locality_id   INT AUTO_INCREMENT PRIMARY KEY,
    locality_name VARCHAR(100) UNIQUE
);

DELETE FROM localities;
ALTER TABLE localities AUTO_INCREMENT = 1;

INSERT INTO localities (locality_name)
SELECT DISTINCT locality
FROM properties_raw
WHERE locality IS NOT NULL;

SELECT * FROM localities;



CREATE TABLE properties (
    property_id     INT AUTO_INCREMENT PRIMARY KEY,
    locality_id     INT,
    society         VARCHAR(255),
    bhk             INT,
    bathroom        INT,
    area_type       VARCHAR(20),
    area_sqft       DOUBLE,
    furnishing      VARCHAR(50),
    floor_no        INT,
    total_floors    INT,
    transaction_type VARCHAR(50),
    posted_by_type  VARCHAR(50),
    posted_by_name  VARCHAR(255),
    price_inr       DOUBLE,
    price_per_sqft  DOUBLE,
    pps_outlier     INT,
    price_band      VARCHAR(50),
    FOREIGN KEY (locality_id) REFERENCES localities(locality_id)
);
SET SQL_SAFE_UPDATES = 0;
UPDATE properties_raw
SET floor_no = NULL
WHERE floor_no = '' OR TRIM(floor_no) = '';

UPDATE properties_raw
SET total_floors = NULL
WHERE total_floors = '' OR TRIM(total_floors) = '';

DELETE FROM properties;
ALTER TABLE properties AUTO_INCREMENT = 1;

INSERT INTO properties (
    locality_id, society, bhk, bathroom, area_type, area_sqft,
    furnishing, floor_no, total_floors, transaction_type,
    posted_by_type, posted_by_name, price_inr, price_per_sqft, price_band
)
SELECT
    l.locality_id, r.society, r.bhk, r.bathroom, r.area_type, r.area_sqft,
    r.furnishing, r.floor_no, r.total_floors, r.`transaction`,
    r.posted_by_type, r.posted_by_name, r.price_inr, r.price_per_sqft, r.price_band
FROM properties_raw r
LEFT JOIN localities l ON r.locality = l.locality_name;

SHOW COLUMNS FROM properties_raw;

SELECT COUNT(*) FROM properties;
SELECT COUNT(*) FROM properties WHERE floor_no IS NULL;
SELECT COUNT(*) FROM properties WHERE floor_no = 0;

SELECT COUNT(*) FROM localities;
SELECT COUNT(*) FROM properties_raw;