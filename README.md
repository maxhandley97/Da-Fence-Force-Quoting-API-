# Fence Quoting API

### Identification of the problem and why does it need solving?

The traditional approach to quoting is inefficient. Thousands of dollars and hours are wasted in the process of quoting and general lack of centralised management in the construction industry in particular, in which business owners travel and spend sometimes hours to have a look at a project without the assurance of even getting the job. There are multiple business operations that could also be streamlined and centralised to manage larger companies, for instance automating job allocation to increase employee efficiency, the industry gets a bad wrap for "standing around".

The same inefficiency is apparent for potential customers needing to take time off work to meet multiple businesses to ensure they are getting the best product and price before operations have commenced.

To streamline and centralise this in a relatively small industry to start off with, The Fence Force Quoting API is needed. By having a central platform in which potential customers can post details and pictures of the quote_request of work. Businesses will then be able to look at the quote_request of work and offer a price and and timeframe to customers. Once accepted, businesses owners will have a central platform for allocation and managing the operations until completion.

### Why have you chosen this database system. What are the drawbacks compared to others?

PostgreSQL (Postgres) is the chosen database management system (DBMS) because of it's robust features, security and scalability. It's a free and popular database system in the software developement industry.

Postgres is free and open source by nature, making it accessable to all an extensive range of community-driven development of extensions and applications.

The extensive feature set supports writing database functions using Python, Java, JS and many other major programming languages and supports various data types. Postgres also conceptualised and developed features such as triggers, foreign keys and enabling complex queries.

PostgreSQL comes with security features authentication and authorization to access databases and uses encryption methods like SSL/TLS to encrypt data in transit and Transparent Data Encryption while at rest.

Another major advantage of PostgreSQL is scalability, simplifying maintainenace of larger datasets by supporting partitioning and indexing.

For projects requiring specific requirements or constraints, PostgreSQL has drawbacks like a steeper learning curve and performance and memory drawbacks relative to other DBMS's.

Postgres has been explained as to have too many moving parts, when combined with an extensive feature set, requiring exceptional expertise in certain cases of administration and setup.

The comparative performance of Postgres may not match the speed of other DBMSs in cases in which timeliness is required. Other DBMS’s focus on simplicity and speed in cases such as key-value lookups, where PostgreSQL focuses on complex indexing and data types.

Postgres’ complex indexing, archived write-ahead logging and the use of buffer caching in combination with intensive datasets or high traffic is inefficient in terms of memory consumption comparatively. 

### Identify and discuss the key functionalities and benefits of an ORM

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

### enitites

Jobs(job_id, estimated_start:date, estimated_completion:date, completion_status:string, total_price:sting, assigned_hours, quote_id, employee_id, job_material_id)

Quotes(quote_id, fence_type:string, fence_height_mm, fence_length_m, images_url:string, status:string, date_posted: date)

Barters(barter_id, post_date:date, quote_id, employee_id, business_id)










