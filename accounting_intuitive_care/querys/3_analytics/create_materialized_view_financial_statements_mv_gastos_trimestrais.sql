CREATE MATERIALIZED VIEW financial_statements.mv_gastos_trimestrais AS
SELECT 
    cadop.razao_social AS "EMPRESA",
    cadop.nome_fantasia AS "NOME FANTASIA",
    cadop.registro_ans AS "REGISTRO ANS",
    tri.descricao AS "DESCRIÇÃO",
    (REPLACE(tri.vl_saldo_final::TEXT, ',', '.')::NUMERIC(15,2)) AS "GASTOS TRIMESTRAL FINAL",
    EXTRACT(YEAR FROM tri.data_movimento) AS "ANO",
    CASE 
        WHEN EXTRACT(MONTH FROM tri.data_movimento) BETWEEN 1 AND 3 THEN '1º Trimestre'
        WHEN EXTRACT(MONTH FROM tri.data_movimento) BETWEEN 4 AND 6 THEN '2º Trimestre'
        WHEN EXTRACT(MONTH FROM tri.data_movimento) BETWEEN 7 AND 9 THEN '3º Trimestre'
        WHEN EXTRACT(MONTH FROM tri.data_movimento) BETWEEN 10 AND 12 THEN '4º Trimestre'
        ELSE 'Data inválida'
    END AS trimestre
FROM (
    SELECT * FROM financial_statements."2023_01"
    UNION ALL
    SELECT * FROM financial_statements."2023_02"
    UNION ALL
    SELECT * FROM financial_statements."2023_03"
    UNION ALL
    SELECT * FROM financial_statements."2023_04"
    UNION ALL
    SELECT * FROM financial_statements."2024_01"
    UNION ALL
    SELECT * FROM financial_statements."2024_02"
    UNION ALL
    SELECT * FROM financial_statements."2024_03"
    UNION ALL
    SELECT * FROM financial_statements."2024_04"
) AS tri
JOIN operator_plans.report_cadop cadop
    ON tri.reg_ans = cadop.registro_ans
WHERE
    tri.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY
    tri.data_movimento,
    tri.reg_ans,
    tri.descricao,
    cadop.registro_ans,
    cadop.nome_fantasia,
    cadop.razao_social,
    tri.vl_saldo_final
ORDER BY
    "GASTOS TRIMESTRAL FINAL" DESC;