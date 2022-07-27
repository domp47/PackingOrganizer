CREATE TABLE box ( 
	id                   INTEGER PRIMARY KEY AUTOINCREMENT,
	label                varchar(512) NOT NULL,
	description          varchar(512) NOT NULL
);

CREATE TABLE item ( 
	id                   INTEGER PRIMARY KEY AUTOINCREMENT,
	box_id               bigint NOT NULL,
	name                 varchar(512) NOT NULL,
	FOREIGN KEY(box_id) REFERENCES box(id)
);