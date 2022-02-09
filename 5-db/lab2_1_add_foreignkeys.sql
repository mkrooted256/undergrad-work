use lab1;
go

alter table Rooms
add constraint 
	RoomsDivisionForeign foreign key (DivisionName)
	references Divisions;

alter table Abonents add 
constraint
	AbonentRoomForeign foreign key (RoomID)
	references Rooms
	on delete cascade
	-- TODO: unique pair (Number, Division)
GO
-- ------------------------------------