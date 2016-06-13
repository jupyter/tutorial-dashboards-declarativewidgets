DOMAIN:=mybluemix.net
CF_API:=https://api.ng.bluemix.net
CF_ORG:=pparent@us.ibm.com

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pydata-reg.mybluemix.net: ## cf push the registration app to prod
	@cf target | grep -E 'API endpoint:[[:space:]]+$(CF_API)' || (echo "ERROR: not pointing at $(CF_API)"; exit 1)
	@cf target -o $(CF_ORG) -s production
	cf push pydata-reg

pydata-reg-dev.mybluemix.net: ## cf push the registration app to dev
	@cf target | grep -E 'API endpoint:[[:space:]]+$(CF_API)' || (echo "ERROR: not pointing at $(CF_API)"; exit 1)
	@cf target -o $(CF_ORG) -s dev
	cf push pydata-reg-dev
