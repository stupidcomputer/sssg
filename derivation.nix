{ python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "sssg-py";
  version = "1.0";

  propagatedBuildInputs = [ markdown jinja2 watchdog ];

  src = ./.;
}
