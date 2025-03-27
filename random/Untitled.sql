use ap
;

select count(*)
from invoices
;

select vendor_id, count(vendor_id)
from invoices
group by vendor_id
having count(vendor_id) > 1
;


select distinct vendor_id, invoice_id
from invoices
;

# Same
select *
from vendors
where vendor_state <> "CA"
;

select *
from vendors
where not vendor_state = "CA"
;

# Same
select *
from vendors
where vendor_state = "DC" or vendor_state = "WI" or vendor_state = "IA"
;

select *
from vendors
where vendor_state in ("DC", "WI", "IA")
;

select distinct vendor_state
from vendors
;

select *
from vendors
where vendor_state in (select distinct vendor_state from vendors)
;

select *
from vendors
where vendor_name like '%U%'  -- Where U is inside the string
;

select *
from vendors
where vendor_name like 'U__ca_'  -- _ for single char % for any length 
;


select *
from vendors
where vendor_address2 is not null
;

select *
from vendors
order by vendor_state, vendor_name
;


-- Subquery and joins
-- Will 
select v.vendor_id, v.vendor_name, v.vendor_address1
from vendors v
left join invoices i on v.vendor_id = i.vendor_id
where i.invoice_id is null
;

-- Same
select v.vendor_id, v.vendor_name, v.vendor_address1
from vendors v
where v.vendor_id not in (select vendor_id from invoices)
;

-- Same
select v.vendor_id, v.vendor_name, v.vendor_address1
from vendors v
where v.vendor_id != all(select vendor_id from invoices)
;


-- Feb 12
select vendor_name
from vendors
where vendor_id not in (select vendor_id from invocies)
order by vendor_id
;


-- returning the vendor id's and names of the vendors that have not made an invoice
select vendor_id, vendor_name
from vendors v
where not exists (select * from invoices i where i.vendor_id = v.vendor_id)
order by v.vendor_id
;


-- returning all the vendors that have not made an invoice 
-- in this case the subquery would be more effiecient than the join below
select
    vendor_id,
    vendor_name
    (
        select max(payment_total) from invoices i where i.vendor_id = v.vendor_id
    ) as max_payment
from vendor v
where
    not exists (
        select i.vendor_id, v.vendor_id from invoices i where i.vendor_id = v.vendor_id
    )
;


-- Same with join instead of subquerys
select v.vendor_id, v.vendor_name, max(payment_total)
from vendors v
join invoices i on v.vendor_id = i.vendor_id
group by v.vendor_id
;

