USE habitTracker;
GO

-- Shows basic habit info and sorts by newest first
SELECT HabitId, Title,IsActive,CreatedAt
FROM dbo.Habits
WHERE UserId=1
ORDER BY CreatedAt DESC;

-- Show the log history (timeline) for one habit
SELECT LogDate, Completed, Notes
FROM dbo.HabitLogs
WHERE HabitId=1
ORDER BY LogDate DESC;

-- Completion percentage per habit (last 7 days)
SELECT 
    h.HabitId,
    h.Title,
    CAST(100.0*SUM(CASE WHEN hl.Completed=1 THEN 1 ELSE 0 END)/NULLIF(COUNT(*),0) AS DECIMAL(5,2)) AS CompletionRate
FROM dbo.Habits h
LEFT JOIN dbo.HabitLogs hl
    ON hl.HabitId=h.HabitId
    AND hl.LogDate>=DATEADD(DAY,-6,CAST(GETDATE() AS DATE))
WHERE h.UserId=1
GROUP BY h.HabitId,h.Title
ORDER BY CompletionRate DESC;

-- Completion rate by day of the week (last 30 days)
SELECT 
    DATENAME(WEEKDAY,hl.LogDate) AS WeekdayName,
    COUNT(*) AS TotalLogs,
    SUM(CASE WHEN hl.Completed=1 THEN 1 ELSE 0 END) AS CompletedLogs,
    CAST(100.0*SUM(CASE WHEN hl.Completed=1 THEN 1 ELSE 0 END)/ NULLIF(COUNT(*), 0) AS DECIMAL(5,2)) AS CompletionRate
FROM dbo.HabitLogs hl
WHERE hl.LogDate>=DATEADD(DAY,-29,CAST(GETDATE() AS DATE))
GROUP BY DATENAME(WEEKDAY,hl.LogDate)
ORDER BY TotalLogs DESC;

-- Top 5 habits by consistency (last 30 days)
SELECT TOP 5
    h.HabitId,
    h.Title,
    COUNT(*) AS DaysTracked,
    SUM(CASE WHEN hl.Completed=1 THEN 1 ELSE 0 END) AS DaysCompleted
FROM dbo.Habits h
JOIN dbo.HabitLogs hl ON hl.HabitId= h.HabitId
WHERE h.UserId=1
  AND hl.LogDate>=DATEADD(DAY,-29,CAST(GETDATE() AS DATE))
GROUP BY h.HabitId,h.Title
ORDER BY DaysCompleted DESC, DaysTracked DESC;
