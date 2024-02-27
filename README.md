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

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (release v0.0.1)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v1.2.1)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 273 ns
libipld  : 175 ns
dag_cbor : 4214 ns

Hello World Encode:
===================
cbrrr    : 162 ns
libipld  : 150 ns
dag_cbor : 5052 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.81 ms (264.31 MB/s)
canada.json.dagcbor            libipld  : 5.81 ms (173.32 MB/s)
canada.json.dagcbor            dag_cbor : 111.47 ms (9.04 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.35 ms (138.79 MB/s)
citm_catalog.json.dagcbor      libipld  : 3.68 ms (88.71 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 48.06 ms (6.79 MB/s)
twitter.json.dagcbor           cbrrr    : 1.37 ms (280.97 MB/s)
twitter.json.dagcbor           libipld  : 2.04 ms (187.95 MB/s)
twitter.json.dagcbor           dag_cbor : 20.21 ms (19.01 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.80 ms (1256.85 MB/s)
canada.json.dagcbor            libipld  : 1.66 ms (606.11 MB/s)
canada.json.dagcbor            dag_cbor : 228.18 ms (4.41 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.36 ms (240.84 MB/s)
citm_catalog.json.dagcbor      libipld  : 3.22 ms (101.55 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 65.17 ms (5.01 MB/s)
twitter.json.dagcbor           cbrrr    : 0.61 ms (630.62 MB/s)
twitter.json.dagcbor           libipld  : 1.55 ms (247.37 MB/s)
twitter.json.dagcbor           dag_cbor : 24.85 ms (15.46 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     32.2 ms (121.47 MB/s)
torture_cids.dagcbor           libipld   32.9 ms (118.94 MB/s)
torture_cids.dagcbor           dag_cbor  7135.1 ms (0.55 MB/s)
torture_nested_lists.dagcbor   cbrrr     747.7 ms (12.75 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1219.0 ms (15.65 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
