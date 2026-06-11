CREATE OR REPLACE FUNCTION check_channel_subscribers_limit()
RETURNS TRIGGER AS $$
DECLARE
	max_subscribers INT := 1000;  -- ← твой лимит N
	current_count INT;
BEGIN
	-- Считаем текущее количество подписчиков канала
	SELECT COUNT(*) INTO current_count
	FROM channel_subscriber 
	WHERE channel_id = NEW.channel_id;

	IF current_count >= max_subscribers THEN
		RAISE EXCEPTION 'Channel % has reached the maximum number of subscribers (%)', 
			NEW.channel_id, max_subscribers;
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Создаём триггер
CREATE TRIGGER trigger_channel_subscribers_limit
BEFORE INSERT ON channel_subscriber
FOR EACH ROW
EXECUTE FUNCTION check_channel_subscribers_limit();