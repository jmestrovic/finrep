-- List of companies with incorrect abbreviation
select c.name, c.abbreviation, s.security_type, s.isin, substr(s.isin, 3, 4), rtrim(substr(s.isin, 3, 4), '0')
  from gfi_securities s
       inner join gfi_companies c on s.company_id = c.id
 where c.abbreviation != rtrim(substr(s.isin, 3, 4), '0');



update gfi_companies
   set abbreviation = (select rtrim(substr(s.isin, 3, 4), '0') from gfi_securities s where s.company_id = gfi_companies.id)
 where abbreviation != (select rtrim(substr(s.isin, 3, 4), '0') from gfi_securities s where s.company_id = gfi_companies.id);
