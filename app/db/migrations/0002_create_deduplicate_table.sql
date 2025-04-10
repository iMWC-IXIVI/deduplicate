CREATE TABLE IF NOT EXISTS original (
    id UUID,
    hash String,
    raw_data String,
    created DateTime
) ENGINE = MergeTree()
ORDER BY (hash, created)