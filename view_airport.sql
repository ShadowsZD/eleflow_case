
CREATE VIEW airports AS (
    WITH ranking AS (
        WITH decolagens AS(
            SELECT 
                EXTRACT(YEAR FROM "partida_Real") as "Ano",
                "icao_Aeródromo_Origem" AS "Aeroporto Origem",
                "icao_Empresa_Aérea" AS "Companhia",
                COUNT(*) AS "Decolagens"
            FROM vra
            GROUP BY 1,2,3
        ),
        pousos AS (
            SELECT 
                EXTRACT(YEAR FROM "PartidaReal") as "Ano",
                "icao_Aeródromo_Destino" AS "Aeroporto Destino",
                "icao_Empresa_Aérea" AS "Companhia",
                COUNT(*) AS "Pousos"
            FROM vra
            GROUP BY 1,2,3
        ), airports as (
            SELECT 
                "icao_Empresa_Aérea",
                "icao_Aeródromo_Destino" AS "AIRPORT",
                EXTRACT(YEAR FROM "PartidaReal") as "Ano"
            FROM vra as vt1
            UNION DISTINCT
            SELECT 
                "icao_Empresa_Aérea",
                "icao_Aeródromo_Destino" AS "AIRPORT",
                EXTRACT(YEAR FROM "PartidaReal") as "Ano"
            FROM vra as vt2
        ) SELECT 
            a.*, 
            COALESCE(p."Pousos",0) as "Pousos", 
            COALESCE(d."Decolagens", 0) AS "Decolagens",
            COALESCE(p."Pousos",0) + COALESCE(d."Decolagens",0) as "Total",
            ROW_NUMBER() OVER(PARTITION BY a."AIRPORT", a."Ano" ORDER BY COALESCE(p."Pousos",0) + COALESCE(d."Decolagens",0) desc) as "rank_total"
        FROM airports AS a
        LEFT JOIN pousos p 
            ON a."Ano" = p."Ano"
            AND a."COMPANY" = p."Companhia"
            AND a."AIRPORT" = p."Aeroporto Destino"
        LEFT JOIN decolagens d
        ON a."Ano" = d."Ano"
        AND a."COMPANY" = d."Companhia"
        AND a."AIRPORT" = d."Aeroporto Origem"
    ) SELECT * FROM ranking
    WHERE "rank_total" = 1
)