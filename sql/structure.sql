drop table if exists ticker_buffer;
drop table if exists insider_buffer;
drop table if exists insider_log;
drop table if exists insider;
drop table if exists ticker_log;
drop table if exists company;

create sequence if not exists seq_id;
create sequence if not exists buf_id;
create sequence if not exists session_id;


create table company(
  id bigint primary key default nextval('seq_id'),
  code char(20) not null unique
);

create table ticker_log(
  id bigint primary key default nextval('seq_id'),
  company_id bigint not null,
  date date not null,
  c_open decimal(20,10),
  c_close decimal(20,10),
  c_low decimal(20,10),
  c_high decimal(20,10),
  volume bigint,
  unique(company_id, date),
  foreign key(company_id) references company(id)
);

create table insider(
  id bigint primary key default nextval('seq_id'),
  company_id bigint not null,
  name varchar(255) not null,
  relation varchar(50),
  unique(company_id, name),
  foreign key(company_id) references company(id)
);

create table insider_log(
  id bigint primary key default nextval('seq_id'),
  insider_id bigint not null,
  date date not null,
  transaction_type varchar(50),
  owner_type varchar(50),
  shares_traded bigint,
  last_price decimal(20,10),
  shares_held bigint,
  foreign key(insider_id) references insider(id)
);

create index on insider_log (insider_id, date);

create table ticker_buffer(
  id bigint primary key default nextval('buf_id'),
  session_id bigint not null,
  ticker char(20) not null,
  date date not null,
  c_open decimal(20,10),
  c_close decimal(20,10),
  c_low decimal(20,10),
  c_high decimal(20,10),
  volume bigint,
  unique(session_id, ticker, date)
);

create table insider_buffer(
  id bigint primary key default nextval('buf_id'),
  session_id bigint not null,
  ticker char(20) not null,
  name varchar(255) not null,
  relation varchar(50),
  date date not null,
  transaction_type varchar(50),
  owner_type varchar(50),
  shares_traded bigint,
  last_price decimal(20,10),
  shares_held bigint
);

create index on insider_buffer(session_id, ticker, name);