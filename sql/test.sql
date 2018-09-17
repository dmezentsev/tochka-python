/*
insert into company (code, name)
  values
    ('AAPL', 'Apple'),
    ('GOOG', 'Google');

insert into ticker_log
    (company_id, date, c_open, c_close)
  values
    (1, '2018-08-01', 200, 250),
    (1, '2018-08-02', 250, 270),
    (1, '2018-08-03', 270, 220),
    (1, '2018-08-04', 220, 250),
    (1, '2018-08-05', 250, 300),
    (1, '2018-08-06', 200, 250),
    (1, '2018-08-07', 200, 250),
    (1, '2018-08-08', 200, 250),
    (1, '2018-08-09', 200, 250),
    (1, '2018-08-10', 200, 250),
    (1, '2018-08-11', 200, 250),
    (1, '2018-08-12', 200, 250),
    (1, '2018-08-13', 200, 250);*/

select tl_f.company_id, tl_f.date as date_from, tl_l.date as date_to,
  tl_l.c_open - tl_f.c_open
    from
      ticker_log tl_f
        join
      ticker_log tl_l on
          tl_l.company_id = tl_f.company_id and
          tl_l.date > tl_f.date
    where abs(tl_l.c_open - tl_f.c_open) > 50
    order by tl_f.date, tl_l.date
    limit 1;