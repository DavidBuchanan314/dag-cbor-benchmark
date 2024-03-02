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
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v1.2.2)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 208 ns
libipld  : 149 ns
dag_cbor : 4408 ns

Hello World Encode:
===================
cbrrr    : 137 ns
libipld  : 136 ns
dag_cbor : 5164 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.99 ms (252.65 MB/s)
canada.json.dagcbor            libipld  : 5.97 ms (168.67 MB/s)
canada.json.dagcbor            dag_cbor : 109.49 ms (9.20 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.48 ms (131.63 MB/s)
citm_catalog.json.dagcbor      libipld  : 4.03 ms (80.99 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 47.18 ms (6.92 MB/s)
twitter.json.dagcbor           cbrrr    : 1.40 ms (274.81 MB/s)
twitter.json.dagcbor           libipld  : 2.27 ms (169.52 MB/s)
twitter.json.dagcbor           dag_cbor : 19.82 ms (19.38 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 0.88 ms (1138.76 MB/s)
canada.json.dagcbor            libipld  : 1.78 ms (566.43 MB/s)
canada.json.dagcbor            dag_cbor : 231.38 ms (4.35 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.38 ms (237.35 MB/s)
citm_catalog.json.dagcbor      libipld  : 2.31 ms (141.30 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 65.75 ms (4.97 MB/s)
twitter.json.dagcbor           cbrrr    : 0.63 ms (607.27 MB/s)
twitter.json.dagcbor           libipld  : 0.87 ms (439.38 MB/s)
twitter.json.dagcbor           dag_cbor : 25.18 ms (15.26 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     31.6 ms (123.87 MB/s)
torture_cids.dagcbor           libipld   28.4 ms (137.66 MB/s)
torture_cids.dagcbor           dag_cbor  7419.9 ms (0.53 MB/s)
torture_nested_lists.dagcbor   cbrrr     771.0 ms (12.37 MB/s)
torture_nested_lists.dagcbor   libipld   SEGFAULT
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1244.3 ms (15.33 MB/s)
torture_nested_maps.dagcbor    libipld   SEGFAULT
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
