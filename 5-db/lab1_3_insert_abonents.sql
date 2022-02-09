USE [lab1]
GO

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

           ('111-14-10', 'Lastname100', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('230')),
           ('111-14-11', 'Lastname101', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('231')),
           ('111-14-12', 'Lastname102', 'Name', 'Fathername', '05-11-2001', dbo.getRoomByNumber('231-1'))
GO

