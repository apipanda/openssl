TAG ?= latest

# docker
REPO_NAME=bern
APP_NAME=sslme
DIRTY_FILES=$$(git status --porcelain --untracked-files=all)


run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		inform-builder;

build-image:
	docker build -t $(REPO_NAME)/$(APP_NAME):$(TAG) -f docker.run .;

build-image-nc:
	docker build --no-cache -t $(REPO_NAME)/$(APP_NAME):$(TAG) -f docker.run .;


tag: tag-latest tag-version

tag-latest:
	@echo 'create tag latest'
	docker tag $(REPO_NAME)/$(APP_NAME) $(REPO_NAME)/$(APP_NAME):latest

tag-version:
	@echo 'create tag $(TAG)'
	docker tag $(REPO_NAME)/$(APP_NAME) $(REPO_NAME)/$(APP_NAME):$(TAG)

# Docker publish
push-image: publish-latest publish-version

publish-latest: tag-latest
	@echo 'publish latest to $(REPO_NAME)'
	docker push $(DOCKER_REPO)/$(REPO_NAME)/$(APP_NAME):latest

publish-version: tag-version
	@echo 'publish $(TAG) to $(REPO_NAME)'
	docker push $(DOCKER_REPO)/$(REPO_NAME)/$(APP_NAME):$(TAG)

push:
	@for path in $(DIRTY_FILES); do \
		git add $$path; \
		git commit -sm "Update $$path"; \
	done; \
	git add .; \
	git commit -sm 'refactor codebase'; \
	git push origin master;
