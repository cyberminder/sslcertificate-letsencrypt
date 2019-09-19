#!/usr/bin/env bash
pylint --rcfile=pylint.cfg $(find . -maxdepth 4 -name "*.py" -print) --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint.log
