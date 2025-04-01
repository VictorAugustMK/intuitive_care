-- DROP PROCEDURE operator_plans.report_cadop_data();

CREATE OR REPLACE PROCEDURE operator_plans.report_cadop_data()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    table_name TEXT;
    temp_table TEXT;
    file_path TEXT;
BEGIN
    -- Define corretamente o nome das tabelas
	table_name := 'operator_plans.report_cadop';
    temp_table := 'temp_report_cadop_data';
    file_path := 'C:\\repo\\intuitive_care\\accounting_intuitive_care\\operator_plans\\Relatorio_cadop.csv';
    
    -- Removendo a tabela temporária se existir
    EXECUTE format('DROP TABLE IF EXISTS %s;', temp_table);

    -- Criando a tabela temporária
    EXECUTE format(
        'CREATE TEMP TABLE %s (
            registro_ans TEXT,
            cnpj TEXT,
            razao_social TEXT,
            nome_fantasia TEXT,
            modalidade TEXT,
            logradouro TEXT,
            numero TEXT,
            complemento TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            cep TEXT,
            ddd TEXT,
            telefone TEXT,
            fax TEXT,
            endereco_eletronico TEXT,
            representante TEXT,
            cargo_representante TEXT,
            regiao_de_comercializacao INT,
            data_registro_ans DATE
        );', temp_table
    );

    -- Importando os dados do CSV
    EXECUTE format(
        'COPY %s (
            registro_ans,  -- Corrigido de "registro_operadora" para "registro_ans"
            cnpj,
            razao_social,
            nome_fantasia,
            modalidade,
            logradouro,
            numero,
            complemento,
            bairro,
            cidade,
            uf,
            cep,
            ddd,
            telefone,
            fax,
            endereco_eletronico,
            representante,
            cargo_representante,
            regiao_de_comercializacao,
            data_registro_ans
        ) 
        FROM %L 
        DELIMITER '';'' 
        CSV HEADER;',
        temp_table, file_path
    );

    -- Inserindo dados na tabela final, garantindo que os valores sejam numéricos
    EXECUTE format(
        'INSERT INTO %s (
            registro_ans,
            cnpj,
            razao_social,
            nome_fantasia,
            modalidade,
            logradouro,
            numero,
            complemento,
            bairro,
            cidade,
            uf,
            cep,
            ddd,
            telefone,
            fax,
            endereco_eletronico,
            representante,
            cargo_representante,
            regiao_de_comercializacao,
            data_registro_ans
        ) 
        SELECT 
            registro_ans,  -- Corrigido de "resgistro_ans" para "registro_ans"
            cnpj,
            razao_social,
            nome_fantasia,
            modalidade,
            logradouro,
            numero,
            complemento,
            bairro,
            cidade,
            uf,
            cep,
            ddd,
            telefone,
            fax,
            endereco_eletronico,
            representante,
            cargo_representante,
            regiao_de_comercializacao,
            data_registro_ans
        FROM %s;',
        table_name, temp_table
    );
END;
$procedure$
;
