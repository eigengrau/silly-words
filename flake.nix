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
        packages = { silly-words = pkgs.silly-words; };
        defaultPackage = packages.silly-words;
        defaultApp = {
          type = "app";
          program = "${packages.silly-words}/bin/silly-words";
        };
      }));
}
