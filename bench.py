import os
import time
import timeit
from typing import Dict
from multiprocessing import Process, Queue

# our contestants:
import cbrrr     # https://github.com/DavidBuchanan314/dag-cbrrr
import libipld   # https://github.com/MarshalX/python-libipld
import dag_cbor  # https://github.com/hashberg-io/dag-cbor

decoders = {
	"cbrrr": cbrrr.decode_dag_cbor,
	"libipld": libipld.decode_dag_cbor,
	"dag_cbor": dag_cbor.decode,
}

encoders = {
	"cbrrr": cbrrr.encode_dag_cbor,
	# libipld does not support encoding
	"dag_cbor": dag_cbor.encode,
}

DATA_DIR = "./data/"

testcases: Dict[str, bytes] = {}

for testcase in os.listdir(DATA_DIR):
	data = open(DATA_DIR + testcase, "rb").read()
	testcases[testcase] = data

print()
print("Hello World Decode:")
print("===================")
HELLO_ITERS = 100000
for name, decodefn in decoders.items():
	res = timeit.timeit(lambda: decodefn(testcases["trivial_helloworld.dagcbor"]), number=HELLO_ITERS)
	ns_per_it = (res / HELLO_ITERS) * 1000 * 1000 * 1000
	print(f"{name:<9}: {ns_per_it:.0f} ns")

print()
print("Hello World Encode:")
print("===================")
HELLO_ITERS = 100000
for name, encodefn in encoders.items():
	decoded = decoders[name](testcases["trivial_helloworld.dagcbor"])
	res = timeit.timeit(lambda: encodefn(decoded), number=HELLO_ITERS)
	ns_per_it = (res / HELLO_ITERS) * 1000 * 1000 * 1000
	print(f"{name:<9}: {ns_per_it:.0f} ns")

print()
print("Realistic Decode Tests:")
print("=======================")
REALISTIC_ITERS = 25
for testname, testcase in testcases.items():
	if testname.startswith("torture_") or testname.startswith("trivial_"):
		continue
	for decodername, decodefn in decoders.items():
		res = timeit.timeit(lambda: decodefn(testcase), number=REALISTIC_ITERS)
		res /= REALISTIC_ITERS
		ms_per_it = res * 1000
		mbps = len(testcase)/1024/1024/res
		print(f"{testname:<30} {decodername:<9}: {ms_per_it:.2f} ms ({mbps:.2f} MB/s)")

print()
print("Realistic Encode Tests:")
print("=======================")
REALISTIC_ITERS = 25
for testname, testcase in testcases.items():
	if testname.startswith("torture_") or testname.startswith("trivial_"):
		continue
	for encodername, encodefn in encoders.items():
		decoded = decoders[encodername](testcase)
		res = timeit.timeit(lambda: encodefn(decoded), number=REALISTIC_ITERS)
		res /= REALISTIC_ITERS
		ms_per_it = res * 1000
		mbps = len(testcase)/1024/1024/res
		print(f"{testname:<30} {encodername:<9}: {ms_per_it:.2f} ms ({mbps:.2f} MB/s)")

print()
print("Decode Torture Tests:")
print("=====================")
for testname, testcase in testcases.items():
	if not testname.startswith("torture_"):
		continue
	for decodername, decodefn in decoders.items():
		q = Queue()
		def run_and_except():
			try:
				decodefn(testcase)
				q.put("success")
			except Exception as e:
				q.put(str(e))
		p = Process(target=run_and_except)
		start = time.time()
		p.start()
		p.join()
		duration = time.time() - start
		if p.exitcode:
			print(testname.ljust(30, " "), decodername.ljust(9, " "), "SEGFAULT" if p.exitcode == -11 else "ERROR")
			continue

		res = q.get()
		if res == "success":
			duration_ms = duration * 1000
			mbps = len(testcase)/1024/1024/duration
			print(testname.ljust(30, " "), decodername.ljust(9, " "), f"{duration_ms:.1f} ms ({mbps:.2f} MB/s)")
		else:
			print(testname.ljust(30, " "), decodername.ljust(9, " "), "ERROR:", res)
