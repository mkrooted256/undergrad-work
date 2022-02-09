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
	DivisionID int CONSTRAINT RoomsDivisionForeign FOREIGN KEY references Divisions
);
GO

create table Abonents (
	AbonentID int IDENTITY primary key,
	Number varchar(16) not null,
	PName varchar(32) not null,
	IName varchar(32) not null,
	BName varchar(32) not null,
	DOB varchar(10) not null,
	RoomID int CONSTRAINT AbonentsRoomForeign FOREIGN KEY references Rooms
);
GO

-- This function is needed to insert new Rooms easily 
CREATE FUNCTION dbo.getDivisionByName(@div_name varchar(32))
RETURNS int
WITH SCHEMABINDING
AS BEGIN
	RETURN (select DivisionID from dbo.Divisions where dbo.Divisions.DivisionName=@div_name);
END
GO

-- This function is needed to insert new Abonents easily 
-- Note: returns only FIRST FOUND room 
CREATE FUNCTION dbo.getRoomByNumber(@room_num varchar(10))
RETURNS int
WITH SCHEMABINDING
AS BEGIN
	RETURN (select top (1) RoomID from dbo.Rooms where Rooms.RoomNumber=@room_num);
END
GO

-- Returns how many abonents with number @number are in the room's division 
CREATE FUNCTION dbo.sameNumbersInDivisionByRoom(@number varchar(16), @room_id int)
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
