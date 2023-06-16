# Servey Stub

This project uses code generation to build python libraries containing service stubs for servey services.
The objective is to allow multiple services to coordinate without having details of whether the code for 
other services...

* Is in the same python container
* Is based on AWS lambda
* Is accessed via http

### Rationale

A lot of people have strong opinions on the Microservice vs Monolith debate, and the technologies involved mean
we frequently end up with the downsides of both and the benefits of neither. This project is an attempt to reign in
the chaos, at least in the context of [servey](https://github.org/tofarr/servey) projects.

Ideally, I want to be in a position where I can host and test with minimal configuration and external dependencies,
while still being able to take advantage of a microservice architecture in a production environment. It would be nice
to not have to run a server for each microservice when in a local development environment, but instead to be able
to rely on pre-built stubs.

I generally dislike code generation as a practice, but in this case using code generation means we can take advantage
of code completion available in most modern IDEs.

I think the best practice is still to layer projects, with higher layers have stubs only for the projects in layers 
below them. (rather than a self referencing free for all)

## Installation

`pip install servey-stub`

## Usage

All commands should be run in the project directory for your servey project.

* `--name` parameters specifies the name of the output project / module (Defaults to the current SERVEY_MAIN
  environment variable).
* `--dir` specifies the output directory in which the generated project directory should be placed (Defaults to ./dist)
* Any action which has a web trigger will be stubbed. (Since it indicates that the action can be invoked externally).
  Actions can be limited by name with `--only`, or excluded with `--exclude`

## Lambda

Generates / Updates a service stub project directory for invoking actions as AWS lambdas, and places it in the specified 
output directory.

`python -m servey_stub --mode=lambdas`

Yields: `/servey_stub/my-service-lambdas/...`

## HTTP

Generates / Updates a service stub project directory for invoking actions over http, and places it in the specified 
output directory.

`python -m servey_stub --mode=http --server_url=https://foo.com/bar`

Yields: `/servey_stub/my-service-http/...`

TODO: We need to support some sort of authentication / authorization here (Probably oauth). These will need to be from
the enviroment.
e.g.: --headers=val:foo:bar,env:foo:bar

Passing authentication may present an issue - will need to encode - and if we encode, we need a key which the client
respects.

## Mock

Generates a service stub for invoking actions as mocks, and places it in the specified output directory. The mocks are
based on definitions in the servey actions.

`python -m servey_stub --mode=mock`

Yields: `/servey_stub/my-service-mock/...`

## Example

## Release Procedure

![status](https://github.com/tofarr/servey-stub/actions/workflows/quality.yml/badge.svg?branch=main)

The typical process here is:
* Create a PR with changes. Merge these to main (The `Quality` workflows make sure that your PR
  meets the styling, linting, and code coverage standards).
* New releases created in github are automatically uploaded to pypi
