set foreign_key_checks=0;
drop database if exists team11;
create database team11;

use team11;

drop table if exists user;
create table user (
    user_id int primary key auto_increment,
    email varchar(50) unique not null,
    password varchar(20) not null,
    name varchar(50) not null,
    suspended boolean not null,
    is_admin boolean not null
);

drop table if exists address;
create table address (
    address_id int primary key auto_increment,
    street_number int,
    street varchar(50) not null,
    city varchar(50) not null,
    state varchar(50),
    zip varchar(10) not null,
    country varchar(50) not null
);

drop table if exists credit_card;
create table credit_card (
    credit_card_id int primary key auto_increment,
    cc_number varchar(16) unique not null,
    address_id int not null,
    expiry date not null,
    cvv int not null,
    user_id int not null,

    foreign key (user_id) references user(user_id)
        on update cascade
        on delete cascade,

    foreign key (address_id) references address(address_id)
        on update cascade
        on delete cascade
);

drop table if exists trip;
create table trip (
    trip_id int primary key auto_increment,
    city varchar(50),
    start_date date,
    credit_card_id int not null,
    user_id int not null,

    foreign key (credit_card_id) references credit_card(credit_card_id)
        on update cascade
        on delete cascade,
    foreign key (user_id) references user(user_id)
        on update cascade
        on delete cascade
);

drop table if exists attraction;
create table attraction (
    attraction_id int primary key auto_increment,
    name varchar(75) not null,
    address_id int not null,
    transit_stop varchar(50),
    description text,
    price decimal(6,2),

    foreign key (address_id) references address(address_id)
        on update cascade
        on delete cascade
);

drop table if exists hours_of_operation;
create table hours_of_operation (
    day_of_week enum('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
    opening_time time,
    closing_time time,
    attraction_id int not null,

    foreign key (attraction_id) references attraction(attraction_id)
        on update cascade
        on delete cascade
);

drop table if exists time_slot;
create table time_slot (
    time_slot_id int primary key auto_increment,
    attraction_id int not null,
    quantity int,
    start_time time not null,
    end_time time not null,

    foreign key (attraction_id) references attraction(attraction_id)
        on update cascade
        on delete cascade
);


drop table if exists review;
create table review (
    title varchar(50) not null,
    body text,
    review_created datetime default current_timestamp,
    user_id int not null,
    attraction_id int,

    foreign key (user_id) references user(user_id)
        on update cascade
        on delete cascade,

    foreign key (attraction_id) references attraction(attraction_id)
        on update cascade
        on delete cascade

);


drop table if exists activity;
create table activity (
    activity_id int auto_increment,
    start_date_time datetime,
    end_date_time datetime,
    attraction_id int not null,
    trip_id int not null,

    foreign key (attraction_id) references attraction(attraction_id)
      on update cascade
      on delete cascade,

    foreign key (trip_id) references trip(trip_id)
      on update cascade
      on delete cascade,

    primary key (activity_id, attraction_id)
);

drop table if exists reservation;
create table reservation (
    res_num int primary key auto_increment,
    activity_id int not null,
    time_slot_id int not null,
    res_date date not null,

    foreign key (activity_id) references activity(activity_id)
      on update cascade
      on delete cascade,

    foreign key (time_slot_id) references time_slot(time_slot_id)
      on update cascade
      on delete cascade
);