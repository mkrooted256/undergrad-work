USE [lab1]
GO

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


