APP_NAME=app.app:app
CONFIGURATION_SETUP=app.core.settings.DevelopmentConfig
CONFIG_PATH?=fixtures_v1.yaml

load-fixtures:
	docker exec -it backend-ferp sh -c " \
		export CONFIGURATION_SETUP=$(CONFIGURATION_SETUP) \
		&& export FLASK_APP=$(APP_NAME) \
		&& flask fixtures load-fixtures $(CONFIG_PATH) \
	"
