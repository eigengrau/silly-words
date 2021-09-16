{ pkgs }:
pkgs.python38Packages.buildPythonPackage {
  pname = "silly-words";
  version = "0.1.0.0";
  propagatedBuildInputs = (with pkgs.python38Packages; [ pyparsing nltk ]);
  src = ../.;
}
