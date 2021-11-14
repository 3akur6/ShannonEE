# ShannonEE

A dynamic analysis environment for Samsung's Shannon baseband fully inspired by [grant-h/ShannonEE](https://github.com/grant-h/ShannonEE).

* use [avatar2](https://github.com/avatartwo/avatar2) to emulate peripherals (still need more prototypes)
* use [pandare](https://github.com/panda-re/panda) to create ARM-cortex-r7 runtime (patches required), plug in hooks and register callbacks 
* distribute logs into different parts for advanced analysis


## Requirements

* [avatar2](https://github.com/avatartwo/avatar2)
* [pandare](https://github.com/panda-re/panda) with patches
* static analysis tool, e.g. IDA, ghidra (strongly recommended with [ShannonLoader plugin](https://github.com/grant-h/ShannonBaseband/tree/master/reversing/ghidra/ShannonLoader))

You can also build image from [Dockerfile](./Dockerfile) to kick off quickly.

`docker build -t shannon-ee -f ./Dockerfile .`


## Usage

1. Statically analyze modem firmware to locate boot entry point (default: 0x40000000)
2. Parse firmware segments and export BOOT seg and MAIN seg to current working directory (use [ShannonLoader](https://github.com/grant-h/ShannonBaseband/tree/master/reversing/ghidra/ShannonLoader) with less pain)
3. Define:
    * segments to tell ShannonEE how to arrange memory
    * callbacks to monitor specified cpu or memory behaviors
    * hooks to hook instruction area, getting immediate register value
    * patches to directly modify memory
4. Create a instance of ShannonEE passed with segments (callbacks, hooks, patches are optional) definition
5. Execute then analyze detailed logs to add more patches and peripherals
6. Repeat step 5

Example can be found in [main.py](./main.py)

TRY HARD and KEEP PATIENT to make firmware run.


## Artifacts

Blackhat USA 2020 Talk - https://www.blackhat.com/us-20/briefings/schedule/index.html#emulating-samsungs-baseband-for-security-testing-20564
