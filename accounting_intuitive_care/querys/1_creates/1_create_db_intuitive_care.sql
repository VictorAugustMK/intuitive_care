DROP DATABASE IF EXISTS intuitive_care;

CREATE DATABASE intuitive_care
WITH 
    OWNER postgres
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8'
    TEMPLATE template0;

DROP SCHEMA IF EXISTS public CASCADE;
