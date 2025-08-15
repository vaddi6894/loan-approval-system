-- Create database and tables for loan approval app
CREATE DATABASE IF NOT EXISTS loan_app;
USE loan_app;

-- Table to store submitted applications and predictions
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id VARCHAR(64) NULL,
    no_of_dependents INT NULL,
    education VARCHAR(32) NULL,
    self_employed VARCHAR(8) NULL,
    income_annum BIGINT NULL,
    loan_amount BIGINT NULL,
    loan_term INT NULL,
    cibil_score INT NULL,
    residential_assets_value BIGINT NULL,
    commercial_assets_value BIGINT NULL,
    luxury_assets_value BIGINT NULL,
    bank_asset_value BIGINT NULL,
    predicted_probability DECIMAL(6,5) NULL,
    predicted_status VARCHAR(16) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
