use lab1;
go

create or alter view AbonentsDivisions
as 
	select Abonents.*, Rooms.RoomNumber, Rooms.DivisionID, Divisions.DivisionName from Abonents 
		join Rooms on Rooms.RoomID = Abonents.RoomID
		full join Divisions on Divisions.DivisionID = Rooms.DivisionID;
go

---- 1
create or alter trigger OnDivisionDelete
on Divisions
after DELETE
as 
	declare @c int;
	select @c = count(a.AbonentID) from AbonentsDivisions as a 
		where a.DivisionID in (select DivisionID from deleted);

	IF @c > 0
	BEGIN 
		RAISERROR(N'Не можна видаляти підрозділ поки в ньому працюють люди!',16,1)
		ROLLBACK
	END;
go

select * from Divisions;

delete from Abonents where AbonentID in (select AbonentID from AbonentsDivisions where DivisionID = 6);
select * from AbonentsDivisions where DivisionID = 6;
delete from Divisions where DivisionID = 6;

select * from Divisions;

--2

drop table DivisionTypes;
go
create table DivisionTypes (
	DivisionType varchar(32) primary key,
	AbonentCount int
);
go

create or alter procedure UpdateDivisionTypes
as
	truncate table DivisionTypes;
	insert into DivisionTypes (DivisionType, AbonentCount) select b.DivisionType, Count(a.AbonentID)
	from AbonentsDivisions as a 
	join Divisions as b on a.DivisionID = b.DivisionID 
	group by b.DivisionType;
go

create or alter trigger OnAbonentInsert
on Abonents
after Insert, Update, Delete
as 
	exec UpdateDivisionTypes;
go

exec UpdateDivisionTypes;

select * from DivisionTypes;

INSERT INTO [dbo].[Abonents] ([Number] ,[PName] ,[IName] ,[BName] ,[DOB] ,[RoomID])
     VALUES
           ('954-23-23', 'Lastname100', 'Name100', 'Fathername100', '01-11-1991', dbo.getRoomByNumber('101'));

		   
select * from DivisionTypes;


delete from Abonents where AbonentID < 5;
select * from DivisionTypes;