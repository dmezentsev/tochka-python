drop table if exists insider_trade;
drop table if exists insider;
drop table if exists ticker_log;
drop table if exists company;

create sequence if not exists seq_id;


create table company(
  id bigint primary key default nextval('seq_id'),
  code char(20) not null unique,
  name varchar(255) not null
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

create table insider_trade(
  id bigint primary key default nextval('seq_id'),
  insider_id bigint not null,
  date date not null,
  transaction_type varchar(50),
  owner_type varchar(50),
  shares_traded bigint,
  last_price decimal(20,10),
  shares_held bigint,
  unique(insider_id, date),
  foreign key(insider_id) references insider(id)
);