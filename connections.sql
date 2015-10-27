create or replace view connections (src,dst,dep_date,flightno1,flightno2, layover, dep_time, arr_time, price, seats1, seats2, dep_date2) as
select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time-a1.arr_time, a1.dep_time, a2.arr_time, (a1.price+a2.price), a1.seats, a2.seats, to_char(a2.dep_date, 'DD-MON-YYYY')
from available_flights a1, available_flights a2
where a1.dst=a2.src and (a2.dep_time - a1.arr_time) > 0 and (a2.dep_time - a1.arr_time) <= 1
