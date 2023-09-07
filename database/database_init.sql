CREATE TABLE CARGO(
    id_cargo INTEGER NOT NULL PRIMARY KEY,
    cargo VARCHAR(50) NOT NULL
);

CREATE TABLE PARTIDO(
    id_partido INTEGER NOT NULL PRIMARY KEY,
    nombre_partido VARCHAR(75) NOT NULL,
    siglas VARCHAR(15) NOT NULL,
    fundacion DATE NOT NULL
);

CREATE TABLE DEPARTAMENTO(
    id_departamento INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL
);

CREATE TABLE MESA(
    id_mesa INTEGER NOT NULL PRIMARY KEY,
    id_departamento INTEGER,
    FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO (id_departamento)
);

CREATE TABLE CIUDADANO(
    dpi_ciudadano BIGINT NOT NULL PRIMARY KEY,
    nombre VARCHAR(15) NOT NULL,
    apellido VARCHAR(15) NOT NULL,
    direccion VARCHAR(250) NOT NULL,
    telefono INTEGER NOT NULL,
    edad INTEGER NOT NULL,
    genero CHAR(1) NOT NULL
);

CREATE TABLE VOTACION(
    id_voto INTEGER NOT NULL PRIMARY KEY,
    id_mesa INTEGER NOT NULL,
    dpi_ciudadano BIGINT NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    FOREIGN KEY (id_mesa) REFERENCES MESA (id_mesa),
    FOREIGN KEY (dpi_ciudadano) REFERENCES CIUDADANO (dpi_ciudadano)
);

CREATE TABLE CANDIDATO(
    id_candidato INTEGER NOT NULL PRIMARY KEY,
    id_cargo INTEGER NOT NULL,
    id_partido INTEGER NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES CARGO (id_cargo),
    FOREIGN KEY (id_partido) REFERENCES PARTIDO (id_partido)
);

CREATE TABLE CANDIDATO_VOTADO(
    id_votado INTEGER NOT NULL PRIMARY KEY,
    id_voto INTEGER NOT NULL,
    id_candidato INTEGER NOT NULL,
    FOREIGN KEY (id_voto) REFERENCES VOTACION (id_voto),
    FOREIGN KEY (id_candidato) REFERENCES CANDIDATO (id_candidato)
);