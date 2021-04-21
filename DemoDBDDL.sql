CREATE DATABASE ETLDemo
GO

USE ETLDemo

DROP TABLE IF EXISTS Expenses

CREATE TABLE Expenses
(
	[date] datetime,
	USD money,
	rate DECIMAL(6,5),
	CAD money
)