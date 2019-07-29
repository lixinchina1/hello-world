select * from (
select totalqty, totalsum, charindex(month,'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC')/4+1 as month,catname from(
select sum(qtysold) as totalqty, sum(pricepaid) as totalsum, month, ROW_NUMBER() OVER(Partition by month order by totalsum DESC) as monthrange, catname from (
select sales.eventid, sales.qtysold, sales.pricepaid, date.month, category.catname 
from sales 
inner join date on sales.dateid = date.dateid 
inner join event on sales.eventid = event.eventid  
inner join category on category.catid = event.catid 
order by month, catname)
group by month, catname
order by month,totalsum DESC)
where monthrange < 4)
Order By Case When month < extract(month from GetDate()) Then month +12
ELSE month END
