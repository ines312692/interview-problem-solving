# SQL Database Problem-Solving Guide

## Table of Contents
1. [Basic Query Patterns](#basic-query-patterns)
2. [Aggregation and Grouping](#aggregation-and-grouping)
3. [Joins](#joins)
4. [Subqueries](#subqueries)
5. [Window Functions](#window-functions)
6. [Common Table Expressions (CTEs)](#common-table-expressions-ctes)
7. [Date and Time Operations](#date-and-time-operations)
8. [String Manipulation](#string-manipulation)
9. [Performance Optimization](#performance-optimization)
10. [Common Interview Problems](#common-interview-problems)

---

## Basic Query Patterns

### Filtering with WHERE
```sql
-- Find all employees with salary > 50000
SELECT * FROM employees
WHERE salary > 50000;

-- Multiple conditions
SELECT * FROM employees
WHERE salary > 50000 AND department = 'Engineering';

-- Using IN for multiple values
SELECT * FROM employees
WHERE department IN ('Engineering', 'Sales', 'Marketing');

-- Pattern matching with LIKE
SELECT * FROM employees
WHERE name LIKE 'John%';  -- Starts with John
```

### Sorting with ORDER BY
```sql
-- Sort by salary descending
SELECT * FROM employees
ORDER BY salary DESC;

-- Multiple column sorting
SELECT * FROM employees
ORDER BY department ASC, salary DESC;
```

### Limiting Results
```sql
-- Get top 10 highest paid employees
SELECT * FROM employees
ORDER BY salary DESC
LIMIT 10;

-- Pagination (skip 10, take 10)
SELECT * FROM employees
ORDER BY id
LIMIT 10 OFFSET 10;
```

---

## Aggregation and Grouping

### Basic Aggregations
```sql
-- Count, Sum, Average, Min, Max
SELECT
    COUNT(*) as total_employees,
    SUM(salary) as total_payroll,
    AVG(salary) as average_salary,
    MIN(salary) as lowest_salary,
    MAX(salary) as highest_salary
FROM employees;
```

### GROUP BY
```sql
-- Average salary by department
SELECT
    department,
    AVG(salary) as avg_salary,
    COUNT(*) as employee_count
FROM employees
GROUP BY department;

-- Multiple grouping columns
SELECT
    department,
    job_title,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department, job_title;
```

### HAVING Clause
```sql
-- Departments with more than 10 employees
SELECT
    department,
    COUNT(*) as employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

-- Departments with average salary > 60000
SELECT
    department,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000;
```

---

## Joins

### INNER JOIN
```sql
-- Join employees with departments
SELECT
    e.name,
    e.salary,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

### LEFT JOIN
```sql
-- Get all employees, including those without departments
SELECT
    e.name,
    e.salary,
    d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
```

### RIGHT JOIN
```sql
-- Get all departments, including those without employees
SELECT
    e.name,
    d.department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
```

### FULL OUTER JOIN
```sql
-- Get all employees and departments
SELECT
    e.name,
    d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

### SELF JOIN
```sql
-- Find employees and their managers
SELECT
    e1.name as employee_name,
    e2.name as manager_name
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

### CROSS JOIN
```sql
-- Cartesian product of two tables
SELECT
    p.product_name,
    c.category_name
FROM products p
CROSS JOIN categories c;
```

---

## Subqueries

### Subquery in WHERE Clause
```sql
-- Employees earning more than average
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Employees in departments with > 10 people
SELECT * FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM employees
    GROUP BY department_id
    HAVING COUNT(*) > 10
);
```

### Subquery in SELECT Clause
```sql
-- Show each employee with their department's average salary
SELECT
    name,
    salary,
    (SELECT AVG(salary)
     FROM employees e2
     WHERE e2.department_id = e1.department_id) as dept_avg_salary
FROM employees e1;
```

### Subquery in FROM Clause (Derived Table)
```sql
-- Get departments with above-average salaries
SELECT dept_stats.*
FROM (
    SELECT
        department_id,
        AVG(salary) as avg_salary,
        COUNT(*) as emp_count
    FROM employees
    GROUP BY department_id
) dept_stats
WHERE dept_stats.avg_salary > 60000;
```

### Correlated Subquery
```sql
-- Employees earning more than their department average
SELECT e1.name, e1.salary, e1.department_id
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);
```

---

## Window Functions

### ROW_NUMBER()
```sql
-- Assign unique row numbers within each department
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank_in_dept
FROM employees;
```

### RANK() and DENSE_RANK()
```sql
-- Rank employees by salary (with gaps for ties)
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;
```

### Running Totals
```sql
-- Calculate running total of salaries
SELECT
    name,
    salary,
    SUM(salary) OVER (ORDER BY id) as running_total
FROM employees;
```

### Moving Average
```sql
-- Calculate 3-month moving average of sales
SELECT
    month,
    sales,
    AVG(sales) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3months
FROM monthly_sales;
```

### LAG() and LEAD()
```sql
-- Compare current month sales with previous month
SELECT
    month,
    sales,
    LAG(sales, 1) OVER (ORDER BY month) as prev_month_sales,
    LEAD(sales, 1) OVER (ORDER BY month) as next_month_sales
FROM monthly_sales;
```

### NTILE()
```sql
-- Divide employees into 4 salary quartiles
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile
FROM employees;
```

---

## Common Table Expressions (CTEs)

### Basic CTE
```sql
-- Calculate department statistics first, then filter
WITH dept_stats AS (
    SELECT
        department_id,
        AVG(salary) as avg_salary,
        COUNT(*) as emp_count
    FROM employees
    GROUP BY department_id
)
SELECT * FROM dept_stats
WHERE avg_salary > 60000;
```

### Multiple CTEs
```sql
-- Multiple CTEs in one query
WITH
high_earners AS (
    SELECT * FROM employees WHERE salary > 80000
),
dept_counts AS (
    SELECT department_id, COUNT(*) as count
    FROM employees
    GROUP BY department_id
)
SELECT
    h.name,
    h.salary,
    d.count as dept_size
FROM high_earners h
JOIN dept_counts d ON h.department_id = d.department_id;
```

### Recursive CTE
```sql
-- Find all employees in a management hierarchy
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees reporting to previous level
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;
```

---

## Date and Time Operations

### Current Date/Time
```sql
-- Current date and time functions
SELECT
    CURRENT_DATE as today,
    CURRENT_TIME as now_time,
    CURRENT_TIMESTAMP as now_datetime;
```

### Date Arithmetic
```sql
-- Add/subtract days
SELECT
    order_date,
    order_date + INTERVAL '7 days' as delivery_date,
    order_date - INTERVAL '1 month' as month_ago
FROM orders;
```

### Date Extraction
```sql
-- Extract parts of a date
SELECT
    order_date,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    EXTRACT(DAY FROM order_date) as day,
    EXTRACT(DOW FROM order_date) as day_of_week
FROM orders;
```

### Date Formatting
```sql
-- Format dates
SELECT
    order_date,
    TO_CHAR(order_date, 'YYYY-MM-DD') as formatted_date,
    TO_CHAR(order_date, 'Month DD, YYYY') as readable_date
FROM orders;
```

### Date Filtering
```sql
-- Orders from last 30 days
SELECT * FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Orders from specific year
SELECT * FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2024;

-- Orders from date range
SELECT * FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
```

---

## String Manipulation

### Concatenation
```sql
-- Concatenate strings
SELECT
    first_name || ' ' || last_name as full_name,
    CONCAT(first_name, ' ', last_name) as full_name_alt
FROM employees;
```

### Case Conversion
```sql
-- Convert case
SELECT
    UPPER(name) as uppercase_name,
    LOWER(name) as lowercase_name,
    INITCAP(name) as capitalized_name
FROM employees;
```

### Substring
```sql
-- Extract substring
SELECT
    name,
    SUBSTRING(name FROM 1 FOR 3) as first_three_chars,
    LEFT(name, 3) as first_three_alt,
    RIGHT(name, 3) as last_three
FROM employees;
```

### String Length
```sql
-- Get string length
SELECT
    name,
    LENGTH(name) as name_length,
    CHAR_LENGTH(name) as char_count
FROM employees;
```

### Trimming
```sql
-- Remove whitespace
SELECT
    TRIM(name) as trimmed,
    LTRIM(name) as left_trimmed,
    RTRIM(name) as right_trimmed
FROM employees;
```

### Pattern Matching
```sql
-- LIKE patterns
SELECT * FROM employees
WHERE name LIKE 'J%'        -- Starts with J
   OR name LIKE '%son'      -- Ends with son
   OR name LIKE '%ann%';    -- Contains ann

-- Regular expressions (PostgreSQL)
SELECT * FROM employees
WHERE name ~ '^[A-M]';      -- Starts with A-M
```

---

## Performance Optimization

### Indexing Strategies
```sql
-- Create indexes on frequently queried columns
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_salary ON employees(salary);
CREATE INDEX idx_employees_name ON employees(name);

-- Composite index for queries filtering multiple columns
CREATE INDEX idx_employees_dept_salary ON employees(department_id, salary);

-- Unique index
CREATE UNIQUE INDEX idx_employees_email ON employees(email);
```

### Query Optimization Tips

1. **Use EXPLAIN to analyze queries**
```sql
EXPLAIN ANALYZE
SELECT * FROM employees
WHERE department_id = 5;
```

2. **Avoid SELECT ***
```sql
-- Bad
SELECT * FROM employees;

-- Good
SELECT id, name, salary FROM employees;
```

3. **Use WHERE instead of HAVING when possible**
```sql
-- Less efficient
SELECT department_id, COUNT(*)
FROM employees
GROUP BY department_id
HAVING department_id = 5;

-- More efficient
SELECT department_id, COUNT(*)
FROM employees
WHERE department_id = 5
GROUP BY department_id;
```

4. **Use EXISTS instead of IN for large subqueries**
```sql
-- Less efficient for large datasets
SELECT * FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE budget > 1000000);

-- More efficient
SELECT * FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d
    WHERE d.id = e.department_id AND d.budget > 1000000
);
```

5. **Limit result sets early**
```sql
-- Use WHERE clauses to filter before joining
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary > 50000;  -- Filter before joining when possible
```

---

## Common Interview Problems

### 1. Second Highest Salary
```sql
-- Find the second highest salary
SELECT MAX(salary) as second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Alternative using LIMIT/OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Using window functions
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;
```

### 2. Duplicate Emails
```sql
-- Find all duplicate emails
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

### 3. Delete Duplicate Rows
```sql
-- Delete duplicates keeping only the row with minimum id
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id)
    FROM users
    GROUP BY email
);

-- Using window functions (PostgreSQL)
DELETE FROM users
WHERE id IN (
    SELECT id
    FROM (
        SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) as rn
        FROM users
    ) t
    WHERE rn > 1
);
```

### 4. Nth Highest Value
```sql
-- Function to get Nth highest salary
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS TABLE (Salary INT) AS $$
BEGIN
  RETURN QUERY (
    SELECT DISTINCT salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 1 OFFSET N-1
  );
END;
$$ LANGUAGE plpgsql;
```

### 5. Consecutive Numbers
```sql
-- Find numbers that appear at least 3 times consecutively
SELECT DISTINCT l1.num as ConsecutiveNums
FROM logs l1
JOIN logs l2 ON l1.id = l2.id - 1
JOIN logs l3 ON l1.id = l3.id - 2
WHERE l1.num = l2.num AND l2.num = l3.num;
```

### 6. Department Top 3 Salaries
```sql
-- Find top 3 earners in each department
WITH ranked_employees AS (
    SELECT
        e.name,
        e.salary,
        d.name as department,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) as rank
    FROM employees e
    JOIN departments d ON e.department_id = d.id
)
SELECT department, name, salary
FROM ranked_employees
WHERE rank <= 3;
```

### 7. Cumulative Salary
```sql
-- Calculate cumulative salary for each employee by month
SELECT
    employee_id,
    month,
    SUM(salary) OVER (
        PARTITION BY employee_id
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as cumulative_salary
FROM salaries
ORDER BY employee_id, month;
```

### 8. Market Analysis
```sql
-- Find customers who bought products from all categories
SELECT customer_id
FROM orders o
JOIN products p ON o.product_id = p.id
GROUP BY customer_id
HAVING COUNT(DISTINCT p.category_id) = (SELECT COUNT(*) FROM categories);
```

### 9. Median Calculation
```sql
-- Calculate median salary
WITH ordered_salaries AS (
    SELECT
        salary,
        ROW_NUMBER() OVER (ORDER BY salary) as row_num,
        COUNT(*) OVER () as total_count
    FROM employees
)
SELECT AVG(salary) as median_salary
FROM ordered_salaries
WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);
```

### 10. Year-over-Year Growth
```sql
-- Calculate year-over-year revenue growth
WITH yearly_revenue AS (
    SELECT
        EXTRACT(YEAR FROM order_date) as year,
        SUM(amount) as revenue
    FROM orders
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT
    year,
    revenue,
    LAG(revenue) OVER (ORDER BY year) as prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year)) * 100.0 /
        LAG(revenue) OVER (ORDER BY year),
        2
    ) as growth_percentage
FROM yearly_revenue;
```

---

## Advanced Patterns

### Pivoting Data
```sql
-- Transform rows to columns
SELECT
    product_id,
    SUM(CASE WHEN month = 'Jan' THEN sales ELSE 0 END) as jan_sales,
    SUM(CASE WHEN month = 'Feb' THEN sales ELSE 0 END) as feb_sales,
    SUM(CASE WHEN month = 'Mar' THEN sales ELSE 0 END) as mar_sales
FROM monthly_sales
GROUP BY product_id;
```

### Unpivoting Data
```sql
-- Transform columns to rows
SELECT product_id, 'Jan' as month, jan_sales as sales FROM sales
UNION ALL
SELECT product_id, 'Feb' as month, feb_sales FROM sales
UNION ALL
SELECT product_id, 'Mar' as month, mar_sales FROM sales;
```

### Gap and Island Problems
```sql
-- Find continuous ranges of dates
WITH date_groups AS (
    SELECT
        date,
        date - ROW_NUMBER() OVER (ORDER BY date) * INTERVAL '1 day' as group_id
    FROM attendance
)
SELECT
    MIN(date) as start_date,
    MAX(date) as end_date,
    COUNT(*) as consecutive_days
FROM date_groups
GROUP BY group_id;
```

---

## Best Practices

1. **Use meaningful aliases**: Makes queries more readable
2. **Indent and format**: Proper formatting improves maintainability
3. **Comment complex logic**: Explain non-obvious business rules
4. **Use CTEs for readability**: Break complex queries into logical steps
5. **Test with small datasets first**: Verify logic before running on large tables
6. **Consider NULL handling**: Use COALESCE, NULLIF, or IS NULL appropriately
7. **Use transactions**: For data modifications affecting multiple tables
8. **Avoid N+1 queries**: Use JOINs instead of multiple separate queries
9. **Use appropriate data types**: Ensures data integrity and optimal storage
10. **Regular maintenance**: Update statistics, rebuild indexes, vacuum tables

---

## Resources for Practice

- LeetCode SQL Problems
- HackerRank SQL Challenges
- SQLZoo Interactive Tutorials
- Mode Analytics SQL Tutorial
- PostgreSQL Documentation
- MySQL Documentation

---

## Common Mistakes to Avoid

1. **Forgetting GROUP BY columns**: All non-aggregated columns must be in GROUP BY
2. **Misusing WHERE vs HAVING**: WHERE filters rows before grouping, HAVING filters after
3. **NULL comparisons**: Use IS NULL, not = NULL
4. **Cartesian products**: Always specify JOIN conditions
5. **Correlated subquery performance**: Can be slow on large datasets
6. **Not handling edge cases**: Empty sets, NULLs, duplicates
7. **Timezone issues**: Be explicit about timezone handling
8. **String case sensitivity**: Depends on database collation settings

---

This guide covers the essential SQL patterns and techniques needed for problem-solving and technical interviews. Practice regularly and always test your queries with different datasets to ensure correctness.