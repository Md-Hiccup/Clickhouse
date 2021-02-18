# Clickhouse
ClickHouse is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).

Column-oriented databases store records in blocks grouped by columns instead of rows, spend less time reading data while completing queries.

OLAP is an acronym for Online Analytical Processing. OLAP performs multidimensional analysis of business data and provides the capability for complex calculations, trend analysis, and sophisticated data modeling.

Reference:
1. [Clickhouse](https://clickhouse.tech/docs/en/)
2. [Installation](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-clickhouse-on-ubuntu-18-04)


## Installation

```
$   sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
$   echo "deb http://repo.yandex.ru/clickhouse/deb/stable/ main/" | sudo tee /etc/apt/sources.list.d/clickhouse.list
$   sudo apt-get update
$   sudo apt-get install -y clickhouse-server clickhouse-client
```

## Server commands
```
$   sudo service clickhouse-server start    # To start server
$   sudo service clickhouse-server status   # To check status
$   sudo service clickhouse-server stop     # To stop server
```

## Introduction of Clickhouse

1. ###  To Run client session
    ```
    $   clickhouse-client
    ```

2. ###  Create Database
    ```
    Syntax:
        CREATE DATABASE database_name;
    ```
    Ex:
    ```
    -   CREATE DATABASE myDB;
    ```

3. ###  Use Database
    ```
    -   USE myDB;
    ```

4. ###  Create Table
    ```
    Syntax:
        CREATE TABLE table_name
        (
            column_name1 column_type [options],
            column_name2 column_type [options],
            ...
        ) ENGINE = engine;
    ```
    Ex:
    ```
    -   CREATE TABLE student
        (
            id UInt64,
            name String,
            marks Float64,
            created DateTime
        ) ENGINE = MergeTree()
        ORDER BY id ;
    ```
5. ###  Data Types
    1.  UInt64  : storing integer values in the range 0 to 18446744073709551615.
    2.  Float64 : storing floating point numbers such as 12349.23, 132.3 etc.
    3.  String  : storing variable length characters (Doesn't require max length).
    4.  Date    : storing dates in format "YYYY-MM-DD".
    5.  DateTime: storing datetime in format "YYYY-MM-DD HH:MM:SS".

6. ###  INSERT, UPDATE, DELETE Data and Columns

    1.  INSERT Syntax
        >   INSERT INTO table_name VALUES (column_1_value, column_2_value, ....);

        Ex:
        ```
        -   INSERT INTO student VALUES (1, "Adam", 10.5, '2019-01-01 00:01:01');
        -   INSERT INTO student VALUES (2, "Bruce", 40.2, '2019-01-03 10:01:01');
        -   INSERT INTO student VALUES (3, "Charlie", 13, '2019-01-03 12:01:01');
        -   INSERT INTO student VALUES (4, "Dome", 20.8, '2019-01-04 02:01:01');
        ```

    2.  UPDATE Syntax
        >   ALTER TABLE table_name UPDATE  column_1 = value_1, column_2 = value_2 ...  WHERE  filter_conditions;

        Ex:
        ```
        -   ALTER TABLE student UPDATE marks=25.5  WHERE name='Adam';
        ```

    3.  DELETE Syntax
        >   ALTER TABLE table_name DELETE WHERE filter_conditions;

        Ex:
        ```
        -   ALTER TABLE student DELETE WHERE name='Bruce';
        ```

    4.  Add Columns
        >   ALTER TABLE table_name ADD COLUMN column_name column_type;

        Ex:
        ```
        -   ALTER TABLE student ADD COLUMN labs String;
        ```

    5.  Drop Column
        >   ALTER TABLE table_name DROP COLUMN column_name;

        Ex:
        ```
        -   ALTER TABLE student DROP COLUMN labs;
        ```

    6.  RENAME Table
        >   RENAME TABLE table_name to new_table_name;

        Ex:
        ```
        -   RENAME TABLE student to students;
        ```

7. ###  SELECT Querying Data

    1.  SELECT Syntax
        ```
        >   SELECT func_1(column_1), func_2(column_2) FROM table_name WHERE filter_conditions row_options;
        ```
        Ex:
        ```
        -   SELECT name, marks FROM students WHERE marks > 20 LIMIT 2;
        ```

    2.  Aggregate functions
        1. count: returns the count of rows matching the conditions specified.
        2. sum: returns the sum of selected column values.
        3. avg: returns the average of selected column values.
        4. uniq: returns an approximate number of distinct rows matched.
        5. uniqExact: returns exact distinct rows matched.(Takes memory to traverse)
        6. topK: returns an array of the most frequent values of a specific column using an approximation algorithm.

        Ex:
        ```
        -   SELECT SUM(marks) FROM students;
        -   SELECT topK(2)(name) FROM students;
        ```


##  To Check PROCESSLIST
    -   show processlist
        or
    -   SELECT query_id, elapsed time, is_cancelled as canc, read_rows, memory_usage mem, peak_memory_usage peak_mem, query FROM system.processes


##  IMPORTING CSV file to clickhouse
    Syntax:
    >   cat /path/to/file/filename.csv | clickhouse-client --query='Insert into db_name.table_name FORMAT CSV';

    Ex:
    -   cat /path/to/file/student.csv | clickhouse-client --query='Insert into myDB.students FORMAT CSV';


## EXPORTING Clickhouse data to CSV file
    Syntax:
    >   clickhouse-client --query "SELECT * from db_name.table_name" --format FormatName > result.txt

    Ex:
    -   clickhouse-client --query "select * from myDB.students" --format CSV > /path/to/file/student.csv


## REMOVING DUPLICATE ROWS [NOTE: Use Engine as engine=ReplacingMergeTree]

    Syntax:
    >   OPTIMIZE TABLE table_name FINAL;

    Ex:
    -   create table xx (A String, X UInt64) engine=ReplacingMergeTree order by A;
    -   insert into xx values ('a', 1);
    -   insert into xx values ('a', 1);
    -   select  * from xx;
        ┌─A─┬─X─┐
        │ a │ 1 │
        │ a │ 1 │
        └───┴───┘

    -   optimize table xx final;
    -   select * from xx
        ┌─A─┬─X─┐
        │ a │ 1 │
        └───┴───┘

## INSERTING data from Other tables
    Syntax:
    >   INSERT into db_name.table_name select col1, col2, ... from db_name.tbl_name limit 100

    Ex:
    -   insert into myDB.stud select * from myDB.students limit 100;

##  DROP Table and Databases
    Syntax:
    >   DROP TABLE table_name;
    >   DROP DATABASE database_name;

    Ex:
    -   DROP TABLE students;
    -   DROP DATABASE myDB;
