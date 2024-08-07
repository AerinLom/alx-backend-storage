-- Create the index on the first letter of name and the score
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
