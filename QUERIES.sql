
-- CREATE DATABASE smartphone_analytics_db;
-- USE smartphone_analytics_db;

-- CREATE TABLE dim_phones (
--     phone_id INT PRIMARY KEY,
--     brand VARCHAR(50),
--     model_name VARCHAR(100),
--     storage VARCHAR(20),
--     base_price DECIMAL(10, 2)
-- );

-- CREATE TABLE dim_stores (
--     store_id INT PRIMARY KEY,
--     store_location VARCHAR(50),
--     store_type VARCHAR(50)
-- );

-- CREATE TABLE fact_sales (
--     order_id INT PRIMARY KEY AUTO_INCREMENT,
--     order_date DATE,
--     phone_id INT,
--     store_id INT,
--     quantity INT,
--     discount_percent DECIMAL(5, 2),
--     final_price DECIMAL(10, 2),
--     profit_margin DECIMAL(10, 2),
--     FOREIGN KEY (phone_id) REFERENCES dim_phones(phone_id),
--     FOREIGN KEY (store_id) REFERENCES dim_stores(store_id)
-- );

-- VIEW ----->>>

-- CREATE VIEW v_executive_summary AS
-- SELECT 
--     f.order_date,
--     p.brand,
--     p.model_name,
--     s.store_location,
--     s.store_type,
--     f.quantity,
--     f.final_price AS revenue,
--     f.profit_margin AS profit,
--     (f.profit_margin / f.final_price) * 100 AS profit_percentage
-- FROM fact_sales f
-- JOIN dim_phones p ON f.phone_id = p.phone_id
-- JOIN dim_stores s ON f.store_id = s.store_id;

-- SELECT * FROM v_executive_summary;

-- CTE ----->>>

-- USE smartphone_analytics_db;
-- WITH RankedSales AS (
--     SELECT 
--         store_location,
--         model_name,
--         SUM(quantity) as units_sold,
--         DENSE_RANK() OVER(PARTITION BY store_location ORDER BY SUM(quantity) DESC) as sales_rank
--     FROM v_executive_summary
--     GROUP BY store_location, model_name
-- )

-- SELECT * FROM RankedSales WHERE sales_rank <= 3;

-- PROCEDURE ----->>>
-- USE smartphone_analytics_db;
-- DELIMITER //
-- CREATE PROCEDURE CheckStoreTarget(IN target_amt DECIMAL(10,2))
-- BEGIN
--     SELECT 
--         store_location, 
--         SUM(revenue) as total_sales,
--         CASE 
--             WHEN SUM(revenue) >= target_amt THEN 'Target Achieved ✅'
--             ELSE 'Below Target ❌'
--         END as status
--     FROM v_executive_summary
--     GROUP BY store_location;
-- END //

-- DELIMITER ;
-- CALL CheckStoreTarget(5000000);




