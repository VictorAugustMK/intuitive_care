
DROP TABLE IF EXISTS operator_plans.dictionary_operator_cadop;
CREATE TABLE IF NOT exists operator_plans.dictionary_active_plans  (
                field_name varchar NULL,
                type varchar NULL,
                size numeric NULL,
                "desc" TEXT null);

INSERT INTO operator_plans.dictionary_operator_cadop (field, type, size, desc) VALUES
('REGISTRO_OPERADORA', 'Texto', 6, 'Registro de operadora de plano privado de assistência à saúde concedido pela ANS à pessoa jurídica para operação no setor de saúde suplementar'),
('CNPJ', 'Texto', 14, 'CNPJ da Operadora'),
('Razao_Social', 'Texto', 140, 'Razão Social da Operadora'),
('Nome_Fantasia', 'Texto', 140, 'Nome Fantasia da Operadora'),
('Modalidade', 'Texto', 2, 'Classificação das operadoras de planos privados de assistência à saúde de acordo com seu estatuto jurídico'),
('Logradouro', 'Texto', 40, 'Endereço da Sede da Operadora'),
('Número', 'Texto', 20, 'Número do Endereço da Sede da Operadora'),
('Complemento', 'Texto', 40, 'Complemento do Endereço da Sede da Operadora'),
('Bairro', 'Texto', 30, 'Bairro do Endereço da Sede da Operadora'),
('Cidade', 'Texto', 30, 'Cidade do Endereço da Sede da Operadora'),
('UF', 'Texto', 2, 'Estado do Endereço da Sede da Operadora'),
('CEP', 'Texto', 8, 'CEP do Endereço da Sede da Operadora'),
('DDD', 'Texto', 4, 'Código de DDD da Operadora'),
('Telefone', 'Texto', 20, 'Número de Telefone da Operadora'),
('Fax', 'Texto', 20, 'Número de Fax da Operadora'),
('Endereco_eletronico', 'Texto', 255, 'e-mail da Operadora'),
('Representante', 'Texto', 50, 'Representante Legal da Operadora'),
('Cargo_Representante', 'Texto', 40, 'Cargo do Representante Legal da Operadora'),
('Regiao_de_Comercializacao', 'Numero', 1, 'Área onde a operadora de plano privado de assistência à saúde comercializa ou disponibiliza seu plano de saúde, conforme Resolução Normativa nº 209/2009, da ANS'),
('Data_Registro_ANS', 'Data', 8, 'Data do Registro da Operadora na ANS (formato AAAA-MM-DD)');
