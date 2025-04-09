CREATE TABLE IF NOT EXISTS migrations (
    id UUID,
    name_migration String,
    time_migration DateTime
) ENGINE = MergeTree()
ORDER BY time_migration;