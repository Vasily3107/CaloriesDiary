CREATE TABLE users (
--  column:               type:             constraints:
    email                 VARCHAR(320)      PRIMARY KEY,
    [password]            VARCHAR(20)       NOT NULL,
    calories_score        INT               DEFAULT(0),
    goals_achieved        INT               DEFAULT(0),
    sex                   CHAR(1)           CHECK(sex in ('M', 'F')),
    age                   INT               CHECK(age > 0),
    [weight]              INT               CHECK([weight] > 0),
    height                INT               CHECK(height > 0),
    goal                  VARCHAR(30)       CHECK(goal in ('Lose weight', 'Stay fit', 'Gain weight'))
);

CREATE TABLE meals (
--  column:               type:             constraints:
    email                 VARCHAR(320)      FOREIGN KEY REFERENCES users(email),
    [name]                VARCHAR(100)      NOT NULL,
    calories              INT               CHECK(calories > 0),
    [when]                DATETIME          DEFAULT(GETDATE())
);

CREATE TRIGGER sub_calories ON meals AFTER INSERT AS
BEGIN
	DECLARE @user_email VARCHAR(320) = (SELECT email FROM inserted);
	DECLARE @quantity_of_calories INT = (SELECT calories FROM inserted);

	UPDATE users
	SET calories_score -= @quantity_of_calories
	WHERE email = @user_email;
END;

CREATE TABLE activities (
--  column:               type:             constraints:
    email                 VARCHAR(320)      FOREIGN KEY REFERENCES users(email),
    [name]                VARCHAR(100)      NOT NULL,
    calories              INT               CHECK(calories > 0),
    [when]                DATETIME          DEFAULT(GETDATE())
);

CREATE TRIGGER add_calories ON activities AFTER INSERT AS
BEGIN
	DECLARE @user_email VARCHAR(320) = (SELECT email FROM inserted);
	DECLARE @quantity_of_calories INT = (SELECT calories FROM inserted);

	UPDATE users
	SET calories_score += @quantity_of_calories
	WHERE email = @user_email;
END;
