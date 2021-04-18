CREATE TABLE dbo.Box ( 
	Id                   bigint NOT NULL   IDENTITY ,
	Label                nvarchar(max) NOT NULL    ,
	Description          nvarchar(max) NOT NULL    ,
	CONSTRAINT Pk_Box_Id PRIMARY KEY  ( Id ) 
 );

CREATE TABLE dbo.Item ( 
	Id                   bigint NOT NULL   IDENTITY ,
	BoxId                bigint NOT NULL    ,
	Name                 nvarchar(max) NOT NULL    ,
	CONSTRAINT Pk_Item_Id PRIMARY KEY  ( Id ) 
 );

ALTER TABLE dbo.Item ADD CONSTRAINT fk_item_box FOREIGN KEY ( BoxId ) REFERENCES dbo.Box( Id ) ON DELETE CASCADE ON UPDATE CASCADE;
