--Write a query in SQL to display the first name, last name, department number, and department name for each employee.
SELECT E1.FIRST_NAME,E1.LAST_NAME,E1.DEPARTMENT_ID,D1.DEPARTMENT_NAME 
FROM EMPLOYEES E1 JOIN DEPARTMENTS D1 ON D1.DEPARTMENT_ID = E1.DEPARTMENT_ID;


--Write a query in SQL to display the first and last name, department, city, and state province for each employee.
SELECT EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, DEPARTMENTS.DEPARTMENT_NAME, LOCATIONS.CITY, LOCATIONS.STATE_PROVINCE
FROM EMPLOYEES JOIN DEPARTMENTS ON DEPARTMENTS.DEPARTMENT_ID = EMPLOYEES.DEPARTMENT_ID
JOIN LOCATIONS ON DEPARTMENTS.LOCATION_ID = LOCATIONS.LOCATION_ID;

--Write a query in SQL to display the first name, last name, salary, and job grade for all employees. 
SELECT EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, EMPLOYEES.SALARY, JOBS.JOB_TITLE 
FROM EMPLOYEES LEFT OUTER JOIN JOBS ON JOBS.JOB_ID = EMPLOYEES.JOB_ID;

--Write a query in SQL to display the first name, last name, department number and department name, for all employees for departments 80 or 40.
SELECT E.FIRST_NAME, E.LAST_NAME, E.SALARY, D.DEPARTMENT_ID
FROM EMPLOYEES E JOIN DEPARTMENTS D ON D.DEPARTMENT_ID = E.DEPARTMENT_ID 
WHERE 
--DEPARTMENTS.DEPARTMENT_ID = 80 OR DEPARTMENTS.DEPARTMENT_ID = 40
d.department_id IN (40,80)

;

SELECT E.FIRST_NAME, E.LAST_NAME, E.SALARY, D.DEPARTMENT_ID
FROM EMPLOYEES E JOIN DEPARTMENTS D ON D.DEPARTMENT_ID = E.DEPARTMENT_ID AND (d.department_id=80 OR D.DEPARTMENT_ID = 40);





--Write a query in SQL to display those employees who contain a letter z to their first name and also display their last name, department, city, and state province.
SELECT EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, DEPARTMENTS.DEPARTMENT_NAME, LOCATIONS.CITY, LOCATIONS.STATE_PROVINCE,INSTR(EMPLOYEES.FIRST_NAME, 'z')
FROM EMPLOYEES JOIN DEPARTMENTS ON DEPARTMENTS.DEPARTMENT_ID = EMPLOYEES.DEPARTMENT_ID JOIN LOCATIONS ON DEPARTMENTS.LOCATION_ID = LOCATIONS.LOCATION_ID
WHERE INSTR(EMPLOYEES.FIRST_NAME, 'z') > 0;

--Write a query in SQL to display all departments including those where does not have any employee.
SELECT DEPARTMENTS.DEPARTMENT_NAME, EMPLOYEES.FIRST_NAME FROM DEPARTMENTS LEFT OUTER JOIN EMPLOYEES ON DEPARTMENTS.DEPARTMENT_ID = EMPLOYEES.DEPARTMENT_ID WHERE EMPLOYEES.FIRST_NAME IS NULL;

--Write a query in SQL to display the first and last name and salary for those employees who earn less than the employee earn whose number is 182.
SELECT EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, EMPLOYEES.SALARY
FROM EMPLOYEES 
WHERE EMPLOYEES.SALARY < 
(SELECT EMPLOYEES.SALARY FROM EMPLOYEES WHERE EMPLOYEES.EMPLOYEE_ID = 182);

--Write a query in SQL to display the first name of all employees including the first name of their manager.
SELECT E1.FIRST_NAME AS EMPLOYEE,E2.FIRST_NAME AS MANAGER FROM EMPLOYEES E1, EMPLOYEES E2 WHERE E1.MANAGER_ID = E2.EMPLOYEE_ID;

--Write a query in SQL to display the department name, city, and state province for each department.
SELECT DEPARTMENTS.DEPARTMENT_NAME, LOCATIONS.CITY, LOCATIONS.STATE_PROVINCE
FROM DEPARTMENTS JOIN LOCATIONS ON DEPARTMENTS.LOCATION_ID = LOCATIONS.LOCATION_ID;

--Write a query in SQL to display the first name, last name, department number and name, for all employees who have or have not any department.
SELECT EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, DEPARTMENTS.DEPARTMENT_ID, DEPARTMENTS.DEPARTMENT_NAME FROM EMPLOYEES LEFT OUTER JOIN DEPARTMENTS ON EMPLOYEES.DEPARTMENT_ID = DEPARTMENTS.DEPARTMENT_ID;

--Write a query in SQL to display the first name of all employees and the first name of their manager including those who does not working under any manager.
SELECT E1.FIRST_NAME, E2.FIRST_NAME FROM EMPLOYEES E1 LEFT OUTER JOIN EMPLOYEES E2 ON E1.MANAGER_ID = E2.EMPLOYEE_ID;

--Write a query in SQL to display the first name, last name, and department number for those employees who works in the same department as the employee who holds the last name as Taylor.
SELECT E1.FIRST_NAME, E1.LAST_NAME, E1.DEPARTMENT_ID 
FROM EMPLOYEES E1 JOIN EMPLOYEES E2 on E1.DEPARTMENT_ID = E2.DEPARTMENT_ID
WHERE E2.LAST_NAME = 'Taylor';

--Write a query in SQL to display the job title, department name, full name (first and last name ) of employee, and starting date for all the jobs 
--which started on or after 1st January, 1993 and ending with on or before 31 August, 1997.
SELECT JOBS.JOB_TITLE, DEPARTMENTS.DEPARTMENT_NAME, EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, JOB_HISTORY.START_DATE, JOB_HISTORY.END_DATE
FROM EMPLOYEES JOIN DEPARTMENTS ON EMPLOYEES.DEPARTMENT_ID = DEPARTMENTS.DEPARTMENT_ID 
JOIN JOBS ON JOBS.JOB_ID = EMPLOYEES.JOB_ID
JOIN JOB_HISTORY ON JOB_HISTORY.EMPLOYEE_ID = EMPLOYEES.EMPLOYEE_ID
WHERE START_DATE >= TO_DATE('01-JUN-93','DD-MM-YY') AND END_DATE <= TO_DATE('31-AUG-97')

HIRE_DATE BETWEEN TO_DATE('01-JUN-93','DD-MM-YY') AND END_DATE <= TO_DATE('31-AUG-97')
;

--Write a query in SQL to display job title, full name (first and last name ) of employee, and the difference between maximum salary for the job and salary of the employee.
SELECT JOBS.JOB_TITLE, EMPLOYEES.FIRST_NAME, EMPLOYEES.LAST_NAME, (JOBS.MAX_SALARY-EMPLOYEES.SALARY) FROM EMPLOYEES JOIN JOBS ON EMPLOYEES.JOB_ID = JOBS.JOB_ID;

--Write a query in SQL to display the name of the department, average salary and number of employees working in that department who got commission.
SELECT DEPARTMENTS.DEPARTMENT_NAME,departments.location_id ,AVG(EMPLOYEES.SALARY), COUNT(COMMISSION_PCT)
FROM DEPARTMENTS
JOIN EMPLOYEES USING(DEPARTMENT_ID)
GROUP BY DEPARTMENTS.DEPARTMENT_NAME, DEPARTMENTS.LOCATION_ID;

-- Write a query in SQL to display the full name (first and last name ) of employees, job title and the salary differences to their own job for those employees who is working in the department ID 80.
SELECT E1.FIRST_NAME, E1.LAST_NAME, JOBS.JOB_TITLE, ABS(E1.SALARY - E2.SALARY)
FROM EMPLOYEES E1 JOIN EMPLOYEES E2 ON E1.JOB_ID = E2.JOB_ID JOIN JOBS ON JOBS.JOB_ID = E1.JOB_ID
WHERE E2.DEPARTMENT_ID = 80;



