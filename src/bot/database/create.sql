DROP TABLE IF EXISTS public.borrows;

select * from books

select * from borrows

insert into books (title, author, published, date_added, date_deleted)
values
	('Mein Kampf', 'The Great Imperor', '1925', '2023-04-15', null),
	('Illiad', 'Homer', 'c. 8th century BC', '2023-04-11', null)


CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,
	title varchar(255) NOT NULL,
	author varchar(255) NOT NULL,
	published varchar(255) NOT NULL,
	date_added date NOT NULL,
	date_deleted date
);
CREATE TABLE IF NOT EXISTS borrows (
    borrow_id SERIAL PRIMARY KEY,
	book_id integer NOT NULL,
	date_start date NOT NULL,
	date_end date,
	user_id integer
);

ALTER TABLE IF EXISTS public.borrows
    OWNER to postgres;