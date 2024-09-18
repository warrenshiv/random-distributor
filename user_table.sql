
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    number INTEGER
);

INSERT INTO User (email, number) VALUES 
    ('member1@example.com', NULL),
    ('member2@example.com', NULL),
    ('member3@example.com', NULL),
    ('member4@example.com', NULL),
    ('member5@example.com', NULL),
    ('member6@example.com', NULL),
    ('member7@example.com', NULL),
    ('member8@example.com', NULL),
    ('member9@example.com', NULL),
    ('member10@example.com', NULL);
