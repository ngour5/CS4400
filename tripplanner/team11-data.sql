use team11;

#Users
  insert into user (email, password, name, suspended, is_admin) values ('blah@gmail.com', 'wabbits',  'donald', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('goofy@gmail.com', 'ruh roh', 'goofy', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('mickeymouse@gmail.com', 'glove', 'mickey', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('minniemouse@gmail.com', 'bow', 'minnie', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('popeye@gmail.com', 'spinach', 'popeye', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('olive@gmail.com', 'oil', 'olive', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('wah@gmail.com', 'tennis', 'waluigi', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('someone@example.com', 'password', 'Charles de Gaulle', 0, 0);
  insert into user (email, password, name, suspended, is_admin) values ('admin@example.com', 'password', 'Napoleon Bonaparte', 0, 1);


#Addresses
  insert into address (address_id, street_number, street, city, state, zip, country)
    values (1, 3600, 'Elm Street', 'Smallville', 'Ohio', '50210', 'USA');
  insert into address (address_id, street_number, street, city, state, zip, country)
    values (2, 4441, 'Peachtree Street', 'Atlanta', 'Georgia', '30341', 'USA');
  insert into address (address_id, street_number, street, city, state, zip, country)
    values (3, 7894, 'Main Street', 'Los Angeles', 'California', '43821', 'USA');
  insert into address (address_id, street_number, street, city, state, zip, country)
    values (4, 5341, 'Main Street', 'Los Angeles', 'California', '43821', 'USA');
  insert into address (address_id, street_number, street, city, state, zip, country)
    values (5, 5, 'Avenue Anatole', 'Paris', NULL, '75007', 'France');
  insert into address (address_id, street_number, street, city, state, zip, country)
      values (6, NULL, 'Rue de Rivoli', 'Paris', NULL, '75001', 'France');
  insert into address (address_id, street_number, street, city, state, zip, country)
      values (7, 1, 'Avenue du Colonel Henri Rol-Tanguy', 'Paris', NULL, '75001', 'France');
  insert into address (address_id, street_number, street, city, state, zip, country)
      values (8, 4567, 'Threws Court', 'London', NULL, '12345', 'Kenya');
  insert into address (address_id, street_number, street, city, state, zip, country)
      values (9, 909, 'Johnson Way', 'McLondon', NULL, '28232', 'Canada');

#Credit Cards
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(0123456789012345, 1, '2020-06-01', 854, 1);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(1234567890123450, 2, '2021-12-01', 123, 2);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(1111222233334444, 3, '2019-07-01', 456, 3);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(2222333344445555, 4, '2024-01-01', 987, 4);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(3333444455556666, 5, '2023-06-01', 352, 5);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(4444555566667777, 6, '2022-02-01', 635, 6);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(5555666677778888, 7, '2020-06-01', 854, 7);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(6666777788889999, 8, '2023-07-01', 929, 8);
insert into credit_card (cc_number, address_id, expiry, cvv, user_id)
  values(7777888899990000, 9, '2023-05-01', 334, 9);

#Trips

# Attractions
  insert into attraction values (1, 'Eiffel Tower', 4, 'Tour Eiffel', 'Big ol tower', 25.00);
  insert into attraction values (2, 'Louvre', 5, NULL, 'The Louvre Museum is the worlds
    largest art museum and a historic monument of Paris. It is former royal palace.',
    15.00);
  insert into attraction values (3, 'Catacombs of Paris', 8, NULL, 'The Catacombs of
    Paris The Underground ossuaries which hold the remains of more than six million
    people in a small part of a tunnel network built to consolidate Paris ancient
    stone mines.', 13.00);


#Public Transportation

#Time Slots

#Reserved Attractions

#Reviews

#Activities

#Reservations

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, 'Place dArmes', 'Metz', NULL, '57000,', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Metz Cathedral', (select address_id from address order by address_id desc limit 1), 'Mirabelle TV', 'One of the tallest cathedrals in France, the 12th-century building is also known for its extensive use of stained-glass windows.', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, 'Allee Jean Burger', 'Metz', NULL, '57070,', 'France');
insert into attraction values (NULL, 'Fort de Queuleu', (select address_id from address order by address_id desc limit 1), 'Gare Routiere de METZ', 'No description available on TripAdvisor', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, '61 rue Mazelle', 'Metz', NULL, '57000,', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Saint Maximin', (select address_id from address order by address_id desc limit 1), 'Gare Routiere de METZ', 'No description available on TripAdvisor', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, '1 rue de la Legion dHonneur', 'Paris', NULL, '75007', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Musee dOrsay', (select address_id from address order by address_id desc limit 1), 'Gare Musée dOrsay', 'This beautiful museum, once a railroad station, now houses a staggering collection of Impressionist art, as well as other items created between 1848 and 1914. In 2011, the museum is running a renovation of the top floor (impressionist gallery). Only ground and medium floor are accessible. The top floor will re-open on the 20th of October. Meanwhile, some impressionist masterpieces are not visible.', 12.00);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, '8 Boulevard du Palais', 'Paris', NULL, '75001', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Sainte-Chapelle', (select address_id from address order by address_id desc limit 1), 'Cité - Palais de Justice', 'The Sainte-Chapelle is the finest royal chapel to be built in France and features a truly exceptional collection of stained-glass windows. It was built in the mid 13th century by Louis IX, at the heart of the royal residence, the Palais de la Cité. It was built to house the relics of the Passion of Christ. Adorned with a unique collection of fifteen glass panels and a large rose window forming a veritable wall of light,the Sainte-Chapelle is a gem of French Gothic architecture. Designated world heritage site by UNESCO. Open:> 1st March to 31st October: Monday to Friday: from 9.30 a.m. to 12.45 a.m. and to 2.15 p.m. to 6 p.m. Saturday and Sunday: from 9.30 a.m. to 6 p.m.> 1st November to 29th February: Monday to Friday: from 9 a.m. to 12.45 a.m. and to 2.15 p.m. to 5 p.m. Saturday and Sunday: from 9 a.m. to 5 p.m. Last admission 30 minutes before closing time. The best time to visit is in the morning from Tuesday to Friday. Closed:> 1st January, 1st May and 25th December and in case of negative temperatures.', 10.00);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, '8 Rue Scribe, Place de lOpera', 'Paris', NULL, '75009', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Palais Garnier - Opera National de Paris', (select address_id from address order by address_id desc limit 1), 'Opera', 'This performance hall hosts opera, ballet and chamber music performances.', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, 'Rue Stanislas', 'Nancy', NULL, '54000,', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Place Stanislas', (select address_id from address order by address_id desc limit 1), 'Place Dombasle', 'No description available on TripAdvisor', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, '38 rue du Sergent Blandan', 'Nancy', NULL, '54000,', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Musee de lEcole de Nancy', (select address_id from address order by address_id desc limit 1), 'Nancy Thermal', 'No description available on TripAdvisor', 0);

insert into address (address_id, street_number, street, city, state, zip, country) values (NULL, NULL, 'place Stanislas', 'Nancy', NULL, '55200,', 'France');
insert into attraction (attraction_id, name, address_id, transit_stop, description, price) values (NULL, 'Hotel de Ville', (select address_id from address order by address_id desc limit 1), 'Amerval', 'No description available on TripAdvisor', 0);

#Hours of Operation
insert into hours_of_operation (day_of_week, opening_time, closing_time, attraction_id) values (1, '8:00', '18:00', 1);
insert into hours_of_operation (day_of_week, opening_time, closing_time, attraction_id) values (2, '9:00', '19:00', 2);
insert into hours_of_operation (day_of_week, opening_time, closing_time, attraction_id) values (3, '10:00', '20:00', 3);

# Time Slot
insert into time_slot (attraction_id, quantity, start_time, end_time) values (7, 20, '08:00', '12:00');

# Trip
insert into trip (city, start_date, credit_card_id, user_id) values ('Paris', '2018-07-28', 8, 8);


# Activities for above trip
insert into activity (start_date_time, end_date_time, attraction_id, trip_id) values ('2018-07-28 08:00', '2018-07-28 12:00',
                                                                                         7, (select trip_id from trip order by trip_id desc limit 1));
insert into reservation (activity_id, time_slot_id, res_date) values ((select activity_id from activity order by activity_id desc limit 1),
                                                                      (select time_slot_id from time_slot order by time_slot_id desc limit 1),
                                                                         '2018-07-28');

insert into activity (start_date_time, end_date_time, attraction_id, trip_id) values ('2018-07-28 12:15', '2018-07-28 15:15',
                                                                                         8, (select trip_id from trip order by trip_id desc limit 1));

insert into activity (start_date_time, end_date_time, attraction_id, trip_id) values ('2018-07-28 16:00', '2018-07-28 17:00',
                                                                                         9, (select trip_id from trip order by trip_id desc limit 1))
