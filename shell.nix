{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = [
      pkgs.python3
      pkgs.python311Packages.markdown
      pkgs.python311Packages.jinja2
      pkgs.python311Packages.watchdog
    ];
  }

