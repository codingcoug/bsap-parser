# Bro Analyzer Files
 
## Installation ##
In order to integrate with Bro, you have to compile your own Bro and integrate these files before compilation.
- in [init-default.bro](bro/bro-src/scripts/base/init-default.bro), add the line `@load base/protocols/bsap`
- in [CMakeLists.txt](bro/bro-src/src/analyzer/protocol/CMakeLists.txt), add the line `add_subdirectory(bsap)`
- Make the two symlinks, ensuring that the links point with an absolute reference:
 * in [bro-src/scripts/base/protocols](bro/bro-src/scripts/base/protocols): bsap -> [base](bro/base)
 * in [bro-src/src/analyzer/protocol](bro/bro-src/src/analyzer/protocol): bsap -> [analyzer](bro/analyzer)

## Usage ##
Everything is integrated with Bro and started dynamically using [dpd](https://www.bro.org/development/howtos/dpd.html). Bro will detect BSAP traffic (following [dpd.sig](bro/base/dpd.sig)) and start the analyzer as needed.

## Modifying ##
If installed following these instructions, you should be able to edit the scripts in your [base](bro/base/) directory and restart Bro (with `broctl restart`). Any edits to the [analyzer](bro/analyzer) directory require recompiling Bro.
