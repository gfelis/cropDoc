DROP TABLE IF EXISTS fields;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS fields_points;

CREATE TABLE fields (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  field_name TEXT UNIQUE NOT NULL,
  region TEXT NOT NULL,
  country TEXT NOT NULL
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT UNIQUE NOT NULL,
    field_id INTEGER,
    longitude TEXT,
    latitude TEXT,
    altitude TEXT,
    diagnose DECIMAL NOT NULL,
    FOREIGN KEY (field_id) REFERENCES fields (id) 
);

CREATE TABLE fields_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_id INTEGER NOT NULL,
    longitude TEXT NOT NULL,
    latitude TEXT NOT NULL,
    altitude TEXT NOT NULL,
    FOREIGN KEY (field_id) REFERENCES fields (id) 
);