USE habitTracker;
GO

-- Inserting user 1 into the Users table
INSERT INTO dbo.Users (FullName, Email)
VALUES ('Lucia','lucia@gmail.com');

-- Insert 3 habits for the user 1
INSERT INTO dbo.Habits(UserId, Title, Description)
VALUES
(1, 'Tomar agua', '8 vasos al día'),
(1, 'Caminar', '30 minutos'),
(1, 'Dormir temprano', 'Antes de las 11pm');

-- Insert daily logs for habits (completed / not completed)
INSERT INTO dbo.HabitLogs(HabitId,LogDate, Completed,Notes)
VALUES
(1, '2026-01-17', 1, 'ok'),
(1, '2026-01-18', 1, 'ok'),
(1, '2026-01-19', 1, 'ok'),
(2, '2026-01-18', 1, NULL),
(3, '2026-01-17', 0, 'me dormí tarde');
GO
