PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE `migration_log` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `migration_id` TEXT NOT NULL
, `sql` TEXT NOT NULL
, `success` INTEGER NOT NULL
, `error` TEXT NOT NULL
, `timestamp` DATETIME NOT NULL
);
INSERT INTO migration_log VALUES(1,'create migration_log table',replace('CREATE TABLE IF NOT EXISTS `migration_log` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `migration_id` TEXT NOT NULL\n, `sql` TEXT NOT NULL\n, `success` INTEGER NOT NULL\n, `error` TEXT NOT NULL\n, `timestamp` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(2,'create user table',replace('CREATE TABLE IF NOT EXISTS `user` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `login` TEXT NOT NULL\n, `email` TEXT NOT NULL\n, `name` TEXT NULL\n, `password` TEXT NULL\n, `salt` TEXT NULL\n, `rands` TEXT NULL\n, `company` TEXT NULL\n, `account_id` INTEGER NOT NULL\n, `is_admin` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(3,'add unique index user.login','CREATE UNIQUE INDEX `UQE_user_login` ON `user` (`login`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(4,'add unique index user.email','CREATE UNIQUE INDEX `UQE_user_email` ON `user` (`email`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(5,'drop index UQE_user_login - v1','DROP INDEX `UQE_user_login`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(6,'drop index UQE_user_email - v1','DROP INDEX `UQE_user_email`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(7,'Rename table user to user_v1 - v1','ALTER TABLE `user` RENAME TO `user_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(8,'create user table v2',replace('CREATE TABLE IF NOT EXISTS `user` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `login` TEXT NOT NULL\n, `email` TEXT NOT NULL\n, `name` TEXT NULL\n, `password` TEXT NULL\n, `salt` TEXT NULL\n, `rands` TEXT NULL\n, `company` TEXT NULL\n, `org_id` INTEGER NOT NULL\n, `is_admin` INTEGER NOT NULL\n, `email_verified` INTEGER NULL\n, `theme` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(9,'create index UQE_user_login - v2','CREATE UNIQUE INDEX `UQE_user_login` ON `user` (`login`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(10,'create index UQE_user_email - v2','CREATE UNIQUE INDEX `UQE_user_email` ON `user` (`email`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(11,'copy data_source v1 to v2',replace('INSERT INTO `user` (`email`\n, `name`\n, `password`\n, `org_id`\n, `created`\n, `login`\n, `version`\n, `salt`\n, `rands`\n, `company`\n, `is_admin`\n, `updated`\n, `id`) SELECT `email`\n, `name`\n, `password`\n, `account_id`\n, `created`\n, `login`\n, `version`\n, `salt`\n, `rands`\n, `company`\n, `is_admin`\n, `updated`\n, `id` FROM `user_v1`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(12,'Drop old table user_v1','DROP TABLE IF EXISTS `user_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(13,'Add column help_flags1 to user table','alter table `user` ADD COLUMN `help_flags1` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(14,'Update user table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(15,'Add last_seen_at column to user','alter table `user` ADD COLUMN `last_seen_at` DATETIME NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(16,'Add missing user data','code migration',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(17,'Add is_disabled column to user','alter table `user` ADD COLUMN `is_disabled` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(18,'Add index user.login/user.email','CREATE INDEX `IDX_user_login_email` ON `user` (`login`,`email`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(19,'Add is_service_account column to user','alter table `user` ADD COLUMN `is_service_account` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(20,'Update is_service_account column to nullable',replace('ALTER TABLE user ADD COLUMN tmp_service_account BOOLEAN DEFAULT 0;\nUPDATE user SET tmp_service_account = is_service_account;\nALTER TABLE user DROP COLUMN is_service_account;\nALTER TABLE user RENAME COLUMN tmp_service_account TO is_service_account;','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(21,'create temp user table v1-7',replace('CREATE TABLE IF NOT EXISTS `temp_user` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `email` TEXT NOT NULL\n, `name` TEXT NULL\n, `role` TEXT NULL\n, `code` TEXT NOT NULL\n, `status` TEXT NOT NULL\n, `invited_by_user_id` INTEGER NULL\n, `email_sent` INTEGER NOT NULL\n, `email_sent_on` DATETIME NULL\n, `remote_addr` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(22,'create index IDX_temp_user_email - v1-7','CREATE INDEX `IDX_temp_user_email` ON `temp_user` (`email`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(23,'create index IDX_temp_user_org_id - v1-7','CREATE INDEX `IDX_temp_user_org_id` ON `temp_user` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(24,'create index IDX_temp_user_code - v1-7','CREATE INDEX `IDX_temp_user_code` ON `temp_user` (`code`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(25,'create index IDX_temp_user_status - v1-7','CREATE INDEX `IDX_temp_user_status` ON `temp_user` (`status`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(26,'Update temp_user table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(27,'drop index IDX_temp_user_email - v1','DROP INDEX `IDX_temp_user_email`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(28,'drop index IDX_temp_user_org_id - v1','DROP INDEX `IDX_temp_user_org_id`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(29,'drop index IDX_temp_user_code - v1','DROP INDEX `IDX_temp_user_code`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(30,'drop index IDX_temp_user_status - v1','DROP INDEX `IDX_temp_user_status`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(31,'Rename table temp_user to temp_user_tmp_qwerty - v1','ALTER TABLE `temp_user` RENAME TO `temp_user_tmp_qwerty`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(32,'create temp_user v2',replace('CREATE TABLE IF NOT EXISTS `temp_user` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `email` TEXT NOT NULL\n, `name` TEXT NULL\n, `role` TEXT NULL\n, `code` TEXT NOT NULL\n, `status` TEXT NOT NULL\n, `invited_by_user_id` INTEGER NULL\n, `email_sent` INTEGER NOT NULL\n, `email_sent_on` DATETIME NULL\n, `remote_addr` TEXT NULL\n, `created` INTEGER NOT NULL DEFAULT 0\n, `updated` INTEGER NOT NULL DEFAULT 0\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(33,'create index IDX_temp_user_email - v2','CREATE INDEX `IDX_temp_user_email` ON `temp_user` (`email`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(34,'create index IDX_temp_user_org_id - v2','CREATE INDEX `IDX_temp_user_org_id` ON `temp_user` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(35,'create index IDX_temp_user_code - v2','CREATE INDEX `IDX_temp_user_code` ON `temp_user` (`code`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(36,'create index IDX_temp_user_status - v2','CREATE INDEX `IDX_temp_user_status` ON `temp_user` (`status`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(37,'copy temp_user v1 to v2',replace('INSERT INTO `temp_user` (`org_id`\n, `email`\n, `name`\n, `code`\n, `invited_by_user_id`\n, `id`\n, `role`\n, `status`\n, `email_sent`\n, `email_sent_on`\n, `remote_addr`\n, `version`) SELECT `org_id`\n, `email`\n, `name`\n, `code`\n, `invited_by_user_id`\n, `id`\n, `role`\n, `status`\n, `email_sent`\n, `email_sent_on`\n, `remote_addr`\n, `version` FROM `temp_user_tmp_qwerty`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(38,'drop temp_user_tmp_qwerty','DROP TABLE IF EXISTS `temp_user_tmp_qwerty`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(39,'Set created for temp users that will otherwise prematurely expire','code migration',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(40,'create star table',replace('CREATE TABLE IF NOT EXISTS `star` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `user_id` INTEGER NOT NULL\n, `dashboard_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(41,'add unique index star.user_id_dashboard_id','CREATE UNIQUE INDEX `UQE_star_user_id_dashboard_id` ON `star` (`user_id`,`dashboard_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(42,'create org table v1',replace('CREATE TABLE IF NOT EXISTS `org` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `name` TEXT NOT NULL\n, `address1` TEXT NULL\n, `address2` TEXT NULL\n, `city` TEXT NULL\n, `state` TEXT NULL\n, `zip_code` TEXT NULL\n, `country` TEXT NULL\n, `billing_email` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(43,'create index UQE_org_name - v1','CREATE UNIQUE INDEX `UQE_org_name` ON `org` (`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(44,'create org_user table v1',replace('CREATE TABLE IF NOT EXISTS `org_user` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `user_id` INTEGER NOT NULL\n, `role` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(45,'create index IDX_org_user_org_id - v1','CREATE INDEX `IDX_org_user_org_id` ON `org_user` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(46,'create index UQE_org_user_org_id_user_id - v1','CREATE UNIQUE INDEX `UQE_org_user_org_id_user_id` ON `org_user` (`org_id`,`user_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(47,'create index IDX_org_user_user_id - v1','CREATE INDEX `IDX_org_user_user_id` ON `org_user` (`user_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(48,'Update org table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(49,'Update org_user table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(50,'Migrate all Read Only Viewers to Viewers','UPDATE org_user SET role = ''Viewer'' WHERE role = ''Read Only Editor''',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(51,'create dashboard table',replace('CREATE TABLE IF NOT EXISTS `dashboard` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `slug` TEXT NOT NULL\n, `title` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `account_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(52,'add index dashboard.account_id','CREATE INDEX `IDX_dashboard_account_id` ON `dashboard` (`account_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(53,'add unique index dashboard_account_id_slug','CREATE UNIQUE INDEX `UQE_dashboard_account_id_slug` ON `dashboard` (`account_id`,`slug`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(54,'create dashboard_tag table',replace('CREATE TABLE IF NOT EXISTS `dashboard_tag` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `dashboard_id` INTEGER NOT NULL\n, `term` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(55,'add unique index dashboard_tag.dasboard_id_term','CREATE UNIQUE INDEX `UQE_dashboard_tag_dashboard_id_term` ON `dashboard_tag` (`dashboard_id`,`term`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(56,'drop index UQE_dashboard_tag_dashboard_id_term - v1','DROP INDEX `UQE_dashboard_tag_dashboard_id_term`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(57,'Rename table dashboard to dashboard_v1 - v1','ALTER TABLE `dashboard` RENAME TO `dashboard_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(58,'create dashboard v2',replace('CREATE TABLE IF NOT EXISTS `dashboard` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `slug` TEXT NOT NULL\n, `title` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(59,'create index IDX_dashboard_org_id - v2','CREATE INDEX `IDX_dashboard_org_id` ON `dashboard` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(60,'create index UQE_dashboard_org_id_slug - v2','CREATE UNIQUE INDEX `UQE_dashboard_org_id_slug` ON `dashboard` (`org_id`,`slug`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(61,'copy dashboard v1 to v2',replace('INSERT INTO `dashboard` (`version`\n, `slug`\n, `title`\n, `data`\n, `org_id`\n, `created`\n, `updated`\n, `id`) SELECT `version`\n, `slug`\n, `title`\n, `data`\n, `account_id`\n, `created`\n, `updated`\n, `id` FROM `dashboard_v1`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(62,'drop table dashboard_v1','DROP TABLE IF EXISTS `dashboard_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(63,'alter dashboard.data to mediumtext v1','SELECT 0;',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(64,'Add column updated_by in dashboard - v2','alter table `dashboard` ADD COLUMN `updated_by` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(65,'Add column created_by in dashboard - v2','alter table `dashboard` ADD COLUMN `created_by` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(66,'Add column gnetId in dashboard','alter table `dashboard` ADD COLUMN `gnet_id` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(67,'Add index for gnetId in dashboard','CREATE INDEX `IDX_dashboard_gnet_id` ON `dashboard` (`gnet_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(68,'Add column plugin_id in dashboard','alter table `dashboard` ADD COLUMN `plugin_id` TEXT NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(69,'Add index for plugin_id in dashboard','CREATE INDEX `IDX_dashboard_org_id_plugin_id` ON `dashboard` (`org_id`,`plugin_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(70,'Add index for dashboard_id in dashboard_tag','CREATE INDEX `IDX_dashboard_tag_dashboard_id` ON `dashboard_tag` (`dashboard_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(71,'Update dashboard table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(72,'Update dashboard_tag table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(73,'Add column folder_id in dashboard','alter table `dashboard` ADD COLUMN `folder_id` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(74,'Add column isFolder in dashboard','alter table `dashboard` ADD COLUMN `is_folder` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(75,'Add column has_acl in dashboard','alter table `dashboard` ADD COLUMN `has_acl` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(76,'Add column uid in dashboard','alter table `dashboard` ADD COLUMN `uid` TEXT NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(77,'Update uid column values in dashboard','UPDATE dashboard SET uid=printf(''%09d'',id) WHERE uid IS NULL;',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(78,'Add unique index dashboard_org_id_uid','CREATE UNIQUE INDEX `UQE_dashboard_org_id_uid` ON `dashboard` (`org_id`,`uid`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(79,'Remove unique index org_id_slug','DROP INDEX `UQE_dashboard_org_id_slug`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(80,'Update dashboard title length','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(81,'Add unique index for dashboard_org_id_title_folder_id','CREATE UNIQUE INDEX `UQE_dashboard_org_id_folder_id_title` ON `dashboard` (`org_id`,`folder_id`,`title`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(82,'create dashboard_provisioning',replace('CREATE TABLE IF NOT EXISTS `dashboard_provisioning` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `dashboard_id` INTEGER NULL\n, `name` TEXT NOT NULL\n, `external_id` TEXT NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(83,'Rename table dashboard_provisioning to dashboard_provisioning_tmp_qwerty - v1','ALTER TABLE `dashboard_provisioning` RENAME TO `dashboard_provisioning_tmp_qwerty`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(84,'create dashboard_provisioning v2',replace('CREATE TABLE IF NOT EXISTS `dashboard_provisioning` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `dashboard_id` INTEGER NULL\n, `name` TEXT NOT NULL\n, `external_id` TEXT NOT NULL\n, `updated` INTEGER NOT NULL DEFAULT 0\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(85,'create index IDX_dashboard_provisioning_dashboard_id - v2','CREATE INDEX `IDX_dashboard_provisioning_dashboard_id` ON `dashboard_provisioning` (`dashboard_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(86,'create index IDX_dashboard_provisioning_dashboard_id_name - v2','CREATE INDEX `IDX_dashboard_provisioning_dashboard_id_name` ON `dashboard_provisioning` (`dashboard_id`,`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(87,'copy dashboard_provisioning v1 to v2',replace('INSERT INTO `dashboard_provisioning` (`name`\n, `external_id`\n, `id`\n, `dashboard_id`) SELECT `name`\n, `external_id`\n, `id`\n, `dashboard_id` FROM `dashboard_provisioning_tmp_qwerty`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(88,'drop dashboard_provisioning_tmp_qwerty','DROP TABLE IF EXISTS `dashboard_provisioning_tmp_qwerty`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(89,'Add check_sum column','alter table `dashboard_provisioning` ADD COLUMN `check_sum` TEXT NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(90,'Add index for dashboard_title','CREATE INDEX `IDX_dashboard_title` ON `dashboard` (`title`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(91,'delete tags for deleted dashboards','DELETE FROM dashboard_tag WHERE dashboard_id NOT IN (SELECT id FROM dashboard)',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(92,'delete stars for deleted dashboards','DELETE FROM star WHERE dashboard_id NOT IN (SELECT id FROM dashboard)',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(93,'Add index for dashboard_is_folder','CREATE INDEX `IDX_dashboard_is_folder` ON `dashboard` (`is_folder`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(94,'create data_source table',replace('CREATE TABLE IF NOT EXISTS `data_source` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `account_id` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `type` TEXT NOT NULL\n, `name` TEXT NOT NULL\n, `access` TEXT NOT NULL\n, `url` TEXT NOT NULL\n, `password` TEXT NULL\n, `user` TEXT NULL\n, `database` TEXT NULL\n, `basic_auth` INTEGER NOT NULL\n, `basic_auth_user` TEXT NULL\n, `basic_auth_password` TEXT NULL\n, `is_default` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(95,'add index data_source.account_id','CREATE INDEX `IDX_data_source_account_id` ON `data_source` (`account_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(96,'add unique index data_source.account_id_name','CREATE UNIQUE INDEX `UQE_data_source_account_id_name` ON `data_source` (`account_id`,`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(97,'drop index IDX_data_source_account_id - v1','DROP INDEX `IDX_data_source_account_id`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(98,'drop index UQE_data_source_account_id_name - v1','DROP INDEX `UQE_data_source_account_id_name`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(99,'Rename table data_source to data_source_v1 - v1','ALTER TABLE `data_source` RENAME TO `data_source_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(100,'create data_source table v2',replace('CREATE TABLE IF NOT EXISTS `data_source` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `type` TEXT NOT NULL\n, `name` TEXT NOT NULL\n, `access` TEXT NOT NULL\n, `url` TEXT NOT NULL\n, `password` TEXT NULL\n, `user` TEXT NULL\n, `database` TEXT NULL\n, `basic_auth` INTEGER NOT NULL\n, `basic_auth_user` TEXT NULL\n, `basic_auth_password` TEXT NULL\n, `is_default` INTEGER NOT NULL\n, `json_data` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(101,'create index IDX_data_source_org_id - v2','CREATE INDEX `IDX_data_source_org_id` ON `data_source` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(102,'create index UQE_data_source_org_id_name - v2','CREATE UNIQUE INDEX `UQE_data_source_org_id_name` ON `data_source` (`org_id`,`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(103,'copy data_source v1 to v2',replace('INSERT INTO `data_source` (`version`\n, `user`\n, `basic_auth_user`\n, `org_id`\n, `access`\n, `password`\n, `basic_auth`\n, `is_default`\n, `created`\n, `id`\n, `url`\n, `updated`\n, `name`\n, `database`\n, `basic_auth_password`\n, `type`) SELECT `version`\n, `user`\n, `basic_auth_user`\n, `account_id`\n, `access`\n, `password`\n, `basic_auth`\n, `is_default`\n, `created`\n, `id`\n, `url`\n, `updated`\n, `name`\n, `database`\n, `basic_auth_password`\n, `type` FROM `data_source_v1`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(104,'Drop old table data_source_v1 #2','DROP TABLE IF EXISTS `data_source_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(105,'Add column with_credentials','alter table `data_source` ADD COLUMN `with_credentials` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(106,'Add secure json data column','alter table `data_source` ADD COLUMN `secure_json_data` TEXT NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(107,'Update data_source table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(108,'Update initial version to 1','UPDATE data_source SET version = 1 WHERE version = 0',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(109,'Add read_only data column','alter table `data_source` ADD COLUMN `read_only` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(110,'Migrate logging ds to loki ds','UPDATE data_source SET type = ''loki'' WHERE type = ''logging''',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(111,'Update json_data with nulls','UPDATE data_source SET json_data = ''{}'' WHERE json_data is null',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(112,'Add uid column','alter table `data_source` ADD COLUMN `uid` TEXT NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(113,'Update uid value','UPDATE data_source SET uid=printf(''%09d'',id);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(114,'Add unique index datasource_org_id_uid','CREATE UNIQUE INDEX `UQE_data_source_org_id_uid` ON `data_source` (`org_id`,`uid`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(115,'add unique index datasource_org_id_is_default','CREATE INDEX `IDX_data_source_org_id_is_default` ON `data_source` (`org_id`,`is_default`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(116,'create api_key table',replace('CREATE TABLE IF NOT EXISTS `api_key` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `account_id` INTEGER NOT NULL\n, `name` TEXT NOT NULL\n, `key` TEXT NOT NULL\n, `role` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(117,'add index api_key.account_id','CREATE INDEX `IDX_api_key_account_id` ON `api_key` (`account_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(118,'add index api_key.key','CREATE UNIQUE INDEX `UQE_api_key_key` ON `api_key` (`key`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(119,'add index api_key.account_id_name','CREATE UNIQUE INDEX `UQE_api_key_account_id_name` ON `api_key` (`account_id`,`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(120,'drop index IDX_api_key_account_id - v1','DROP INDEX `IDX_api_key_account_id`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(121,'drop index UQE_api_key_key - v1','DROP INDEX `UQE_api_key_key`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(122,'drop index UQE_api_key_account_id_name - v1','DROP INDEX `UQE_api_key_account_id_name`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(123,'Rename table api_key to api_key_v1 - v1','ALTER TABLE `api_key` RENAME TO `api_key_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(124,'create api_key table v2',replace('CREATE TABLE IF NOT EXISTS `api_key` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `name` TEXT NOT NULL\n, `key` TEXT NOT NULL\n, `role` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(125,'create index IDX_api_key_org_id - v2','CREATE INDEX `IDX_api_key_org_id` ON `api_key` (`org_id`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(126,'create index UQE_api_key_key - v2','CREATE UNIQUE INDEX `UQE_api_key_key` ON `api_key` (`key`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(127,'create index UQE_api_key_org_id_name - v2','CREATE UNIQUE INDEX `UQE_api_key_org_id_name` ON `api_key` (`org_id`,`name`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(128,'copy api_key v1 to v2',replace('INSERT INTO `api_key` (`id`\n, `org_id`\n, `name`\n, `key`\n, `role`\n, `created`\n, `updated`) SELECT `id`\n, `account_id`\n, `name`\n, `key`\n, `role`\n, `created`\n, `updated` FROM `api_key_v1`','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(129,'Drop old table api_key_v1','DROP TABLE IF EXISTS `api_key_v1`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(130,'Update api_key table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(131,'Add expires to api_key table','alter table `api_key` ADD COLUMN `expires` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(132,'Add service account foreign key','alter table `api_key` ADD COLUMN `service_account_id` INTEGER NULL ',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(133,'set service account foreign key to nil if 0','UPDATE api_key SET service_account_id = NULL WHERE service_account_id = 0;',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(134,'create dashboard_snapshot table v4',replace('CREATE TABLE IF NOT EXISTS `dashboard_snapshot` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `name` TEXT NOT NULL\n, `key` TEXT NOT NULL\n, `dashboard` TEXT NOT NULL\n, `expires` DATETIME NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(135,'drop table dashboard_snapshot_v4 #1','DROP TABLE IF EXISTS `dashboard_snapshot`',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(136,'create dashboard_snapshot table v5 #2',replace('CREATE TABLE IF NOT EXISTS `dashboard_snapshot` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `name` TEXT NOT NULL\n, `key` TEXT NOT NULL\n, `delete_key` TEXT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `user_id` INTEGER NOT NULL\n, `external` INTEGER NOT NULL\n, `external_url` TEXT NOT NULL\n, `dashboard` TEXT NOT NULL\n, `expires` DATETIME NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(137,'create index UQE_dashboard_snapshot_key - v5','CREATE UNIQUE INDEX `UQE_dashboard_snapshot_key` ON `dashboard_snapshot` (`key`);',1,'','2022-05-17 11:51:39');
INSERT INTO migration_log VALUES(138,'create index UQE_dashboard_snapshot_delete_key - v5','CREATE UNIQUE INDEX `UQE_dashboard_snapshot_delete_key` ON `dashboard_snapshot` (`delete_key`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(139,'create index IDX_dashboard_snapshot_user_id - v5','CREATE INDEX `IDX_dashboard_snapshot_user_id` ON `dashboard_snapshot` (`user_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(140,'alter dashboard_snapshot to mediumtext v2','SELECT 0;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(141,'Update dashboard_snapshot table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(142,'Add column external_delete_url to dashboard_snapshots table','alter table `dashboard_snapshot` ADD COLUMN `external_delete_url` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(143,'Add encrypted dashboard json column','alter table `dashboard_snapshot` ADD COLUMN `dashboard_encrypted` BLOB NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(144,'Change dashboard_encrypted column to MEDIUMBLOB','SELECT 0;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(145,'create quota table v1',replace('CREATE TABLE IF NOT EXISTS `quota` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NULL\n, `user_id` INTEGER NULL\n, `target` TEXT NOT NULL\n, `limit` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(146,'create index UQE_quota_org_id_user_id_target - v1','CREATE UNIQUE INDEX `UQE_quota_org_id_user_id_target` ON `quota` (`org_id`,`user_id`,`target`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(147,'Update quota table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(148,'create plugin_setting table',replace('CREATE TABLE IF NOT EXISTS `plugin_setting` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NULL\n, `plugin_id` TEXT NOT NULL\n, `enabled` INTEGER NOT NULL\n, `pinned` INTEGER NOT NULL\n, `json_data` TEXT NULL\n, `secure_json_data` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(149,'create index UQE_plugin_setting_org_id_plugin_id - v1','CREATE UNIQUE INDEX `UQE_plugin_setting_org_id_plugin_id` ON `plugin_setting` (`org_id`,`plugin_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(150,'Add column plugin_version to plugin_settings','alter table `plugin_setting` ADD COLUMN `plugin_version` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(151,'Update plugin_setting table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(152,'create session table',replace('CREATE TABLE IF NOT EXISTS `session` (\n`key` TEXT PRIMARY KEY NOT NULL\n, `data` BLOB NOT NULL\n, `expiry` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(153,'Drop old table playlist table','DROP TABLE IF EXISTS `playlist`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(154,'Drop old table playlist_item table','DROP TABLE IF EXISTS `playlist_item`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(155,'create playlist table v2',replace('CREATE TABLE IF NOT EXISTS `playlist` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `name` TEXT NOT NULL\n, `interval` TEXT NOT NULL\n, `org_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(156,'create playlist item table v2',replace('CREATE TABLE IF NOT EXISTS `playlist_item` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `playlist_id` INTEGER NOT NULL\n, `type` TEXT NOT NULL\n, `value` TEXT NOT NULL\n, `title` TEXT NOT NULL\n, `order` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(157,'Update playlist table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(158,'Update playlist_item table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(159,'drop preferences table v2','DROP TABLE IF EXISTS `preferences`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(160,'drop preferences table v3','DROP TABLE IF EXISTS `preferences`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(161,'create preferences table v3',replace('CREATE TABLE IF NOT EXISTS `preferences` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `user_id` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `home_dashboard_id` INTEGER NOT NULL\n, `timezone` TEXT NOT NULL\n, `theme` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(162,'Update preferences table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(163,'Add column team_id in preferences','alter table `preferences` ADD COLUMN `team_id` INTEGER NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(164,'Update team_id column values in preferences','UPDATE preferences SET team_id=0 WHERE team_id IS NULL;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(165,'Add column week_start in preferences','alter table `preferences` ADD COLUMN `week_start` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(166,'Add column preferences.json_data','alter table `preferences` ADD COLUMN `json_data` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(167,'alter preferences.json_data to mediumtext v1','SELECT 0;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(168,'create alert table v1',replace('CREATE TABLE IF NOT EXISTS `alert` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `version` INTEGER NOT NULL\n, `dashboard_id` INTEGER NOT NULL\n, `panel_id` INTEGER NOT NULL\n, `org_id` INTEGER NOT NULL\n, `name` TEXT NOT NULL\n, `message` TEXT NOT NULL\n, `state` TEXT NOT NULL\n, `settings` TEXT NOT NULL\n, `frequency` INTEGER NOT NULL\n, `handler` INTEGER NOT NULL\n, `severity` TEXT NOT NULL\n, `silenced` INTEGER NOT NULL\n, `execution_error` TEXT NOT NULL\n, `eval_data` TEXT NULL\n, `eval_date` DATETIME NULL\n, `new_state_date` DATETIME NOT NULL\n, `state_changes` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(169,'add index alert org_id & id ','CREATE INDEX `IDX_alert_org_id_id` ON `alert` (`org_id`,`id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(170,'add index alert state','CREATE INDEX `IDX_alert_state` ON `alert` (`state`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(171,'add index alert dashboard_id','CREATE INDEX `IDX_alert_dashboard_id` ON `alert` (`dashboard_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(172,'Create alert_rule_tag table v1',replace('CREATE TABLE IF NOT EXISTS `alert_rule_tag` (\n`alert_id` INTEGER NOT NULL\n, `tag_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(173,'Add unique index alert_rule_tag.alert_id_tag_id','CREATE UNIQUE INDEX `UQE_alert_rule_tag_alert_id_tag_id` ON `alert_rule_tag` (`alert_id`,`tag_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(174,'drop index UQE_alert_rule_tag_alert_id_tag_id - v1','DROP INDEX `UQE_alert_rule_tag_alert_id_tag_id`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(175,'Rename table alert_rule_tag to alert_rule_tag_v1 - v1','ALTER TABLE `alert_rule_tag` RENAME TO `alert_rule_tag_v1`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(176,'Create alert_rule_tag table v2',replace('CREATE TABLE IF NOT EXISTS `alert_rule_tag` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `alert_id` INTEGER NOT NULL\n, `tag_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(177,'create index UQE_alert_rule_tag_alert_id_tag_id - Add unique index alert_rule_tag.alert_id_tag_id V2','CREATE UNIQUE INDEX `UQE_alert_rule_tag_alert_id_tag_id` ON `alert_rule_tag` (`alert_id`,`tag_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(178,'copy alert_rule_tag v1 to v2',replace('INSERT INTO `alert_rule_tag` (`alert_id`\n, `tag_id`) SELECT `alert_id`\n, `tag_id` FROM `alert_rule_tag_v1`','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(179,'drop table alert_rule_tag_v1','DROP TABLE IF EXISTS `alert_rule_tag_v1`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(180,'create alert_notification table v1',replace('CREATE TABLE IF NOT EXISTS `alert_notification` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `name` TEXT NOT NULL\n, `type` TEXT NOT NULL\n, `settings` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(181,'Add column is_default','alter table `alert_notification` ADD COLUMN `is_default` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(182,'Add column frequency','alter table `alert_notification` ADD COLUMN `frequency` INTEGER NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(183,'Add column send_reminder','alter table `alert_notification` ADD COLUMN `send_reminder` INTEGER NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(184,'Add column disable_resolve_message','alter table `alert_notification` ADD COLUMN `disable_resolve_message` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(185,'add index alert_notification org_id & name','CREATE UNIQUE INDEX `UQE_alert_notification_org_id_name` ON `alert_notification` (`org_id`,`name`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(186,'Update alert table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(187,'Update alert_notification table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(188,'create notification_journal table v1',replace('CREATE TABLE IF NOT EXISTS `alert_notification_journal` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `alert_id` INTEGER NOT NULL\n, `notifier_id` INTEGER NOT NULL\n, `sent_at` INTEGER NOT NULL\n, `success` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(189,'add index notification_journal org_id & alert_id & notifier_id','CREATE INDEX `IDX_alert_notification_journal_org_id_alert_id_notifier_id` ON `alert_notification_journal` (`org_id`,`alert_id`,`notifier_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(190,'drop alert_notification_journal','DROP TABLE IF EXISTS `alert_notification_journal`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(191,'create alert_notification_state table v1',replace('CREATE TABLE IF NOT EXISTS `alert_notification_state` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `alert_id` INTEGER NOT NULL\n, `notifier_id` INTEGER NOT NULL\n, `state` TEXT NOT NULL\n, `version` INTEGER NOT NULL\n, `updated_at` INTEGER NOT NULL\n, `alert_rule_state_updated_version` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(192,'add index alert_notification_state org_id & alert_id & notifier_id','CREATE UNIQUE INDEX `UQE_alert_notification_state_org_id_alert_id_notifier_id` ON `alert_notification_state` (`org_id`,`alert_id`,`notifier_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(193,'Add for to alert table','alter table `alert` ADD COLUMN `for` INTEGER NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(194,'Add column uid in alert_notification','alter table `alert_notification` ADD COLUMN `uid` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(195,'Update uid column values in alert_notification','UPDATE alert_notification SET uid=printf(''%09d'',id) WHERE uid IS NULL;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(196,'Add unique index alert_notification_org_id_uid','CREATE UNIQUE INDEX `UQE_alert_notification_org_id_uid` ON `alert_notification` (`org_id`,`uid`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(197,'Remove unique index org_id_name','DROP INDEX `UQE_alert_notification_org_id_name`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(198,'Add column secure_settings in alert_notification','alter table `alert_notification` ADD COLUMN `secure_settings` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(199,'alter alert.settings to mediumtext','SELECT 0;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(200,'Add non-unique index alert_notification_state_alert_id','CREATE INDEX `IDX_alert_notification_state_alert_id` ON `alert_notification_state` (`alert_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(201,'Add non-unique index alert_rule_tag_alert_id','CREATE INDEX `IDX_alert_rule_tag_alert_id` ON `alert_rule_tag` (`alert_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(202,'Drop old annotation table v4','DROP TABLE IF EXISTS `annotation`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(203,'create annotation table v5',replace('CREATE TABLE IF NOT EXISTS `annotation` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `alert_id` INTEGER NULL\n, `user_id` INTEGER NULL\n, `dashboard_id` INTEGER NULL\n, `panel_id` INTEGER NULL\n, `category_id` INTEGER NULL\n, `type` TEXT NOT NULL\n, `title` TEXT NOT NULL\n, `text` TEXT NOT NULL\n, `metric` TEXT NULL\n, `prev_state` TEXT NOT NULL\n, `new_state` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `epoch` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(204,'add index annotation 0 v3','CREATE INDEX `IDX_annotation_org_id_alert_id` ON `annotation` (`org_id`,`alert_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(205,'add index annotation 1 v3','CREATE INDEX `IDX_annotation_org_id_type` ON `annotation` (`org_id`,`type`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(206,'add index annotation 2 v3','CREATE INDEX `IDX_annotation_org_id_category_id` ON `annotation` (`org_id`,`category_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(207,'add index annotation 3 v3','CREATE INDEX `IDX_annotation_org_id_dashboard_id_panel_id_epoch` ON `annotation` (`org_id`,`dashboard_id`,`panel_id`,`epoch`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(208,'add index annotation 4 v3','CREATE INDEX `IDX_annotation_org_id_epoch` ON `annotation` (`org_id`,`epoch`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(209,'Update annotation table charset','-- NOT REQUIRED',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(210,'Add column region_id to annotation table','alter table `annotation` ADD COLUMN `region_id` INTEGER NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(211,'Drop category_id index','DROP INDEX `IDX_annotation_org_id_category_id`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(212,'Add column tags to annotation table','alter table `annotation` ADD COLUMN `tags` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(213,'Create annotation_tag table v2',replace('CREATE TABLE IF NOT EXISTS `annotation_tag` (\n`annotation_id` INTEGER NOT NULL\n, `tag_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(214,'Add unique index annotation_tag.annotation_id_tag_id','CREATE UNIQUE INDEX `UQE_annotation_tag_annotation_id_tag_id` ON `annotation_tag` (`annotation_id`,`tag_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(215,'drop index UQE_annotation_tag_annotation_id_tag_id - v2','DROP INDEX `UQE_annotation_tag_annotation_id_tag_id`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(216,'Rename table annotation_tag to annotation_tag_v2 - v2','ALTER TABLE `annotation_tag` RENAME TO `annotation_tag_v2`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(217,'Create annotation_tag table v3',replace('CREATE TABLE IF NOT EXISTS `annotation_tag` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `annotation_id` INTEGER NOT NULL\n, `tag_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(218,'create index UQE_annotation_tag_annotation_id_tag_id - Add unique index annotation_tag.annotation_id_tag_id V3','CREATE UNIQUE INDEX `UQE_annotation_tag_annotation_id_tag_id` ON `annotation_tag` (`annotation_id`,`tag_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(219,'copy annotation_tag v2 to v3',replace('INSERT INTO `annotation_tag` (`annotation_id`\n, `tag_id`) SELECT `annotation_id`\n, `tag_id` FROM `annotation_tag_v2`','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(220,'drop table annotation_tag_v2','DROP TABLE IF EXISTS `annotation_tag_v2`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(221,'Update alert annotations and set TEXT to empty','UPDATE annotation SET TEXT = '''' WHERE alert_id > 0',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(222,'Add created time to annotation table','alter table `annotation` ADD COLUMN `created` INTEGER NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(223,'Add updated time to annotation table','alter table `annotation` ADD COLUMN `updated` INTEGER NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(224,'Add index for created in annotation table','CREATE INDEX `IDX_annotation_org_id_created` ON `annotation` (`org_id`,`created`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(225,'Add index for updated in annotation table','CREATE INDEX `IDX_annotation_org_id_updated` ON `annotation` (`org_id`,`updated`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(226,'Convert existing annotations from seconds to milliseconds','UPDATE annotation SET epoch = (epoch*1000) where epoch < 9999999999',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(227,'Add epoch_end column','alter table `annotation` ADD COLUMN `epoch_end` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(228,'Add index for epoch_end','CREATE INDEX `IDX_annotation_org_id_epoch_epoch_end` ON `annotation` (`org_id`,`epoch`,`epoch_end`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(229,'Make epoch_end the same as epoch','UPDATE annotation SET epoch_end = epoch',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(230,'Move region to single row','code migration',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(231,'Remove index org_id_epoch from annotation table','DROP INDEX `IDX_annotation_org_id_epoch`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(232,'Remove index org_id_dashboard_id_panel_id_epoch from annotation table','DROP INDEX `IDX_annotation_org_id_dashboard_id_panel_id_epoch`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(233,'Add index for org_id_dashboard_id_epoch_end_epoch on annotation table','CREATE INDEX `IDX_annotation_org_id_dashboard_id_epoch_end_epoch` ON `annotation` (`org_id`,`dashboard_id`,`epoch_end`,`epoch`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(234,'Add index for org_id_epoch_end_epoch on annotation table','CREATE INDEX `IDX_annotation_org_id_epoch_end_epoch` ON `annotation` (`org_id`,`epoch_end`,`epoch`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(235,'Remove index org_id_epoch_epoch_end from annotation table','DROP INDEX `IDX_annotation_org_id_epoch_epoch_end`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(236,'Add index for alert_id on annotation table','CREATE INDEX `IDX_annotation_alert_id` ON `annotation` (`alert_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(237,'create test_data table',replace('CREATE TABLE IF NOT EXISTS `test_data` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `metric1` TEXT NULL\n, `metric2` TEXT NULL\n, `value_big_int` INTEGER NULL\n, `value_double` REAL NULL\n, `value_float` REAL NULL\n, `value_int` INTEGER NULL\n, `time_epoch` INTEGER NOT NULL\n, `time_date_time` DATETIME NOT NULL\n, `time_time_stamp` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(238,'create dashboard_version table v1',replace('CREATE TABLE IF NOT EXISTS `dashboard_version` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `dashboard_id` INTEGER NOT NULL\n, `parent_version` INTEGER NOT NULL\n, `restored_from` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `created_by` INTEGER NOT NULL\n, `message` TEXT NOT NULL\n, `data` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(239,'add index dashboard_version.dashboard_id','CREATE INDEX `IDX_dashboard_version_dashboard_id` ON `dashboard_version` (`dashboard_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(240,'add unique index dashboard_version.dashboard_id and dashboard_version.version','CREATE UNIQUE INDEX `UQE_dashboard_version_dashboard_id_version` ON `dashboard_version` (`dashboard_id`,`version`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(241,'Set dashboard version to 1 where 0','UPDATE dashboard SET version = 1 WHERE version = 0',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(242,'save existing dashboard data in dashboard_version table v1',replace('INSERT INTO dashboard_version\n(\n	dashboard_id,\n	version,\n	parent_version,\n	restored_from,\n	created,\n	created_by,\n	message,\n	data\n)\nSELECT\n	dashboard.id,\n	dashboard.version,\n	dashboard.version,\n	dashboard.version,\n	dashboard.updated,\n	COALESCE(dashboard.updated_by, -1),\n	'''',\n	dashboard.data\nFROM dashboard;','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(243,'alter dashboard_version.data to mediumtext v1','SELECT 0;',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(244,'create team table',replace('CREATE TABLE IF NOT EXISTS `team` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `name` TEXT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(245,'add index team.org_id','CREATE INDEX `IDX_team_org_id` ON `team` (`org_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(246,'add unique index team_org_id_name','CREATE UNIQUE INDEX `UQE_team_org_id_name` ON `team` (`org_id`,`name`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(247,'create team member table',replace('CREATE TABLE IF NOT EXISTS `team_member` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `team_id` INTEGER NOT NULL\n, `user_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(248,'add index team_member.org_id','CREATE INDEX `IDX_team_member_org_id` ON `team_member` (`org_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(249,'add unique index team_member_org_id_team_id_user_id','CREATE UNIQUE INDEX `UQE_team_member_org_id_team_id_user_id` ON `team_member` (`org_id`,`team_id`,`user_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(250,'add index team_member.team_id','CREATE INDEX `IDX_team_member_team_id` ON `team_member` (`team_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(251,'Add column email to team table','alter table `team` ADD COLUMN `email` TEXT NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(252,'Add column external to team_member table','alter table `team_member` ADD COLUMN `external` INTEGER NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(253,'Add column permission to team_member table','alter table `team_member` ADD COLUMN `permission` INTEGER NULL ',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(254,'create dashboard acl table',replace('CREATE TABLE IF NOT EXISTS `dashboard_acl` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `dashboard_id` INTEGER NOT NULL\n, `user_id` INTEGER NULL\n, `team_id` INTEGER NULL\n, `permission` INTEGER NOT NULL DEFAULT 4\n, `role` TEXT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(255,'add index dashboard_acl_dashboard_id','CREATE INDEX `IDX_dashboard_acl_dashboard_id` ON `dashboard_acl` (`dashboard_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(256,'add unique index dashboard_acl_dashboard_id_user_id','CREATE UNIQUE INDEX `UQE_dashboard_acl_dashboard_id_user_id` ON `dashboard_acl` (`dashboard_id`,`user_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(257,'add unique index dashboard_acl_dashboard_id_team_id','CREATE UNIQUE INDEX `UQE_dashboard_acl_dashboard_id_team_id` ON `dashboard_acl` (`dashboard_id`,`team_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(258,'add index dashboard_acl_user_id','CREATE INDEX `IDX_dashboard_acl_user_id` ON `dashboard_acl` (`user_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(259,'add index dashboard_acl_team_id','CREATE INDEX `IDX_dashboard_acl_team_id` ON `dashboard_acl` (`team_id`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(260,'add index dashboard_acl_org_id_role','CREATE INDEX `IDX_dashboard_acl_org_id_role` ON `dashboard_acl` (`org_id`,`role`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(261,'add index dashboard_permission','CREATE INDEX `IDX_dashboard_acl_permission` ON `dashboard_acl` (`permission`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(262,'save default acl rules in dashboard_acl table',replace('\nINSERT INTO dashboard_acl\n	(\n		org_id,\n		dashboard_id,\n		permission,\n		role,\n		created,\n		updated\n	)\n	VALUES\n		(-1,-1, 1,''Viewer'',''2017-06-20'',''2017-06-20''),\n		(-1,-1, 2,''Editor'',''2017-06-20'',''2017-06-20'')\n	','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(263,'delete acl rules for deleted dashboards and folders','DELETE FROM dashboard_acl WHERE dashboard_id NOT IN (SELECT id FROM dashboard) AND dashboard_id != -1',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(264,'create tag table',replace('CREATE TABLE IF NOT EXISTS `tag` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `key` TEXT NOT NULL\n, `value` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(265,'add index tag.key_value','CREATE UNIQUE INDEX `UQE_tag_key_value` ON `tag` (`key`,`value`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(266,'create login attempt table',replace('CREATE TABLE IF NOT EXISTS `login_attempt` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `username` TEXT NOT NULL\n, `ip_address` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(267,'add index login_attempt.username','CREATE INDEX `IDX_login_attempt_username` ON `login_attempt` (`username`);',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(268,'drop index IDX_login_attempt_username - v1','DROP INDEX `IDX_login_attempt_username`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(269,'Rename table login_attempt to login_attempt_tmp_qwerty - v1','ALTER TABLE `login_attempt` RENAME TO `login_attempt_tmp_qwerty`',1,'','2022-05-17 11:51:40');
INSERT INTO migration_log VALUES(270,'create login_attempt v2',replace('CREATE TABLE IF NOT EXISTS `login_attempt` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `username` TEXT NOT NULL\n, `ip_address` TEXT NOT NULL\n, `created` INTEGER NOT NULL DEFAULT 0\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(271,'create index IDX_login_attempt_username - v2','CREATE INDEX `IDX_login_attempt_username` ON `login_attempt` (`username`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(272,'copy login_attempt v1 to v2',replace('INSERT INTO `login_attempt` (`id`\n, `username`\n, `ip_address`) SELECT `id`\n, `username`\n, `ip_address` FROM `login_attempt_tmp_qwerty`','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(273,'drop login_attempt_tmp_qwerty','DROP TABLE IF EXISTS `login_attempt_tmp_qwerty`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(274,'create user auth table',replace('CREATE TABLE IF NOT EXISTS `user_auth` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `user_id` INTEGER NOT NULL\n, `auth_module` TEXT NOT NULL\n, `auth_id` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(275,'create index IDX_user_auth_auth_module_auth_id - v1','CREATE INDEX `IDX_user_auth_auth_module_auth_id` ON `user_auth` (`auth_module`,`auth_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(276,'alter user_auth.auth_id to length 190','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(277,'Add OAuth access token to user_auth','alter table `user_auth` ADD COLUMN `o_auth_access_token` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(278,'Add OAuth refresh token to user_auth','alter table `user_auth` ADD COLUMN `o_auth_refresh_token` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(279,'Add OAuth token type to user_auth','alter table `user_auth` ADD COLUMN `o_auth_token_type` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(280,'Add OAuth expiry to user_auth','alter table `user_auth` ADD COLUMN `o_auth_expiry` DATETIME NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(281,'Add index to user_id column in user_auth','CREATE INDEX `IDX_user_auth_user_id` ON `user_auth` (`user_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(282,'Add OAuth ID token to user_auth','alter table `user_auth` ADD COLUMN `o_auth_id_token` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(283,'create server_lock table',replace('CREATE TABLE IF NOT EXISTS `server_lock` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `operation_uid` TEXT NOT NULL\n, `version` INTEGER NOT NULL\n, `last_execution` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(284,'add index server_lock.operation_uid','CREATE UNIQUE INDEX `UQE_server_lock_operation_uid` ON `server_lock` (`operation_uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(285,'create user auth token table',replace('CREATE TABLE IF NOT EXISTS `user_auth_token` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `user_id` INTEGER NOT NULL\n, `auth_token` TEXT NOT NULL\n, `prev_auth_token` TEXT NOT NULL\n, `user_agent` TEXT NOT NULL\n, `client_ip` TEXT NOT NULL\n, `auth_token_seen` INTEGER NOT NULL\n, `seen_at` INTEGER NULL\n, `rotated_at` INTEGER NOT NULL\n, `created_at` INTEGER NOT NULL\n, `updated_at` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(286,'add unique index user_auth_token.auth_token','CREATE UNIQUE INDEX `UQE_user_auth_token_auth_token` ON `user_auth_token` (`auth_token`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(287,'add unique index user_auth_token.prev_auth_token','CREATE UNIQUE INDEX `UQE_user_auth_token_prev_auth_token` ON `user_auth_token` (`prev_auth_token`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(288,'add index user_auth_token.user_id','CREATE INDEX `IDX_user_auth_token_user_id` ON `user_auth_token` (`user_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(289,'Add revoked_at to the user auth token','alter table `user_auth_token` ADD COLUMN `revoked_at` INTEGER NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(290,'create cache_data table',replace('CREATE TABLE IF NOT EXISTS `cache_data` (\n`cache_key` TEXT PRIMARY KEY NOT NULL\n, `data` BLOB NOT NULL\n, `expires` INTEGER NOT NULL\n, `created_at` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(291,'add unique index cache_data.cache_key','CREATE UNIQUE INDEX `UQE_cache_data_cache_key` ON `cache_data` (`cache_key`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(292,'create short_url table v1',replace('CREATE TABLE IF NOT EXISTS `short_url` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `uid` TEXT NOT NULL\n, `path` TEXT NOT NULL\n, `created_by` INTEGER NOT NULL\n, `created_at` INTEGER NOT NULL\n, `last_seen_at` INTEGER NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(293,'add index short_url.org_id-uid','CREATE UNIQUE INDEX `UQE_short_url_org_id_uid` ON `short_url` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(294,'delete alert_definition table','DROP TABLE IF EXISTS `alert_definition`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(295,'recreate alert_definition table',replace('CREATE TABLE IF NOT EXISTS `alert_definition` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `title` TEXT NOT NULL\n, `condition` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `updated` DATETIME NOT NULL\n, `interval_seconds` INTEGER NOT NULL DEFAULT 60\n, `version` INTEGER NOT NULL DEFAULT 0\n, `uid` TEXT NOT NULL DEFAULT 0\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(296,'add index in alert_definition on org_id and title columns','CREATE INDEX `IDX_alert_definition_org_id_title` ON `alert_definition` (`org_id`,`title`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(297,'add index in alert_definition on org_id and uid columns','CREATE INDEX `IDX_alert_definition_org_id_uid` ON `alert_definition` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(298,'alter alert_definition table data column to mediumtext in mysql','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(299,'drop index in alert_definition on org_id and title columns','DROP INDEX `IDX_alert_definition_org_id_title`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(300,'drop index in alert_definition on org_id and uid columns','DROP INDEX `IDX_alert_definition_org_id_uid`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(301,'add unique index in alert_definition on org_id and title columns','CREATE UNIQUE INDEX `UQE_alert_definition_org_id_title` ON `alert_definition` (`org_id`,`title`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(302,'add unique index in alert_definition on org_id and uid columns','CREATE UNIQUE INDEX `UQE_alert_definition_org_id_uid` ON `alert_definition` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(303,'Add column paused in alert_definition','alter table `alert_definition` ADD COLUMN `paused` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(304,'drop alert_definition table','DROP TABLE IF EXISTS `alert_definition`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(305,'delete alert_definition_version table','DROP TABLE IF EXISTS `alert_definition_version`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(306,'recreate alert_definition_version table',replace('CREATE TABLE IF NOT EXISTS `alert_definition_version` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `alert_definition_id` INTEGER NOT NULL\n, `alert_definition_uid` TEXT NOT NULL DEFAULT 0\n, `parent_version` INTEGER NOT NULL\n, `restored_from` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `title` TEXT NOT NULL\n, `condition` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `interval_seconds` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(307,'add index in alert_definition_version table on alert_definition_id and version columns','CREATE UNIQUE INDEX `UQE_alert_definition_version_alert_definition_id_version` ON `alert_definition_version` (`alert_definition_id`,`version`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(308,'add index in alert_definition_version table on alert_definition_uid and version columns','CREATE UNIQUE INDEX `UQE_alert_definition_version_alert_definition_uid_version` ON `alert_definition_version` (`alert_definition_uid`,`version`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(309,'alter alert_definition_version table data column to mediumtext in mysql','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(310,'drop alert_definition_version table','DROP TABLE IF EXISTS `alert_definition_version`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(311,'create alert_instance table',replace('CREATE TABLE IF NOT EXISTS `alert_instance` (\n`def_org_id` INTEGER NOT NULL\n, `def_uid` TEXT NOT NULL DEFAULT 0\n, `labels` TEXT NOT NULL\n, `labels_hash` TEXT NOT NULL\n, `current_state` TEXT NOT NULL\n, `current_state_since` INTEGER NOT NULL\n, `last_eval_time` INTEGER NOT NULL\n, PRIMARY KEY ( `def_org_id`,`def_uid`,`labels_hash` ));','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(312,'add index in alert_instance table on def_org_id, def_uid and current_state columns','CREATE INDEX `IDX_alert_instance_def_org_id_def_uid_current_state` ON `alert_instance` (`def_org_id`,`def_uid`,`current_state`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(313,'add index in alert_instance table on def_org_id, current_state columns','CREATE INDEX `IDX_alert_instance_def_org_id_current_state` ON `alert_instance` (`def_org_id`,`current_state`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(314,'add column current_state_end to alert_instance','alter table `alert_instance` ADD COLUMN `current_state_end` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(315,'remove index def_org_id, def_uid, current_state on alert_instance','DROP INDEX `IDX_alert_instance_def_org_id_def_uid_current_state`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(316,'remove index def_org_id, current_state on alert_instance','DROP INDEX `IDX_alert_instance_def_org_id_current_state`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(317,'rename def_org_id to rule_org_id in alert_instance','ALTER TABLE alert_instance RENAME COLUMN def_org_id TO rule_org_id;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(318,'rename def_uid to rule_uid in alert_instance','ALTER TABLE alert_instance RENAME COLUMN def_uid TO rule_uid;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(319,'add index rule_org_id, rule_uid, current_state on alert_instance','CREATE INDEX `IDX_alert_instance_rule_org_id_rule_uid_current_state` ON `alert_instance` (`rule_org_id`,`rule_uid`,`current_state`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(320,'add index rule_org_id, current_state on alert_instance','CREATE INDEX `IDX_alert_instance_rule_org_id_current_state` ON `alert_instance` (`rule_org_id`,`current_state`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(321,'create alert_rule table',replace('CREATE TABLE IF NOT EXISTS `alert_rule` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `title` TEXT NOT NULL\n, `condition` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `updated` DATETIME NOT NULL\n, `interval_seconds` INTEGER NOT NULL DEFAULT 60\n, `version` INTEGER NOT NULL DEFAULT 0\n, `uid` TEXT NOT NULL DEFAULT 0\n, `namespace_uid` TEXT NOT NULL\n, `rule_group` TEXT NOT NULL\n, `no_data_state` TEXT NOT NULL DEFAULT ''NoData''\n, `exec_err_state` TEXT NOT NULL DEFAULT ''Alerting''\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(322,'add index in alert_rule on org_id and title columns','CREATE UNIQUE INDEX `UQE_alert_rule_org_id_title` ON `alert_rule` (`org_id`,`title`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(323,'add index in alert_rule on org_id and uid columns','CREATE UNIQUE INDEX `UQE_alert_rule_org_id_uid` ON `alert_rule` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(324,'add index in alert_rule on org_id, namespace_uid, group_uid columns','CREATE INDEX `IDX_alert_rule_org_id_namespace_uid_rule_group` ON `alert_rule` (`org_id`,`namespace_uid`,`rule_group`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(325,'alter alert_rule table data column to mediumtext in mysql','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(326,'add column for to alert_rule','alter table `alert_rule` ADD COLUMN `for` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(327,'add column annotations to alert_rule','alter table `alert_rule` ADD COLUMN `annotations` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(328,'add column labels to alert_rule','alter table `alert_rule` ADD COLUMN `labels` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(329,'remove unique index from alert_rule on org_id, title columns','DROP INDEX `UQE_alert_rule_org_id_title`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(330,'add index in alert_rule on org_id, namespase_uid and title columns','CREATE UNIQUE INDEX `UQE_alert_rule_org_id_namespace_uid_title` ON `alert_rule` (`org_id`,`namespace_uid`,`title`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(331,'add dashboard_uid column to alert_rule','alter table `alert_rule` ADD COLUMN `dashboard_uid` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(332,'add panel_id column to alert_rule','alter table `alert_rule` ADD COLUMN `panel_id` INTEGER NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(333,'add index in alert_rule on org_id, dashboard_uid and panel_id columns','CREATE INDEX `IDX_alert_rule_org_id_dashboard_uid_panel_id` ON `alert_rule` (`org_id`,`dashboard_uid`,`panel_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(334,'create alert_rule_version table',replace('CREATE TABLE IF NOT EXISTS `alert_rule_version` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `rule_org_id` INTEGER NOT NULL\n, `rule_uid` TEXT NOT NULL DEFAULT 0\n, `rule_namespace_uid` TEXT NOT NULL\n, `rule_group` TEXT NOT NULL\n, `parent_version` INTEGER NOT NULL\n, `restored_from` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `title` TEXT NOT NULL\n, `condition` TEXT NOT NULL\n, `data` TEXT NOT NULL\n, `interval_seconds` INTEGER NOT NULL\n, `no_data_state` TEXT NOT NULL DEFAULT ''NoData''\n, `exec_err_state` TEXT NOT NULL DEFAULT ''Alerting''\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(335,'add index in alert_rule_version table on rule_org_id, rule_uid and version columns','CREATE UNIQUE INDEX `UQE_alert_rule_version_rule_org_id_rule_uid_version` ON `alert_rule_version` (`rule_org_id`,`rule_uid`,`version`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(336,'add index in alert_rule_version table on rule_org_id, rule_namespace_uid and rule_group columns','CREATE INDEX `IDX_alert_rule_version_rule_org_id_rule_namespace_uid_rule_group` ON `alert_rule_version` (`rule_org_id`,`rule_namespace_uid`,`rule_group`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(337,'alter alert_rule_version table data column to mediumtext in mysql','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(338,'add column for to alert_rule_version','alter table `alert_rule_version` ADD COLUMN `for` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(339,'add column annotations to alert_rule_version','alter table `alert_rule_version` ADD COLUMN `annotations` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(340,'add column labels to alert_rule_version','alter table `alert_rule_version` ADD COLUMN `labels` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(341,'create_alert_configuration_table',replace('CREATE TABLE IF NOT EXISTS `alert_configuration` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `alertmanager_configuration` TEXT NOT NULL\n, `configuration_version` TEXT NOT NULL\n, `created_at` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(342,'Add column default in alert_configuration','alter table `alert_configuration` ADD COLUMN `default` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(343,'alert alert_configuration alertmanager_configuration column from TEXT to MEDIUMTEXT if mysql','SELECT 0;',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(344,'add column org_id in alert_configuration','alter table `alert_configuration` ADD COLUMN `org_id` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(345,'add index in alert_configuration table on org_id column','CREATE INDEX `IDX_alert_configuration_org_id` ON `alert_configuration` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(346,'add configuration_hash column to alert_configuration','alter table `alert_configuration` ADD COLUMN `configuration_hash` TEXT NOT NULL DEFAULT ''not-yet-calculated'' ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(347,'create_ngalert_configuration_table',replace('CREATE TABLE IF NOT EXISTS `ngalert_configuration` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `alertmanagers` TEXT NULL\n, `created_at` INTEGER NOT NULL\n, `updated_at` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(348,'add index in ngalert_configuration on org_id column','CREATE UNIQUE INDEX `UQE_ngalert_configuration_org_id` ON `ngalert_configuration` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(349,'add column send_alerts_to in ngalert_configuration','alter table `ngalert_configuration` ADD COLUMN `send_alerts_to` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(350,'create provenance_type table',replace('CREATE TABLE IF NOT EXISTS `provenance_type` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `record_key` TEXT NOT NULL\n, `record_type` TEXT NOT NULL\n, `provenance` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(351,'add index to uniquify (record_key, record_type, org_id) columns','CREATE UNIQUE INDEX `UQE_provenance_type_record_type_record_key_org_id` ON `provenance_type` (`record_type`,`record_key`,`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(352,'move dashboard alerts to unified alerting','code migration',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(353,'create library_element table v1',replace('CREATE TABLE IF NOT EXISTS `library_element` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `folder_id` INTEGER NOT NULL\n, `uid` TEXT NOT NULL\n, `name` TEXT NOT NULL\n, `kind` INTEGER NOT NULL\n, `type` TEXT NOT NULL\n, `description` TEXT NOT NULL\n, `model` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `created_by` INTEGER NOT NULL\n, `updated` DATETIME NOT NULL\n, `updated_by` INTEGER NOT NULL\n, `version` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(354,'add index library_element org_id-folder_id-name-kind','CREATE UNIQUE INDEX `UQE_library_element_org_id_folder_id_name_kind` ON `library_element` (`org_id`,`folder_id`,`name`,`kind`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(355,'create library_element_connection table v1',replace('CREATE TABLE IF NOT EXISTS `library_element_connection` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `element_id` INTEGER NOT NULL\n, `kind` INTEGER NOT NULL\n, `connection_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `created_by` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(356,'add index library_element_connection element_id-kind-connection_id','CREATE UNIQUE INDEX `UQE_library_element_connection_element_id_kind_connection_id` ON `library_element_connection` (`element_id`,`kind`,`connection_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(357,'add unique index library_element org_id_uid','CREATE UNIQUE INDEX `UQE_library_element_org_id_uid` ON `library_element` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(358,'increase max description length to 2048','-- NOT REQUIRED',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(359,'clone move dashboard alerts to unified alerting','code migration',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(360,'create data_keys table',replace('CREATE TABLE IF NOT EXISTS `data_keys` (\n`name` TEXT PRIMARY KEY NOT NULL\n, `active` INTEGER NOT NULL\n, `scope` TEXT NOT NULL\n, `provider` TEXT NOT NULL\n, `encrypted_data` BLOB NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(361,'create kv_store table v1',replace('CREATE TABLE IF NOT EXISTS `kv_store` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `namespace` TEXT NOT NULL\n, `key` TEXT NOT NULL\n, `value` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(362,'add index kv_store.org_id-namespace-key','CREATE UNIQUE INDEX `UQE_kv_store_org_id_namespace_key` ON `kv_store` (`org_id`,`namespace`,`key`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(363,'update dashboard_uid and panel_id from existing annotations','set dashboard_uid and panel_id migration',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(364,'create permission table',replace('CREATE TABLE IF NOT EXISTS `permission` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `role_id` INTEGER NOT NULL\n, `action` TEXT NOT NULL\n, `scope` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(365,'add unique index permission.role_id','CREATE INDEX `IDX_permission_role_id` ON `permission` (`role_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(366,'add unique index role_id_action_scope','CREATE UNIQUE INDEX `UQE_permission_role_id_action_scope` ON `permission` (`role_id`,`action`,`scope`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(367,'create role table',replace('CREATE TABLE IF NOT EXISTS `role` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `name` TEXT NOT NULL\n, `description` TEXT NULL\n, `version` INTEGER NOT NULL\n, `org_id` INTEGER NOT NULL\n, `uid` TEXT NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(368,'add column display_name','alter table `role` ADD COLUMN `display_name` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(369,'add column group_name','alter table `role` ADD COLUMN `group_name` TEXT NULL ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(370,'add index role.org_id','CREATE INDEX `IDX_role_org_id` ON `role` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(371,'add unique index role_org_id_name','CREATE UNIQUE INDEX `UQE_role_org_id_name` ON `role` (`org_id`,`name`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(372,'add index role_org_id_uid','CREATE UNIQUE INDEX `UQE_role_org_id_uid` ON `role` (`org_id`,`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(373,'create team role table',replace('CREATE TABLE IF NOT EXISTS `team_role` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `team_id` INTEGER NOT NULL\n, `role_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(374,'add index team_role.org_id','CREATE INDEX `IDX_team_role_org_id` ON `team_role` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(375,'add unique index team_role_org_id_team_id_role_id','CREATE UNIQUE INDEX `UQE_team_role_org_id_team_id_role_id` ON `team_role` (`org_id`,`team_id`,`role_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(376,'add index team_role.team_id','CREATE INDEX `IDX_team_role_team_id` ON `team_role` (`team_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(377,'create user role table',replace('CREATE TABLE IF NOT EXISTS `user_role` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `user_id` INTEGER NOT NULL\n, `role_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(378,'add index user_role.org_id','CREATE INDEX `IDX_user_role_org_id` ON `user_role` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(379,'add unique index user_role_org_id_user_id_role_id','CREATE UNIQUE INDEX `UQE_user_role_org_id_user_id_role_id` ON `user_role` (`org_id`,`user_id`,`role_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(380,'add index user_role.user_id','CREATE INDEX `IDX_user_role_user_id` ON `user_role` (`user_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(381,'create builtin role table',replace('CREATE TABLE IF NOT EXISTS `builtin_role` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `role` TEXT NOT NULL\n, `role_id` INTEGER NOT NULL\n, `created` DATETIME NOT NULL\n, `updated` DATETIME NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(382,'add index builtin_role.role_id','CREATE INDEX `IDX_builtin_role_role_id` ON `builtin_role` (`role_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(383,'add index builtin_role.name','CREATE INDEX `IDX_builtin_role_role` ON `builtin_role` (`role`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(384,'Add column org_id to builtin_role table','alter table `builtin_role` ADD COLUMN `org_id` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(385,'add index builtin_role.org_id','CREATE INDEX `IDX_builtin_role_org_id` ON `builtin_role` (`org_id`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(386,'add unique index builtin_role_org_id_role_id_role','CREATE UNIQUE INDEX `UQE_builtin_role_org_id_role_id_role` ON `builtin_role` (`org_id`,`role_id`,`role`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(387,'Remove unique index role_org_id_uid','DROP INDEX `UQE_role_org_id_uid`',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(388,'add unique index role.uid','CREATE UNIQUE INDEX `UQE_role_uid` ON `role` (`uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(389,'create seed assignment table',replace('CREATE TABLE IF NOT EXISTS `seed_assignment` (\n`builtin_role` TEXT NOT NULL\n, `role_name` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(390,'add unique index builtin_role_role_name','CREATE UNIQUE INDEX `UQE_seed_assignment_builtin_role_role_name` ON `seed_assignment` (`builtin_role`,`role_name`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(391,'add column hidden to role table','alter table `role` ADD COLUMN `hidden` INTEGER NOT NULL DEFAULT 0 ',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(392,'create query_history table v1',replace('CREATE TABLE IF NOT EXISTS `query_history` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `uid` TEXT NOT NULL\n, `org_id` INTEGER NOT NULL\n, `datasource_uid` TEXT NOT NULL\n, `created_by` INTEGER NOT NULL\n, `created_at` INTEGER NOT NULL\n, `comment` TEXT NOT NULL\n, `queries` TEXT NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(393,'add index query_history.org_id-created_by-datasource_uid','CREATE INDEX `IDX_query_history_org_id_created_by_datasource_uid` ON `query_history` (`org_id`,`created_by`,`datasource_uid`);',1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(394,'create query_history_star table v1',replace('CREATE TABLE IF NOT EXISTS `query_history_star` (\n`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\n, `query_uid` TEXT NOT NULL\n, `user_id` INTEGER NOT NULL\n);','\n',char(10)),1,'','2022-05-17 11:51:41');
INSERT INTO migration_log VALUES(395,'add index query_history.user_id-query_uid','CREATE UNIQUE INDEX `UQE_query_history_star_user_id_query_uid` ON `query_history_star` (`user_id`,`query_uid`);',1,'','2022-05-17 11:51:41');
CREATE TABLE `user` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `version` INTEGER NOT NULL
, `login` TEXT NOT NULL
, `email` TEXT NOT NULL
, `name` TEXT NULL
, `password` TEXT NULL
, `salt` TEXT NULL
, `rands` TEXT NULL
, `company` TEXT NULL
, `org_id` INTEGER NOT NULL
, `is_admin` INTEGER NOT NULL
, `email_verified` INTEGER NULL
, `theme` TEXT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `help_flags1` INTEGER NOT NULL DEFAULT 0, `last_seen_at` DATETIME NULL, `is_disabled` INTEGER NOT NULL DEFAULT 0, is_service_account BOOLEAN DEFAULT 0);
INSERT INTO user VALUES(1,0,'admin','admin@localhost','','f9ffe6a74f9bad2469683eb29be1405f547794b3848cdd22955b9e2a0ea21d073d5edd2de7fee0e42757bcd0a7608f1af08f','pZLmZk4dI6','x88N1uHieo','',1,1,0,'','2022-05-17 11:51:41','2022-05-17 11:51:41',0,'2012-05-17 11:51:41',0,0);
CREATE TABLE `temp_user` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `version` INTEGER NOT NULL
, `email` TEXT NOT NULL
, `name` TEXT NULL
, `role` TEXT NULL
, `code` TEXT NOT NULL
, `status` TEXT NOT NULL
, `invited_by_user_id` INTEGER NULL
, `email_sent` INTEGER NOT NULL
, `email_sent_on` DATETIME NULL
, `remote_addr` TEXT NULL
, `created` INTEGER NOT NULL DEFAULT 0
, `updated` INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE `star` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `user_id` INTEGER NOT NULL
, `dashboard_id` INTEGER NOT NULL
);
CREATE TABLE `org` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `version` INTEGER NOT NULL
, `name` TEXT NOT NULL
, `address1` TEXT NULL
, `address2` TEXT NULL
, `city` TEXT NULL
, `state` TEXT NULL
, `zip_code` TEXT NULL
, `country` TEXT NULL
, `billing_email` TEXT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
INSERT INTO org VALUES(1,0,'Main Org.','','','','','','',NULL,'2022-05-17 11:51:41','2022-05-17 11:51:41');
CREATE TABLE `org_user` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `user_id` INTEGER NOT NULL
, `role` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
INSERT INTO org_user VALUES(1,1,1,'Admin','2022-05-17 11:51:41','2022-05-17 11:51:41');
CREATE TABLE `dashboard_tag` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `dashboard_id` INTEGER NOT NULL
, `term` TEXT NOT NULL
);
CREATE TABLE `dashboard` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `version` INTEGER NOT NULL
, `slug` TEXT NOT NULL
, `title` TEXT NOT NULL
, `data` TEXT NOT NULL
, `org_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `updated_by` INTEGER NULL, `created_by` INTEGER NULL, `gnet_id` INTEGER NULL, `plugin_id` TEXT NULL, `folder_id` INTEGER NOT NULL DEFAULT 0, `is_folder` INTEGER NOT NULL DEFAULT 0, `has_acl` INTEGER NOT NULL DEFAULT 0, `uid` TEXT NULL);
INSERT INTO dashboard VALUES(1,1,'accessbot-metrics','AccessBot Metrics','{"annotations":{"list":[{"builtIn":1,"datasource":{"type":"grafana","uid":"-- Grafana --"},"enable":true,"hide":true,"iconColor":"rgba(0, 211, 255, 1)","name":"Annotations \u0026 Alerts","target":{"limit":100,"matchAny":false,"tags":[],"type":"dashboard"},"type":"dashboard"}]},"editable":true,"fiscalYearStartMonth":0,"graphTooltip":0,"hideControls":false,"id":null,"links":[],"liveNow":false,"panels":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":0},"id":2,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_received_messages[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Received Messages Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":0},"id":3,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"builder","expr":"changes(accessbot_total_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":0},"id":4,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_pending_access_requests","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Pending Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":8},"id":6,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_manual_approves[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Manually Approved Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":8},"id":8,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_auto_approves[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Auto Approved Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":8},"id":7,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_denied_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Manually Denied Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":16},"id":5,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_timed_out_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Timed Out Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":16},"id":9,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_consecutive_errors","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Total Consecutive Errors Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"thresholds"},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":16},"id":10,"options":{"orientation":"auto","reduceOptions":{"calcs":["lastNotNull"],"fields":"","values":false},"showThresholdLabels":false,"showThresholdMarkers":true},"pluginVersion":"8.5.1","targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_consecutive_errors \u003e bool 0","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Last Execution Status","type":"gauge"}],"refresh":"5s","schemaVersion":36,"style":"dark","tags":[],"templating":{"list":[]},"time":{"from":"now-15m","to":"now"},"timepicker":{},"timezone":"","title":"AccessBot Metrics","uid":"982GyKX7z","version":1,"weekStart":""}',1,'2022-05-17 12:11:23','2022-05-17 12:11:23',-1,-1,0,'',0,0,0,'982GyKX7z');
CREATE TABLE `dashboard_provisioning` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `dashboard_id` INTEGER NULL
, `name` TEXT NOT NULL
, `external_id` TEXT NOT NULL
, `updated` INTEGER NOT NULL DEFAULT 0
, `check_sum` TEXT NULL);
CREATE TABLE `data_source` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `version` INTEGER NOT NULL
, `type` TEXT NOT NULL
, `name` TEXT NOT NULL
, `access` TEXT NOT NULL
, `url` TEXT NOT NULL
, `password` TEXT NULL
, `user` TEXT NULL
, `database` TEXT NULL
, `basic_auth` INTEGER NOT NULL
, `basic_auth_user` TEXT NULL
, `basic_auth_password` TEXT NULL
, `is_default` INTEGER NOT NULL
, `json_data` TEXT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `with_credentials` INTEGER NOT NULL DEFAULT 0, `secure_json_data` TEXT NULL, `read_only` INTEGER NULL, `uid` TEXT NOT NULL DEFAULT 0);
INSERT INTO data_source VALUES(1,1,2,'prometheus','Prometheus','proxy','http://prometheus:9090','','','',0,'','',1,X'7b22687474704d6574686f64223a22504f5354227d','2022-05-17 11:51:54','2022-05-17 11:52:07',0,'{}',0,'VAwRPKXnk');
CREATE TABLE `api_key` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `name` TEXT NOT NULL
, `key` TEXT NOT NULL
, `role` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `expires` INTEGER NULL, `service_account_id` INTEGER NULL);
CREATE TABLE `dashboard_snapshot` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `name` TEXT NOT NULL
, `key` TEXT NOT NULL
, `delete_key` TEXT NOT NULL
, `org_id` INTEGER NOT NULL
, `user_id` INTEGER NOT NULL
, `external` INTEGER NOT NULL
, `external_url` TEXT NOT NULL
, `dashboard` TEXT NOT NULL
, `expires` DATETIME NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `external_delete_url` TEXT NULL, `dashboard_encrypted` BLOB NULL);
CREATE TABLE `quota` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NULL
, `user_id` INTEGER NULL
, `target` TEXT NOT NULL
, `limit` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
CREATE TABLE `plugin_setting` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NULL
, `plugin_id` TEXT NOT NULL
, `enabled` INTEGER NOT NULL
, `pinned` INTEGER NOT NULL
, `json_data` TEXT NULL
, `secure_json_data` TEXT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `plugin_version` TEXT NULL);
CREATE TABLE `session` (
`key` TEXT PRIMARY KEY NOT NULL
, `data` BLOB NOT NULL
, `expiry` INTEGER NOT NULL
);
CREATE TABLE `playlist` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `name` TEXT NOT NULL
, `interval` TEXT NOT NULL
, `org_id` INTEGER NOT NULL
);
CREATE TABLE `playlist_item` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `playlist_id` INTEGER NOT NULL
, `type` TEXT NOT NULL
, `value` TEXT NOT NULL
, `title` TEXT NOT NULL
, `order` INTEGER NOT NULL
);
CREATE TABLE `preferences` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `user_id` INTEGER NOT NULL
, `version` INTEGER NOT NULL
, `home_dashboard_id` INTEGER NOT NULL
, `timezone` TEXT NOT NULL
, `theme` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `team_id` INTEGER NULL, `week_start` TEXT NULL, `json_data` TEXT NULL);
CREATE TABLE `alert` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `version` INTEGER NOT NULL
, `dashboard_id` INTEGER NOT NULL
, `panel_id` INTEGER NOT NULL
, `org_id` INTEGER NOT NULL
, `name` TEXT NOT NULL
, `message` TEXT NOT NULL
, `state` TEXT NOT NULL
, `settings` TEXT NOT NULL
, `frequency` INTEGER NOT NULL
, `handler` INTEGER NOT NULL
, `severity` TEXT NOT NULL
, `silenced` INTEGER NOT NULL
, `execution_error` TEXT NOT NULL
, `eval_data` TEXT NULL
, `eval_date` DATETIME NULL
, `new_state_date` DATETIME NOT NULL
, `state_changes` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `for` INTEGER NULL);
CREATE TABLE `alert_rule_tag` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `alert_id` INTEGER NOT NULL
, `tag_id` INTEGER NOT NULL
);
CREATE TABLE `alert_notification` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `name` TEXT NOT NULL
, `type` TEXT NOT NULL
, `settings` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `is_default` INTEGER NOT NULL DEFAULT 0, `frequency` INTEGER NULL, `send_reminder` INTEGER NULL DEFAULT 0, `disable_resolve_message` INTEGER NOT NULL DEFAULT 0, `uid` TEXT NULL, `secure_settings` TEXT NULL);
CREATE TABLE `alert_notification_state` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `alert_id` INTEGER NOT NULL
, `notifier_id` INTEGER NOT NULL
, `state` TEXT NOT NULL
, `version` INTEGER NOT NULL
, `updated_at` INTEGER NOT NULL
, `alert_rule_state_updated_version` INTEGER NOT NULL
);
CREATE TABLE `annotation` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `alert_id` INTEGER NULL
, `user_id` INTEGER NULL
, `dashboard_id` INTEGER NULL
, `panel_id` INTEGER NULL
, `category_id` INTEGER NULL
, `type` TEXT NOT NULL
, `title` TEXT NOT NULL
, `text` TEXT NOT NULL
, `metric` TEXT NULL
, `prev_state` TEXT NOT NULL
, `new_state` TEXT NOT NULL
, `data` TEXT NOT NULL
, `epoch` INTEGER NOT NULL
, `region_id` INTEGER NULL DEFAULT 0, `tags` TEXT NULL, `created` INTEGER NULL DEFAULT 0, `updated` INTEGER NULL DEFAULT 0, `epoch_end` INTEGER NOT NULL DEFAULT 0);
CREATE TABLE `annotation_tag` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `annotation_id` INTEGER NOT NULL
, `tag_id` INTEGER NOT NULL
);
CREATE TABLE `test_data` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `metric1` TEXT NULL
, `metric2` TEXT NULL
, `value_big_int` INTEGER NULL
, `value_double` REAL NULL
, `value_float` REAL NULL
, `value_int` INTEGER NULL
, `time_epoch` INTEGER NOT NULL
, `time_date_time` DATETIME NOT NULL
, `time_time_stamp` DATETIME NOT NULL
);
CREATE TABLE `dashboard_version` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `dashboard_id` INTEGER NOT NULL
, `parent_version` INTEGER NOT NULL
, `restored_from` INTEGER NOT NULL
, `version` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `created_by` INTEGER NOT NULL
, `message` TEXT NOT NULL
, `data` TEXT NOT NULL
);
INSERT INTO dashboard_version VALUES(1,1,0,0,1,'2022-05-17 12:11:23',-1,'','{"annotations":{"list":[{"builtIn":1,"datasource":{"type":"grafana","uid":"-- Grafana --"},"enable":true,"hide":true,"iconColor":"rgba(0, 211, 255, 1)","name":"Annotations \u0026 Alerts","target":{"limit":100,"matchAny":false,"tags":[],"type":"dashboard"},"type":"dashboard"}]},"editable":true,"fiscalYearStartMonth":0,"graphTooltip":0,"hideControls":false,"id":null,"links":[],"liveNow":false,"panels":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":0},"id":2,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_received_messages[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Received Messages Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":0},"id":3,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"builder","expr":"changes(accessbot_total_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":0},"id":4,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_pending_access_requests","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Pending Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":8},"id":6,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_manual_approves[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Manually Approved Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":8},"id":8,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_auto_approves[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Auto Approved Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":8},"id":7,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_denied_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Manually Denied Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":0,"y":16},"id":5,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"changes(accessbot_total_timed_out_access_requests[5m])","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Timed Out Access Requests Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"palette-classic"},"custom":{"axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":0,"gradientMode":"none","hideFrom":{"legend":false,"tooltip":false,"viz":false},"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"auto","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":8,"y":16},"id":9,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom"},"tooltip":{"mode":"single","sort":"none"}},"targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_consecutive_errors","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Total Consecutive Errors Count","type":"timeseries"},{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"fieldConfig":{"defaults":{"color":{"mode":"thresholds"},"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"red","value":80}]}},"overrides":[]},"gridPos":{"h":8,"w":8,"x":16,"y":16},"id":10,"options":{"orientation":"auto","reduceOptions":{"calcs":["lastNotNull"],"fields":"","values":false},"showThresholdLabels":false,"showThresholdMarkers":true},"pluginVersion":"8.5.1","targets":[{"datasource":{"type":"prometheus","uid":"VAwRPKXnk"},"editorMode":"code","expr":"accessbot_total_consecutive_errors \u003e bool 0","legendFormat":"{{job}}","range":true,"refId":"A"}],"title":"Last Execution Status","type":"gauge"}],"refresh":"5s","schemaVersion":36,"style":"dark","tags":[],"templating":{"list":[]},"time":{"from":"now-15m","to":"now"},"timepicker":{},"timezone":"","title":"AccessBot Metrics","uid":"982GyKX7z","version":1,"weekStart":""}');
CREATE TABLE `team` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `name` TEXT NOT NULL
, `org_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `email` TEXT NULL);
CREATE TABLE `team_member` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `team_id` INTEGER NOT NULL
, `user_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `external` INTEGER NULL, `permission` INTEGER NULL);
CREATE TABLE `dashboard_acl` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `dashboard_id` INTEGER NOT NULL
, `user_id` INTEGER NULL
, `team_id` INTEGER NULL
, `permission` INTEGER NOT NULL DEFAULT 4
, `role` TEXT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
INSERT INTO dashboard_acl VALUES(1,-1,-1,NULL,NULL,1,'Viewer','2017-06-20','2017-06-20');
INSERT INTO dashboard_acl VALUES(2,-1,-1,NULL,NULL,2,'Editor','2017-06-20','2017-06-20');
CREATE TABLE `tag` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `key` TEXT NOT NULL
, `value` TEXT NOT NULL
);
CREATE TABLE `login_attempt` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `username` TEXT NOT NULL
, `ip_address` TEXT NOT NULL
, `created` INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE `user_auth` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `user_id` INTEGER NOT NULL
, `auth_module` TEXT NOT NULL
, `auth_id` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `o_auth_access_token` TEXT NULL, `o_auth_refresh_token` TEXT NULL, `o_auth_token_type` TEXT NULL, `o_auth_expiry` DATETIME NULL, `o_auth_id_token` TEXT NULL);
CREATE TABLE `server_lock` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `operation_uid` TEXT NOT NULL
, `version` INTEGER NOT NULL
, `last_execution` INTEGER NOT NULL
);
INSERT INTO server_lock VALUES(1,'cleanup expired auth tokens',1,1652788303);
INSERT INTO server_lock VALUES(2,'delete old login attempts',4,1652790703);
CREATE TABLE `user_auth_token` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `user_id` INTEGER NOT NULL
, `auth_token` TEXT NOT NULL
, `prev_auth_token` TEXT NOT NULL
, `user_agent` TEXT NOT NULL
, `client_ip` TEXT NOT NULL
, `auth_token_seen` INTEGER NOT NULL
, `seen_at` INTEGER NULL
, `rotated_at` INTEGER NOT NULL
, `created_at` INTEGER NOT NULL
, `updated_at` INTEGER NOT NULL
, `revoked_at` INTEGER NULL);
CREATE TABLE `cache_data` (
`cache_key` TEXT PRIMARY KEY NOT NULL
, `data` BLOB NOT NULL
, `expires` INTEGER NOT NULL
, `created_at` INTEGER NOT NULL
);
CREATE TABLE `short_url` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `uid` TEXT NOT NULL
, `path` TEXT NOT NULL
, `created_by` INTEGER NOT NULL
, `created_at` INTEGER NOT NULL
, `last_seen_at` INTEGER NULL
);
CREATE TABLE `alert_instance` (
"rule_org_id" INTEGER NOT NULL
, "rule_uid" TEXT NOT NULL DEFAULT 0
, `labels` TEXT NOT NULL
, `labels_hash` TEXT NOT NULL
, `current_state` TEXT NOT NULL
, `current_state_since` INTEGER NOT NULL
, `last_eval_time` INTEGER NOT NULL
, `current_state_end` INTEGER NOT NULL DEFAULT 0, PRIMARY KEY ( "rule_org_id","rule_uid",`labels_hash` ));
CREATE TABLE `alert_rule` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `title` TEXT NOT NULL
, `condition` TEXT NOT NULL
, `data` TEXT NOT NULL
, `updated` DATETIME NOT NULL
, `interval_seconds` INTEGER NOT NULL DEFAULT 60
, `version` INTEGER NOT NULL DEFAULT 0
, `uid` TEXT NOT NULL DEFAULT 0
, `namespace_uid` TEXT NOT NULL
, `rule_group` TEXT NOT NULL
, `no_data_state` TEXT NOT NULL DEFAULT 'NoData'
, `exec_err_state` TEXT NOT NULL DEFAULT 'Alerting'
, `for` INTEGER NOT NULL DEFAULT 0, `annotations` TEXT NULL, `labels` TEXT NULL, `dashboard_uid` TEXT NULL, `panel_id` INTEGER NULL);
CREATE TABLE `alert_rule_version` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `rule_org_id` INTEGER NOT NULL
, `rule_uid` TEXT NOT NULL DEFAULT 0
, `rule_namespace_uid` TEXT NOT NULL
, `rule_group` TEXT NOT NULL
, `parent_version` INTEGER NOT NULL
, `restored_from` INTEGER NOT NULL
, `version` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `title` TEXT NOT NULL
, `condition` TEXT NOT NULL
, `data` TEXT NOT NULL
, `interval_seconds` INTEGER NOT NULL
, `no_data_state` TEXT NOT NULL DEFAULT 'NoData'
, `exec_err_state` TEXT NOT NULL DEFAULT 'Alerting'
, `for` INTEGER NOT NULL DEFAULT 0, `annotations` TEXT NULL, `labels` TEXT NULL);
CREATE TABLE `alert_configuration` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `alertmanager_configuration` TEXT NOT NULL
, `configuration_version` TEXT NOT NULL
, `created_at` INTEGER NOT NULL
, `default` INTEGER NOT NULL DEFAULT 0, `org_id` INTEGER NOT NULL DEFAULT 0, `configuration_hash` TEXT NOT NULL DEFAULT 'not-yet-calculated');
INSERT INTO alert_configuration VALUES(1,replace('{\n	"alertmanager_config": {\n		"route": {\n			"receiver": "grafana-default-email"\n		},\n		"receivers": [{\n			"name": "grafana-default-email",\n			"grafana_managed_receiver_configs": [{\n				"uid": "",\n				"name": "email receiver",\n				"type": "email",\n				"isDefault": true,\n				"settings": {\n					"addresses": "<example@email.com>"\n				}\n			}]\n		}]\n	}\n}\n','\n',char(10)),'v1',1652788303,1,1,'8c409350c88d78d2ee938448449e628d');
CREATE TABLE `ngalert_configuration` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `alertmanagers` TEXT NULL
, `created_at` INTEGER NOT NULL
, `updated_at` INTEGER NOT NULL
, `send_alerts_to` INTEGER NOT NULL DEFAULT 0);
CREATE TABLE `provenance_type` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `record_key` TEXT NOT NULL
, `record_type` TEXT NOT NULL
, `provenance` TEXT NOT NULL
);
CREATE TABLE `library_element` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `folder_id` INTEGER NOT NULL
, `uid` TEXT NOT NULL
, `name` TEXT NOT NULL
, `kind` INTEGER NOT NULL
, `type` TEXT NOT NULL
, `description` TEXT NOT NULL
, `model` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `created_by` INTEGER NOT NULL
, `updated` DATETIME NOT NULL
, `updated_by` INTEGER NOT NULL
, `version` INTEGER NOT NULL
);
CREATE TABLE `library_element_connection` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `element_id` INTEGER NOT NULL
, `kind` INTEGER NOT NULL
, `connection_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `created_by` INTEGER NOT NULL
);
CREATE TABLE `data_keys` (
`name` TEXT PRIMARY KEY NOT NULL
, `active` INTEGER NOT NULL
, `scope` TEXT NOT NULL
, `provider` TEXT NOT NULL
, `encrypted_data` BLOB NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
CREATE TABLE `kv_store` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `namespace` TEXT NOT NULL
, `key` TEXT NOT NULL
, `value` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
INSERT INTO kv_store VALUES(1,1,'alertmanager','notifications','','2022-05-17 12:06:43','2022-05-17 12:06:43');
INSERT INTO kv_store VALUES(2,1,'alertmanager','silences','','2022-05-17 12:06:43','2022-05-17 12:06:43');
CREATE TABLE `permission` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `role_id` INTEGER NOT NULL
, `action` TEXT NOT NULL
, `scope` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
);
CREATE TABLE `role` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `name` TEXT NOT NULL
, `description` TEXT NULL
, `version` INTEGER NOT NULL
, `org_id` INTEGER NOT NULL
, `uid` TEXT NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `display_name` TEXT NULL, `group_name` TEXT NULL, `hidden` INTEGER NOT NULL DEFAULT 0);
CREATE TABLE `team_role` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `team_id` INTEGER NOT NULL
, `role_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
);
CREATE TABLE `user_role` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `org_id` INTEGER NOT NULL
, `user_id` INTEGER NOT NULL
, `role_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
);
CREATE TABLE `builtin_role` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `role` TEXT NOT NULL
, `role_id` INTEGER NOT NULL
, `created` DATETIME NOT NULL
, `updated` DATETIME NOT NULL
, `org_id` INTEGER NOT NULL DEFAULT 0);
CREATE TABLE `seed_assignment` (
`builtin_role` TEXT NOT NULL
, `role_name` TEXT NOT NULL
);
CREATE TABLE `query_history` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `uid` TEXT NOT NULL
, `org_id` INTEGER NOT NULL
, `datasource_uid` TEXT NOT NULL
, `created_by` INTEGER NOT NULL
, `created_at` INTEGER NOT NULL
, `comment` TEXT NOT NULL
, `queries` TEXT NOT NULL
);
CREATE TABLE `query_history_star` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
, `query_uid` TEXT NOT NULL
, `user_id` INTEGER NOT NULL
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('migration_log',395);
INSERT INTO sqlite_sequence VALUES('user',1);
INSERT INTO sqlite_sequence VALUES('temp_user',0);
INSERT INTO sqlite_sequence VALUES('dashboard',1);
INSERT INTO sqlite_sequence VALUES('dashboard_provisioning',0);
INSERT INTO sqlite_sequence VALUES('data_source',1);
INSERT INTO sqlite_sequence VALUES('api_key',0);
INSERT INTO sqlite_sequence VALUES('alert_rule_tag',0);
INSERT INTO sqlite_sequence VALUES('annotation_tag',0);
INSERT INTO sqlite_sequence VALUES('dashboard_version',1);
INSERT INTO sqlite_sequence VALUES('dashboard_acl',2);
INSERT INTO sqlite_sequence VALUES('login_attempt',0);
INSERT INTO sqlite_sequence VALUES('org',1);
INSERT INTO sqlite_sequence VALUES('org_user',1);
INSERT INTO sqlite_sequence VALUES('alert_configuration',1);
INSERT INTO sqlite_sequence VALUES('server_lock',2);
INSERT INTO sqlite_sequence VALUES('kv_store',2);
CREATE UNIQUE INDEX `UQE_user_login` ON `user` (`login`);
CREATE UNIQUE INDEX `UQE_user_email` ON `user` (`email`);
CREATE INDEX `IDX_user_login_email` ON `user` (`login`,`email`);
CREATE INDEX `IDX_temp_user_email` ON `temp_user` (`email`);
CREATE INDEX `IDX_temp_user_org_id` ON `temp_user` (`org_id`);
CREATE INDEX `IDX_temp_user_code` ON `temp_user` (`code`);
CREATE INDEX `IDX_temp_user_status` ON `temp_user` (`status`);
CREATE UNIQUE INDEX `UQE_star_user_id_dashboard_id` ON `star` (`user_id`,`dashboard_id`);
CREATE UNIQUE INDEX `UQE_org_name` ON `org` (`name`);
CREATE INDEX `IDX_org_user_org_id` ON `org_user` (`org_id`);
CREATE UNIQUE INDEX `UQE_org_user_org_id_user_id` ON `org_user` (`org_id`,`user_id`);
CREATE INDEX `IDX_org_user_user_id` ON `org_user` (`user_id`);
CREATE INDEX `IDX_dashboard_org_id` ON `dashboard` (`org_id`);
CREATE INDEX `IDX_dashboard_gnet_id` ON `dashboard` (`gnet_id`);
CREATE INDEX `IDX_dashboard_org_id_plugin_id` ON `dashboard` (`org_id`,`plugin_id`);
CREATE INDEX `IDX_dashboard_tag_dashboard_id` ON `dashboard_tag` (`dashboard_id`);
CREATE UNIQUE INDEX `UQE_dashboard_org_id_uid` ON `dashboard` (`org_id`,`uid`);
CREATE UNIQUE INDEX `UQE_dashboard_org_id_folder_id_title` ON `dashboard` (`org_id`,`folder_id`,`title`);
CREATE INDEX `IDX_dashboard_provisioning_dashboard_id` ON `dashboard_provisioning` (`dashboard_id`);
CREATE INDEX `IDX_dashboard_provisioning_dashboard_id_name` ON `dashboard_provisioning` (`dashboard_id`,`name`);
CREATE INDEX `IDX_dashboard_title` ON `dashboard` (`title`);
CREATE INDEX `IDX_dashboard_is_folder` ON `dashboard` (`is_folder`);
CREATE INDEX `IDX_data_source_org_id` ON `data_source` (`org_id`);
CREATE UNIQUE INDEX `UQE_data_source_org_id_name` ON `data_source` (`org_id`,`name`);
CREATE UNIQUE INDEX `UQE_data_source_org_id_uid` ON `data_source` (`org_id`,`uid`);
CREATE INDEX `IDX_data_source_org_id_is_default` ON `data_source` (`org_id`,`is_default`);
CREATE INDEX `IDX_api_key_org_id` ON `api_key` (`org_id`);
CREATE UNIQUE INDEX `UQE_api_key_key` ON `api_key` (`key`);
CREATE UNIQUE INDEX `UQE_api_key_org_id_name` ON `api_key` (`org_id`,`name`);
CREATE UNIQUE INDEX `UQE_dashboard_snapshot_key` ON `dashboard_snapshot` (`key`);
CREATE UNIQUE INDEX `UQE_dashboard_snapshot_delete_key` ON `dashboard_snapshot` (`delete_key`);
CREATE INDEX `IDX_dashboard_snapshot_user_id` ON `dashboard_snapshot` (`user_id`);
CREATE UNIQUE INDEX `UQE_quota_org_id_user_id_target` ON `quota` (`org_id`,`user_id`,`target`);
CREATE UNIQUE INDEX `UQE_plugin_setting_org_id_plugin_id` ON `plugin_setting` (`org_id`,`plugin_id`);
CREATE INDEX `IDX_alert_org_id_id` ON `alert` (`org_id`,`id`);
CREATE INDEX `IDX_alert_state` ON `alert` (`state`);
CREATE INDEX `IDX_alert_dashboard_id` ON `alert` (`dashboard_id`);
CREATE UNIQUE INDEX `UQE_alert_rule_tag_alert_id_tag_id` ON `alert_rule_tag` (`alert_id`,`tag_id`);
CREATE UNIQUE INDEX `UQE_alert_notification_state_org_id_alert_id_notifier_id` ON `alert_notification_state` (`org_id`,`alert_id`,`notifier_id`);
CREATE UNIQUE INDEX `UQE_alert_notification_org_id_uid` ON `alert_notification` (`org_id`,`uid`);
CREATE INDEX `IDX_alert_notification_state_alert_id` ON `alert_notification_state` (`alert_id`);
CREATE INDEX `IDX_alert_rule_tag_alert_id` ON `alert_rule_tag` (`alert_id`);
CREATE INDEX `IDX_annotation_org_id_alert_id` ON `annotation` (`org_id`,`alert_id`);
CREATE INDEX `IDX_annotation_org_id_type` ON `annotation` (`org_id`,`type`);
CREATE UNIQUE INDEX `UQE_annotation_tag_annotation_id_tag_id` ON `annotation_tag` (`annotation_id`,`tag_id`);
CREATE INDEX `IDX_annotation_org_id_created` ON `annotation` (`org_id`,`created`);
CREATE INDEX `IDX_annotation_org_id_updated` ON `annotation` (`org_id`,`updated`);
CREATE INDEX `IDX_annotation_org_id_dashboard_id_epoch_end_epoch` ON `annotation` (`org_id`,`dashboard_id`,`epoch_end`,`epoch`);
CREATE INDEX `IDX_annotation_org_id_epoch_end_epoch` ON `annotation` (`org_id`,`epoch_end`,`epoch`);
CREATE INDEX `IDX_annotation_alert_id` ON `annotation` (`alert_id`);
CREATE INDEX `IDX_dashboard_version_dashboard_id` ON `dashboard_version` (`dashboard_id`);
CREATE UNIQUE INDEX `UQE_dashboard_version_dashboard_id_version` ON `dashboard_version` (`dashboard_id`,`version`);
CREATE INDEX `IDX_team_org_id` ON `team` (`org_id`);
CREATE UNIQUE INDEX `UQE_team_org_id_name` ON `team` (`org_id`,`name`);
CREATE INDEX `IDX_team_member_org_id` ON `team_member` (`org_id`);
CREATE UNIQUE INDEX `UQE_team_member_org_id_team_id_user_id` ON `team_member` (`org_id`,`team_id`,`user_id`);
CREATE INDEX `IDX_team_member_team_id` ON `team_member` (`team_id`);
CREATE INDEX `IDX_dashboard_acl_dashboard_id` ON `dashboard_acl` (`dashboard_id`);
CREATE UNIQUE INDEX `UQE_dashboard_acl_dashboard_id_user_id` ON `dashboard_acl` (`dashboard_id`,`user_id`);
CREATE UNIQUE INDEX `UQE_dashboard_acl_dashboard_id_team_id` ON `dashboard_acl` (`dashboard_id`,`team_id`);
CREATE INDEX `IDX_dashboard_acl_user_id` ON `dashboard_acl` (`user_id`);
CREATE INDEX `IDX_dashboard_acl_team_id` ON `dashboard_acl` (`team_id`);
CREATE INDEX `IDX_dashboard_acl_org_id_role` ON `dashboard_acl` (`org_id`,`role`);
CREATE INDEX `IDX_dashboard_acl_permission` ON `dashboard_acl` (`permission`);
CREATE UNIQUE INDEX `UQE_tag_key_value` ON `tag` (`key`,`value`);
CREATE INDEX `IDX_login_attempt_username` ON `login_attempt` (`username`);
CREATE INDEX `IDX_user_auth_auth_module_auth_id` ON `user_auth` (`auth_module`,`auth_id`);
CREATE INDEX `IDX_user_auth_user_id` ON `user_auth` (`user_id`);
CREATE UNIQUE INDEX `UQE_server_lock_operation_uid` ON `server_lock` (`operation_uid`);
CREATE UNIQUE INDEX `UQE_user_auth_token_auth_token` ON `user_auth_token` (`auth_token`);
CREATE UNIQUE INDEX `UQE_user_auth_token_prev_auth_token` ON `user_auth_token` (`prev_auth_token`);
CREATE INDEX `IDX_user_auth_token_user_id` ON `user_auth_token` (`user_id`);
CREATE UNIQUE INDEX `UQE_cache_data_cache_key` ON `cache_data` (`cache_key`);
CREATE UNIQUE INDEX `UQE_short_url_org_id_uid` ON `short_url` (`org_id`,`uid`);
CREATE INDEX `IDX_alert_instance_rule_org_id_rule_uid_current_state` ON `alert_instance` (`rule_org_id`,`rule_uid`,`current_state`);
CREATE INDEX `IDX_alert_instance_rule_org_id_current_state` ON `alert_instance` (`rule_org_id`,`current_state`);
CREATE UNIQUE INDEX `UQE_alert_rule_org_id_uid` ON `alert_rule` (`org_id`,`uid`);
CREATE INDEX `IDX_alert_rule_org_id_namespace_uid_rule_group` ON `alert_rule` (`org_id`,`namespace_uid`,`rule_group`);
CREATE UNIQUE INDEX `UQE_alert_rule_org_id_namespace_uid_title` ON `alert_rule` (`org_id`,`namespace_uid`,`title`);
CREATE INDEX `IDX_alert_rule_org_id_dashboard_uid_panel_id` ON `alert_rule` (`org_id`,`dashboard_uid`,`panel_id`);
CREATE UNIQUE INDEX `UQE_alert_rule_version_rule_org_id_rule_uid_version` ON `alert_rule_version` (`rule_org_id`,`rule_uid`,`version`);
CREATE INDEX `IDX_alert_rule_version_rule_org_id_rule_namespace_uid_rule_group` ON `alert_rule_version` (`rule_org_id`,`rule_namespace_uid`,`rule_group`);
CREATE INDEX `IDX_alert_configuration_org_id` ON `alert_configuration` (`org_id`);
CREATE UNIQUE INDEX `UQE_ngalert_configuration_org_id` ON `ngalert_configuration` (`org_id`);
CREATE UNIQUE INDEX `UQE_provenance_type_record_type_record_key_org_id` ON `provenance_type` (`record_type`,`record_key`,`org_id`);
CREATE UNIQUE INDEX `UQE_library_element_org_id_folder_id_name_kind` ON `library_element` (`org_id`,`folder_id`,`name`,`kind`);
CREATE UNIQUE INDEX `UQE_library_element_connection_element_id_kind_connection_id` ON `library_element_connection` (`element_id`,`kind`,`connection_id`);
CREATE UNIQUE INDEX `UQE_library_element_org_id_uid` ON `library_element` (`org_id`,`uid`);
CREATE UNIQUE INDEX `UQE_kv_store_org_id_namespace_key` ON `kv_store` (`org_id`,`namespace`,`key`);
CREATE INDEX `IDX_permission_role_id` ON `permission` (`role_id`);
CREATE UNIQUE INDEX `UQE_permission_role_id_action_scope` ON `permission` (`role_id`,`action`,`scope`);
CREATE INDEX `IDX_role_org_id` ON `role` (`org_id`);
CREATE UNIQUE INDEX `UQE_role_org_id_name` ON `role` (`org_id`,`name`);
CREATE INDEX `IDX_team_role_org_id` ON `team_role` (`org_id`);
CREATE UNIQUE INDEX `UQE_team_role_org_id_team_id_role_id` ON `team_role` (`org_id`,`team_id`,`role_id`);
CREATE INDEX `IDX_team_role_team_id` ON `team_role` (`team_id`);
CREATE INDEX `IDX_user_role_org_id` ON `user_role` (`org_id`);
CREATE UNIQUE INDEX `UQE_user_role_org_id_user_id_role_id` ON `user_role` (`org_id`,`user_id`,`role_id`);
CREATE INDEX `IDX_user_role_user_id` ON `user_role` (`user_id`);
CREATE INDEX `IDX_builtin_role_role_id` ON `builtin_role` (`role_id`);
CREATE INDEX `IDX_builtin_role_role` ON `builtin_role` (`role`);
CREATE INDEX `IDX_builtin_role_org_id` ON `builtin_role` (`org_id`);
CREATE UNIQUE INDEX `UQE_builtin_role_org_id_role_id_role` ON `builtin_role` (`org_id`,`role_id`,`role`);
CREATE UNIQUE INDEX `UQE_role_uid` ON `role` (`uid`);
CREATE UNIQUE INDEX `UQE_seed_assignment_builtin_role_role_name` ON `seed_assignment` (`builtin_role`,`role_name`);
CREATE INDEX `IDX_query_history_org_id_created_by_datasource_uid` ON `query_history` (`org_id`,`created_by`,`datasource_uid`);
CREATE UNIQUE INDEX `UQE_query_history_star_user_id_query_uid` ON `query_history_star` (`user_id`,`query_uid`);
COMMIT;
