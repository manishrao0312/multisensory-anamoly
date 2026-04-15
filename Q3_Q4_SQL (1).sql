-- Q3

WITH plant_stats AS (
    SELECT
        Plant,
        AVG(Temperature) AS temp_mean,
        STDEV(Temperature) AS temp_std,
        AVG(Vibration) AS vib_mean,
        STDEV(Vibration) AS vib_std,
        AVG(Pressure) AS pres_mean,
        STDEV(Pressure) AS pres_std
    FROM sensor_data
    GROUP BY Plant
),
flagged AS (
    SELECT
        s.Timestamp,
        s.MachineID,
        s.Plant,
        CASE
            WHEN s.Temperature < p.temp_mean - 3 * p.temp_std
              OR s.Temperature > p.temp_mean + 3 * p.temp_std
              OR s.Vibration < p.vib_mean - 3 * p.vib_std
              OR s.Vibration > p.vib_mean + 3 * p.vib_std
              OR s.Pressure < p.pres_mean - 3 * p.pres_std
              OR s.Pressure > p.pres_mean + 3 * p.pres_std
            THEN 1 ELSE 0
        END AS is_anomaly
    FROM sensor_data s
    JOIN plant_stats p ON s.Plant = p.Plant
)
SELECT
    Plant,
    COUNT(*) AS total_records,
    SUM(is_anomaly) AS anomaly_count,
    ROUND(100.0 * SUM(is_anomaly) / COUNT(*), 2) AS anomaly_rate_pct
FROM flagged
GROUP BY Plant
ORDER BY anomaly_count DESC;

WITH plant_stats AS (
    SELECT
        Plant,
        AVG(Temperature) AS temp_mean,
        STDEV(Temperature) AS temp_std,
        AVG(Vibration) AS vib_mean,
        STDEV(Vibration) AS vib_std,
        AVG(Pressure) AS pres_mean,
        STDEV(Pressure) AS pres_std
    FROM sensor_data
    GROUP BY Plant
),
flagged AS (
    SELECT
        s.MachineID,
        s.Plant,
        CASE
            WHEN s.Temperature < p.temp_mean - 3*p.temp_std
              OR s.Temperature > p.temp_mean + 3*p.temp_std
              OR s.Vibration < p.vib_mean - 3*p.vib_std
              OR s.Vibration > p.vib_mean + 3*p.vib_std
              OR s.Pressure < p.pres_mean - 3*p.pres_std
              OR s.Pressure > p.pres_mean + 3*p.pres_std
            THEN 1 ELSE 0
        END AS is_anomaly
    FROM sensor_data s
    JOIN plant_stats p ON s.Plant = p.Plant
)
SELECT
    Plant,
    MachineID,
    COUNT(*) AS total_records,
    SUM(is_anomaly) AS anomaly_count,
    ROUND(100.0 * SUM(is_anomaly) / COUNT(*), 2) AS anomaly_rate_pct
FROM flagged
GROUP BY Plant, MachineID
ORDER BY anomaly_count DESC;


-- Q4

IF OBJECT_ID('dbo.sensor_condition_2025', 'V') IS NOT NULL
    DROP VIEW dbo.sensor_condition_2025;
GO

CREATE VIEW sensor_condition_2025 AS
WITH global_stats AS (
    SELECT
        AVG(Temperature) AS t_mean, STDEV(Temperature) AS t_std,
        AVG(Vibration) AS v_mean, STDEV(Vibration) AS v_std,
        AVG(Pressure) AS p_mean, STDEV(Pressure) AS p_std
    FROM sensor_data
),
machine_agg AS (
    SELECT
        s.MachineID,
        MAX(s.Plant) AS Plant,
        ROUND(AVG(s.Temperature), 4) AS AvgTemp,
        ROUND(AVG(s.Vibration), 4) AS AvgVib,
        ROUND(AVG(s.Pressure), 4) AS AvgPressure,
        ROUND(
            AVG(s.EnergyConsumption) /
            NULLIF(AVG(CAST(s.ProductionUnits AS FLOAT)), 0), 4
        ) AS AvgEnergyPerUnit,
        SUM(s.DefectCount) AS TotalDefects,
        SUM(s.MaintenanceFlag) AS MaintenanceCount,
        ROUND(AVG(
            0.40 * (s.Temperature - g.t_mean) / NULLIF(g.t_std, 0) +
            0.35 * (s.Vibration - g.v_mean) / NULLIF(g.v_std, 0) +
            0.25 * (s.Pressure - g.p_mean) / NULLIF(g.p_std, 0)
        ), 4) AS AvgConditionIndex
    FROM sensor_data s
    CROSS JOIN global_stats g
    GROUP BY s.MachineID
),
ranked AS (
    SELECT *,
        PERCENT_RANK() OVER (ORDER BY AvgConditionIndex DESC) AS pct_rank
    FROM machine_agg
)
SELECT
    MachineID,
    Plant,
    AvgTemp,
    AvgVib,
    AvgPressure,
    AvgEnergyPerUnit,
    TotalDefects,
    MaintenanceCount,
    AvgConditionIndex,
    CASE
        WHEN pct_rank <= 0.10 THEN 'Critical'
        WHEN pct_rank <= 0.30 THEN 'Warning'
        ELSE 'Normal'
    END AS ConditionBucket
FROM ranked;
GO