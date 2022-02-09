USE [lab1]
GO

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


