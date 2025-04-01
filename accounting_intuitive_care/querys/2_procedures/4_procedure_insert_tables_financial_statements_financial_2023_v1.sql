-- DROP PROCEDURE financial_statements.financial_quarter_2023_v1();

CREATE OR REPLACE PROCEDURE financial_statements.financial_quarter_2023_v1()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    i INT;
    table_name TEXT;
    temp_table TEXT;
    file_path TEXT;
BEGIN
    FOR i IN 1..4 LOOP
        -- Define corretamente o nome das tabelas
        table_name := format('financial_statements.%I', format('2023_0%s', i));
        temp_table := format('financial_statements_temp_2023_0%s', i);
        file_path := format('C:\\repo\\intuitive_care\\accounting_intuitive_care\\financial_statements\\2023\\%sT2023.csv', i);
        
        -- Removendo a tabela temporária se existir
        EXECUTE format('DROP TABLE IF EXISTS %I;', temp_table);

        -- Criando a tabela temporária
        EXECUTE format(
            'CREATE TEMP TABLE %I (
                data_movimento DATE,
                reg_ans TEXT,
                cd_conta_contabil INT,
                descricao TEXT,
                vl_saldo_inicial TEXT, -- Tipo TEXT temporário para facilitar a importação
                vl_saldo_final TEXT
            );', temp_table
        );

        -- Importando os dados do CSV
        EXECUTE format(
            'COPY %I (data_movimento, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
             FROM %L DELIMITER '';'' CSV HEADER;',
            temp_table, file_path
        );

        -- Convertendo valores para NUMERIC corretamente
        EXECUTE format(
            'UPDATE %I 
             SET vl_saldo_inicial = NULLIF(REPLACE(vl_saldo_inicial, '','', ''.''), '''')::NUMERIC(15,2),
                 vl_saldo_final = NULLIF(REPLACE(vl_saldo_final, '','', ''.''), '''')::NUMERIC(15,2)
             WHERE vl_saldo_inicial IS NOT NULL AND vl_saldo_final IS NOT NULL;',
            temp_table
        );

        -- Inserindo dados na tabela final, garantindo que os valores sejam numéricos
		EXECUTE format(
            'INSERT INTO %s (data_movimento, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
             SELECT data_movimento, reg_ans, cd_conta_contabil, descricao, 
                    vl_saldo_inicial::NUMERIC(15,2), 
                    vl_saldo_final::NUMERIC(15,2)
             FROM %I;',
            table_name, temp_table
        );

    END LOOP;
END;
$procedure$
;
