# Copy Central

allows you to copy dependencies from central pubspec to any target pubspec.
It'll only update the versions for the dependencies you already have in target.

Note: It also deletes target pubspec.lock file in order to reduce the chances of caching.

## Setup

* `pip install pygithub`
* populate `bin/env.py`
* populate `bin/env.dart`

## Run

* `dart run bin/copy_central.dart`

Note: Script is supposed to be run from `copy_central` folder. If you're running it from a different location, please change the paths in `copy_central/bin/run_download_central_pubspec.sh` and `copy_central/bin/env.py`