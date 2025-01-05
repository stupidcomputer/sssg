{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = [
      ( pkgs.callPackage ./derivation.nix {} )
    ];
  }

