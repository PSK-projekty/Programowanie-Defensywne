CREATE TABLE clients (
	id INTEGER NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	password_hash VARCHAR NOT NULL, 
	phone_number VARCHAR NOT NULL, 
	address VARCHAR NOT NULL, 
	postal_code VARCHAR NOT NULL, 
	totp_secret VARCHAR, 
	totp_confirmed BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_clients_id ON clients (id);
CREATE UNIQUE INDEX ix_clients_email ON clients (email);
CREATE TABLE doctors (
	id INTEGER NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	password_hash VARCHAR NOT NULL, 
	specialization VARCHAR NOT NULL, 
	permit_number VARCHAR NOT NULL, 
	totp_secret VARCHAR, 
	totp_confirmed BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_doctors_id ON doctors (id);
CREATE UNIQUE INDEX ix_doctors_email ON doctors (email);
CREATE TABLE consultants (
	id INTEGER NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	password_hash VARCHAR NOT NULL, 
	totp_secret VARCHAR, 
	totp_confirmed BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_consultants_email ON consultants (email);
CREATE INDEX ix_consultants_id ON consultants (id);
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE animals (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	species VARCHAR NOT NULL, 
	breed VARCHAR, 
	gender VARCHAR, 
	birth_date DATE, 
	age INTEGER, 
	weight FLOAT, 
	microchip_number VARCHAR, 
	notes TEXT, 
	owner_id INTEGER NOT NULL, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP), last_visit DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES clients (id), 
	UNIQUE (microchip_number)
);
CREATE INDEX ix_animals_id ON animals (id);
CREATE INDEX ix_animals_name ON animals (name);
CREATE INDEX ix_animals_species ON animals (species);
CREATE TABLE appointments (
	id INTEGER NOT NULL, 
	visit_datetime DATETIME NOT NULL, 
	reason TEXT, 
	status VARCHAR NOT NULL, 
	doctor_id INTEGER NOT NULL, 
	animal_id INTEGER NOT NULL, 
	owner_id INTEGER NOT NULL, 
	notes TEXT, 
	created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	PRIMARY KEY (id), 
	FOREIGN KEY(animal_id) REFERENCES animals (id), 
	FOREIGN KEY(doctor_id) REFERENCES doctors (id), 
	FOREIGN KEY(owner_id) REFERENCES clients (id)
);
CREATE INDEX ix_appointments_id ON appointments (id);
