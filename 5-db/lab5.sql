use lab1;
go


select * from Abonents;
go


create or alter view AbonentsDivisions
as 
	select Abonents.*, Rooms.RoomNumber, Divisions.DivisionID, Divisions.DivisionName from Abonents 
		join Rooms on Rooms.RoomID = Abonents.RoomID
		join Divisions on Divisions.DivisionID = Rooms.DivisionID;
go

create or alter view AvgCallsByDivisions
as
	select DivisionID, AVG(CallsPerMonth) as avg_calls from AbonentsDivisions group by DivisionID;
go

select * from AvgCallsByDivisions;

--print('1')
----- 1
--select Number, CallsPerMonth, DivisionName from AbonentsDivisions
--where 
--	CallsPerMonth >= (select avg_calls from AvgCallsByDivisions where AvgCallsByDivisions.DivisionID = AbonentsDivisions.DivisionID)
	
--print('2')
------ 2
--select Number, CallsPerMonth, DivisionName from AbonentsDivisions as b
--where 
--	b.CallsPerMonth = (
--		select MAX(a.CallsPerMonth) from AbonentsDivisions as a 
--		where a.DivisionID = b.DivisionID
--	);


print('3')
---- 3

select AvgCallsByDivisions.DivisionID, AvgCallsByDivisions.avg_calls from AvgCallsByDivisions 
where avg_calls >= (select AVG(CallsPerMonth) from AbonentsDivisions)

select a.Number, a.CallsPerMonth, a.DivisionName, a.DivisionID from AbonentsDivisions as a 
where a.DivisionID in (
	select AvgCallsByDivisions.DivisionID from AvgCallsByDivisions 
	where avg_calls >= (select AVG(CallsPerMonth) from AbonentsDivisions)
)