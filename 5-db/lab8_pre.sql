use lab1;

alter table dbo.Abonents
	drop constraint AbonentNumberInDivisionUnique;

drop function dbo.getDivisionByName;
drop function dbo.getRoomByNumber;
drop function dbo.sameNumbersInDivisionByRoom;

drop table dbo.Abonents;
drop table dbo.Rooms;
drop table dbo.Divisions;
GO


create table Divisions (
	DivisionID int IDENTITY primary key,
	DivisionName varchar(32),
	DivisionType varchar(32)
);

create table Rooms (
	RoomID int IDENTITY primary key,
	RoomNumber varchar(10),
	RoomName varchar(32) null,
	RoomType varchar(16) null,
	RoomFloor SMALLINT,
	DivisionID int
);
GO

create table Abonents (
	AbonentID int IDENTITY primary key,
	Number varchar(16) not null,
	PName varchar(32) not null,
	IName varchar(32) not null,
	BName varchar(32) not null,
	DOB varchar(10) not null,
	RoomID int,
	CallsPerMonth int default rand(abs(checksum(NEWID()))) * 1000 
);
GO

-- This function is needed to insert new Rooms easily 
CREATE or alter FUNCTION dbo.getDivisionByName(@div_name varchar(32))
RETURNS int
WITH SCHEMABINDING
AS BEGIN
	RETURN (select DivisionID from dbo.Divisions where dbo.Divisions.DivisionName=@div_name);
END
GO

-- This function is needed to insert new Abonents easily 
-- Note: returns only FIRST FOUND room 
CREATE or alter FUNCTION dbo.getRoomByNumber(@room_num varchar(10))
RETURNS int
WITH SCHEMABINDING
AS BEGIN
	RETURN (select top (1) RoomID from dbo.Rooms where Rooms.RoomNumber=@room_num);
END
GO

-- Returns how many abonents with number @number are in the room's division 
CREATE or alter FUNCTION dbo.sameNumbersInDivisionByRoom(@number varchar(16), @room_id int)
RETURNS int
AS BEGIN
	declare @a int; 
	(select @a = count(Number) from dbo.Abonents as a join dbo.Rooms as r on a.RoomID = r.RoomID 
		where a.Number=@number and r.DivisionID = (select DivisionID from dbo.Rooms where RoomID=@room_id))
	return @a;
END
GO

-- Abonent Numbers must be unique in the scope of Division
alter table Abonents add 
constraint AbonentNumberInDivisionUnique
	CHECK (dbo.sameNumbersInDivisionByRoom([Number], RoomID) < 2);
go

------
------

--create trigger dbo.RandomizeAbonents
--on dbo.Abonents
--after INSERT 
--as
--	update dbo.Abonents 
--	set CallsPerMonth = rand(abs(checksum(NEWID()))) * 1000 
--	where Abonents.AbonentID in (select AbonentID from inserted);
--go
------
------


DELETE FROM [dbo].[Divisions];
GO

INSERT INTO [dbo].[Divisions]
           ([DivisionName]
           ,[DivisionType])
     VALUES
           ('Reception', 'Type1'),
		   ('Security', 'Type1'),
		   ('Engineering', 'Type2'),
		   ('HR', 'Type3'),
		   ('IT', 'Type3'),
		   ('Admin', 'Type3'),
		   ('Accounting', 'Type3')
GO

------

DELETE FROM [dbo].[Rooms];
GO

INSERT INTO [dbo].[Rooms]
           ([RoomNumber]
           ,[RoomName]
           ,[RoomType]
           ,[DivisionID]
           ,[RoomFloor])
     VALUES
           ('001'  , 'Reception', null, dbo.getDivisionByName('Reception'), 1),
           ('002'  , 'Outdoor Security', null, dbo.getDivisionByName('Security'), 1),
           ('101'  , 'Security HQ', 'Room', dbo.getDivisionByName('Security'), 1),
           ('102'  , 'Client Services', 'Room', dbo.getDivisionByName('Reception'), 1),
           ('103'  , 'Client Manager', 'Room', dbo.getDivisionByName('Reception'), 1),
           ('201'  , 'Administration', 'Room', dbo.getDivisionByName('Admin'), 2),
           ('201-2', 'CEO', 'Room', dbo.getDivisionByName('Admin'), 2),
           ('202'  , 'IT', 'Room', dbo.getDivisionByName('IT'), 2),
           ('202-2', 'CTO', 'Room', dbo.getDivisionByName('IT'), 2),
           ('210'  , 'IT Open Space', 'Open Space', dbo.getDivisionByName('IT'), 2),
			   ('210-1', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-2', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-3', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-4', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-5', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-6', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-7', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
			   ('210-8', null, 'Cubicle', dbo.getDivisionByName('IT'), 2),
           ('220', 'Engineer On-Duty', 'Room', dbo.getDivisionByName('Engineering'),2 ),
           ('221', 'Engineering', 'Open Space', dbo.getDivisionByName('Engineering'),2 ),
		       ('221-1', null, 'Desk', dbo.getDivisionByName('Engineering'), 2),
		       ('221-2', null, 'Desk', dbo.getDivisionByName('Engineering'), 2),
		       ('221-3', null, 'Desk', dbo.getDivisionByName('Engineering'), 2),
		       ('221-4', null, 'Desk', dbo.getDivisionByName('Engineering'), 2),
           ('330', 'Chief Accountant', 'Room', dbo.getDivisionByName('Admin'), 3),
           ('331', 'Finances', null, dbo.getDivisionByName('Admin'), 3),
		       ('331-1', null, 'Desk', dbo.getDivisionByName('Admin'), 3),
		       ('331-2', null, 'Desk', dbo.getDivisionByName('Admin'), 3),
		       ('331-3', null, 'Desk', dbo.getDivisionByName('Admin'), 3),
		       ('331-4', null, 'Desk', dbo.getDivisionByName('Admin'), 3)
GO


-----


DELETE FROM [dbo].[Abonents];
GO

INSERT INTO [dbo].[Abonents]
           ([Number]
           ,[PName]
           ,[IName]
           ,[BName]
           ,[DOB]
           ,[RoomID])
     VALUES
           ('111-11-11', 'Lastname1', 'Name1', 'Fathername1', '01-11-2001', dbo.getRoomByNumber('101')),
           ('111-11-12', 'Lastname2', 'Name2', 'Fathername2', '02-11-2001', dbo.getRoomByNumber('101')),
           ('111-11-13', 'Lastname3', 'Name3', 'Fathername3', '03-11-2001', dbo.getRoomByNumber('001')),
           ('111-11-14', 'Lastname4', 'Name4', 'Fathername4', '04-11-2001', dbo.getRoomByNumber('102')),
           ('111-11-15', 'Lastname5', 'Name5', 'Fathername5', '05-11-2001', dbo.getRoomByNumber('103')),

           ('111-12-10', 'Lastname6', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('201-2')),
           ('111-12-11', 'Lastname7', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('202-2')),
           ('111-13-10', 'Lastname8', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('220')),
           ('111-13-11', 'Lastname9', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('221')),
           ('111-13-12', 'Lastname10', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('221-1')),
           ('111-13-13', 'Lastname10', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('221-2')),
           ('111-13-14', 'Lastname11', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('221-3')),
           ('111-13-15', 'Lastname12', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('221-4')),

           ('111-14-10', 'Lastname100', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('330')),
           ('111-14-11', 'Lastname101', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('331')),
           ('111-14-12', 'Lastname102', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('331-1'))
GO


select * from Divisions;
select * from Rooms;