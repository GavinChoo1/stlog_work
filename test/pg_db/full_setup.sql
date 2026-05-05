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
ALTER SCHEMA general OWNER TO admin;

-- Set search path to prioritize general schema
SET search_path = general, public;

-- 1. Create the 'accounts' table in general schema
CREATE TABLE IF NOT EXISTS general.accounts (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE general.accounts OWNER TO admin;

-- 2. Insert the test credentials
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

-- 3. Verify the data
SELECT * FROM general.accounts;

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
