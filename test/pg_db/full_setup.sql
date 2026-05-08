--
-- PostgreSQL database setup
--

-- The 'admin' role is already created by the Docker image via POSTGRES_USER environment variable.

--
-- Create additional databases requested by user
--
CREATE DATABASE hot_db OWNER admin;
CREATE DATABASE cold_db OWNER admin;

--
-- Setup hot_db
--
\connect hot_db

CREATE SCHEMA IF NOT EXISTS general;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE TABLE IF NOT EXISTS orders.orders (
    order_id SERIAL PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE orders.orders OWNER TO admin;

ALTER SCHEMA general OWNER TO admin;
ALTER SCHEMA orders OWNER TO admin;

-- Set search path to prioritize general schema
SET search_path = general, orders, public;

-- 1. Create the 'accounts' table in general schema
CREATE TABLE IF NOT EXISTS general.accounts (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE general.accounts OWNER TO admin;

INSERT INTO general.accounts(username, password_hash, role) VALUES
('test_user_01', 'P@ssword123!', 'Standard'),
('admin_tester', 'Admin#Alpha2026', 'Admin'),
('qa_engineer', 'Verify_Me_99', 'QA'),
('guest_viewer', 'GuestAccess#1', 'Guest'),
('dev_local', 'LocalDev_Safe88', 'Developer'),
('beta_tester_A', 'Beta_Testing!22', 'Beta'),
('manager_test', 'Mng_Secure_7', 'Manager'),
('support_demo', 'HelpDesk_2026', 'Support'),
('power_user_09', 'PowerUp_9977!', 'Power User'),
('readonly_user', 'JustLooking!0', 'Read-Only')
ON CONFLICT (username) DO NOTHING;

SELECT * FROM general.accounts;

-- 2. Create the 'orders' table in orders schema
CREATE TABLE IF NOT EXISTS orders.raw_orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    item VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE orders.raw_orders OWNER TO admin;

-- 3. Create the 'raw_hc_operation_orders_5m' table in orders schema
CREATE TABLE IF NOT EXISTS orders.raw_hc_operation_orders_5m (
    dtstatdate_h text NOT NULL, 
    id int NOT NULL,
    vertical_id int,
    project_id int,
    delivery_order_id int,
    zone_id int,
    start_point_id int,
    end_point_id int,
    vehicle_id int,
    repeat_direction_id int,
    vehicle_task_id int,
    courier_ms_job_id int,
    packing_task_id int,
    name varchar(100),
    description varchar(4000),
    start_date_time timestamptz,
    delivery_date timestamptz,
    duration varchar(100),
    start_point_instruction varchar(4000),
    end_point_instruction varchar(4000),
    tags varchar(4000),
    error_description varchar(4000),
    closure_reason varchar(4000),
    group_code varchar(50),
    group_name varchar(20),
    do_number varchar(100),
    end_point_code varchar(50),
    is_product_code_scan_enabled boolean,
    is_customer_card_scan_enabled boolean,
    is_nric_scan_enabled boolean,
    is_sending_email boolean,
    is_sending_sms boolean,
    is_sent_email boolean,
    is_rescheduled boolean,
    is_courier_ms boolean,
    external_updated_date_time timestamptz,
    epod_distance_meter float,
    priority int,
    task_status int,
    file_uploaded_count int,
    require_start_point_epod boolean,
    require_end_point_epod boolean,
    parent_id int,
    route_plan_no varchar(100),
    delivery_route_plan_date_time timestamptz,
    is_sent_consolidated_email boolean,
    sensitive_do boolean,
    created_date_time timestamptz,
    modified_date_time timestamptz,
    created_user_id varchar(128),
    modified_user_id varchar(128), -- Fixed: Added missing comma
    
    -- Fixed: Added 'id' to the PK to ensure ID uniqueness per partition
    PRIMARY KEY (id, dtstatdate_h) 
) PARTITION BY RANGE (dtstatdate_h);

ALTER TABLE orders.raw_hc_operation_orders_5m OWNER TO admin;





--
-- Database "postgres" setup (if needed)
--
\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL setup complete
--
