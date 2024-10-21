$env:python_packages="atmosphere"

# Remove unused imports
autoflake "--ignore-init-module-imports" "--in-place" "-r" "--remove-all-unused-imports" "$env:python_packages"
# Sort imports one per line, so autoflake can remove unused imports
autopep8 --in-place --aggressive --aggressive --recursive $env:python_packages
isort --force-single-line-imports $env:python_packages
# --exclude=__init__.py
black $env:python_packages
isort $env:python_packages
