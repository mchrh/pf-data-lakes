CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE
);

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2),
    transaction_date TIMESTAMP,
    product_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES
(1, 'John Doe', 'john.doe@email.com', '2024-01-01'),
(2, 'Jane Smith', 'jane.smith@email.com', '2024-01-02'),
(3, 'Bob Wilson', 'bob.wilson@email.com', '2024-01-03');

INSERT INTO transactions VALUES
(1, 1, 99.99, '2024-01-01 10:00:00', 123),
(2, 2, 149.99, '2024-01-02 11:30:00', 124),
(3, 1, 79.99, '2024-01-03 15:45:00', 125);