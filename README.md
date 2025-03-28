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

Resutlts of `bench.py`, on Python 3.12.9, Fedora 40, 2021 M1 Pro MBP

Contestants:

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (release v1.0.1)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v3.0.1)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 193 ns
libipld  : 122 ns
dag_cbor : 3936 ns

Hello World Encode:
===================
cbrrr    : 124 ns
libipld  : 109 ns
dag_cbor : 4564 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.87 ms (259.96 MB/s)
canada.json.dagcbor            libipld  : 4.26 ms (236.40 MB/s)
canada.json.dagcbor            dag_cbor : 100.44 ms (10.03 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.41 ms (135.31 MB/s)
citm_catalog.json.dagcbor      libipld  : 2.97 ms (109.81 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 43.82 ms (7.45 MB/s)
twitter.json.dagcbor           cbrrr    : 1.37 ms (279.79 MB/s)
twitter.json.dagcbor           libipld  : 1.64 ms (234.64 MB/s)
twitter.json.dagcbor           dag_cbor : 18.42 ms (20.85 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.80 ms (1259.39 MB/s)
canada.json.dagcbor            libipld  : 2.62 ms (383.93 MB/s)
canada.json.dagcbor            dag_cbor : 208.59 ms (4.83 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.31 ms (248.68 MB/s)
citm_catalog.json.dagcbor      libipld  : 1.61 ms (202.47 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 59.15 ms (5.52 MB/s)
twitter.json.dagcbor           cbrrr    : 0.61 ms (626.25 MB/s)
twitter.json.dagcbor           libipld  : 0.63 ms (612.57 MB/s)
twitter.json.dagcbor           dag_cbor : 22.95 ms (16.74 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     30.4 ms (128.43 MB/s)
torture_cids.dagcbor           libipld   20.4 ms (191.30 MB/s)
torture_cids.dagcbor           dag_cbor  6988.5 ms (0.56 MB/s)
torture_nested_lists.dagcbor   cbrrr     747.4 ms (12.76 MB/s)
torture_nested_lists.dagcbor   libipld   ERROR: RecursionError: maximum recursion depth exceeded in DAG-CBOR decoding
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1207.0 ms (15.80 MB/s)
torture_nested_maps.dagcbor    libipld   ERROR: RecursionError: maximum recursion depth exceeded in DAG-CBOR decoding
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
