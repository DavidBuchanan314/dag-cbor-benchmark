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
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (branch [add-encode-dag-cbor](https://github.com/MarshalX/python-libipld/pull/5) commit 9f53eaf1312db2b9bb56e73071a2ce3aef0f4581)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 261 ns
libipld  : 139 ns
dag_cbor : 4253 ns

Hello World Encode:
===================
cbrrr    : 132 ns
libipld  : 500 ns
dag_cbor : 5126 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.93 ms (256.33 MB/s)
canada.json.dagcbor            libipld  : 9.80 ms (102.78 MB/s)
canada.json.dagcbor            dag_cbor : 108.31 ms (9.30 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.44 ms (133.75 MB/s)
citm_catalog.json.dagcbor      libipld  : 6.99 ms (46.70 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 46.79 ms (6.98 MB/s)
twitter.json.dagcbor           cbrrr    : 1.39 ms (275.85 MB/s)
twitter.json.dagcbor           libipld  : 3.33 ms (115.27 MB/s)
twitter.json.dagcbor           dag_cbor : 19.40 ms (19.80 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.88 ms (1145.51 MB/s)
canada.json.dagcbor            libipld  : 45.64 ms (22.07 MB/s)
canada.json.dagcbor            dag_cbor : 230.52 ms (4.37 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.40 ms (232.80 MB/s)
citm_catalog.json.dagcbor      libipld  : 13.39 ms (24.39 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 63.61 ms (5.13 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (608.82 MB/s)
twitter.json.dagcbor           libipld  : 5.40 ms (71.19 MB/s)
twitter.json.dagcbor           dag_cbor : 24.25 ms (15.84 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     34.3 ms (114.07 MB/s)
torture_cids.dagcbor           libipld   32.8 ms (119.24 MB/s)
torture_cids.dagcbor           dag_cbor  7297.5 ms (0.54 MB/s)
torture_nested_lists.dagcbor   cbrrr     781.3 ms (12.21 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1269.2 ms (15.03 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
