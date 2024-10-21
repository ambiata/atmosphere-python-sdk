$env:python_packages="atmosphere"

isort --check-only --verbose $env:python_packages
$env:EXIT_STATUS=$LASTEXITCODE
pylint $env:python_packages
$env:EXIT_STATUS=$LASTEXITCODE

exit $env:EXIT_STATUS
