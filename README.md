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

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (release v1.0.0)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v2.0.0)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 264 ns
libipld  : 130 ns
dag_cbor : 4239 ns

Hello World Encode:
===================
cbrrr    : 133 ns
libipld  : 98 ns
dag_cbor : 5086 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.96 ms (254.65 MB/s)
canada.json.dagcbor            libipld  : 4.15 ms (242.86 MB/s)
canada.json.dagcbor            dag_cbor : 108.44 ms (9.29 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.44 ms (133.67 MB/s)
citm_catalog.json.dagcbor      libipld  : 3.06 ms (106.64 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 46.36 ms (7.04 MB/s)
twitter.json.dagcbor           cbrrr    : 1.38 ms (277.45 MB/s)
twitter.json.dagcbor           libipld  : 1.75 ms (219.49 MB/s)
twitter.json.dagcbor           dag_cbor : 19.38 ms (19.82 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.88 ms (1149.58 MB/s)
canada.json.dagcbor            libipld  : 1.00 ms (1004.89 MB/s)
canada.json.dagcbor            dag_cbor : 228.99 ms (4.40 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.36 ms (240.80 MB/s)
citm_catalog.json.dagcbor      libipld  : 1.41 ms (231.18 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 64.53 ms (5.06 MB/s)
twitter.json.dagcbor           cbrrr    : 0.62 ms (614.70 MB/s)
twitter.json.dagcbor           libipld  : 0.54 ms (715.02 MB/s)
twitter.json.dagcbor           dag_cbor : 24.20 ms (15.88 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     30.8 ms (126.83 MB/s)
torture_cids.dagcbor           libipld   19.4 ms (201.47 MB/s)
torture_cids.dagcbor           dag_cbor  7174.4 ms (0.55 MB/s)
torture_encode_quadratic_buffer_copy.dagcbor cbrrr     3.6 ms (266.22 MB/s)
torture_encode_quadratic_buffer_copy.dagcbor libipld   2.6 ms (363.33 MB/s)
torture_encode_quadratic_buffer_copy.dagcbor dag_cbor  7.9 ms (120.20 MB/s)
torture_nested_lists.dagcbor   cbrrr     812.9 ms (11.73 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1328.3 ms (14.36 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
