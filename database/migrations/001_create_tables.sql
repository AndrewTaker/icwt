-- Create the category table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Create the product table
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES category(id) ON DELETE CASCADE
);

-- Create the sale table
CREATE TABLE sale (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0),
    sale_date DATE NOT NULL
);

-- Insert sample data into the category table
INSERT INTO category (name) VALUES
('Electronics'),
('Clothing'),
('Books');

-- Insert sample data into the product table
INSERT INTO product (name, category_id) VALUES
('Laptop', 1),          -- Electronics
('Smartphone', 1),      -- Electronics
('T-Shirt', 2),         -- Clothing
('Jeans', 2),           -- Clothing
('Python Programming', 3), -- Books
('The Great Gatsby', 3);   -- Books

-- Insert sample data into the sale table
INSERT INTO sale (product_id, quantity, sale_date) VALUES
(1, 2, '2023-10-01'),  -- 2 Laptops sold on 2023-10-01
(2, 5, '2023-10-02'),  -- 5 Smartphones sold on 2023-10-02
(3, 10, '2023-10-03'), -- 10 T-Shirts sold on 2023-10-03
(4, 7, '2023-10-04'),  -- 7 Jeans sold on 2023-10-04
(5, 3, '2023-10-05'),  -- 3 Python Programming books sold on 2023-10-05
(6, 8, '2023-10-06');  -- 8 The Great Gatsby books sold on 2023-10-06
