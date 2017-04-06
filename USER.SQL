drop user "tgthbdbusr"@localhost;
create user "tgthbdbusr"@"localhost" identified by "tgthbdbpass";
grant drop, create, select, insert, update, delete on TGTHB.* to "tgthbdbusr"@localhost;
create database TGTHB;