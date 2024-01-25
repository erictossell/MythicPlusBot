{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication overrides;
      in
      {
        packages = {
          myapp = mkPoetryApplication { 
	    projectDir = self;
 	    overrides = overrides.withDefaults (self: super: {
	      dnspython = super.dnspython.overridePythonAttrs (
	        old: {
		  nativeBuildInputs = (old.nativeBuildInputs or []) ++ [
		    self.hatchling
		    ];
		}
	      );
	      asyncio = super.asyncio.overridePythonAttrs (
	        old: {
		  nativeBuildInputs = (old.nativeBuildInputs or []) ++ [
		    self.setuptools
		    ];
		}
	      );
	   });
	  };
          default = self.packages.${system}.myapp;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.myapp ];
          packages = [ pkgs.poetry pkgs.libgcc pkgs.libstdcxx5 ];
        };
      });
}
