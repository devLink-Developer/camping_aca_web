# Devlink DB - Panorama

Generado (UTC): 2026-02-17 22:08:17

- Host: 200.58.107.187
- Puerto usado: 5456 (5455 primero, 5456 fallback)
- DB: devlink
- Usuario: devlink

> Nota: reporte generado con consultas SELECT (solo lectura).

## Schemas (no sistema)

| schema |
| --- |
| public |

## Tablas (no sistema)

| table_schema | table_name |
| --- | --- |
| public | async_jobs |
| public | auth_group |
| public | auth_group_permissions |
| public | auth_permission |
| public | auth_user |
| public | auth_user_groups |
| public | auth_user_user_permissions |
| public | campana_envios |
| public | campana_templates |
| public | campanas |
| public | clientes |
| public | config |
| public | django_admin_log |
| public | django_apscheduler_djangojob |
| public | django_apscheduler_djangojobexecution |
| public | django_content_type |
| public | django_migrations |
| public | django_session |
| public | generic_job_configs |
| public | generic_job_run_logs |
| public | mensajes |
| public | menu_opciones |
| public | menus |
| public | respuestas |
| public | sesiones |
| public | waba_config |

## Columnas

| table_schema | table_name | ordinal_position | column_name | data_type | udt_name | is_nullable | column_default |
| --- | --- | --- | --- | --- | --- | --- | --- |
| public | async_jobs | 1 | id | uuid | uuid | NO |  |
| public | async_jobs | 2 | name | character varying | varchar | NO |  |
| public | async_jobs | 3 | job_type | character varying | varchar | NO |  |
| public | async_jobs | 4 | status | character varying | varchar | NO |  |
| public | async_jobs | 5 | payload | jsonb | jsonb | NO |  |
| public | async_jobs | 6 | result | jsonb | jsonb | YES |  |
| public | async_jobs | 7 | progress | numeric | numeric | NO |  |
| public | async_jobs | 8 | message | text | text | NO |  |
| public | async_jobs | 9 | backend | character varying | varchar | NO |  |
| public | async_jobs | 10 | cancel_requested | boolean | bool | NO |  |
| public | async_jobs | 11 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | async_jobs | 12 | started_at | timestamp with time zone | timestamptz | YES |  |
| public | async_jobs | 13 | finished_at | timestamp with time zone | timestamptz | YES |  |
| public | async_jobs | 14 | last_heartbeat_at | timestamp with time zone | timestamptz | YES |  |
| public | async_jobs | 15 | user_id | integer | int4 | YES |  |
| public | auth_group | 1 | id | integer | int4 | NO |  |
| public | auth_group | 2 | name | character varying | varchar | NO |  |
| public | auth_group_permissions | 1 | id | bigint | int8 | NO |  |
| public | auth_group_permissions | 2 | group_id | integer | int4 | NO |  |
| public | auth_group_permissions | 3 | permission_id | integer | int4 | NO |  |
| public | auth_permission | 1 | id | integer | int4 | NO |  |
| public | auth_permission | 2 | name | character varying | varchar | NO |  |
| public | auth_permission | 3 | content_type_id | integer | int4 | NO |  |
| public | auth_permission | 4 | codename | character varying | varchar | NO |  |
| public | auth_user | 1 | id | integer | int4 | NO |  |
| public | auth_user | 2 | password | character varying | varchar | NO |  |
| public | auth_user | 3 | last_login | timestamp with time zone | timestamptz | YES |  |
| public | auth_user | 4 | is_superuser | boolean | bool | NO |  |
| public | auth_user | 5 | username | character varying | varchar | NO |  |
| public | auth_user | 6 | first_name | character varying | varchar | NO |  |
| public | auth_user | 7 | last_name | character varying | varchar | NO |  |
| public | auth_user | 8 | email | character varying | varchar | NO |  |
| public | auth_user | 9 | is_staff | boolean | bool | NO |  |
| public | auth_user | 10 | is_active | boolean | bool | NO |  |
| public | auth_user | 11 | date_joined | timestamp with time zone | timestamptz | NO |  |
| public | auth_user_groups | 1 | id | bigint | int8 | NO |  |
| public | auth_user_groups | 2 | user_id | integer | int4 | NO |  |
| public | auth_user_groups | 3 | group_id | integer | int4 | NO |  |
| public | auth_user_user_permissions | 1 | id | bigint | int8 | NO |  |
| public | auth_user_user_permissions | 2 | user_id | integer | int4 | NO |  |
| public | auth_user_user_permissions | 3 | permission_id | integer | int4 | NO |  |
| public | campana_envios | 1 | id | bigint | int8 | NO |  |
| public | campana_envios | 2 | estado | character varying | varchar | NO |  |
| public | campana_envios | 3 | programado_para | timestamp with time zone | timestamptz | YES |  |
| public | campana_envios | 4 | enviado_en | timestamp with time zone | timestamptz | YES |  |
| public | campana_envios | 5 | error | character varying | varchar | YES |  |
| public | campana_envios | 6 | payload_json | jsonb | jsonb | YES |  |
| public | campana_envios | 7 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | campana_envios | 8 | campana_id | bigint | int8 | NO |  |
| public | campana_envios | 9 | cliente_id | character varying | varchar | NO |  |
| public | campana_templates | 1 | id | bigint | int8 | NO |  |
| public | campana_templates | 2 | nombre | character varying | varchar | NO |  |
| public | campana_templates | 3 | idioma | character varying | varchar | NO |  |
| public | campana_templates | 4 | cuerpo | text | text | NO |  |
| public | campana_templates | 5 | variables_json | jsonb | jsonb | YES |  |
| public | campana_templates | 6 | activo | boolean | bool | NO |  |
| public | campana_templates | 7 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | campana_templates | 8 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | campanas | 1 | id | bigint | int8 | NO |  |
| public | campanas | 2 | nombre | character varying | varchar | NO |  |
| public | campanas | 3 | descripcion | character varying | varchar | YES |  |
| public | campanas | 4 | activo | boolean | bool | NO |  |
| public | campanas | 5 | canal | character varying | varchar | NO |  |
| public | campanas | 6 | tipo | character varying | varchar | NO |  |
| public | campanas | 7 | direccion_offset | character varying | varchar | NO |  |
| public | campanas | 8 | dias_offset | integer | int4 | NO |  |
| public | campanas | 9 | hora_envio | time without time zone | time | YES |  |
| public | campanas | 10 | template_nombre | character varying | varchar | YES |  |
| public | campanas | 11 | template_idioma | character varying | varchar | YES |  |
| public | campanas | 12 | texto_estatico | text | text | NO |  |
| public | campanas | 13 | variables_json | jsonb | jsonb | YES |  |
| public | campanas | 14 | segmento_json | jsonb | jsonb | YES |  |
| public | campanas | 15 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | campanas | 16 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | campanas | 17 | template_id | bigint | int8 | YES |  |
| public | clientes | 1 | phone_number | character varying | varchar | NO |  |
| public | clientes | 2 | nombre | character varying | varchar | YES |  |
| public | clientes | 3 | primer_contacto_ms | bigint | int8 | NO |  |
| public | clientes | 4 | ultimo_contacto_ms | bigint | int8 | NO |  |
| public | clientes | 5 | mensajes_totales | bigint | int8 | NO |  |
| public | clientes | 6 | ultimo_mensaje | character varying | varchar | YES |  |
| public | clientes | 7 | activo | boolean | bool | NO |  |
| public | clientes | 8 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | clientes | 9 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | clientes | 10 | alias_waba | character varying | varchar | YES |  |
| public | clientes | 11 | correo | character varying | varchar | YES |  |
| public | clientes | 12 | direccion | character varying | varchar | YES |  |
| public | clientes | 13 | fecha_nacimiento | date | date | YES |  |
| public | clientes | 14 | marketing_opt_in | boolean | bool | NO |  |
| public | config | 1 | id | character varying | varchar | NO |  |
| public | config | 2 | seccion | character varying | varchar | NO |  |
| public | config | 3 | valor | jsonb | jsonb | NO |  |
| public | config | 4 | descripcion | character varying | varchar | YES |  |
| public | config | 5 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | config | 6 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | django_admin_log | 1 | id | integer | int4 | NO |  |
| public | django_admin_log | 2 | action_time | timestamp with time zone | timestamptz | NO |  |
| public | django_admin_log | 3 | object_id | text | text | YES |  |
| public | django_admin_log | 4 | object_repr | character varying | varchar | NO |  |
| public | django_admin_log | 5 | action_flag | smallint | int2 | NO |  |
| public | django_admin_log | 6 | change_message | text | text | NO |  |
| public | django_admin_log | 7 | content_type_id | integer | int4 | YES |  |
| public | django_admin_log | 8 | user_id | integer | int4 | NO |  |
| public | django_apscheduler_djangojob | 1 | id | character varying | varchar | NO |  |
| public | django_apscheduler_djangojob | 3 | next_run_time | timestamp with time zone | timestamptz | YES |  |
| public | django_apscheduler_djangojob | 4 | job_state | bytea | bytea | NO |  |
| public | django_apscheduler_djangojobexecution | 1 | id | bigint | int8 | NO |  |
| public | django_apscheduler_djangojobexecution | 2 | status | character varying | varchar | NO |  |
| public | django_apscheduler_djangojobexecution | 3 | run_time | timestamp with time zone | timestamptz | NO |  |
| public | django_apscheduler_djangojobexecution | 4 | duration | numeric | numeric | YES |  |
| public | django_apscheduler_djangojobexecution | 6 | finished | numeric | numeric | YES |  |
| public | django_apscheduler_djangojobexecution | 7 | exception | character varying | varchar | YES |  |
| public | django_apscheduler_djangojobexecution | 8 | traceback | text | text | YES |  |
| public | django_apscheduler_djangojobexecution | 9 | job_id | character varying | varchar | NO |  |
| public | django_content_type | 1 | id | integer | int4 | NO |  |
| public | django_content_type | 3 | app_label | character varying | varchar | NO |  |
| public | django_content_type | 4 | model | character varying | varchar | NO |  |
| public | django_migrations | 1 | id | bigint | int8 | NO |  |
| public | django_migrations | 2 | app | character varying | varchar | NO |  |
| public | django_migrations | 3 | name | character varying | varchar | NO |  |
| public | django_migrations | 4 | applied | timestamp with time zone | timestamptz | NO |  |
| public | django_session | 1 | session_key | character varying | varchar | NO |  |
| public | django_session | 2 | session_data | text | text | NO |  |
| public | django_session | 3 | expire_date | timestamp with time zone | timestamptz | NO |  |
| public | generic_job_configs | 1 | id | uuid | uuid | NO |  |
| public | generic_job_configs | 2 | name | character varying | varchar | NO |  |
| public | generic_job_configs | 3 | description | text | text | NO |  |
| public | generic_job_configs | 4 | callable_path | character varying | varchar | NO |  |
| public | generic_job_configs | 5 | callable_kwargs | jsonb | jsonb | NO |  |
| public | generic_job_configs | 6 | enabled | boolean | bool | NO |  |
| public | generic_job_configs | 7 | paused | boolean | bool | NO |  |
| public | generic_job_configs | 8 | schedule_type | character varying | varchar | NO |  |
| public | generic_job_configs | 9 | daily_time | time without time zone | time | YES |  |
| public | generic_job_configs | 10 | interval_minutes | integer | int4 | YES |  |
| public | generic_job_configs | 11 | cron_expression | character varying | varchar | NO |  |
| public | generic_job_configs | 12 | max_instances | integer | int4 | NO |  |
| public | generic_job_configs | 13 | coalesce | boolean | bool | NO |  |
| public | generic_job_configs | 14 | misfire_grace_seconds | integer | int4 | NO |  |
| public | generic_job_configs | 15 | cancel_requested | boolean | bool | NO |  |
| public | generic_job_configs | 16 | cancel_requested_at | timestamp with time zone | timestamptz | YES |  |
| public | generic_job_configs | 17 | last_run_at | timestamp with time zone | timestamptz | YES |  |
| public | generic_job_configs | 18 | next_run_at | timestamp with time zone | timestamptz | YES |  |
| public | generic_job_configs | 19 | last_status | character varying | varchar | YES |  |
| public | generic_job_configs | 20 | last_message | text | text | NO |  |
| public | generic_job_configs | 21 | last_duration_ms | bigint | int8 | YES |  |
| public | generic_job_configs | 22 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | generic_job_configs | 23 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | generic_job_configs | 24 | chained_job_id | uuid | uuid | YES |  |
| public | generic_job_configs | 25 | owner_id | integer | int4 | YES |  |
| public | generic_job_run_logs | 1 | id | uuid | uuid | NO |  |
| public | generic_job_run_logs | 2 | job_type | character varying | varchar | NO |  |
| public | generic_job_run_logs | 3 | source_identifier | character varying | varchar | NO |  |
| public | generic_job_run_logs | 4 | triggered_by | character varying | varchar | NO |  |
| public | generic_job_run_logs | 5 | started_at | timestamp with time zone | timestamptz | NO |  |
| public | generic_job_run_logs | 6 | finished_at | timestamp with time zone | timestamptz | YES |  |
| public | generic_job_run_logs | 7 | status | character varying | varchar | NO |  |
| public | generic_job_run_logs | 8 | message | text | text | NO |  |
| public | generic_job_run_logs | 9 | payload | jsonb | jsonb | NO |  |
| public | generic_job_run_logs | 10 | duration_ms | bigint | int8 | YES |  |
| public | generic_job_run_logs | 11 | run_identifier | character varying | varchar | NO |  |
| public | generic_job_run_logs | 12 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | generic_job_run_logs | 13 | config_id | uuid | uuid | YES |  |
| public | generic_job_run_logs | 14 | user_id | integer | int4 | YES |  |
| public | mensajes | 1 | id | bigint | int8 | NO |  |
| public | mensajes | 2 | phone_number | character varying | varchar | NO |  |
| public | mensajes | 3 | nombre | character varying | varchar | YES |  |
| public | mensajes | 4 | direccion | character varying | varchar | NO |  |
| public | mensajes | 5 | tipo | character varying | varchar | NO |  |
| public | mensajes | 6 | contenido | character varying | varchar | YES |  |
| public | mensajes | 7 | wa_message_id | character varying | varchar | YES |  |
| public | mensajes | 8 | timestamp_ms | bigint | int8 | NO |  |
| public | mensajes | 9 | metadata_json | jsonb | jsonb | YES |  |
| public | mensajes | 10 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | mensajes | 11 | attempts | integer | int4 | NO |  |
| public | mensajes | 12 | delivery_status | character varying | varchar | YES |  |
| public | mensajes | 13 | delivery_timestamp_ms | bigint | int8 | YES |  |
| public | mensajes | 14 | error | text | text | YES |  |
| public | mensajes | 15 | locked_at_ms | bigint | int8 | YES |  |
| public | mensajes | 16 | process_after_ms | bigint | int8 | YES |  |
| public | mensajes | 17 | processed_at_ms | bigint | int8 | YES |  |
| public | mensajes | 18 | queue_status | character varying | varchar | NO |  |
| public | menu_opciones | 1 | id | bigint | int8 | NO |  |
| public | menu_opciones | 2 | key | character varying | varchar | NO |  |
| public | menu_opciones | 3 | label | character varying | varchar | NO |  |
| public | menu_opciones | 4 | orden | integer | int4 | NO |  |
| public | menu_opciones | 5 | activo | boolean | bool | NO |  |
| public | menu_opciones | 6 | menu_id | character varying | varchar | NO |  |
| public | menu_opciones | 7 | target_menu_id | character varying | varchar | YES |  |
| public | menu_opciones | 8 | target_respuesta_id | character varying | varchar | YES |  |
| public | menus | 1 | id | character varying | varchar | NO |  |
| public | menus | 2 | titulo | character varying | varchar | NO |  |
| public | menus | 3 | submenu | character varying | varchar | NO |  |
| public | menus | 4 | contenido | text | text | NO |  |
| public | menus | 5 | opciones | jsonb | jsonb | YES |  |
| public | menus | 6 | activo | boolean | bool | NO |  |
| public | menus | 7 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | menus | 8 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | menus | 9 | orden | integer | int4 | NO |  |
| public | menus | 10 | parent_id | character varying | varchar | YES |  |
| public | menus | 11 | is_main | boolean | bool | NO |  |
| public | menus | 12 | flow_id | character varying | varchar | YES |  |
| public | menus | 13 | flow_name | character varying | varchar | YES |  |
| public | menus | 14 | flow_status | character varying | varchar | YES |  |
| public | menus | 15 | flow_valid | boolean | bool | NO |  |
| public | menus | 16 | flow_last_checked_at | timestamp with time zone | timestamptz | YES |  |
| public | menus | 17 | flow_validation | jsonb | jsonb | YES |  |
| public | menus | 18 | flow_json | jsonb | jsonb | YES |  |
| public | respuestas | 1 | id | character varying | varchar | NO |  |
| public | respuestas | 2 | categoria | character varying | varchar | NO |  |
| public | respuestas | 3 | contenido | character varying | varchar | NO |  |
| public | respuestas | 4 | siguientes_pasos | jsonb | jsonb | NO |  |
| public | respuestas | 5 | metadata | jsonb | jsonb | YES |  |
| public | respuestas | 6 | activo | boolean | bool | NO |  |
| public | respuestas | 7 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | respuestas | 8 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | sesiones | 1 | phone_number | character varying | varchar | NO |  |
| public | sesiones | 2 | nombre | character varying | varchar | YES |  |
| public | sesiones | 3 | activa | boolean | bool | NO |  |
| public | sesiones | 4 | estado_actual | character varying | varchar | NO |  |
| public | sesiones | 5 | historial_navegacion | jsonb | jsonb | NO |  |
| public | sesiones | 6 | ultimo_mensaje | character varying | varchar | YES |  |
| public | sesiones | 7 | timestamp_ultimo_mensaje | bigint | int8 | YES |  |
| public | sesiones | 8 | inicio_sesion_ms | bigint | int8 | NO |  |
| public | sesiones | 9 | ultimo_acceso_ms | bigint | int8 | NO |  |
| public | sesiones | 10 | primer_acceso | boolean | bool | NO |  |
| public | sesiones | 11 | intentos_fallidos | bigint | int8 | NO |  |
| public | sesiones | 12 | datos_extra | jsonb | jsonb | YES |  |
| public | sesiones | 13 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | sesiones | 14 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | waba_config | 1 | id | bigint | int8 | NO |  |
| public | waba_config | 2 | name | character varying | varchar | NO |  |
| public | waba_config | 3 | active | boolean | bool | NO |  |
| public | waba_config | 4 | phone_id | character varying | varchar | NO |  |
| public | waba_config | 5 | access_token | text | text | NO |  |
| public | waba_config | 6 | verify_token | character varying | varchar | NO |  |
| public | waba_config | 7 | api_base | character varying | varchar | NO |  |
| public | waba_config | 8 | api_version | character varying | varchar | NO |  |
| public | waba_config | 9 | business_id | character varying | varchar | NO |  |
| public | waba_config | 10 | waba_id | character varying | varchar | NO |  |
| public | waba_config | 11 | webhook_url | character varying | varchar | NO |  |
| public | waba_config | 12 | created_at | timestamp with time zone | timestamptz | NO |  |
| public | waba_config | 13 | updated_at | timestamp with time zone | timestamptz | NO |  |
| public | waba_config | 14 | interactive_enabled | boolean | bool | NO |  |
| public | waba_config | 15 | flow_enabled | boolean | bool | NO |  |

## Constraints

| table_schema | table_name | constraint_name | definition |
| --- | --- | --- | --- |
| public | async_jobs | async_jobs_pkey | PRIMARY KEY (id) |
| public | async_jobs | async_jobs_user_id_0d48b5cd_fk_auth_user_id | FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_group | auth_group_name_key | UNIQUE (name) |
| public | auth_group | auth_group_pkey | PRIMARY KEY (id) |
| public | auth_group_permissions | auth_group_permissio_permission_id_84c5c92e_fk_auth_perm | FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_group_permissions | auth_group_permissions_group_id_b120cbf9_fk_auth_group_id | FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_group_permissions | auth_group_permissions_group_id_permission_id_0cd325b0_uniq | UNIQUE (group_id, permission_id) |
| public | auth_group_permissions | auth_group_permissions_pkey | PRIMARY KEY (id) |
| public | auth_permission | auth_permission_content_type_id_2f476e4b_fk_django_co | FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_permission | auth_permission_content_type_id_codename_01ab375a_uniq | UNIQUE (content_type_id, codename) |
| public | auth_permission | auth_permission_pkey | PRIMARY KEY (id) |
| public | auth_user | auth_user_pkey | PRIMARY KEY (id) |
| public | auth_user | auth_user_username_key | UNIQUE (username) |
| public | auth_user_groups | auth_user_groups_group_id_97559544_fk_auth_group_id | FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_user_groups | auth_user_groups_pkey | PRIMARY KEY (id) |
| public | auth_user_groups | auth_user_groups_user_id_6a12ed8b_fk_auth_user_id | FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_user_groups | auth_user_groups_user_id_group_id_94350c0c_uniq | UNIQUE (user_id, group_id) |
| public | auth_user_user_permissions | auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm | FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_user_user_permissions | auth_user_user_permissions_pkey | PRIMARY KEY (id) |
| public | auth_user_user_permissions | auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id | FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | auth_user_user_permissions | auth_user_user_permissions_user_id_permission_id_14a6b632_uniq | UNIQUE (user_id, permission_id) |
| public | campana_envios | campana_envios_campana_id_5dcf9002_fk_campanas_id | FOREIGN KEY (campana_id) REFERENCES campanas(id) DEFERRABLE INITIALLY DEFERRED |
| public | campana_envios | campana_envios_cliente_id_22177c69_fk_clientes_phone_number | FOREIGN KEY (cliente_id) REFERENCES clientes(phone_number) DEFERRABLE INITIALLY DEFERRED |
| public | campana_envios | campana_envios_pkey | PRIMARY KEY (id) |
| public | campana_envios | uniq_campana_cliente_programado | UNIQUE (campana_id, cliente_id, programado_para) |
| public | campana_templates | campana_templates_pkey | PRIMARY KEY (id) |
| public | campanas | campanas_pkey | PRIMARY KEY (id) |
| public | campanas | campanas_template_id_4a1183f4_fk_campana_templates_id | FOREIGN KEY (template_id) REFERENCES campana_templates(id) DEFERRABLE INITIALLY DEFERRED |
| public | clientes | clientes_pkey | PRIMARY KEY (phone_number) |
| public | config | config_pkey | PRIMARY KEY (id) |
| public | django_admin_log | django_admin_log_action_flag_check | CHECK ((action_flag >= 0)) |
| public | django_admin_log | django_admin_log_content_type_id_c4bce8eb_fk_django_co | FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED |
| public | django_admin_log | django_admin_log_pkey | PRIMARY KEY (id) |
| public | django_admin_log | django_admin_log_user_id_c564eba6_fk_auth_user_id | FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | django_apscheduler_djangojob | django_apscheduler_djangojob_pkey | PRIMARY KEY (id) |
| public | django_apscheduler_djangojobexecution | django_apscheduler_djangojobexecution_job_id_daf5090a_fk | FOREIGN KEY (job_id) REFERENCES django_apscheduler_djangojob(id) DEFERRABLE INITIALLY DEFERRED |
| public | django_apscheduler_djangojobexecution | django_apscheduler_djangojobexecution_pkey | PRIMARY KEY (id) |
| public | django_apscheduler_djangojobexecution | unique_job_executions | UNIQUE (job_id, run_time) |
| public | django_content_type | django_content_type_app_label_model_76bd3d3b_uniq | UNIQUE (app_label, model) |
| public | django_content_type | django_content_type_pkey | PRIMARY KEY (id) |
| public | django_migrations | django_migrations_pkey | PRIMARY KEY (id) |
| public | django_session | django_session_pkey | PRIMARY KEY (session_key) |
| public | generic_job_configs | generic_job_configs_chained_job_id_748cdabd_fk_generic_j | FOREIGN KEY (chained_job_id) REFERENCES generic_job_configs(id) DEFERRABLE INITIALLY DEFERRED |
| public | generic_job_configs | generic_job_configs_interval_minutes_check | CHECK ((interval_minutes >= 0)) |
| public | generic_job_configs | generic_job_configs_max_instances_check | CHECK ((max_instances >= 0)) |
| public | generic_job_configs | generic_job_configs_misfire_grace_seconds_check | CHECK ((misfire_grace_seconds >= 0)) |
| public | generic_job_configs | generic_job_configs_name_key | UNIQUE (name) |
| public | generic_job_configs | generic_job_configs_owner_id_76233a8b_fk_auth_user_id | FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | generic_job_configs | generic_job_configs_pkey | PRIMARY KEY (id) |
| public | generic_job_run_logs | generic_job_run_logs_config_id_24f29e59_fk_generic_j | FOREIGN KEY (config_id) REFERENCES generic_job_configs(id) DEFERRABLE INITIALLY DEFERRED |
| public | generic_job_run_logs | generic_job_run_logs_pkey | PRIMARY KEY (id) |
| public | generic_job_run_logs | generic_job_run_logs_user_id_4467a0e9_fk_auth_user_id | FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED |
| public | mensajes | mensajes_attempts_check | CHECK ((attempts >= 0)) |
| public | mensajes | mensajes_pkey | PRIMARY KEY (id) |
| public | menu_opciones | menu_opciones_menu_id_d6c73bd2_fk_menus_id | FOREIGN KEY (menu_id) REFERENCES menus(id) DEFERRABLE INITIALLY DEFERRED |
| public | menu_opciones | menu_opciones_pkey | PRIMARY KEY (id) |
| public | menu_opciones | menu_opciones_target_menu_id_3de0c038_fk_menus_id | FOREIGN KEY (target_menu_id) REFERENCES menus(id) DEFERRABLE INITIALLY DEFERRED |
| public | menu_opciones | menu_opciones_target_respuesta_id_d577ddf6_fk_respuestas_id | FOREIGN KEY (target_respuesta_id) REFERENCES respuestas(id) DEFERRABLE INITIALLY DEFERRED |
| public | menu_opciones | uniq_menu_key | UNIQUE (menu_id, key) |
| public | menus | menus_parent_id_52b006c5_fk_menus_id | FOREIGN KEY (parent_id) REFERENCES menus(id) DEFERRABLE INITIALLY DEFERRED |
| public | menus | menus_pkey | PRIMARY KEY (id) |
| public | respuestas | respuestas_pkey | PRIMARY KEY (id) |
| public | sesiones | sesiones_pkey | PRIMARY KEY (phone_number) |
| public | waba_config | waba_config_name_key | UNIQUE (name) |
| public | waba_config | waba_config_pkey | PRIMARY KEY (id) |

## Índices

| table_schema | table_name | index_name | index_def |
| --- | --- | --- | --- |
| public | async_jobs | async_jobs_pkey | CREATE UNIQUE INDEX async_jobs_pkey ON public.async_jobs USING btree (id) |
| public | async_jobs | async_jobs_user_id_0d48b5cd | CREATE INDEX async_jobs_user_id_0d48b5cd ON public.async_jobs USING btree (user_id) |
| public | async_jobs | asyncjob_created_idx | CREATE INDEX asyncjob_created_idx ON public.async_jobs USING btree (created_at) |
| public | async_jobs | asyncjob_status_idx | CREATE INDEX asyncjob_status_idx ON public.async_jobs USING btree (status, job_type) |
| public | auth_group | auth_group_name_a6ea08ec_like | CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops) |
| public | auth_group | auth_group_name_key | CREATE UNIQUE INDEX auth_group_name_key ON public.auth_group USING btree (name) |
| public | auth_group | auth_group_pkey | CREATE UNIQUE INDEX auth_group_pkey ON public.auth_group USING btree (id) |
| public | auth_group_permissions | auth_group_permissions_group_id_b120cbf9 | CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id) |
| public | auth_group_permissions | auth_group_permissions_group_id_permission_id_0cd325b0_uniq | CREATE UNIQUE INDEX auth_group_permissions_group_id_permission_id_0cd325b0_uniq ON public.auth_group_permissions USING btree (group_id, permission_id) |
| public | auth_group_permissions | auth_group_permissions_permission_id_84c5c92e | CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id) |
| public | auth_group_permissions | auth_group_permissions_pkey | CREATE UNIQUE INDEX auth_group_permissions_pkey ON public.auth_group_permissions USING btree (id) |
| public | auth_permission | auth_permission_content_type_id_2f476e4b | CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id) |
| public | auth_permission | auth_permission_content_type_id_codename_01ab375a_uniq | CREATE UNIQUE INDEX auth_permission_content_type_id_codename_01ab375a_uniq ON public.auth_permission USING btree (content_type_id, codename) |
| public | auth_permission | auth_permission_pkey | CREATE UNIQUE INDEX auth_permission_pkey ON public.auth_permission USING btree (id) |
| public | auth_user | auth_user_pkey | CREATE UNIQUE INDEX auth_user_pkey ON public.auth_user USING btree (id) |
| public | auth_user | auth_user_username_6821ab7c_like | CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops) |
| public | auth_user | auth_user_username_key | CREATE UNIQUE INDEX auth_user_username_key ON public.auth_user USING btree (username) |
| public | auth_user_groups | auth_user_groups_group_id_97559544 | CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id) |
| public | auth_user_groups | auth_user_groups_pkey | CREATE UNIQUE INDEX auth_user_groups_pkey ON public.auth_user_groups USING btree (id) |
| public | auth_user_groups | auth_user_groups_user_id_6a12ed8b | CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id) |
| public | auth_user_groups | auth_user_groups_user_id_group_id_94350c0c_uniq | CREATE UNIQUE INDEX auth_user_groups_user_id_group_id_94350c0c_uniq ON public.auth_user_groups USING btree (user_id, group_id) |
| public | auth_user_user_permissions | auth_user_user_permissions_permission_id_1fbb5f2c | CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id) |
| public | auth_user_user_permissions | auth_user_user_permissions_pkey | CREATE UNIQUE INDEX auth_user_user_permissions_pkey ON public.auth_user_user_permissions USING btree (id) |
| public | auth_user_user_permissions | auth_user_user_permissions_user_id_a95ead1b | CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id) |
| public | auth_user_user_permissions | auth_user_user_permissions_user_id_permission_id_14a6b632_uniq | CREATE UNIQUE INDEX auth_user_user_permissions_user_id_permission_id_14a6b632_uniq ON public.auth_user_user_permissions USING btree (user_id, permission_id) |
| public | campana_envios | campana_env_campana_5e5491_idx | CREATE INDEX campana_env_campana_5e5491_idx ON public.campana_envios USING btree (campana_id, estado) |
| public | campana_envios | campana_env_cliente_3ae355_idx | CREATE INDEX campana_env_cliente_3ae355_idx ON public.campana_envios USING btree (cliente_id, estado) |
| public | campana_envios | campana_envios_campana_id_5dcf9002 | CREATE INDEX campana_envios_campana_id_5dcf9002 ON public.campana_envios USING btree (campana_id) |
| public | campana_envios | campana_envios_cliente_id_22177c69 | CREATE INDEX campana_envios_cliente_id_22177c69 ON public.campana_envios USING btree (cliente_id) |
| public | campana_envios | campana_envios_cliente_id_22177c69_like | CREATE INDEX campana_envios_cliente_id_22177c69_like ON public.campana_envios USING btree (cliente_id varchar_pattern_ops) |
| public | campana_envios | campana_envios_pkey | CREATE UNIQUE INDEX campana_envios_pkey ON public.campana_envios USING btree (id) |
| public | campana_envios | uniq_campana_cliente_programado | CREATE UNIQUE INDEX uniq_campana_cliente_programado ON public.campana_envios USING btree (campana_id, cliente_id, programado_para) |
| public | campana_templates | campana_tem_nombre_eed262_idx | CREATE INDEX campana_tem_nombre_eed262_idx ON public.campana_templates USING btree (nombre, idioma) |
| public | campana_templates | campana_templates_nombre_af0822c6 | CREATE INDEX campana_templates_nombre_af0822c6 ON public.campana_templates USING btree (nombre) |
| public | campana_templates | campana_templates_nombre_af0822c6_like | CREATE INDEX campana_templates_nombre_af0822c6_like ON public.campana_templates USING btree (nombre varchar_pattern_ops) |
| public | campana_templates | campana_templates_pkey | CREATE UNIQUE INDEX campana_templates_pkey ON public.campana_templates USING btree (id) |
| public | campanas | campanas_nombre_fba5deaf | CREATE INDEX campanas_nombre_fba5deaf ON public.campanas USING btree (nombre) |
| public | campanas | campanas_nombre_fba5deaf_like | CREATE INDEX campanas_nombre_fba5deaf_like ON public.campanas USING btree (nombre varchar_pattern_ops) |
| public | campanas | campanas_pkey | CREATE UNIQUE INDEX campanas_pkey ON public.campanas USING btree (id) |
| public | campanas | campanas_template_id_4a1183f4 | CREATE INDEX campanas_template_id_4a1183f4 ON public.campanas USING btree (template_id) |
| public | clientes | clientes_phone_number_2031c6d5_like | CREATE INDEX clientes_phone_number_2031c6d5_like ON public.clientes USING btree (phone_number varchar_pattern_ops) |
| public | clientes | clientes_pkey | CREATE UNIQUE INDEX clientes_pkey ON public.clientes USING btree (phone_number) |
| public | config | config_id_4d1475e4_like | CREATE INDEX config_id_4d1475e4_like ON public.config USING btree (id varchar_pattern_ops) |
| public | config | config_pkey | CREATE UNIQUE INDEX config_pkey ON public.config USING btree (id) |
| public | config | config_seccion_1f411781 | CREATE INDEX config_seccion_1f411781 ON public.config USING btree (seccion) |
| public | config | config_seccion_1f411781_like | CREATE INDEX config_seccion_1f411781_like ON public.config USING btree (seccion varchar_pattern_ops) |
| public | django_admin_log | django_admin_log_content_type_id_c4bce8eb | CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id) |
| public | django_admin_log | django_admin_log_pkey | CREATE UNIQUE INDEX django_admin_log_pkey ON public.django_admin_log USING btree (id) |
| public | django_admin_log | django_admin_log_user_id_c564eba6 | CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id) |
| public | django_apscheduler_djangojob | django_apscheduler_djangojob_next_run_time_2f022619 | CREATE INDEX django_apscheduler_djangojob_next_run_time_2f022619 ON public.django_apscheduler_djangojob USING btree (next_run_time) |
| public | django_apscheduler_djangojob | django_apscheduler_djangojob_pkey | CREATE UNIQUE INDEX django_apscheduler_djangojob_pkey ON public.django_apscheduler_djangojob USING btree (id) |
| public | django_apscheduler_djangojobexecution | django_apscheduler_djangojobexecution_job_id_daf5090a | CREATE INDEX django_apscheduler_djangojobexecution_job_id_daf5090a ON public.django_apscheduler_djangojobexecution USING btree (job_id) |
| public | django_apscheduler_djangojobexecution | django_apscheduler_djangojobexecution_pkey | CREATE UNIQUE INDEX django_apscheduler_djangojobexecution_pkey ON public.django_apscheduler_djangojobexecution USING btree (id) |
| public | django_apscheduler_djangojobexecution | django_apscheduler_djangojobexecution_run_time_16edd96b | CREATE INDEX django_apscheduler_djangojobexecution_run_time_16edd96b ON public.django_apscheduler_djangojobexecution USING btree (run_time) |
| public | django_apscheduler_djangojobexecution | unique_job_executions | CREATE UNIQUE INDEX unique_job_executions ON public.django_apscheduler_djangojobexecution USING btree (job_id, run_time) |
| public | django_content_type | django_content_type_app_label_model_76bd3d3b_uniq | CREATE UNIQUE INDEX django_content_type_app_label_model_76bd3d3b_uniq ON public.django_content_type USING btree (app_label, model) |
| public | django_content_type | django_content_type_pkey | CREATE UNIQUE INDEX django_content_type_pkey ON public.django_content_type USING btree (id) |
| public | django_migrations | django_migrations_pkey | CREATE UNIQUE INDEX django_migrations_pkey ON public.django_migrations USING btree (id) |
| public | django_session | django_session_expire_date_a5c62663 | CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date) |
| public | django_session | django_session_pkey | CREATE UNIQUE INDEX django_session_pkey ON public.django_session USING btree (session_key) |
| public | django_session | django_session_session_key_c0390e0f_like | CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops) |
| public | generic_job_configs | generic_job_configs_chained_job_id_748cdabd | CREATE INDEX generic_job_configs_chained_job_id_748cdabd ON public.generic_job_configs USING btree (chained_job_id) |
| public | generic_job_configs | generic_job_configs_name_a9eb30d3_like | CREATE INDEX generic_job_configs_name_a9eb30d3_like ON public.generic_job_configs USING btree (name varchar_pattern_ops) |
| public | generic_job_configs | generic_job_configs_name_key | CREATE UNIQUE INDEX generic_job_configs_name_key ON public.generic_job_configs USING btree (name) |
| public | generic_job_configs | generic_job_configs_owner_id_76233a8b | CREATE INDEX generic_job_configs_owner_id_76233a8b ON public.generic_job_configs USING btree (owner_id) |
| public | generic_job_configs | generic_job_configs_pkey | CREATE UNIQUE INDEX generic_job_configs_pkey ON public.generic_job_configs USING btree (id) |
| public | generic_job_configs | gjobcfg_last_run_idx | CREATE INDEX gjobcfg_last_run_idx ON public.generic_job_configs USING btree (last_run_at) |
| public | generic_job_configs | gjobcfg_sched_idx | CREATE INDEX gjobcfg_sched_idx ON public.generic_job_configs USING btree (enabled, paused, schedule_type) |
| public | generic_job_run_logs | generic_job_run_logs_config_id_24f29e59 | CREATE INDEX generic_job_run_logs_config_id_24f29e59 ON public.generic_job_run_logs USING btree (config_id) |
| public | generic_job_run_logs | generic_job_run_logs_job_type_5d8fed31 | CREATE INDEX generic_job_run_logs_job_type_5d8fed31 ON public.generic_job_run_logs USING btree (job_type) |
| public | generic_job_run_logs | generic_job_run_logs_job_type_5d8fed31_like | CREATE INDEX generic_job_run_logs_job_type_5d8fed31_like ON public.generic_job_run_logs USING btree (job_type varchar_pattern_ops) |
| public | generic_job_run_logs | generic_job_run_logs_pkey | CREATE UNIQUE INDEX generic_job_run_logs_pkey ON public.generic_job_run_logs USING btree (id) |
| public | generic_job_run_logs | generic_job_run_logs_source_identifier_0e9369b3 | CREATE INDEX generic_job_run_logs_source_identifier_0e9369b3 ON public.generic_job_run_logs USING btree (source_identifier) |
| public | generic_job_run_logs | generic_job_run_logs_source_identifier_0e9369b3_like | CREATE INDEX generic_job_run_logs_source_identifier_0e9369b3_like ON public.generic_job_run_logs USING btree (source_identifier varchar_pattern_ops) |
| public | generic_job_run_logs | generic_job_run_logs_user_id_4467a0e9 | CREATE INDEX generic_job_run_logs_user_id_4467a0e9 ON public.generic_job_run_logs USING btree (user_id) |
| public | generic_job_run_logs | gjoblog_job_type_idx | CREATE INDEX gjoblog_job_type_idx ON public.generic_job_run_logs USING btree (job_type) |
| public | generic_job_run_logs | gjoblog_source_idx | CREATE INDEX gjoblog_source_idx ON public.generic_job_run_logs USING btree (source_identifier) |
| public | generic_job_run_logs | gjoblog_started_idx | CREATE INDEX gjoblog_started_idx ON public.generic_job_run_logs USING btree (started_at) |
| public | generic_job_run_logs | gjoblog_status_idx | CREATE INDEX gjoblog_status_idx ON public.generic_job_run_logs USING btree (status) |
| public | mensajes | mensajes_created_at_f424f0e0 | CREATE INDEX mensajes_created_at_f424f0e0 ON public.mensajes USING btree (created_at) |
| public | mensajes | mensajes_delivery_status_77f7bad6 | CREATE INDEX mensajes_delivery_status_77f7bad6 ON public.mensajes USING btree (delivery_status) |
| public | mensajes | mensajes_delivery_status_77f7bad6_like | CREATE INDEX mensajes_delivery_status_77f7bad6_like ON public.mensajes USING btree (delivery_status varchar_pattern_ops) |
| public | mensajes | mensajes_direccion_077f8f1a | CREATE INDEX mensajes_direccion_077f8f1a ON public.mensajes USING btree (direccion) |
| public | mensajes | mensajes_direccion_077f8f1a_like | CREATE INDEX mensajes_direccion_077f8f1a_like ON public.mensajes USING btree (direccion varchar_pattern_ops) |
| public | mensajes | mensajes_phone_number_f6380504 | CREATE INDEX mensajes_phone_number_f6380504 ON public.mensajes USING btree (phone_number) |
| public | mensajes | mensajes_phone_number_f6380504_like | CREATE INDEX mensajes_phone_number_f6380504_like ON public.mensajes USING btree (phone_number varchar_pattern_ops) |
| public | mensajes | mensajes_pkey | CREATE UNIQUE INDEX mensajes_pkey ON public.mensajes USING btree (id) |
| public | mensajes | mensajes_process_after_ms_bf74b60a | CREATE INDEX mensajes_process_after_ms_bf74b60a ON public.mensajes USING btree (process_after_ms) |
| public | mensajes | mensajes_queue_status_3e27b00c | CREATE INDEX mensajes_queue_status_3e27b00c ON public.mensajes USING btree (queue_status) |
| public | mensajes | mensajes_queue_status_3e27b00c_like | CREATE INDEX mensajes_queue_status_3e27b00c_like ON public.mensajes USING btree (queue_status varchar_pattern_ops) |
| public | mensajes | mensajes_timestamp_ms_7b7f9edb | CREATE INDEX mensajes_timestamp_ms_7b7f9edb ON public.mensajes USING btree (timestamp_ms) |
| public | mensajes | mensajes_tipo_7ab427e3 | CREATE INDEX mensajes_tipo_7ab427e3 ON public.mensajes USING btree (tipo) |
| public | mensajes | mensajes_tipo_7ab427e3_like | CREATE INDEX mensajes_tipo_7ab427e3_like ON public.mensajes USING btree (tipo varchar_pattern_ops) |
| public | mensajes | mensajes_wa_message_id_2798a806 | CREATE INDEX mensajes_wa_message_id_2798a806 ON public.mensajes USING btree (wa_message_id) |
| public | mensajes | mensajes_wa_message_id_2798a806_like | CREATE INDEX mensajes_wa_message_id_2798a806_like ON public.mensajes USING btree (wa_message_id varchar_pattern_ops) |
| public | mensajes | msg_queue_dir_status_idx | CREATE INDEX msg_queue_dir_status_idx ON public.mensajes USING btree (direccion, queue_status) |
| public | mensajes | msg_queue_due_idx | CREATE INDEX msg_queue_due_idx ON public.mensajes USING btree (queue_status, process_after_ms) |
| public | mensajes | uniq_inbound_wa_message_id | CREATE UNIQUE INDEX uniq_inbound_wa_message_id ON public.mensajes USING btree (wa_message_id) WHERE (((direccion)::text = 'in'::text) AND (wa_message_id IS NOT NULL)) |
| public | menu_opciones | menu_opcion_menu_id_46aee8_idx | CREATE INDEX menu_opcion_menu_id_46aee8_idx ON public.menu_opciones USING btree (menu_id, orden) |
| public | menu_opciones | menu_opcion_menu_id_75bc41_idx | CREATE INDEX menu_opcion_menu_id_75bc41_idx ON public.menu_opciones USING btree (menu_id, key) |
| public | menu_opciones | menu_opciones_menu_id_d6c73bd2 | CREATE INDEX menu_opciones_menu_id_d6c73bd2 ON public.menu_opciones USING btree (menu_id) |
| public | menu_opciones | menu_opciones_menu_id_d6c73bd2_like | CREATE INDEX menu_opciones_menu_id_d6c73bd2_like ON public.menu_opciones USING btree (menu_id varchar_pattern_ops) |
| public | menu_opciones | menu_opciones_pkey | CREATE UNIQUE INDEX menu_opciones_pkey ON public.menu_opciones USING btree (id) |
| public | menu_opciones | menu_opciones_target_menu_id_3de0c038 | CREATE INDEX menu_opciones_target_menu_id_3de0c038 ON public.menu_opciones USING btree (target_menu_id) |
| public | menu_opciones | menu_opciones_target_menu_id_3de0c038_like | CREATE INDEX menu_opciones_target_menu_id_3de0c038_like ON public.menu_opciones USING btree (target_menu_id varchar_pattern_ops) |
| public | menu_opciones | menu_opciones_target_respuesta_id_d577ddf6 | CREATE INDEX menu_opciones_target_respuesta_id_d577ddf6 ON public.menu_opciones USING btree (target_respuesta_id) |
| public | menu_opciones | menu_opciones_target_respuesta_id_d577ddf6_like | CREATE INDEX menu_opciones_target_respuesta_id_d577ddf6_like ON public.menu_opciones USING btree (target_respuesta_id varchar_pattern_ops) |
| public | menu_opciones | uniq_menu_key | CREATE UNIQUE INDEX uniq_menu_key ON public.menu_opciones USING btree (menu_id, key) |
| public | menus | menus_id_eeef60ad_like | CREATE INDEX menus_id_eeef60ad_like ON public.menus USING btree (id varchar_pattern_ops) |
| public | menus | menus_orden_0639551f | CREATE INDEX menus_orden_0639551f ON public.menus USING btree (orden) |
| public | menus | menus_parent_id_52b006c5 | CREATE INDEX menus_parent_id_52b006c5 ON public.menus USING btree (parent_id) |
| public | menus | menus_parent_id_52b006c5_like | CREATE INDEX menus_parent_id_52b006c5_like ON public.menus USING btree (parent_id varchar_pattern_ops) |
| public | menus | menus_pkey | CREATE UNIQUE INDEX menus_pkey ON public.menus USING btree (id) |
| public | respuestas | respuestas_categoria_06ed19cc | CREATE INDEX respuestas_categoria_06ed19cc ON public.respuestas USING btree (categoria) |
| public | respuestas | respuestas_categoria_06ed19cc_like | CREATE INDEX respuestas_categoria_06ed19cc_like ON public.respuestas USING btree (categoria varchar_pattern_ops) |
| public | respuestas | respuestas_id_1b357707_like | CREATE INDEX respuestas_id_1b357707_like ON public.respuestas USING btree (id varchar_pattern_ops) |
| public | respuestas | respuestas_pkey | CREATE UNIQUE INDEX respuestas_pkey ON public.respuestas USING btree (id) |
| public | sesiones | sesiones_phone_number_31f35e20_like | CREATE INDEX sesiones_phone_number_31f35e20_like ON public.sesiones USING btree (phone_number varchar_pattern_ops) |
| public | sesiones | sesiones_pkey | CREATE UNIQUE INDEX sesiones_pkey ON public.sesiones USING btree (phone_number) |
| public | waba_config | uniq_active_waba_config | CREATE UNIQUE INDEX uniq_active_waba_config ON public.waba_config USING btree (active) WHERE active |
| public | waba_config | waba_config_active_9559a999 | CREATE INDEX waba_config_active_9559a999 ON public.waba_config USING btree (active) |
| public | waba_config | waba_config_name_98abb1f3_like | CREATE INDEX waba_config_name_98abb1f3_like ON public.waba_config USING btree (name varchar_pattern_ops) |
| public | waba_config | waba_config_name_key | CREATE UNIQUE INDEX waba_config_name_key ON public.waba_config USING btree (name) |
| public | waba_config | waba_config_pkey | CREATE UNIQUE INDEX waba_config_pkey ON public.waba_config USING btree (id) |

