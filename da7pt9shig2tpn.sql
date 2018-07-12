-- Adminer 4.6.3-dev PostgreSQL dump

\connect "da7pt9shig2tpn";

DROP TABLE IF EXISTS "comments";
DROP SEQUENCE IF EXISTS comments_id_seq;
CREATE SEQUENCE comments_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."comments" (
    "id" integer DEFAULT nextval('comments_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "comment" character varying NOT NULL,
    "place" character varying NOT NULL,
    CONSTRAINT "comments_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "zip";
DROP SEQUENCE IF EXISTS zip_id_seq;
CREATE SEQUENCE zip_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."zip" (
    "id" integer DEFAULT nextval('zip_id_seq') NOT NULL,
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" numeric NOT NULL,
    "long" numeric NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "zip_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-12 21:27:44.613431+00
