drop database if exists TGTHB;
create database TGTHB;
use TGTHB;

drop user if exists "tgthbdbusr"@localhost;
create user "tgthbdbusr"@"localhost" identified by "tgthbdbpass";
grant drop, create, select, insert, update, delete on TGTHB.* to "tgthbdbusr"@localhost;

create table command (
	alias varchar(32) not null primary key,
	cmd varchar(32) not null,
	dsc varchar(4096) not null
);

create table text (
	txtid varchar(8) not null primary key,
	txt varchar(4096) not null
);

create table save (
	var varchar(128) not null primary key,
	val varchar(128) not null
);

create table location (
	locid varchar(8) not null primary key,
	name varchar(64) not null,
	vis boolean not null,
	dsc varchar(4096)
);

create table itemtype (
	typeid varchar(8) not null primary key,
	name varchar(64) not null,
	att int not null,
	def int not null,
	hp int not null,
	val int not null,
	dsc varchar(4096)
);

create table item (
	itemid varchar(8) not null primary key,
	typeid varchar(8) not null,
	locid varchar(8),
	
	foreign key (locid) references location(locid)
);

create table people (
	charid varchar(8) not null primary key,
	locid varchar(8),
	name varchar(64) not null,
	hp int not null,
	att int not null,
	def int not null,
	val int not null,
	dsc varchar(4096),
	
	foreign key (locid) references location(locid)
);

create table dialogue (
	dlgid varchar(8) not null primary key,
	charid varchar(8) not null,
	topic varchar(32),
	txt varchar(4096) not null,
	
	foreign key (charid) references people(charid)
);

create table inventory (
	invid varchar(8) not null primary key,
	charid varchar(8),
	item1 varchar(8),
	item2 varchar(8),
	item3 varchar(8),
	item4 varchar(8),
	item5 varchar(8),
	item6 varchar(8),
	item7 varchar(8),
	item8 varchar(8),
	item9 varchar(8),
	item10 varchar(8),
	
	foreign key (charid) references people(charid),
	foreign key (item1) references item(itemid),
	foreign key (item2) references item(itemid),
	foreign key (item3) references item(itemid),
	foreign key (item4) references item(itemid),
	foreign key (item5) references item(itemid),
	foreign key (item6) references item(itemid),
	foreign key (item7) references item(itemid),
	foreign key (item8) references item(itemid),
	foreign key (item9) references item(itemid),
	foreign key (item10) references item(itemid)
);

create table world (
	fromid varchar(8) not null primary key,
	n varchar(8),
	ne varchar(8),
	e varchar(8),
	se varchar(8),
	s varchar(8),
	sw varchar(8),
	w varchar(8),
	nw varchar(8),
	up varchar(8),
	down varchar(8),
	spec1 varchar(8),
	spec2 varchar(8),
	spec3 varchar(8),
	spec4 varchar(8),
	spec5 varchar(8),
	air1 varchar(8),
	air2 varchar(8),
	air3 varchar(8),
	air4 varchar(8),
	air5 varchar(8),
	sea1 varchar(8),
	sea2 varchar(8),
	sea3 varchar(8),
	sea4 varchar(8),
	sea5 varchar(8),
	
	foreign key (fromid) references location(locid),
	foreign key (n) references location(locid),
	foreign key (ne) references location(locid),
	foreign key (e) references location(locid),
	foreign key (se) references location(locid),
	foreign key (s) references location(locid),
	foreign key (sw) references location(locid),
	foreign key (w) references location(locid),
	foreign key (nw) references location(locid),
	foreign key (up) references location(locid),
	foreign key (down) references location(locid),
	foreign key (spec1) references location(locid),
	foreign key (spec2) references location(locid),
	foreign key (spec3) references location(locid),
	foreign key (spec4) references location(locid),
	foreign key (spec5) references location(locid),
	foreign key (air1) references location(locid),
	foreign key (air2) references location(locid),
	foreign key (air3) references location(locid),
	foreign key (air4) references location(locid),
	foreign key (air5) references location(locid),
	foreign key (sea1) references location(locid),
	foreign key (sea2) references location(locid),
	foreign key (sea3) references location(locid),
	foreign key (sea4) references location(locid),
	foreign key (sea5) references location(locid)
);