\echo 'Delete and recreate scarebnb db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE scarebnb;
CREATE DATABASE scarebnb;
\connect scarebnb

\i scarebnb_schema.sql
\i scarebnb_seed.sql

\echo 'Delete and recreate scarebnb_test db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE scarebnb_test;
CREATE DATABASE scarebnb_test;
\connect scarebnb_test

\i scarebnb_schema.sql
