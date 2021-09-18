{ python3Packages }:
python3Packages.buildPythonPackage {
  pname = "silly-words";
  version = "0.1.0.0";
  propagatedBuildInputs = (with python3Packages; [ pyparsing nltk ]);
  src = ../.;
}
