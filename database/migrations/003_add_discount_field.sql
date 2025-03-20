ALTER TABLE sale ADD COLUMN discount FLOAT;

UPDATE sale
SET discount = ROUND((RANDOM() * (0.25 - 0.05) + 0.05)::NUMERIC, 2);
