# Just Programmer's Manual: https://just.systems/man/en/
# Just Cheat Sheet: https://cheatography.com/linux-china/cheat-sheets/justfile/

env_list := "3.9 3.10 3.11 3.12 3.13"

default:
    just --list

# Run tests with all supported interpreters
test_all:
    for version in {{env_list}}; \
    do \
        uv run --isolated --frozen --python $version --extra dev pytest --doctest-modules src/; \
    done

# Clean the temporary files.
clean:
    #!/usr/bin/env bash
    rm -rf .index-demo
    rm -rf .index-analyzer
