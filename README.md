# Cloudbuildify

Cloudbuildify is an integration tool that connects [Bitbucket](http://bitbucket.org) with [Unity Cloud Build](https://unity3d.com/unity/features/cloud-build) based on [Flask](http://flask.pocoo.org). When a new pull request is created a new build target is automatically created in UCB.

## Configuration

Cloudbuildify is configured with ENV variables.

| Variable | Description |
| --- | --- |
| CLOUDBUILD_API_KEY | Cloud Build API key that you can find in your profile |
| CLOUDBUILD_WEBHOOK_SECRET | Random string included in Cloud Build webhook URL |
| CLOUDBUILD_ORG_ID | Organization ID (for Cloud Build API) |
| CLOUDBUILD_PROJECT_ID | Project ID (for Cloud Build API) |
| CLOUDBUILD_TEMPLATE_BUILD_TARGET | `buildtargetid` field from [Buildtargets list response](https://build-api.cloud.unity3d.com/docs/1.0.0/index.html#operation--orgs--orgid--projects--projectid--buildtargets-get) |
| BITBUCKET_USER | Username that will be used for Bitbucket API |
| BITBUCKET_PASSWORD | Password, use App Passwords for this one |
| BITBUCKET_WEBHOOK_SECRET | Random string included in Bitbucket webhook URL |
| BITBUCKET_ORG_ID | Organization ID (for Bitbucket API) |
| BITBUCKET_PROJECT_ID | Project ID (for Bitbucket API) |

## Structure

Cloudbuildify consists of several modules:

- `bitbucket` - Code for Bitbucket API.
- `cloudbuild` - Code for Unity Cloud Build API.
- `config` - Loading configuration variables.
- `persistence` - Simple Active Record to save Build Target data into the SQLite database.
- `webhooks` - Flask routes for webhooks.
