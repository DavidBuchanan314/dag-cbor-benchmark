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

Results of `bench.py`, on Python 3.13.12, Fedora 42, 2021 M1 Pro MBP

Contestants:

- [DavidBuchanan314/dag-cbrrr](https://github.com/DavidBuchanan314/dag-cbrrr) (release v1.1.0)
- [MarshalX/python-libipld](https://github.com/MarshalX/python-libipld) (release v3.3.2)
- [hashberg-io/dag-cbor](https://github.com/hashberg-io/dag-cbor) (release v0.3.3)

```
Hello World Decode:
===================
cbrrr    : 213 ns
libipld  : 83 ns
dag_cbor : 6323 ns

Hello World Encode:
===================
cbrrr    : 107 ns
libipld  : 87 ns
dag_cbor : 7171 ns

Realistic Decode Tests:
=======================
canada.json.dagcbor            cbrrr    : 3.75 ms (268.85 MB/s)
canada.json.dagcbor            libipld  : 4.10 ms (245.97 MB/s)
canada.json.dagcbor            dag_cbor : 119.39 ms (8.44 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 2.29 ms (142.48 MB/s)
citm_catalog.json.dagcbor      libipld  : 2.26 ms (144.55 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 49.20 ms (6.64 MB/s)
twitter.json.dagcbor           cbrrr    : 1.29 ms (297.85 MB/s)
twitter.json.dagcbor           libipld  : 1.29 ms (297.99 MB/s)
twitter.json.dagcbor           dag_cbor : 20.90 ms (18.38 MB/s)

Realistic Encode Tests:
=======================
canada.json.dagcbor            cbrrr    : 1.10 ms (912.36 MB/s)
canada.json.dagcbor            libipld  : 0.97 ms (1035.73 MB/s)
canada.json.dagcbor            dag_cbor : 205.62 ms (4.90 MB/s)
citm_catalog.json.dagcbor      cbrrr    : 1.31 ms (249.47 MB/s)
citm_catalog.json.dagcbor      libipld  : 1.31 ms (248.73 MB/s)
citm_catalog.json.dagcbor      dag_cbor : 60.35 ms (5.41 MB/s)
twitter.json.dagcbor           cbrrr    : 0.64 ms (597.26 MB/s)
twitter.json.dagcbor           libipld  : 0.50 ms (771.94 MB/s)
twitter.json.dagcbor           dag_cbor : 23.05 ms (16.66 MB/s)

Decode Torture Tests:
=====================
torture_cids.dagcbor           cbrrr     22.1 ms (176.75 MB/s)
torture_cids.dagcbor           libipld   9.8 ms (399.89 MB/s)
torture_cids.dagcbor           dag_cbor  9637.9 ms (0.41 MB/s)
torture_nested_lists.dagcbor   cbrrr     717.6 ms (13.29 MB/s)
torture_nested_lists.dagcbor   libipld   ERROR: RecursionError: maximum recursion depth exceeded in DAG-CBOR decoding
torture_nested_lists.dagcbor   dag_cbor  ERROR: maximum recursion depth exceeded
torture_nested_maps.dagcbor    cbrrr     1315.4 ms (14.50 MB/s)
torture_nested_maps.dagcbor    libipld   ERROR: RecursionError: maximum recursion depth exceeded in DAG-CBOR decoding
torture_nested_maps.dagcbor    dag_cbor  ERROR: maximum recursion depth exceeded
```

Note: "maximum recursion depth exceeded" is an acceptable result for the recursion torture tests - a segfault isn't though :P
