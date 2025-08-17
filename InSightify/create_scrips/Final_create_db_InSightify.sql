-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.1.6
-- PostgreSQL version: 17.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: "NewInSightify" | type: DATABASE --
-- DROP DATABASE IF EXISTS "NewInSightify";
CREATE DATABASE "NewInSightify"
	ENCODING = 'UTF8'
	LC_COLLATE = 'C'
	LC_CTYPE = 'C'
	TABLESPACE = pg_default
	OWNER = postgres;
-- ddl-end --


-- object: in_use | type: SCHEMA --
-- DROP SCHEMA IF EXISTS in_use CASCADE;
CREATE SCHEMA in_use;
-- ddl-end --
ALTER SCHEMA in_use OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,in_use;
-- ddl-end --

-- object: in_use.roles | type: TABLE --
-- DROP TABLE IF EXISTS in_use.roles CASCADE;
CREATE TABLE in_use.roles (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	roles character NOT NULL,
	description character varying NOT NULL,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT roles_pk PRIMARY KEY (id),
	CONSTRAINT unique_roles UNIQUE (roles)
);
-- ddl-end --
ALTER TABLE in_use.roles OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.roles_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.roles_id_seq CASCADE;
-- CREATE SEQUENCE in_use.roles_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.roles_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.users | type: TABLE --
-- DROP TABLE IF EXISTS in_use.users CASCADE;
CREATE TABLE in_use.users (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	this_obj2security_ques smallint NOT NULL,
	name character varying NOT NULL,
	email character varying NOT NULL,
	mob_number character varying NOT NULL,
	password character varying NOT NULL,
	security_ques_answer character varying NOT NULL,
	profile_picture character varying NOT NULL,
	bio character varying,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT unique_email UNIQUE (email),
	CONSTRAINT unique_profile_picture UNIQUE (profile_picture)
);
-- ddl-end --
ALTER TABLE in_use.users OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.users_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.users_id_seq CASCADE;
-- CREATE SEQUENCE in_use.users_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.users_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.votes | type: TABLE --
-- DROP TABLE IF EXISTS in_use.votes CASCADE;
CREATE TABLE in_use.votes (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	this_obj2users smallint NOT NULL,
	this_obj2ideas smallint,
	this_obj2merged_ideas smallint,
	this_obj2comments smallint,
	vote_type smallint NOT NULL,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT votes_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.votes OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.votes_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.votes_id_seq CASCADE;
-- CREATE SEQUENCE in_use.votes_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.votes_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.ideas | type: TABLE --
-- DROP TABLE IF EXISTS in_use.ideas CASCADE;
CREATE TABLE in_use.ideas (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	this_obj2users smallint NOT NULL,
	title character varying NOT NULL,
	subject character varying NOT NULL,
	content character varying NOT NULL,
	refine_content character varying,
	tags_list smallint[],
	link character varying,
	file_path character varying,
	status smallint NOT NULL,
	parent_idea smallint,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT ideas_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.ideas OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.ideas_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.ideas_id_seq CASCADE;
-- CREATE SEQUENCE in_use.ideas_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.ideas_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.comments | type: TABLE --
-- DROP TABLE IF EXISTS in_use.comments CASCADE;
CREATE TABLE in_use.comments (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	this_obj2users smallint NOT NULL,
	this_obj2ideas smallint,
	this_obj2merged_ideas smallint,
	parent_comment smallint DEFAULT '-1'::integer,
	content character varying NOT NULL,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT comments_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.comments OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.comments_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.comments_id_seq CASCADE;
-- CREATE SEQUENCE in_use.comments_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.comments_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.tags | type: TABLE --
-- DROP TABLE IF EXISTS in_use.tags CASCADE;
CREATE TABLE in_use.tags (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	name character varying NOT NULL,
	tag_desc character varying NOT NULL,
	status smallint NOT NULL,
	generated_by character varying NOT NULL,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT tags_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.tags OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.tags_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.tags_id_seq CASCADE;
-- CREATE SEQUENCE in_use.tags_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.tags_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.merged_ideas | type: TABLE --
-- DROP TABLE IF EXISTS in_use.merged_ideas CASCADE;
CREATE TABLE in_use.merged_ideas (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	title character varying,
	subject character varying NOT NULL,
	content character varying NOT NULL,
	tags_list smallint[],
	status smallint NOT NULL,
	create_datetime timestamp NOT NULL,
	lastchange_datetime timestamp NOT NULL,
	CONSTRAINT merged_ideas_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.merged_ideas OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.merged_ideas_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.merged_ideas_id_seq CASCADE;
-- CREATE SEQUENCE in_use.merged_ideas_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.merged_ideas_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: in_use.ideas_merged_ideas_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS in_use.ideas_merged_ideas_id_seq CASCADE;
CREATE SEQUENCE in_use.ideas_merged_ideas_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE in_use.ideas_merged_ideas_id_seq OWNER TO postgres;
-- ddl-end --

-- object: in_use.ideas_merged_ideas | type: TABLE --
-- DROP TABLE IF EXISTS in_use.ideas_merged_ideas CASCADE;
CREATE TABLE in_use.ideas_merged_ideas (
	id integer NOT NULL DEFAULT nextval('in_use.ideas_merged_ideas_id_seq'::regclass),
	id_merged_ideas smallint NOT NULL,
	id_ideas smallint NOT NULL,
	CONSTRAINT ideas_merged_ideas_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.ideas_merged_ideas OWNER TO postgres;
-- ddl-end --

-- object: in_use.users_roles_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS in_use.users_roles_id_seq CASCADE;
CREATE SEQUENCE in_use.users_roles_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE in_use.users_roles_id_seq OWNER TO postgres;
-- ddl-end --

-- object: in_use.users_roles | type: TABLE --
-- DROP TABLE IF EXISTS in_use.users_roles CASCADE;
CREATE TABLE in_use.users_roles (
	id integer NOT NULL DEFAULT nextval('in_use.users_roles_id_seq'::regclass),
	id_roles smallint NOT NULL,
	id_users smallint NOT NULL,
	CONSTRAINT users_roles_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.users_roles OWNER TO postgres;
-- ddl-end --

-- object: in_use.security_ques | type: TABLE --
-- DROP TABLE IF EXISTS in_use.security_ques CASCADE;
CREATE TABLE in_use.security_ques (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	content character varying NOT NULL,
	CONSTRAINT pk_security_ques PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE in_use.security_ques OWNER TO postgres;
-- ddl-end --

-- -- object: in_use.security_ques_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS in_use.security_ques_id_seq CASCADE;
-- CREATE SEQUENCE in_use.security_ques_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE in_use.security_ques_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: fk_this_obj2security_ques | type: CONSTRAINT --
-- ALTER TABLE in_use.users DROP CONSTRAINT IF EXISTS fk_this_obj2security_ques CASCADE;
ALTER TABLE in_use.users ADD CONSTRAINT fk_this_obj2security_ques FOREIGN KEY (this_obj2security_ques)
REFERENCES in_use.security_ques (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2users | type: CONSTRAINT --
-- ALTER TABLE in_use.votes DROP CONSTRAINT IF EXISTS fk_this_obj2users CASCADE;
ALTER TABLE in_use.votes ADD CONSTRAINT fk_this_obj2users FOREIGN KEY (this_obj2users)
REFERENCES in_use.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2ideas | type: CONSTRAINT --
-- ALTER TABLE in_use.votes DROP CONSTRAINT IF EXISTS fk_this_obj2ideas CASCADE;
ALTER TABLE in_use.votes ADD CONSTRAINT fk_this_obj2ideas FOREIGN KEY (this_obj2ideas)
REFERENCES in_use.ideas (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2comments | type: CONSTRAINT --
-- ALTER TABLE in_use.votes DROP CONSTRAINT IF EXISTS fk_this_obj2comments CASCADE;
ALTER TABLE in_use.votes ADD CONSTRAINT fk_this_obj2comments FOREIGN KEY (this_obj2comments)
REFERENCES in_use.comments (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2merged_ideas | type: CONSTRAINT --
-- ALTER TABLE in_use.votes DROP CONSTRAINT IF EXISTS fk_this_obj2merged_ideas CASCADE;
ALTER TABLE in_use.votes ADD CONSTRAINT fk_this_obj2merged_ideas FOREIGN KEY (this_obj2merged_ideas)
REFERENCES in_use.merged_ideas (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2user | type: CONSTRAINT --
-- ALTER TABLE in_use.ideas DROP CONSTRAINT IF EXISTS fk_this_obj2user CASCADE;
ALTER TABLE in_use.ideas ADD CONSTRAINT fk_this_obj2user FOREIGN KEY (this_obj2users)
REFERENCES in_use.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2users | type: CONSTRAINT --
-- ALTER TABLE in_use.comments DROP CONSTRAINT IF EXISTS fk_this_obj2users CASCADE;
ALTER TABLE in_use.comments ADD CONSTRAINT fk_this_obj2users FOREIGN KEY (this_obj2users)
REFERENCES in_use.users (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2ideas | type: CONSTRAINT --
-- ALTER TABLE in_use.comments DROP CONSTRAINT IF EXISTS fk_this_obj2ideas CASCADE;
ALTER TABLE in_use.comments ADD CONSTRAINT fk_this_obj2ideas FOREIGN KEY (this_obj2ideas)
REFERENCES in_use.ideas (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_this_obj2merged_ideas | type: CONSTRAINT --
-- ALTER TABLE in_use.comments DROP CONSTRAINT IF EXISTS fk_this_obj2merged_ideas CASCADE;
ALTER TABLE in_use.comments ADD CONSTRAINT fk_this_obj2merged_ideas FOREIGN KEY (this_obj2merged_ideas)
REFERENCES in_use.merged_ideas (id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: merged_ideas_fk | type: CONSTRAINT --
-- ALTER TABLE in_use.ideas_merged_ideas DROP CONSTRAINT IF EXISTS merged_ideas_fk CASCADE;
ALTER TABLE in_use.ideas_merged_ideas ADD CONSTRAINT merged_ideas_fk FOREIGN KEY (id_merged_ideas)
REFERENCES in_use.merged_ideas (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: ideas_fk | type: CONSTRAINT --
-- ALTER TABLE in_use.ideas_merged_ideas DROP CONSTRAINT IF EXISTS ideas_fk CASCADE;
ALTER TABLE in_use.ideas_merged_ideas ADD CONSTRAINT ideas_fk FOREIGN KEY (id_ideas)
REFERENCES in_use.ideas (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: roles_fk | type: CONSTRAINT --
-- ALTER TABLE in_use.users_roles DROP CONSTRAINT IF EXISTS roles_fk CASCADE;
ALTER TABLE in_use.users_roles ADD CONSTRAINT roles_fk FOREIGN KEY (id_roles)
REFERENCES in_use.roles (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: users_fk | type: CONSTRAINT --
-- ALTER TABLE in_use.users_roles DROP CONSTRAINT IF EXISTS users_fk CASCADE;
ALTER TABLE in_use.users_roles ADD CONSTRAINT users_fk FOREIGN KEY (id_users)
REFERENCES in_use.users (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


