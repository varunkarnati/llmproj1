few_shots = [
    
    {'Question' : "display details and count the number of all employees who have done their phD",
     'SQLQuery' : "SELECT qualification, COUNT(*) FROM employee WHERE qualification LIKE '%Ph(d)%' GROUP BY qualification;",
     'SQLResult': "Result of the SQL query",
     'Answer' : '12'},
     {'Question' : "how many  employees are there with salary more than 50000",
     'SQLQuery' : "SELECT count(*) FROM employee WHERE employee_salary > 50000",
     'SQLResult': "Result of the SQL query",
     'Answer' : '4'},
     {'Question' : "give details of all students",
     'SQLQuery' : "SELECT student_id, student_name, department, academic_year, number_of_backlogs, cumulative_gpa, contact_number, bus_fee FROM student;",
     'SQLResult': "Result of the SQL query",
     'Answer' : 'student_id       student_name    department      academic_year   number_of_backlogs      cumulative_gpa  contact_number  bus_fee 3201    aa      CSE     4th     0       7.40    10000000001     500 3202    bb      CSE     4th     0       2.10    10000000002     500 3203    cc      ECE     4th     1       7.80    10000000003     500 3204    dd      CIVIL   4th     0       9.00    10000000004     500 3205    ee      EEE     4th     0       6.00    10000000005     500'},
    {'Question': "add a new employee who has a phd qualification, and assign unique empid from all other employees ",
     'SQLQuery':"set @newid2 = (SELECT MAX(emp_id) + 1 FROM employee ); INSERT INTO employee values((@newid2),'new_employee', 0, 0,'CSE', 0, 'Ph(d)',500);",
     'SQLResult': "Result of the SQL query",
     'Answer' : '1 row affected'},
     {'Question' : "add a new employee to the table and assign a unique employee id ",
     'SQLQuery' : "set @newid2 = (SELECT MAX(employee_id) + 1 FROM employee );INSERT INTO employee values((@newid2),'new_employee',0,0,'CSE',0,'Ph(d)' ,1000); ",
     'SQLResult': "Result of the SQL query",
     'Answer' : '1 row affected'},
    {'Question': "create a new table and the employees who have done phd into that new table" ,
     'SQLQuery' : """CREATE TABLE phd_employees (
	emp_id INTEGER NOT NULL, 
	emp_name VARCHAR(255), 
	rem_leaves INTEGER, 
	total_leaves INTEGER, 
	`Dept` VARCHAR(255), 
	emp_salary INTEGER, 
	qualification VARCHAR(255), 
	PRIMARY KEY (emp_id)
);

INSERT INTO phd_employees (emp_id, EMP_name, rem_leaves, total_leaves, `Dept`, EMP_salary, qualification)
SELECT EMP_id, EMP_name, rem_leaves, total_leaves, `Dept`, EMP_salary, qualification
FROM employee
WHERE qualification LIKE '%Ph(d)%';
 """,
     'SQLResult': "Result of the SQL query",
     'Answer' :''} 
     
]