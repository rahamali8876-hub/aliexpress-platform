📘 Man Page: run_tests
RUN_TESTS(1)                  Developer Tools                  RUN_TESTS(1)

NAME

run_tests – marker-based automated test runner for domain-driven systems

SYNOPSIS
run_tests.sh MARKER [DOMAIN]

DESCRIPTION

run_tests.sh executes pytest test suites using marker-based filtering.

It supports:

unit tests

integration tests

saga tests

contract tests

chaos tests

full test execution

Tests can be run:

across all domains

or scoped to a single domain

This design enables:

fast local development

selective CI pipelines

scalable microservice testing

ARGUMENTS

MARKER
One of:

unit

integration

contract

saga

chaos

all

DOMAIN (optional)
Restrict test execution to a single domain
(e.g. products, orders, payments).

BEHAVIOR

If MARKER=all, all tests are executed.

Otherwise, pytest is invoked with -m <marker>.

Script exits immediately on failure.

EXAMPLES

Run all unit tests:

./scripts/run_tests.sh unit


Run integration tests for products:

./scripts/run_tests.sh integration products


Run saga tests across all domains:

./scripts/run_tests.sh saga


Run all tests:

./scripts/run_tests.sh all

EXIT STATUS

0 – all tests passed

>0 – pytest failure

ENVIRONMENT

Relies on:

pytest

valid pytest.ini markers configuration

SEE ALSO

create_domain(1), pytest(1)

AliExpress Clone Architecture Toolkit

🔧 Optional: Install as Real Man Pages
sudo cp man/create_domain.1 /usr/local/share/man/man1/
sudo cp man/run_tests.1 /usr/local/share/man/man1/
sudo mandb


Then:

man create_domain
man run_tests


This is real UNIX-level polish.