CREATE TABLE IF NOT EXISTS Language (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	lang VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Books (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Sites (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	site VARCHAR(255) NOT NULL,
	url VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Authors (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS PublishingHouses (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS CoveragesTypes (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS IllustrationTypes (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	genre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS AdditionalCharacteristics (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Publication (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	book_id INTEGER NOT NULL,
	publisher_id INTEGER NOT NULL,
	FOREIGN KEY (publisher_id) REFERENCES PublishingHouses(id),
	FOREIGN KEY (book_id) REFERENCES Books(id)
);

CREATE TABLE IF NOT EXISTS Recension (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
	publication_id INTEGER NOT NULL,
	link VARCHAR(255) NOT NULL,
	FOREIGN KEY (publication_id) REFERENCES Publication(id)
);

CREATE TABLE IF NOT EXISTS PublicationSite (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	publication_id INTEGER NOT NULL,
	site_id INTEGER NOT NULL,
	price REAL NOT NULL,
	image_url VARCHAR(255),
	FOREIGN KEY (site_id) REFERENCES Sites(id),
	FOREIGN KEY (publication_id) REFERENCES Publication(id)
);

CREATE TABLE IF NOT EXISTS PublicationAuthors (
	publication_id INTEGER NOT NULL,
	authors_id INTEGER NOT NULL,
	PRIMARY KEY (publication_id, authors_id),
	FOREIGN KEY (publication_id) REFERENCES Publication(id),
	FOREIGN KEY (authors_id) REFERENCES Authors(id)
);

CREATE TABLE IF NOT EXISTS Annotation (
	publication_site_id INTEGER NOT NULL,
	lang_id INTEGER NOT NULL,
	description TEXT NOT NULL,
	PRIMARY KEY (publication_site_id, lang_id),
	FOREIGN KEY (lang_id) REFERENCES Language(id),
	FOREIGN KEY (publication_site_id) REFERENCES PublicationSite(id)
);

CREATE TABLE IF NOT EXISTS Characteristics (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	publication_id INTEGER,
	ISBN VARCHAR(255) NOT NULL,
	year INTEGER NOT NULL,
	page_count INTEGER NOT NULL,
	dim_x INTEGER,
	dim_y INTEGER,
	dim_z INTEGER,
	cover_id INTEGER,
	illustration_id INTEGER,
	FOREIGN KEY (publication_id) REFERENCES Publication(id),
	FOREIGN KEY (cover_id) REFERENCES CoveragesTypes(id),
	FOREIGN KEY (illustration_id) REFERENCES IllustrationTypes(id)
);

CREATE TABLE IF NOT EXISTS CharacteristicsAdditional (
	characteristic_id INTEGER NOT NULL,
	additional_id INTEGER NOT NULL,
	value TEXT NOT NULL,
	PRIMARY KEY (characteristic_id, additional_id),
	FOREIGN KEY (additional_id) REFERENCES AdditionalCharacteristics(id),
	FOREIGN KEY (characteristic_id) REFERENCES Characteristics(publication_id)
);

CREATE TABLE IF NOT EXISTS CharacteristicsGenre (
    characteristic_id INTEGER NOT NULL,
	genre_id INTEGER NOT NULL,
	PRIMARY KEY (genre_id, characteristic_id),
	FOREIGN KEY (genre_id) REFERENCES Genre(id),
	FOREIGN KEY (characteristic_id) REFERENCES Characteristics(id)
);
