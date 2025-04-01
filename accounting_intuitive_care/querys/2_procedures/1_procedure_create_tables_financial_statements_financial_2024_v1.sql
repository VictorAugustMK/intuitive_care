-- DROP PROCEDURE financial_statements.financial_2024_v1();

CREATE OR REPLACE PROCEDURE financial_statements.financial_2024_v1()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    i INT;
    table_name TEXT;
BEGIN

    EXECUTE 'GRANT ALL ON SCHEMA financial_statements TO postgres';

    FOR i IN 1..4 LOOP

        table_name := format('2024_%s', LPAD(i::TEXT, 2, '0'));

		EXECUTE format('DROP TABLE IF EXISTS financial_statements.%I', table_name);

        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS financial_statements.%I (
                id SERIAL PRIMARY KEY,
                data_movimento DATE NULL,
                reg_ans TEXT NULL,
                cd_conta_contabil INT NULL,
                descricao TEXT NULL,
                vl_saldo_inicial DECIMAL(15,2) NULL,
                vl_saldo_final DECIMAL(15,2) NULL
            )', table_name
        );
    END LOOP;
END;
$procedure$
;
