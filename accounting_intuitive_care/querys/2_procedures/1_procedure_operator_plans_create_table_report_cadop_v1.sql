-- DROP PROCEDURE operator_plans.create_table_report_cadop();

CREATE OR REPLACE PROCEDURE operator_plans.create_table_report_cadop()
 LANGUAGE plpgsql
AS $procedure$
DECLARE

	table_name TEXT;
	
BEGIN
	
	table_name := 'report_cadop';
	
	EXECUTE format('DROP TABLE IF EXISTS operator_plans.%I', table_name);

        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS operator_plans.%I (
                id SERIAL PRIMARY KEY,
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
            )', table_name
        );
	EXECUTE 'CREATE UNIQUE INDEX IF NOT EXISTS idx_registro_ans ON operator_plans.report_cadop (registro_ans)';
END
$procedure$
;
