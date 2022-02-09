use lab1;
go

drop table Abonents;
go
create table Abonents (
	Number varchar(16) primary key,
	PName varchar(32) not null,
	IName varchar(32) not null,
	BName varchar(32) not null,
	DOB varchar(10) not null,
	RoomNumber varchar(10),
	DivisionName varchar(32),
);
go

INSERT INTO [dbo].[Abonents]
     VALUES
           ('111-11-11', 'Lastname1', 'Name1', 'Fathername1', '01-11-2001', '101', 'Security'),
           ('111-11-12', 'Lastname2', 'Name2', 'Fathername2', '01-11-2001', '101', 'Security')
GO

alter table Abonents
	add Active char(1) not null
	constraint AbonentActiveDefault default 'Y';
go

select * from Abonents;

alter table Abonents
	drop column Active;
go

-- error because "The object 'AbonentActiveDefault' is dependent on column 'Active'."

alter table Abonents
	drop constraint AbonentActiveDefault;
go

alter table Abonents
	drop column Active;
go

----------------

alter table Rooms
	with check
	add constraint RoomFloorCheck check (RoomFloor between 1 and 3);
go
 
select * from Rooms where RoomType='Room';

-- Let's add new single room on the roof - 4th floor.
-- We need to temporarly disable constraint RoomFloorCheck

alter table Rooms
	nocheck constraint RoomFloorCheck;
go

insert Rooms values ('404', 'Roof Birdwathing Room', 'Room', 4, 'Admin')

-- turn it back on

alter table Rooms
	with nocheck
	check constraint RoomFloorCheck;
go

select * from Rooms where RoomFloor >= 3;

----------------


select * from Abonents;

-- ^ ok

exec sp_rename 'Abonents', 'Abonenty'
go

select * from Abonenty;

-- ^ ok

exec sp_rename 'Abonenty', 'Abonents'
go
