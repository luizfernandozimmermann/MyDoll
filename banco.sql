
CREATE TABLE IF NOT EXISTS colecoes_estoque (
  id INT PRIMARY KEY AUTO_INCREMENT,
  colecao VARCHAR(100) NOT NULL,
  ativo INT NOT NULL);



CREATE TABLE IF NOT EXISTS produtos_estoque (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_colecao INT NOT NULL,
  imagem VARCHAR(100) NOT NULL,
  produto VARCHAR(100) NOT NULL,
  preco FLOAT NOT NULL,
  ativo INT NOT NULL,
  FOREIGN KEY (id_colecao) REFERENCES colecoes_estoque(id));



CREATE TABLE IF NOT EXISTS subprodutos_estoque (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_produto INT NOT NULL,
  imagem VARCHAR(100) NOT NULL,
  subproduto VARCHAR(100) NOT NULL,
  quantidade INT NOT NULL,
  ativo INT NOT NULL,
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id));


CREATE TABLE IF NOT EXISTS agenda (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL,
  data_entrega DATE NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  ativo INT NOT NULL,
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id)
    );



CREATE TABLE IF NOT EXISTS historico_agenda (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL,
  data_entrega DATE NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  forma_pagamento VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id));



CREATE TABLE IF NOT EXISTS feiras (
  id INT PRIMARY KEY AUTO_INCREMENT,
  data_feira DATE NOT NULL,
  horario_inicio VARCHAR(45) NOT NULL,
  horario_final VARCHAR(45) NOT NULL,
  nome_feira VARCHAR(45) NOT NULL,
  local_feira VARCHAR(45) NOT NULL,
  descricao VARCHAR(45) NOT NULL,
  ativo INT NOT NULL);


CREATE TABLE IF NOT EXISTS produtos_feira (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_feira INT NOT NULL,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL,
  ativo INT NOT NULL,
    FOREIGN KEY (id_feira)
    REFERENCES feiras (id),
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id));



CREATE TABLE IF NOT EXISTS historico_feiras (
  id INT PRIMARY KEY AUTO_INCREMENT,
  horario_inicio VARCHAR(45) NOT NULL,
  horario_final VARCHAR(45) NOT NULL,
  nome_feira VARCHAR(45) NOT NULL,
  local_feira VARCHAR(45) NOT NULL,
  data_feira DATE NOT NULL,
  descricao VARCHAR(45) NOT NULL);


CREATE TABLE IF NOT EXISTS historico_feiras_vendas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_historico_feira INT NOT NULL,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL,
  descricao VARCHAR(45) NOT NULL,
  preco FLOAT NOT NULL,
  forma_pagamento VARCHAR(45) NOT NULL,
    FOREIGN KEY (id_historico_feira)
    REFERENCES historico_feiras (id),
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id));



CREATE TABLE IF NOT EXISTS feiras_vendas (
  id INT PRIMARY KEy AUTO_INCREMENT,
  id_feira INT NOT NULL,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL,
  descricao VARCHAR(45) NOT NULL,
  preco FLOAT NOT NULL,
  forma_pagamento VARCHAR(45) NOT NULL,
  ativo INT NOT NULL,
    FOREIGN KEY (id_feira)
    REFERENCES feiras (id),
    FOREIGN KEY (id_produto)
    REFERENCES produtos_estoque (id));


CREATE TABLE IF NOT EXISTS financas_atual (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  local VARCHAR(45) NOT NULL,
  data DATE NOT NULL,
  forma_pagamento VARCHAR(45) NOT NULL,
  preco FLOAT NOT NULL,
  descricao VARCHAR(45) NOT NULL,
  ativo INT NOT NULL);



CREATE TABLE IF NOT EXISTS historico_financas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  mes VARCHAR(2) NOT NULL,
  ano VARCHAR(2) NOT NULL);



CREATE TABLE IF NOT EXISTS historico_financas_compras (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_historico_financas INT NOT NULL,
  nome VARCHAR(45) NOT NULL,
  local VARCHAR(45) NOT NULL,
  data DATE NOT NULL,
  forma_pagamento VARCHAR(45) NOT NULL,
  preco FLOAT NOT NULL,
  descricao VARCHAR(45) NOT NULL,
    FOREIGN KEY (id_historico_financas)
    REFERENCES historico_financas (id));
