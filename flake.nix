{
  description = "silly-words";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-21.05";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }:
    (utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            (final: prev: {
              silly-words = final.callPackage ./nix/silly-words.nix { };
            })
          ];
        };
      in rec {
        packages = rec {
          default = silly-words;
          silly-words = pkgs.silly-words;
        };
        apps = {
          default = {
            type = "app";
            program = "${packages.silly-words}/bin/silly-words";
          };
        };
      }));
}
