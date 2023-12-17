# Fence Quoting API

## Identification of the problem and why does it need solving?

The traditional approach to quoting is inefficient. Thousands of dollars and hours are wasted in the process of quoting and general lack of centralised management in the construction industry in particular, in which business owners travel and spend sometimes hours to have a look at a project without the assurance of even getting the job. There are multiple business operations that could also be streamlined and centralised to manage larger companies, for instance automating job allocation to increase employee efficiency, the industry gets a bad wrap for "standing around".

The same inefficiency is apparent for potential customers needing to take time off work to meet multiple businesses to ensure they are getting the best product and price before operations have commenced.

To streamline and centralise this in a relatively small industry to start off with, The Fence Force Quoting API is needed. By having a central platform in which potential customers can post details and pictures of the quote_request of work. Businesses will then be able to look at the quote_request of work and offer a price and and timeframe to customers. Once accepted, businesses owners will have a central platform for allocation and managing the operations until completion.

## R3 Why have you chosen this database system. What are the drawbacks compared to others?

PostgreSQL (Postgres) is the chosen database management system (DBMS) because of it's robust features, security and scalability. It's a free and popular database system in the software developement industry.

Postgres is free and open source by nature, making it accessable to all an extensive range of community-driven development of extensions and applications.

The extensive feature set supports writing database functions using Python, Java, JS and many other major programming languages and supports various data types. Postgres also conceptualised and developed features such as triggers, foreign keys and enabling complex queries.

PostgreSQL comes with security features authentication and authorization to access databases and uses encryption methods like SSL/TLS to encrypt data in transit and Transparent Data Encryption while at rest.

Another major advantage of PostgreSQL is scalability, simplifying maintainenace of larger datasets by supporting partitioning and indexing.

For projects requiring specific requirements or constraints, PostgreSQL has drawbacks like a steeper learning curve and performance and memory drawbacks relative to other DBMS's.

Postgres has been explained as to have too many moving parts, when combined with an extensive feature set, requiring exceptional expertise in certain cases of administration and setup.

The comparative performance of Postgres may not match the speed of other DBMSs in cases in which timeliness is required. Other DBMS’s focus on simplicity and speed in cases such as key-value lookups, where PostgreSQL focuses on complex indexing and data types.

Postgres’ complex indexing, archived write-ahead logging and the use of buffer caching in combination with intensive datasets or high traffic is inefficient in terms of memory consumption comparatively. 

## R4 Identify and discuss the key functionalities and benefits of an ORM

Object-relational mapping (ORM) is a part of a library in an object orientated programming (OOP) language which allows developers to interact directly with a database by utilising ORM instances created in the OOP language. This API uses SQLAlchemy as ORM and Python as the OOP. The key functionalities of SQLAlchemy are:

Object mapping - SQLAlchemy uses a declarative mapping structure, a succint method of defining a Python object model and metadata to create standard querie language (SQL) relations in a database. This simplifies interactions with the database and is less time consuming due to using streamlined Python syntax instead of continually entering SQL quieries.

Defining relationships - SQLAlchemy enables relationships to be created between tables by the use of foreign keys to link relations, to have relationships such as one-to-one, one-to-many or many-to-many. If this was to be done manually with SQL, it would be less simplified and efficient due to writing more complex JOIN quieries that wouldn't have a longterm desired result.

CRUD operations - All ORM's including SQLAlchemy allow developers to manipulate enitites without the use of SQL with the use of CREATE, READ, UPDATE and DELETE functions, making for paramount efficiency and readable and maintainable code.

Querying - In ORM's such as SQLAlchemy, one can reusable queries in an OOP language to access data instead of manually queirying with an SQL language. This can be used to create powerful API's, directly accessing data in an efficient manner.

Data Validation and Error Handling - ORMs such as SQLAlchemy provide tools to manage exceptions, validating and sanitising incoming data, ensuring data integrity and reliability in database management.

Using an ORM such as SQLAlchemy creates readable, maintainable and reusable code that abstracts data from relations to interact with databases with unmatched efficiency. It allows developers to use known language syntax powerfully as an interface, to queiry, manipulate and even switch between different databases with extreme ease to abstract. It also adds to data security, preventing the likelihood of SQL injection attacks and integrity in managing databases.

https://www.kdnuggets.com/2022/02/difference-sql-object-relational-mapping-orm.html

https://www.theserverside.com/definition/object-relational-mapping-ORM

https://medium.com/@shubhkarmanrathore/mastering-crud-operations-with-sqlalchemy-a-comprehensive-guide-a05cf70e5dea

## R5 Endpoints for my application
### 

## R6 ERD for my application

![Fencing API ERD](/docs/FencingERD.jpg)

## R7 Detail any third party services that app uses
### Flask

Flask is a Python framework for developing web applications. It simplifies managing URL routes and HTTP CRUD requests and offers extensions to authenticate and encrypt data and routes.
### PostgreSQL
PostgreSQL (postgres) is the Relational Database Management System (RDBMS) that provides a platform for data creation, storage, management and retrieval, structured in relational database. It's open source nature and features like data integrity, indexing and scalability make it the chosen RDBMS for this application.

### SQLAlchemy

SQLAlchemy acts as the Object Relational Mapping (ORM) extension in this application. ORM's allow developers to use an object-orientated programming language to interact with databases. In this case SQLalchemy is the ORM library imported into Python, allowing database manipulation and queries without needing to write raw SQL queries.

### Marshmallow
Marshmallow is a Python library that specialises in converting data formats such as JSON to Python types. It offers serialization, deserialization of the data formats and additional functionalities like data validation, formatting, and nesting, enhancing API data handling.

### Psycopg2
Psycopg2 is a Python library that facilitates a connection between a Python program and a PostgreSQL database. Psycopg2 provides tools and functions to establish connections, execute queries, manage data types and handle errors in a Pythonic way.

### Bcrypt
Bcrypt allows the encryption and safe storage of passwords in the database. Bcrypt adds security to the API, by hashing the passwords after creation.

### JWT Manager
JWT (JSON Web Token) Manager is a python library used to manage JSON web tokens, which handles the creation, parsing, and validation of tokens. JSON web tokens are used to handle the processes involved in authentication of users by generating a JWT token, verifying token integrity and allow the extraction of information from the token to authoirise this appication.


## R8 Describe your projects models in terms of the relationships they have with each other
### Business Model
![Business Model](/docs/businessmodel.png)
The first model I created was the business model which represents businesses signed up and are users of the application. It has a one-to-many relationship with Employee, Quote and Job models. Foreign keys are defined in each of the previously listed models by the insertion of the business id in each relation and within the db.relationship line, the back_populates creates the link between these models and the Business model. The cascade delete all orphans operation ensures that when a Business entity is deleted, it's related Quote, Employee and Job entities are too.

### Employee Model
![Employee Model](/docs/employeemodel.png)
This model represents employees which are also users in this application, which belong to businesses. This is cause for many-to-one relationship between the employee and business model. Employees have a one to many relationship to jobs, which are assignable by business or manager roles to employees. One must be in a business or manager role to create employees. 


### Client Model
![Client Model](/docs/clientmodel.png)
The client model represents clients which are the third user relation of the application. Clients are potential customers that create requests for quotes by posting photos and information about themselves and the job needed to be done. The foreign key link to quote_request defines the one-to-many relationship between the client model and quote request model and also contains a cascading deletion of associated QuoteRequest instances.

### Quote Request Model

![Quote Request Model](/docs/quoterequestmopdel.png)
The quote request model represents a quote request, posted to be commented on by businesses in a bartering fashion. The foreign key of this model is the client_id attribute, defining a many-to-one relationship between the QuoteRequest model and Client model. The QuoteRequest model defines a one to many relationship between itself and the Quotes model, which are created by businesses or managers.

### Quote Model
![Quote Model Model](/docs/Quotemodel.png)
The quote model represents a bartering system of sorts, where business and manager users post their prices and availabilities on quote requests. It has a many-to-one relationship with the business model allowing for business or manager users to post many quotes and a one-to-one relationship with the Job model, meaning when a quote accept route it becomes a job associated with the business associated with the quote.

### Job Model
![Job Model Model](/docs/jobmodel.png)
The Job model represents a current job, accepted by a client and associated with a business. The job model has a many to one relationship with the business and employee models, meaning many jobs can be related and assigned to Business and Employee instances. 


## R9 - Discuss the database relations to be implemented in your application

My application consists of a database called fence_api_db and consists of 6 relations; businesses, employees, clients, quote_requests, quotes and jobs.

The "businesses" table contains the entities of various businesses signed up to the API, consisting of the following attributes; business name, email address, password, abn, roles and is_admin. This table serves as the starting point for accessing and creating employees within the application.

The "employees" table contains entities representing various employees belonging to businesses, with attributes covering personal details of employees, their role (manager or employee used for authentication) as well as the business id and name of the associated business.

The "clients" table contains entities representing clients, or in other words the potential customers that need work to be done. The attributes are their personal information, which is attached to quote requests.

The "quote_requests" table contains information about the scope of work to be done at the associated client's establishment (house, business or property). Many attributes are set to allow nullable values, to cater for vacillating clients. Clients can be associated with multiple quote_requests through the embedded client_id foreign key.

the "quotes" table contains information about the scope of work from a businesses standpoint, including the estimated price, estimated commencement and duration of the job. Businesses or managers can post multiple quotes, on various requests and the business_id associates the quote with the respective business. Multiple quotes can exist and are comments on quote_requests. Once a quote is accepted, a job is automatically created associated with the business that wrote a quote, creating a one-to-one relationship.

The "jobs" table contains extra information the quote and can be assigned to a specific employee, making delegation easier. It also is associated with a business and a quote through the foreign keys, necessary for referencing extra information later. 

## R10 Describe the way tasks are allocated and tracked in your project
### Agile - Kanban

I used elements of the Agile approach to manage and allocate tasks in this project. Trello is the website used to visualise progress and create a Kanban board for tasks, where I used cards for every element of the project and checklists as subtasks and updated after a day of success. 

I didn't make commits as regular as I would have liked to have, my approach to the task was something I have learned from, and I didn't want to commit code unless I had figured the issue out. I tried multiple versions of access control and spent way to much time trying to perfect authorisation instead of creating routes, schemas and errorhandling gracefully first.

This breaking rocks into rubble approach helped me in visualising what I had to complete for the day and broke down the whole mountain into what tasks were involved in the step by step process to finishing. Breaking down larger projects helps to make them appear less daunting, but getting stuck also made progress expectations difficult. Following is a screenshot of my final Kanban board:

![Kanban](/docs/trello_screenshot.png)

### Agile - Standups

Standups helped as a collaborative aspect, it was positive seeing where others were up to in their project as a reference. But this was also a negative in some way because I felt quite behind in this task when seeing how others had completed a lot early on made me feel embarrassed posting if no progress had been made and lying to fit in didn't seem correct either. Although when I did post, it was inspiring to get some moral support from others in the cohort and suggestions.
Following are examples of standup posts made:
![Standup](/docs/Standup1.png)
![Standup](/docs/Standup2.png)
![Standup](/docs/standup3.png)







