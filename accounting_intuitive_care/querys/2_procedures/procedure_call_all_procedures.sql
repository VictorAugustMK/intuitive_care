
-- Chama a procedures de criação das tabelas trimestrais de 2023 e 2024
call financial_statements.financial_2023_v1();
call financial_statements.financial_2024_v1();

-- Chama as procedures de insert de dados dos trimestrais de 2023 e 2024
call financial_statements.financial_quarter_2023_v1();
call financial_statements.financial_quarter_2024_v1();
