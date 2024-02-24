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
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v1.1.1) (Decode only)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 211 ns
libipld  : 131 ns
dag_cbor : 4270 ns

Hello World Encode:
===================
cbrrr    : 136 ns
dag_cbor : 5180 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.89 ms (258.64 MB/s)
canada.json.dagcbor            libipld  : 9.69 ms (104.00 MB/s)
canada.json.dagcbor            dag_cbor : 110.79 ms (9.09 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.46 ms (132.49 MB/s)
citm_catalog.json.dagcbor      libipld  : 7.09 ms (46.03 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 47.39 ms (6.89 MB/s)
twitter.json.dagcbor           cbrrr    : 1.41 ms (272.57 MB/s)
twitter.json.dagcbor           libipld  : 3.41 ms (112.50 MB/s)
twitter.json.dagcbor           dag_cbor : 19.81 ms (19.39 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.89 ms (1131.48 MB/s)
canada.json.dagcbor            dag_cbor : 231.86 ms (4.34 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.35 ms (241.93 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 64.86 ms (5.03 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (609.05 MB/s)
twitter.json.dagcbor           dag_cbor : 24.77 ms (15.51 MB/s)

Decode Torture Tests:
=====================
torture_nested_lists.dagcbor   cbrrr     770.4 ms (12.38 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1279.7 ms (14.90 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
torture_cids.dagcbor           cbrrr     30.7 ms (127.17 MB/s)
torture_cids.dagcbor           libipld   36.6 ms (106.76 MB/s)
torture_cids.dagcbor           dag_cbor  7359.7 ms (0.53 MB/s)
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
