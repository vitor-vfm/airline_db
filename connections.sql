drop view if exists connections;

create view connections (src,dst,dep_date,flightno1,flightno2, layover,price, dep_time, arr_time) as
select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time-a1.arr_time, a1.dep_time, a2.arr_time min(a1.price+a2.price)
from available_flights a1, available_flights a2
where a1.dst=a2.src and a1.arr_time < a2.dep_time
group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time;
