-- Creating the database
CREATE DATABASE habitTracker;
GO

USE habitTracker;
GO

-- USERS TABLE: stores the app users
CREATE TABLE dbo.Users(
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(150) NOT NULL UNIQUE,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

-- HABITS TABLE: stores habits created by a user
CREATE TABLE dbo.Habits(
    HabitId INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    Title NVARCHAR(80) NOT NULL,
    Description NVARCHAR(255) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    -- Each habit must belong to an existing user
    CONSTRAINT FK_Habits_Users FOREIGN KEY(UserId)
        REFERENCES dbo.Users(UserId)
);
GO

-- HABITLOGS TABLE: stores daily records for a habit
CREATE TABLE dbo.HabitLogs(
    HabitLogId INT IDENTITY(1,1) PRIMARY KEY,
    HabitId INT NOT NULL,
    LogDate DATE NOT NULL,
    Completed BIT NOT NULL DEFAULT 1,
    Notes NVARCHAR(255) NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    -- Each log must belong to an existing habit
    CONSTRAINT FK_HabitLogs_Habits FOREIGN KEY(HabitId)
        REFERENCES dbo.Habits(HabitId),

    -- Prevents duplicates 
    CONSTRAINT UQ_HabitLogs_HabitId_LogDate UNIQUE(HabitId, LogDate)
);
GO

CREATE INDEX IX_Habits_UserId ON dbo.Habits(UserId);
CREATE INDEX IX_HabitLogs_HabitId_LogDate ON dbo.HabitLogs(HabitId, LogDate);
GO