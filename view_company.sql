
CREATE VIEW view_companies AS (
    WITH most_used_routes AS (
        WITH trips AS (
            SELECT
                vra."icao_Empresa_Aérea",
                vra."icao_Aeródromo_Origem",
                vra."icao_Aeródromo_Destino",
                count(*) as "trips"
            from vra
            group by 1,2,3
        )
        SELECT 
            "icao_Empresa_Aérea",
            "icao_Aeródromo_Origem",
            "icao_Aeródromo_Destino",
            "trips",
            ROW_NUMBER() OVER(PARTITION BY "icao_Empresa_Aérea" ORDER BY "trips" desc) as "rank_rota"
        FROM trips
    )
    SELECT 
        air_cia."Razão Social" as "Companhia_Aerea",
        ido."name" as "Aeroporto Origem",
        ido."id" as "ID Aeroporto Origem",
        ido."state" as "Estado de Origem",
        idd."name" as "Aeroporto Destino",
        idd."id" as "ID Aeroporto Destino",
        idd."state" as "Estado de Destino",
        mur."trips" as "Numero de Viajens"
    FROM most_used_routes AS mur
    INNER JOIN air_cia ON mur."icao_Empresa_Aérea" = air_cia."ICAO"
    INNER JOIN icao_data AS ido ON mur."icao_Aeródromo_Origem" = ido."ICAO"
    INNER JOIN icao_data AS idd ON mur."icao_Aeródromo_Destino" = idd."ICAO"
    WHERE "rank_rota"= 1
)