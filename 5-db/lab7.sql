use lab1;
go

create or alter function dbo.CountAbonentsInRoom(@room_num varchar(10))
returns int
as begin
	return (
		select count(Abonents.AbonentID) from dbo.Abonents 
		join Rooms on Rooms.RoomID = Abonents.RoomID 
		where  Rooms.RoomNumber = @room_num
	)
end
go

select Rooms.RoomNumber, dbo.CountAbonentsInRoom(Rooms.RoomNumber) as abonent_count from Rooms;
