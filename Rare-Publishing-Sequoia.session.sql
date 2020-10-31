DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS comments;

CREATE TABLE users (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `first_name`  TEXT NOT NULL,
    `last_name`   TEXT NOT NULL,
    `email`       TEXT NOT NULL UNIQUE,
    `display_name` TEXT NOT NULL
);

CREATE TABLE categories (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL UNIQUE
);

CREATE TABLE posts (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `title` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `publication_date` INTEGER NOT NULL,
    `header_img` TEXT,
    `category_id` INTEGER NOT NULL,
    `user_id` INTEGER NOT NULL,
    FOREIGN KEY(`category_id`) REFERENCES `categories`(`id`),
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE tags (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL UNIQUE
);

CREATE TABLE post_tags (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `post_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`post_id`) REFERENCES `posts`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `tags`(`id`)
);

CREATE TABLE comments (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `subject` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `post_id` INTEGER NOT NULL,
    `user_id` INTEGER NOT NULL,
    FOREIGN KEY(`post_id`) REFERENCES `posts`(`id`),
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
);

INSERT INTO `users` VALUES (null, 'First', 'Tester', 'firstTester@email.com', 'First Tester');
INSERT INTO `categories` VALUES (null, 'First Category');
INSERT INTO `posts` VALUES (null, 'First Post Title', 'First post content is here!', 20201031, null, 1, 1);
INSERT INTO `tags` VALUES (null, 'First tag');
INSERT INTO `post_tags` VALUES (null, 1, 1);
INSERT INTO `comments` VALUES (null, 'First comment subject', 'First comment content is here!', 1, 1);

INSERT INTO `users` VALUES (null, 'Second', 'Tester', 'secondTester@email.com', 'Second Tester');
INSERT INTO `categories` VALUES (null, 'Second Category');
INSERT INTO `posts` VALUES (null, 'Second Post Title', 'Second post content is here!', 20201031, null, 2, 2);
INSERT INTO `tags` VALUES (null, 'Second tag');
INSERT INTO `post_tags` VALUES (null, 2, 2);
INSERT INTO `comments` VALUES (null, 'Second comment subject', 'Second comment content is here!', 2, 2);


SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM posts;
SELECT * FROM tags;
SELECT * FROM post_tags;
SELECT * FROM comments;
