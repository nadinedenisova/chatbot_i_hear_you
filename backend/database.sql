-- database.sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Создать схему content
CREATE SCHEMA IF NOT EXISTS content;

-- Создать таблицы в схеме content
CREATE TABLE content."user" (
	"id" VARCHAR(255) PRIMARY KEY,
	"phone_number" VARCHAR(255) NOT NULL,
	"created_at" TIMESTAMP NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE content.menu_node (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"parent_id" UUID,
	"name" VARCHAR(255) NOT NULL,
	"text" TEXT,
	"subscription_type" VARCHAR(255)
);

CREATE TABLE content.content (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"menu_id" UUID NOT NULL,
	"type" SMALLINT NOT NULL,
	"server_path" VARCHAR(500) NOT NULL,
	"created_at" TIMESTAMP NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE content.question (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"user_id" VARCHAR(255) NOT NULL,
	"text" TEXT NOT NULL,
	"admin_answer" TEXT,
	"created_at" TIMESTAMP NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE content.history (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"user_id" VARCHAR(255) NOT NULL,
	"action_date" TIMESTAMP NOT NULL,
	"menu_id" UUID,
	"created_at" TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE content.user_menu_node (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"user_id" VARCHAR(255) NOT NULL,
	"menu_id" UUID NOT NULL,
	"post_rating" BOOLEAN,
	"created_at" TIMESTAMP NOT NULL DEFAULT now(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT now(),
	UNIQUE ("user_id", "menu_id")
);


-- Добавление внешних ключей
ALTER TABLE content.menu_node ADD FOREIGN KEY ("parent_id") REFERENCES content.menu_node ("id");
ALTER TABLE content.content ADD FOREIGN KEY ("menu_id") REFERENCES content.menu_node ("id");
ALTER TABLE content.question ADD FOREIGN KEY ("user_id") REFERENCES content."user" ("id");
ALTER TABLE content.history ADD FOREIGN KEY ("user_id") REFERENCES content."user" ("id");
ALTER TABLE content.history ADD FOREIGN KEY ("menu_id") REFERENCES content.menu_node ("id");
ALTER TABLE content.user_menu_node ADD FOREIGN KEY ("menu_id") REFERENCES content.menu_node ("id");
ALTER TABLE content.user_menu_node ADD FOREIGN KEY ("user_id") REFERENCES content."user" ("id");


-- Вставка тестовых данных
INSERT INTO content."user" ("id", "phone_number") VALUES 
('user_001', '+79161234567'),
('user_002', '+79169876543'),
('user_003', '+79155556677'),
('225894988', '+79648773155');

INSERT INTO content.menu_node ("id", "parent_id", "name", "text", "subscription_type") VALUES 
('00000000-0000-0000-0000-000000000001', NULL, 'Главное меню', 'Здравствуйте! Я бот-помощник "ано я тебя слышу". Мы помогаем семьям с детьми с нарушением слуха. Здесь вы найдете проверенную информацию и поддержку на каждом этапе. Чтобы я мог показать вам самые нужные материалы, выберите, пожалуйста, ваш путь.', 'free'),
('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 'Я волнуюсь о слухе ребенка', 'Вы выбрали раздел для родителей. Это большой путь, и вы не одни. Мы собрали информацию по самым важным темам — от первых шагов после диагноза до вопросов школы и социализации. Выберите, что вас беспокоит в первую очередь.', 'free'),
('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001', 'Я волнуюсь о своем слухе', 'Раздел для взрослых с нарушением слуха находится в разработке.', 'free'),
('00000000-0000-0000-0000-000000000011', '00000000-0000-0000-0000-000000000002', 'Диагноз: что делать?', 'Получение диагноза — это время сильных эмоций: растерянность, страх, непонимание. Это абсолютно нормально. Давайте пройдем этот путь шаг за шагом. Что вас волнует прямо сейчас?', 'free'),
('00000000-0000-0000-0000-000000000012', '00000000-0000-0000-0000-000000000002', 'Слуховые аппараты и кохлеарные импланты', 'Компенсация слуха — важный шаг, который открывает ребенку мир звуков. Здесь мы поможем разобраться в видах аппаратов, процессе их выбора, получения и привыкания.', 'free'),
('00000000-0000-0000-0000-000000000013', '00000000-0000-0000-0000-000000000002', 'Обучение, развитие и социализация', 'Развитие ребенка с нарушением слуха имеет свои особенности. Важно правильно выстроить занятия по развитию слуха и речи, а также помочь ребенку общаться со сверстниками.', 'free'),
('00000000-0000-0000-0000-000000000014', '00000000-0000-0000-0000-000000000002', 'Инклюзия в детском саду и школе', 'Успешная инклюзия — это командная работа семьи, педагогов и ребенка. Здесь вы найдете практические руководства по правам, адаптации среды и выстраиванию отношений с образовательным учреждением.', 'free'),
('00000000-0000-0000-0000-000000000015', '00000000-0000-0000-0000-000000000002', 'Поддержка для родителей', 'Забота о себе — это необходимость. Чтобы быть опорой для ребенка, важно восстанавливать силы. Здесь вы найдете психологическую помощь, общение с теми, кто понимает, и ответы на вопросы.', 'free'),
('00000000-0000-0000-0000-000000000016', '00000000-0000-0000-0000-000000000002', 'Задать свой вопрос', 'Если вы не нашли ответа на свой вопрос в нашей библиотеке, напишите его здесь. Мы обработаем ваш запрос и добавим недостающую информацию.', 'free'),
('00000000-0000-0000-0000-000000000021', '00000000-0000-0000-0000-000000000011', 'Первые шаги: краткий план', 'Как действовать в первые дни: куда обратиться, какие документы нужны. Ключевые специалисты: сурдолог, ЛОР, аудиолог — кого и в какой последовательности посетить.', 'free'),
('00000000-0000-0000-0000-000000000022', '00000000-0000-0000-0000-000000000011', 'Как справиться с шоком?', 'Как принять новость? Что является нормальной реакцией? Поддержка семьи: как разговаривать с партнёром, родственниками. Где найти помощь: группы взаимопомощи, горячие линии, психологи.', 'free'),
('00000000-0000-0000-0000-000000000023', '00000000-0000-0000-0000-000000000011', 'Понимание диагноза', 'Типы нарушений слуха: лёгкая, средняя, тяжёлая, глухота. Почему это важно: как тип и степень влияют на методы коррекции. Может ли слух измениться: динамика состояния, контрольные проверки.', 'free');

INSERT INTO content.content ("menu_id", "type", "server_path") VALUES 
('00000000-0000-0000-0000-000000000011', 1, 'https://example.com/images/diagnosis_help.jpg'),
('00000000-0000-0000-0000-000000000011', 2, 'https://example.com/videos/first_steps.mp4'),
('00000000-0000-0000-0000-000000000012', 1, 'https://example.com/images/hearing_aids.jpg'),
('00000000-0000-0000-0000-000000000012', 3, 'https://example.com/documents/guide.pdf');

INSERT INTO content.question ("user_id", "text", "admin_answer") VALUES 
('user_001', 'Какой график работы вашей службы поддержки?', 'Наша служба поддержки работает с 9:00 до 18:00 по московскому времени в рабочие дни.'),
('user_002', 'Можно ли получить консультацию сурдолога онлайн?', 'Да, мы организуем онлайн-консультации со специалистами. Заполните форму на нашем сайте.'),
('user_003', 'Какие документы нужны для получения слухового аппарата?', NULL);

INSERT INTO content.history ("user_id", "menu_id", "action_date") VALUES 
('user_001', '00000000-0000-0000-0000-000000000001', '2024-01-15 10:00:00'),
('user_001', '00000000-0000-0000-0000-000000000002', '2024-01-15 10:05:00'),
('user_001', '00000000-0000-0000-0000-000000000011', '2024-01-15 10:10:00'),
('user_002', '00000000-0000-0000-0000-000000000001', '2024-01-16 11:00:00'),
('user_002', '00000000-0000-0000-0000-000000000012', '2024-01-16 11:15:00'),
('225894988', '00000000-0000-0000-0000-000000000001', '2024-01-16 11:15:00');

INSERT INTO content.user_menu_node ("user_id", "menu_id", "post_rating") VALUES 
('user_001', '00000000-0000-0000-0000-000000000001', TRUE),
('user_001', '00000000-0000-0000-0000-000000000011', TRUE),
('user_001', '00000000-0000-0000-0000-000000000012', TRUE),
('user_002', '00000000-0000-0000-0000-000000000001', TRUE),
('user_002', '00000000-0000-0000-0000-000000000011', FALSE),
('user_002', '00000000-0000-0000-0000-000000000012', FALSE),
('user_002', '00000000-0000-0000-0000-000000000013', FALSE),
('user_003', '00000000-0000-0000-0000-000000000001', FALSE),
('user_003', '00000000-0000-0000-0000-000000000011', TRUE),
('user_003', '00000000-0000-0000-0000-000000000013', FALSE);


-- Создание индексов
CREATE INDEX CONCURRENTLY idx_menu_node_parent_id ON content.menu_node(parent_id) WHERE parent_id IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_content_menu_id ON content.content(menu_id);
CREATE INDEX CONCURRENTLY idx_history_user_id ON content.history(user_id);
CREATE INDEX CONCURRENTLY idx_history_menu_id ON content.history(menu_id) WHERE menu_id IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_question_user_id ON content.question(user_id);
CREATE INDEX CONCURRENTLY idx_history_user_action_date ON content.history(user_id, action_date);
CREATE INDEX CONCURRENTLY idx_user_menu_node_menu_id_rating ON content.user_menu_node (menu_id, post_rating);
CREATE INDEX CONCURRENTLY idx_user_menu_node_menu_id ON content.user_menu_node(menu_id);