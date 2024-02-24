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
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (["fix-perf" branch](https://github.com/MarshalX/python-libipld/pull/4), commit b04d673b61312d421d0ec89f95bea6e944f1835b ) (Decode only)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 203 ns
libipld  : 204 ns
dag_cbor : 4236 ns

Hello World Encode:
===================
cbrrr    : 133 ns
dag_cbor : 5073 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.76 ms (268.09 MB/s)
canada.json.dagcbor            libipld  : 12.87 ms (78.29 MB/s)
canada.json.dagcbor            dag_cbor : 107.26 ms (9.39 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.82 ms (115.64 MB/s)
citm_catalog.json.dagcbor      libipld  : 13.38 ms (24.41 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 46.54 ms (7.02 MB/s)
twitter.json.dagcbor           cbrrr    : 1.35 ms (284.93 MB/s)
twitter.json.dagcbor           libipld  : 4.91 ms (78.26 MB/s)
twitter.json.dagcbor           dag_cbor : 19.39 ms (19.81 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.90 ms (1113.08 MB/s)
canada.json.dagcbor            dag_cbor : 227.89 ms (4.42 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.36 ms (239.94 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 64.55 ms (5.06 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (612.68 MB/s)
twitter.json.dagcbor           dag_cbor : 24.60 ms (15.61 MB/s)

Decode Torture Tests:
=====================
torture_nested_lists.dagcbor   cbrrr     760.5 ms (12.54 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1274.0 ms (14.97 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
torture_cids.dagcbor           cbrrr     31.4 ms (124.64 MB/s)
torture_cids.dagcbor           libipld   4.0 ms (982.15 MB/s)
torture_cids.dagcbor           dag_cbor  7350.3 ms (0.53 MB/s)
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
