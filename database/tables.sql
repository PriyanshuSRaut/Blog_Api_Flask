CREATE TABLE
    blog_users(
        id INT AUTO_INCREMENT,
        user_name VARCHAR(50) NOT NULL,
        user_email VARCHAR(255) NOT NULL,
        user_password VARCHAR(255) NOT NULL,
        user_avatar VARCHAR(255) DEFAULT "",
        verified TINYINT(1) DEFAULT FALSE,
        token VARCHAR(255) DEFAULT "",
        PRIMARY KEY (id)
    );