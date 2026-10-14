-- TecniGuía Pro — tablas de la base de datos (MySQL / MariaDB de Hostinger)
-- Importa este archivo en phpMyAdmin (hPanel → Bases de datos → phpMyAdmin → Importar).

CREATE TABLE IF NOT EXISTS usuarios (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(190) NOT NULL UNIQUE,
  nombre VARCHAR(120) NOT NULL,
  telefono VARCHAR(40) NOT NULL DEFAULT '',
  clave_hash VARCHAR(255) NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'prueba',   -- prueba | activo | suspendido
  vence DATETIME NULL,
  creado DATETIME NOT NULL,
  ultimo_acceso DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS visitas (
  usuario_id INT UNSIGNED NOT NULL,
  id BIGINT UNSIGNED NOT NULL,
  datos MEDIUMTEXT NOT NULL,
  actualizado DATETIME NOT NULL,
  PRIMARY KEY (usuario_id, id),
  CONSTRAINT fk_visitas_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS uso (
  usuario_id INT UNSIGNED NOT NULL,
  dia DATE NOT NULL,
  llamadas INT UNSIGNED NOT NULL DEFAULT 0,
  tokens_entrada BIGINT UNSIGNED NOT NULL DEFAULT 0,
  tokens_salida BIGINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (usuario_id, dia),
  CONSTRAINT fk_uso_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS intentos (
  ip VARCHAR(64) NOT NULL,
  email VARCHAR(190) NOT NULL,
  momento DATETIME NOT NULL,
  KEY idx_intentos (ip, momento),
  KEY idx_intentos_email (email, momento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
