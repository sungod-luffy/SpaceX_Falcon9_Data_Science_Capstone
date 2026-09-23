-- SQL analysis queries for SpaceX launches

-- First 20 records
SELECT * FROM spacex_launches LIMIT 20;

-- Minimum payload mass
SELECT MIN(payload_mass_kg) FROM spacex_launches;

-- Total payload mass
SELECT SUM(payload_mass_kg) FROM spacex_launches;

-- Mission outcome counts
SELECT class, COUNT(*) as count FROM spacex_launches GROUP BY class;

-- Launch site counts
SELECT launch_site, COUNT(*) as count FROM spacex_launches GROUP BY launch_site ORDER BY count DESC;
