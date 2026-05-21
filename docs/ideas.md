https://github.com/tiangolo/full-stack-fastapi-postgresql
ZomboDb
Postgraphile
Patroni
JHipster (Dockerization etc)
Entando


Include node-red as a default
invenio software
automatic HTTPS : https://github.com/tiangolo/full-stack

Be sure to add
FAB_API_SHOW_STACKTRACE = True
FAB_API_SWAGGER_UI = True
to config.py
Create a config.py editor view

## Other stuff to do
# 0. Refactor view generation into a class in another file
# 0. Rationalize imports
# 0. Generate MasterDetail Views
# 0. Generate ChartViews
# 0. Generate Reports
# 0. REST API
# 0. GraphQL Interface
# 0. Generate code from dbml, sql, ponyORM scripts
# 0. Generate code from existing database
# 0. Generate React, Vue, Angular, Express front ends
# 0. AWS Cognito Integration
# 0. Add a Dockerfile for deployment
# 0. Include Elasticsearch for search
# 0. Include Whoosh for search
# 0. Add an Idea editor file to config the editor view
# 1. Move the files automatically to the right place
# 2. Add an FSM generator page (libero, FSME)
# 3. Spell and grammar check all text areas
# 4. Indicate the characters at the bottom of every text area
# 5. Lookups need to be fixed
# 6. Image and upload fields
# 7. make this into a publishable thing
# 9. Add this a FAB extension or Cookie-cutter template
# 10. Automatically generate test coverage



## Big Things to do
# 1. Generate database seeding scripts
# 2. Generate JHipster code
# 3. Generate components for different field types, Set datetime to calendar, etc
# 4. Generate a mobile app (beeware or Kivy)
# 5. Generate a desktop app
# 6. Produce reports on every table, join table, 3-way table set
# 7. Deploy to aws, gcp
# 8. Create a database design tool (dbdesign.io? or pony-orm or a desktop?
# 9. Automatically Generate database structure and content documentation
# 10. Data Model Library for an ERP


## Docker Deployment
# 0. Deploy and create a postgresqldb
# 0. Deploy to k8s
# 0. Deploy Elasticsearch
# 0. Create Terraform to deploy to GCP, AWS, Azure
# 0. Create both Postgresql and Mysql DBs
# 0.

# DBScript Ideas (extend dbdiagram language)
# 0. Add Field Groups, so that large tables can be better organized (perhaps braced in a table definition)
# 0. Field groups can be used like mixins and added to any table
# 0. Include Array types in the language
# 0. Permit specification of Row Level Security
# 0. Specify derived fields and hidden fields that are not generated
# 0. .

- Duplicate the erdiagram language
- Create an erDiagram editor
- Add a chatbot that can do basic functions by asking for each field  in view
- Add a state charts component that can
- create workflows and authorisation flows
- Implement Row Level Security for each user. Sync users with the postgresql database users
- Auto logout if there has been no activity for a set time
- More intelligent graphing and reporting,. Export reports to pdf and mail them.
- Create a configuration and setup screen for everything in config.py
- Tabbed views with permissions per tab. Extend the permissions system

# Management tasks:
* Autobackup