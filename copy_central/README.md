# Copy Central

allows you to copy dependencies from central pubspec to any target pubspec.
It'll only update the versions for the dependencies you already have in target.

Note: It also deletes target pubspec.lock file in order to reduce the chances of caching.

## Setup

* `pip install pygithub`
* populate `bin/env.py`
* populate `bin/env.dart`

## Run

* `dart run copy_central/bin/copy_central.dart`
