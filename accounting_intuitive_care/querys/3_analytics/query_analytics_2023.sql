

-- 10 operadoras com maiores despesas na "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" categoria no último trimestre
select
	cadop.razao_social as "EMPRESA",
	cadop.nome_fantasia as "NOME FANTASIA",
    cadop.registro_ans AS "REGISTRO ANS",
    tri_01.descricao AS "DESCRIÇÃO",
    (REPLACE(tri_01.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2)) AS "GASTOS TRIMESTRAL FINAL",
    TO_CHAR(tri_01.data_movimento, 'DD/MM/YYYY') AS "DATA MOVIMENTO"
FROM 
	financial_statements."2023_01" as tri_01 -- Altere entre 2023_01, 2023_02, 2023_03, 2023_04
JOIN operator_plans.report_cadop cadop
    ON tri_01.reg_ans = cadop.registro_ans
WHERE
	tri_01.descricao like '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
GROUP BY
    tri_01.data_movimento,
    tri_01.reg_ans,
    tri_01.descricao,
    cadop.registro_ans,
    cadop.nome_fantasia,
    cadop.razao_social,
    tri_01.vl_saldo_final
ORDER BY
    "GASTOS TRIMESTRAL FINAL" DESC
LIMIT 10;


-- 10 operadoras com maiores despesas na "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" categoria no último trimestre
SELECT
	cadop.razao_social as "EMPRESA",
	cadop.nome_fantasia as "NOME FANTASIA",
    cadop.registro_ans AS "REGISTRO ANS",
    report_year_2023.descricao AS "DESCRIÇÃO",
    SUM(REPLACE(report_year_2023.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2)) AS "GASTOS TRIMESTRAL FINAL",
    report_year_2023.data_movimento AS "DATA MOVIMENTO"
FROM 
	(
		SELECT 
			tri_01.reg_ans,
			tri_01.descricao,
    		REPLACE(tri_01.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2) AS vl_saldo_final,
    		TO_CHAR(tri_01.data_movimento, 'DD/MM/YYYY') as data_movimento
		FROM
			financial_statements."2023_01" as tri_01
		WHERE
			tri_01.descricao like '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
		
			
		UNION ALL
			
		SELECT 
			tri_02.reg_ans,
			tri_02.descricao,
    		REPLACE(tri_02.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2) AS vl_saldo_final,
    		TO_CHAR(tri_02.data_movimento, 'DD/MM/YYYY') as data_movimento
		FROM 
			financial_statements."2023_02" as tri_02
		WHERE
			tri_02.descricao like '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
			
		UNION ALL 
		
		SELECT 
			tri_03.reg_ans,
			tri_03.descricao,
    		REPLACE(tri_03.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2) AS vl_saldo_final,
    		TO_CHAR(tri_03.data_movimento, 'DD/MM/YYYY') as data_movimento
		FROM 
			financial_statements."2023_03" as tri_03
		WHERE
			tri_03.descricao like '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
			
		UNION ALL 
		
		SELECT 
			tri_04.reg_ans,
			tri_04.descricao,
    		REPLACE(tri_04.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2) AS vl_saldo_final,
    		TO_CHAR(tri_04.data_movimento, 'DD/MM/YYYY') as data_movimento
		FROM 
			financial_statements."2023_04" as tri_04
		WHERE
			tri_04.descricao like '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %'
		) AS report_year_2023
JOIN operator_plans.report_cadop cadop
    ON report_year_2023.reg_ans = cadop.registro_ans
GROUP BY
    report_year_2023.data_movimento,
    report_year_2023.reg_ans,
    cadop.nome_fantasia,
    cadop.razao_social,
    report_year_2023.descricao,
    cadop.representante,
    cadop.registro_ans
ORDER BY
    "GASTOS TRIMESTRAL FINAL" DESC
LIMIT 10;
		
		
		
		