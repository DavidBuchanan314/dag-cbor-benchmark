# dag-cbor-benchmark
Test data for benchmarking dag-cbor decoders and encoders

The following test cases came from https://github.com/serde-rs/json-benchmark, converted from JSON to DAG-CBOR. They're very "real world", but don't contain any CBOR-specific data types (bytes, CIDs).

```
data/canada.json.dagcbor         1_056_200 bytes  - many lists of floats
data/citm_catalog.json.dagcbor     342_373 bytes  - moderately nested objects, including unicode strings
data/twitter.json.dagcbor          402_814 btyes  - ditto
```

Trivial test cases:

```
data/trivial_helloworld.dagcbor     14 bytes  - A hello world string (sanity check and/or test constant overheads)
```

Synthetic torture tests:

```
data/torture_nested_lists.dagcbor  10_000_001 bytes  - 10M nested lists
data/torture_nested_maps.dagcbor   20_000_001 bytes  - 10M nested maps (each with empty-string keys)
data/torture_cids.dagcbor           4_100_005 btyes  - 100K CIDs (in a flat list)
```

TODO: gather some more real-world DAG-CBOR from bluesky, ideally anonymised (maybe just the MST blocks?)

TODO: include CAR test cases


## Python shootout:

Resutlts of `bench.py`, on Python 3.12.1, Fedora 39, 2021 M1 Pro MBP

Contestants:

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (commit 2f4171e9136f022fd5beb288c767591d57e513c6)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v1.1.0) (Decode only) (NOTE: There's an improved `fix-perf` branch that I haven't tested yet)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 210 ns
libipld  : 454 ns
dag_cbor : 4227 ns

Hello World Encode:
===================
cbrrr    : 135 ns
dag_cbor : 5063 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.73 ms (269.80 MB/s)
canada.json.dagcbor            libipld  : 26.95 ms (37.38 MB/s)
canada.json.dagcbor            dag_cbor : 106.04 ms (9.50 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.44 ms (133.77 MB/s)
citm_catalog.json.dagcbor      libipld  : 17.08 ms (19.12 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 45.63 ms (7.16 MB/s)
twitter.json.dagcbor           cbrrr    : 1.35 ms (284.89 MB/s)
twitter.json.dagcbor           libipld  : 10.83 ms (35.48 MB/s)
twitter.json.dagcbor           dag_cbor : 18.94 ms (20.28 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.91 ms (1109.95 MB/s)
canada.json.dagcbor            dag_cbor : 232.15 ms (4.34 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.38 ms (236.92 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 64.69 ms (5.05 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (605.39 MB/s)
twitter.json.dagcbor           dag_cbor : 24.99 ms (15.37 MB/s)

Decode Torture Tests:
=====================
torture_nested_lists.dagcbor   cbrrr     771.4 ms (12.36 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1274.0 ms (14.97 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
torture_cids.dagcbor           cbrrr     40.4 ms (96.67 MB/s)
torture_cids.dagcbor           libipld   68.5 ms (57.08 MB/s)
torture_cids.dagcbor           dag_cbor  7399.3 ms (0.53 MB/s)
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
