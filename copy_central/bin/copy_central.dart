import 'dart:io';
import 'package:yaml_edit/yaml_edit.dart';
import 'package:yaml/yaml.dart';
import 'package:path/path.dart' as path;

import 'env.dart';

const String version = '0.0.1';

void main(List<String> arguments) {
  const destinationPubspecPath = Env.destinationPubspecAbsolutePath;
  // absolute path

  // download central pubspec.yaml
  final result = Process.runSync(
    "sh",
    ["bin/run_download_central_pubspec.sh"],
  );
  print(result.stderr.toString());

  // load it into memory
  File centralPubspec = File(path.canonicalize("bin/central_pubspec.yaml"));
  final centralYaml = loadYaml(centralPubspec.readAsStringSync());

  // load destination pubspec.yaml into memory
  File destinationPubspec = File(destinationPubspecPath);
  final destinationYaml = loadYaml(destinationPubspec.readAsStringSync());

  // open destination pubspec.yaml for editing
  final destinationYamlEditor =
      YamlEditor(destinationPubspec.readAsStringSync());

  // update dependencies
  for (var key in destinationYaml["dependencies"].keys) {
    if (centralYaml["dependencies"].containsKey(key)) {
      destinationYamlEditor
          .update(["dependencies", key], centralYaml["dependencies"][key]);
    }
  }

  // update dev_dependencies
  for (var key in destinationYaml["dev_dependencies"].keys) {
    if (centralYaml["dev_dependencies"].containsKey(key)) {
      destinationYamlEditor.update(
          ["dev_dependencies", key], centralYaml["dev_dependencies"][key]);
    }
  }

  // update dependency_overrides
  for (var key in destinationYaml["dependency_overrides"].keys) {
    if (centralYaml["dependency_overrides"].containsKey(key)) {
      destinationYamlEditor.update(["dependency_overrides", key],
          centralYaml["dependency_overrides"][key]);
    }
  }

  // update environment
  for (var key in destinationYaml["environment"].keys) {
    if (centralYaml["environment"].containsKey(key)) {
      destinationYamlEditor
          .update(["environment", key], centralYaml["environment"][key]);
    }
  }

  // write updated yaml to destination
  File destinationPubspecUpdated = File(destinationPubspecPath);
  destinationPubspecUpdated.openWrite().write(destinationYamlEditor.toString());

  // delete the destination lock file
  // this is done in order to reduce the chances of caching
  final destinationLockFilePath = File(
      "${destinationPubspecPath.substring(0, destinationPubspecPath.length - 4)}.lock");
  if (destinationLockFilePath.existsSync()) {
    destinationLockFilePath.deleteSync();
  }
}
