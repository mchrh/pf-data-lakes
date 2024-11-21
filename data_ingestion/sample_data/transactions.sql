CREATE TABLE transactions (
transaction_id INTEGER,
amount DECIMAL(10,2),
customer_name VARCHAR(100)
);

INSERT INTO transactions VALUES
(1, 99.99, 'John Doe'),
(2, 149.99, 'Jane Smith'),
(3, 79.99, 'Bob Wilson');