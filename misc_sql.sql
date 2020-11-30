-- 1. Delete table Employee, Department and Company.
DROP TABLE Employee;
DROP TABLE Department;
DROP TABLE Company;

-- 2. Create tables
CREATE TABLE Employee (id INT, emp_name VARCHAR(64), city VARCHAR(64), department VARCHAR(64), salary FLOAT);
CREATE TABLE Department (id INT, dept_name VARCHAR(64));
CREATE TABLE Company (id INT, comp_name VARCHAR(64), revenue FLOAT);

-- 3.Add rows into employee table
INSERT INTO Employee (id, emp_name, city, department, salary) 
VALUES
	(1, 'David', 'London', 'IT', 80000),
	(2, 'Emily', 'London', 'IT', 70000),
	(3, 'Peter', 'Paris', 'IT', 60000),
	(4, 'Ava', 'Paris', 'IT', 50000),
	(5, 'Penny', 'London', 'Management', 110000),
	(6, 'Jim', 'London', 'Management', 90000),
	(7, 'Amy', 'Rome', 'Support', 30000),
	(8, 'Cloe', 'London', 'IT', 110000);

-- 4. Add rows into Department table
INSERT INTO Department (id, dept_name)
VALUES
	(1, 'IT'),
	(2, 'Management'),
	(3, 'IT'),
	(4, 'Support');

-- 5. Add rows into Company table
INSERT INTO Company (id, comp_name, revenue)
VALUES
	(1, 'IBM', 2000000),
	(2, 'GOOGLE', 9000000),
	(3, 'Apple', 10000000);

-- 6. Query all rows from Department table
SELECT * FROM Department;

-- 7. Change the name of department with id =  1 to 'Management'
UPDATE Department
	SET dept_name = 'Management'
	WHERE id = 1;

-- 8. Delete employees with salary greater than 100000
DELETE FROM Employee
	WHERE salary > 100000;

-- 9. Query the names of companies
SELECT comp_name
	FROM Company;

-- 10. Query the name and city of every employee
SELECT emp_name,
	   city
	FROM Employee;

-- 11. Query all companies with revenue greater than 5000000
SELECT * FROM Company WHERE revenue > 5000000;

-- 12. Query all companies with revenue smaller than 5000000
SELECT * FROM Company WHERE revenue < 5000000;

-- 13. Query all companies with revenue smaller than 5000000, but you cannot use the '<' operator
SELECT * FROM Company WHERE revenue BETWEEN 0 AND 5000000;

-- 14. Query all employees with salary greater than 50000 and smaller than 70000
SELECT * FROM Employee WHERE salary BETWEEN 50000 AND 70000;

-- 15. Query all employees with salary greater than 50000 and smaller than 70000, but you cannot use BETWEEN
SELECT * FROM Employee WHERE salary > 50000 AND salary < 70000;

-- 16. Query all employees with salary equal to 80000
SELECT * FROM Employee WHERE salary = 80000;

-- 17. Query all employees with salary not equal to 80000
SELECT * FROM Employee WHERE salary != 80000;

-- 18. Query all names of employees with salary greater than 70000 together with employees who work on the 'IT' department.
SELECT A.emp_name FROM Employee A
	LEFT JOIN Department B ON A.department = B.dept_name
	WHERE A.salary > 70000
	  AND B.dept_name LIKE 'IT';

-- 19. Query all employees that work in city that starts with 'L'
SELECT * FROM Employee WHERE city LIKE 'L%';

-- 20. Query all employees that work in city that starts with 'L' or ends with 's'
SELECT * FROM Employee WHERE city LIKE 'L%' OR city LIKE '%s';


-- 21. Query all employees that  work in city with 'o' somewhere in the middle
SELECT * FROM Employee WHERE city LIKE '%o%';

-- 22. Query all departments (each name only once)
SELECT DISTINCT dept_name FROM Department;

-- 23. Query names of all employees together with id of department they work in, but you cannot use JOIN
SELECT A.emp_name,
	   B.id
	FROM Employee A, Department B
	WHERE A.department = B.dept_name;

-- 24. Query names of all employees together with id of department they work in, using JOIN
SELECT A.emp_name,
	   B.id
	FROM Employee A
	LEFT JOIN Department B ON A.department = B.dept_name;

-- 25. Query name of every company together with every department
SELECT Company.comp_name, Department.dept_name FROM Company, Department;

-- 26. Query name of every company together with departments without the 'Support' department
SELECT Company.comp_name, Department.dept_name FROM Company, Department WHERE Department.dept_name NOT LIKE 'Support';

-- 27. Query employee name together with the department name that they are not working in
SELECT A.emp_name,
	   B.id
	FROM Employee A, Department B
	WHERE A.department != B.dept_name;

-- 28. Query company name together with other companies names
SELECT A.comp_name,
	   B.comp_name
	FROM Company A, Company B 
	WHERE A.id != B.id;

-- 29. Query employee names with salary smaller than 80000 without using NOT and <
SELECT emp_name FROM Employee WHERE salary BETWEEN 0 AND 80000;

-- 30. Query names of every company and change the name of column to 'Company'
SELECT comp_name AS Company FROM Company;

-- 31. Query all employees that work in same department as Peter
WITH CTE_Employee (id, emp_name, city, department, salary) AS (
	SELECT * FROM Employee WHERE emp_name LIKE 'Peter'
)
SELECT A.* 
	FROM Employee A, CTE_Employee B
	WHERE A.department = B.department
