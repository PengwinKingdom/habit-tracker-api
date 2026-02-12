USE habitTracker;

create table dbo.WeeklyReports(
 ReportId int identity(1,1) primary key,
 UserId int not null,
 WeekStartDate date not null,
 WeekEndDate date not null,
 Summary nvarchar(max) not null,
 Highlights nvarchar(max) not null,
 NextActions nvarchar(max) not null,
 Tone nvarchar(50) not null,
 CreatedAt datetime2 not null default sysutcdatetime(),
 constraint UQ_WeeklyReports unique (UserId, WeekStartDate, WeekEndDate)
);

create index IX_WeeklyReports_UserId_CreatedAt
ON dbo.WeeklyReports(UserId, CreatedAt desc);