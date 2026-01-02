{
  description = "Python3 dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};

        python = pkgs.python3;
        pythonEnv = python.withPackages (
          ps:
            with ps; [
              discordpy
              python-dotenv
            ]
        );
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
          ];

          shellHook = ''
            echo "🐍 Python Discord bot dev shell"
            echo "Python: $(python --version)"
          '';
        };
      }
    );
}
