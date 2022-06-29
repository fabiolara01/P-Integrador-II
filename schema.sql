DROP TABLE IF EXISTS cadastros;

CREATE TABLE cadastros (
    id INTEGER NOT NULL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nome TEXT,
    contato TEXT,
    email TEXT NOT NULL,
    cidade TEXT,
    estado TEXT,
    servico TEXT NOT NULL,
    conteudo TEXT,
    numero INTEGER DEFAULT '0',
    tipo CHAR DEFAULT 'A',
    nota INTEGER DEFAULT '0'
);