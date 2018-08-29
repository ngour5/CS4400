use team11;
-- Given a name or username, is the user in the database:
select 'Given a name or username, is the user in the database' as '';
SELECT user_id, name, email
FROM user
WHERE (name = 'goofy') OR (email = 'goofy@gmail.com');

-- Given a name or username, is the user an admin
select 'Given a name or username, is the user an admin' as '';
SELECT name, email, 'TRUE' as 'is_admin'
FROM user
WHERE (name = 'Napoleon Bonaparte' OR email = 'admin@example.com') AND is_admin = 1;

-- Attractions open right now in Paris
select 'Attractions open right now in Paris' as '';
SELECT attraction.name
FROM (attraction join hours_of_operation using (attraction_id))
join address using (address_id)
WHERE (address.city = 'Paris') AND
(CURRENT_TIME BETWEEN hours_of_operation.opening_time AND hours_of_operation.closing_time);

-- Free attractions in Metz
select 'Free attractions in Metz' as '';
SELECT attraction.name
FROM attraction join address using (address_id)
WHERE address.city = 'Metz' AND attraction.price = 0;

-- Show details of one attraction
select 'Show details of one attraction' as '';
SELECT *
FROM (attraction)
join address using (address_id) limit 1;

-- All reviews for an attraction
select 'All reviews for an attraction' as '';
SELECT attraction.name, review.title, review.body, review.review_created
FROM review join attraction using (attraction_id)
WHERE attraction.attraction_id = 1;

-- All reviews by a particular user
select 'All reviews by a particular user' as '';
SELECT attraction.name, review.title, review.body, review.review_created
FROM (review join attraction using (attraction_id)) join user using (user_id)
WHERE user.user_id = 1;

-- Show details of one review
select 'Show details of one review' as '';
SELECT attraction.name, email, review.title, review.body, review.review_created
FROM (review join attraction using (attraction_id)) join user using (user_id)
WHERE title = 'PARIS IS CANCELLED';

-- Trips for a particular user
select 'Trips for a particular user' as '';
SELECT user.name, trip_id, city, start_date
FROM user join trip using (user_id)
WHERE user.user_id = 8;

-- Number of spots remaining for time slots on a given day
select 'Number of spots remaining for time slots on a given day' as '';
select attraction.name as 'attraction', reservation.res_date, time_slot.start_time, time_slot.end_time, time_slot.quantity - count(res_num) as 'remaining spots'
from reservation
  join activity using (activity_id)
  join time_slot using (time_slot_id)
  join attraction on activity.attraction_id = attraction.attraction_id
group by attraction.name, res_date, time_slot_id;

-- For a trip with more than 2 paid attractions, find total cost
select 'For a trip with more than 2 paid attractions, find total cost' as '';
SELECT trip_id, SUM(attraction.price) as 'total cost'
FROM (activity join attraction using (attraction_id)) join trip using (trip_id)
group by trip_id;

-- For one of the public transportation, which attractions are closest
select 'For one of the public transportation, which attractions are closest' as '';
SELECT attraction.transit_stop, attraction.name
FROM attraction
WHERE attraction.transit_stop = 'Opera';