# dag-cbor-benchmark
Test data for benchmarking dag-cbor decoders and encoders

The following test cases came from https://github.com/serde-rs/json-benchmark, converted from JSON to DAG-CBOR:

```
data/canada.json.dagcbor         1056200 bytes  - many lists of floats
data/citm_catalog.json.dagcbor    342373 bytes  - moderately nested objects, including unicode strings
data/twitter.json.dagcbor         402814 btyes  - ditto
```
