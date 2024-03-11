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
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v1.2.3)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 215 ns
libipld  : 138 ns
dag_cbor : 4271 ns

Hello World Encode:
===================
cbrrr    : 139 ns
libipld  : 133 ns
dag_cbor : 5299 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 4.08 ms (246.97 MB/s)
canada.json.dagcbor            libipld  : 5.23 ms (192.48 MB/s)
canada.json.dagcbor            dag_cbor : 111.30 ms (9.05 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.48 ms (131.45 MB/s)
citm_catalog.json.dagcbor      libipld  : 3.65 ms (89.54 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 47.63 ms (6.85 MB/s)
twitter.json.dagcbor           cbrrr    : 1.42 ms (271.47 MB/s)
twitter.json.dagcbor           libipld  : 2.11 ms (182.39 MB/s)
twitter.json.dagcbor           dag_cbor : 19.79 ms (19.41 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.91 ms (1107.29 MB/s)
canada.json.dagcbor            libipld  : 1.34 ms (754.27 MB/s)
canada.json.dagcbor            dag_cbor : 232.05 ms (4.34 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.37 ms (239.11 MB/s)
citm_catalog.json.dagcbor      libipld  : 1.55 ms (211.13 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 65.35 ms (5.00 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (609.71 MB/s)
twitter.json.dagcbor           libipld  : 0.76 ms (506.77 MB/s)
twitter.json.dagcbor           dag_cbor : 25.06 ms (15.33 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     53.3 ms (73.38 MB/s)
torture_cids.dagcbor           libipld   37.0 ms (105.65 MB/s)
torture_cids.dagcbor           dag_cbor  7570.8 ms (0.52 MB/s)
torture_nested_lists.dagcbor   cbrrr     818.0 ms (11.66 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1275.4 ms (14.96 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
