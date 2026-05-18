CREATE SEQUENCE IF NOT EXISTS alunos_ges_matricula_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE IF NOT EXISTS alunos_gec_matricula_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE IF NOT EXISTS alunos (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    curso TEXT NOT NULL CHECK (curso IN ('GES', 'GEC')),
    matricula INTEGER NOT NULL,
    UNIQUE (curso, matricula)
);
