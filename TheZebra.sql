-- This query gives an r-squared value, or coefficient of determination,
-- for the numeric values, in order, compared with a binary split male v female.
-- This shows which factors determine rate, and how they differ between genders.

SELECT REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 'Male' as sex
FROM sajanalexander.candidate_test_rates
WHERE lower(sex) like 'm%'
union
SELECT REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 'Female' as sex
FROM sajanalexander.candidate_test_rates
WHERE lower(sex) like 'f%'

-- Based on query #1 showing education_id as the largest correlate of 
-- rate, I sliced for average rate difference between males and females,
-- based on education_id. Hypothesis confirmed, the M:F rate ratio is highest
-- among lower education levels.

select a.education_id,
	a.avg_rate as avg_rate_male,
	b.avg_rate as avg_rate_female, 
	a.avg_rate/b.avg_rate as rate_ratio
from
(
SELECT education_id, avg(rate) as avg_rate FROM sajanalexander.candidate_test_rates
WHERE LOWER(sex) like 'm%'
GROUP BY education_id
) a
inner join 
(
SELECT education_id, avg(rate) as avg_rate FROM sajanalexander.candidate_test_rates
WHERE LOWER(sex) like 'f%'
GROUP BY education_id
) b
on a.education_id=b.education_id
ORDER BY education_id


-- This query is like #1 one above, except split into the 4 provider companies. 
-- You'll notice first that education is a big determinant *except* for company D,
-- whereas company D is 2x as influenced by age and vehicle class as anyone else,
-- and least by incidents and vehicle year. Company D appears to have significantly
-- different rate formulas and/or market. We could probably determine rate formulas
-- from this information.
SELECT 'A' as Company,
 REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 count(*) as Total_Insured
FROM sajanalexander.candidate_test_rates
WHERE carrier_name = 'Company A'
union
SELECT 'B' as Company,
 REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 count(*) as Total_Insured
FROM sajanalexander.candidate_test_rates
WHERE carrier_name = 'Company B'
union
SELECT 'C' as Company,
 REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 count(*) as Total_Insured
FROM sajanalexander.candidate_test_rates
WHERE carrier_name = 'Company C'
union
SELECT 'D' as Company,
 REGR_R2(education_id,rate) as r2education,
 REGR_R2(age,rate) as r2age,
 REGR_R2(credit_id,rate) as r2credit,
 REGR_R2(vehicle_class_id,rate) as r2vehclass,
 REGR_R2(incidents,rate) as r2incidents,
 REGR_R2(vehicle_year,rate) as r2veh_year,
 count(*) as Total_Insured
FROM sajanalexander.candidate_test_rates
WHERE carrier_name = 'Company D'

-- This query takes the columns with the highest r-squared in order, and groups
-- by these columns, taking the max(rate)/min(rate) as diff_rate_ratio, and 
-- ordering by diff_rate_ratio. This gives those sectors which have the largest
-- split of rates across what would otherwise seem to be comparable insurance 
-- buyers. I also selected the average age, which is typically the same (41-43)
-- across these groups.
-- If you run this query, you'll see that the top 100 rows for this metric are
-- all Company D. 

SELECT count(person_guid) AS num_persons,
       max(rate)-min(rate) as diff_rate,
       max(rate)/min(rate) as diff_rate_ratio,
       avg(age) as mean_age,
       credit_id as credit,
       vehicle_class_id as vclass,
       incidents as inc,
       education_id as edu,
       vehicle_year as v_year,
       carrier_name as c_name
FROM sajanalexander.candidate_test_rates tr
GROUP BY education_id,
        credit_id,
        vehicle_class_id,
        incidents,
        vehicle_year,
        carrier_name
HAVING count(person_guid)>1000
ORDER BY diff_rate_ratio desc,
        num_persons desc,
        incidents desc,
        education_id,
        carrier_name
-- Conclusion: Company D uses a simpler metric than A-C, we should develop
-- linear regression equations to exploit it to get our users the best rates.
