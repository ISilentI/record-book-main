.PHONY: connect
connect:
	docker-compose exec backend bash

.PHONY: logs
logs:
	docker logs --follow record-book-backend-1

.DEFAULT_GOAL :=
