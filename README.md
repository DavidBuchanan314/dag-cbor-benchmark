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

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (commit c6cff1dfe26c5937cd1c8a5b90b1e5973a90dbd3)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (["fix-perf" branch](https://github.com/MarshalX/python-libipld/pull/4), commit bc8d081c39f1f9c9c3436f6d7d926ac1202ed319 ) (Decode only)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 205 ns
libipld  : 127 ns
dag_cbor : 4274 ns

Hello World Encode:
===================
cbrrr    : 134 ns
dag_cbor : 5284 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.83 ms (262.76 MB/s)
canada.json.dagcbor            libipld  : 9.75 ms (103.30 MB/s)
canada.json.dagcbor            dag_cbor : 111.43 ms (9.04 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.44 ms (133.56 MB/s)
citm_catalog.json.dagcbor      libipld  : 7.04 ms (46.38 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 47.70 ms (6.85 MB/s)
twitter.json.dagcbor           cbrrr    : 1.33 ms (288.03 MB/s)
twitter.json.dagcbor           libipld  : 3.50 ms (109.83 MB/s)
twitter.json.dagcbor           dag_cbor : 19.26 ms (19.95 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.86 ms (1169.91 MB/s)
canada.json.dagcbor            dag_cbor : 227.10 ms (4.44 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.33 ms (245.83 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 64.46 ms (5.06 MB/s)
twitter.json.dagcbor           cbrrr    : 0.64 ms (599.85 MB/s)
twitter.json.dagcbor           dag_cbor : 24.63 ms (15.60 MB/s)

Decode Torture Tests:
=====================
torture_nested_lists.dagcbor   cbrrr     770.8 ms (12.37 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1230.9 ms (15.50 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
torture_cids.dagcbor           cbrrr     40.1 ms (97.42 MB/s)
torture_cids.dagcbor           libipld   36.0 ms (108.67 MB/s)
torture_cids.dagcbor           dag_cbor  7404.3 ms (0.53 MB/s)
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
