CREATE TABLE box ( 
	id                   SERIAL PRIMARY KEY,
	label                varchar(512) NOT NULL,
	description          varchar(512) NOT NULL
);

CREATE TABLE item ( 
	id                   SERIAL PRIMARY KEY,
	box_id               bigint NOT NULL,
	name                 varchar(512) NOT NULL
);

ALTER TABLE "item" ADD FOREIGN KEY ("box_id") REFERENCES "box" ("id");