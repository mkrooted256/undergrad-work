use lab1;
go

delete from Abonents;
go
ALTER TABLE Abonents
check constraint AbonentDivisionForeign;
go

INSERT INTO [dbo].[Abonents]
     VALUES
           ('111-11-11', 'Lastname1', 'Name1', 'Fathername1', '01-11-2001', '101', 'Security'),
           ('111-11-12', 'Lastname2', 'Name2', 'Fathername2', '02-11-2001', '101', 'UNNAMED DIVISION');
GO

-- ^ error.  The INSERT statement conflicted with the FOREIGN KEY constraint "AbonentDivisionForeign"

ALTER TABLE Abonents
nocheck constraint AbonentDivisionForeign;

INSERT INTO [dbo].[Abonents]
     VALUES
           ('111-11-11', 'Lastname1', 'Name1', 'Fathername1', '01-11-2001', '101', 'Security'),
           ('111-11-12', 'Lastname2', 'Name2', 'Fathername2', '02-11-2001', '101', 'UNNAMED DIVISION');
GO

select * from Abonents;
go

-- ^ everything ok.

ALTER TABLE Abonents
check constraint AbonentDivisionForeign;
go

-- ^ ok

INSERT INTO [dbo].[Abonents]
     VALUES
           ('111-11-13', 'Lastname3', 'Name3', 'Fathername3', '03-11-2001', '101', 'UNNAMED DIVISION 2');
GO

-- ^ error. The INSERT statement conflicted with the FOREIGN KEY constraint "AbonentDivisionForeign"


ALTER TABLE Abonents
with check
check constraint AbonentDivisionForeign;
go

-- ^ error. now we are checking old data. 
-- ALTER TABLE statement conflicted with the FOREIGN KEY constraint "AbonentDivisionForeign"

select * from
	Abonents A left join Divisions D
	on A.DivisionName = D.DivisionName
	where D.DivisionName is null;

-- Now lets delete all Abonents with invalid DivisionName
delete A from
	Abonents A left join Divisions D
	on A.DivisionName = D.DivisionName
	where D.DivisionName is null;
-- Done!


ALTER TABLE Abonents
with check
check constraint AbonentDivisionForeign;
go

-- ^ ok!

INSERT INTO [dbo].[Abonents]
     VALUES
           ('111-11-13', 'Lastname3', 'Name3', 'Fathername3', '03-11-2001', '101', 'UNNAMED DIVISION 2');
GO

-- ok, error!