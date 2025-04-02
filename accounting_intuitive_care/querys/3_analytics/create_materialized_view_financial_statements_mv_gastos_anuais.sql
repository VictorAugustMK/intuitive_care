CREATE MATERIALIZED VIEW financial_statements.mv_gastos_anuais AS
SELECT
    gt."EMPRESA",
    gt."NOME FANTASIA",
    gt."REGISTRO ANS",
    gt."DESCRIÇÃO",
    gt."ANO",
    gt."GASTOS TRIMESTRAL FINAL" AS "GASTOS ANUAIS"
FROM 
    financial_statements.mv_gastos_trimestrais AS gt
GROUP BY 
    gt."EMPRESA",
    gt."NOME FANTASIA",
    gt."REGISTRO ANS",
    gt."DESCRIÇÃO",
    gt."ANO",gt."GASTOS TRIMESTRAL FINAL"
ORDER BY
    "GASTOS ANUAIS" DESC
LIMIT 10;

SELECT DISTINCT "ANO" FROM financial_statements.mv_gastos_trimestrais ORDER BY "ANO" DESC
