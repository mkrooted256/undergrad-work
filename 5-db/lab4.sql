use lab1
go

-- Варіант 7
--Основні вимоги до функцій системи:
--1 Вибрати номера абонента по підрозділах;
--2 Вибрати номера абонента по приміщеннях;
--3 Підрахувати кількість абонентів по підрозділах, приміщень.

-- 1 Вибрати номера абонента по підрозділах;
CREATE or alter VIEW dbo.NumbersByDivisions
AS
select top 1000 Abonents.AbonentID, Abonents.Number, DivisionName
from Abonents 
  join Rooms on Rooms.RoomID=Abonents.RoomID
  join Divisions on Rooms.DivisionID=Divisions.DivisionID
order by Divisions.DivisionID;
go

-- груповано по підрозділам
print N'груповано по підрозділам';
select * from NumbersByDivisions;

-- вибрати лише один підрозділ
print N'вибрати лише один підрозділ';
select * from NumbersByDivisions where DivisionName = 'Engineering';
go

-- 2 Вибрати номера абонента по приміщеннях;
CREATE or alter VIEW dbo.NumbersByRoom
AS
select top 1000 Abonents.AbonentID, Abonents.Number, Rooms.RoomName
from Abonents 
  join Rooms on Rooms.RoomID=Abonents.RoomID
order by Rooms.RoomID;
go

-- групувати за кімнатами
print N'групувати за кімнатами';
select * from NumbersByRoom;

-- вибрати лише одну кімнату
print N'вибрати лише одну кімнату';
select * from NumbersByRoom where RoomName = 'Engineering';
go

-- 3.1 Підрахувати кількість абонентів по підрозділах
CREATE or alter VIEW dbo.CountAbonentsByDivision
AS
select count(Abonents.AbonentID) as AbonentCount, DivisionName
from Abonents
  join Rooms on Rooms.RoomID=Abonents.RoomID
  join Divisions on Rooms.DivisionID=Divisions.DivisionID
group by Divisions.DivisionName
go

print N'Підрахувати кількість абонентів по підрозділах';
select * from CountAbonentsByDivision;
go

-- 3.2 Підрахувати кількість абонентів по підрозділах та приміщеннях
CREATE or alter VIEW dbo.CountAbonentsByRoomDivision
AS
select count(Abonents.AbonentID) as AbonentCount, RoomName, DivisionName
from Abonents
  join Rooms on Rooms.RoomID=Abonents.RoomID
  join Divisions on Rooms.DivisionID=Divisions.DivisionID
group by RoomName, Divisions.DivisionName
go

print N'Підрахувати кількість абонентів по підрозділах та приміщеннях';
select * from CountAbonentsByRoomDivision;
