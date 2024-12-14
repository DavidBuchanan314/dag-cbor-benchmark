#!/usr/bin/env ruby

require 'benchmark'

require 'cbor'  # https://github.com/cabo/cbor-ruby

DECODERS = {
  "cbor-ruby" => CBOR
}

ENCODERS = {
  "cbor-ruby" => CBOR
}

DATA_DIR = File.expand_path("../data", __dir__)

TESTCASES = Hash[Dir["#{DATA_DIR}/*.dagcbor"].sort.map { |f|
  [File.basename(f, '.dagcbor'), File.read(f, encoding: 'BINARY')]
}]

def run_test(title, mode, cases, iters: 1, unit: 'ns', show_mbps: false)
  puts
  puts "#{title}:"
  puts "=" * (title.length + 1)

  if cases.is_a?(String)
    cases = [cases]
    show_file_name = false
  elsif cases.is_a?(Array)
    show_file_name = true
  else
    raise "cases parameter should be an array"
  end

  method = mode

  cases.each do |test_name|
    data = TESTCASES[test_name]
    raise "Test not found: #{test_name.inspect}" unless data

    coders = (mode == :decode) ? DECODERS : ENCODERS

    coders.each do |lib_name, coder|
      test_label = show_file_name ? test_name.ljust(31) : ''
      lib_label = lib_name.ljust(coders.keys.map(&:length).max)

      begin
        if mode == :decode
          # give each impl a "clean slate", for maximum fairness
          GC.start

          time = Benchmark.realtime {
            iters.times { coder.decode(data) }
          }
        else
          decoded = DECODERS[lib_name].decode(data)
          GC.start

          time = Benchmark.realtime {
            iters.times { coder.encode(decoded) }
          }
        end

        time_per_iter = time / iters
        time_precision = (unit == 'ms') ? 2 : 0
        time_in_unit = time_per_iter * (10 ** (unit == 'ms' ? 3 : 9))
        formatted_time = sprintf("%.#{time_precision}f", time_in_unit) + ' ' + unit

        if show_mbps
          mbps = data.length * 1.0 / (1024 * 1024) / time_per_iter
          mb_speed = "(#{sprintf('%.2f', mbps)} MB/s)"
        else
          mb_speed = ""
        end

        puts "#{test_label}#{lib_label} : #{formatted_time} #{mb_speed}"
      rescue Exception => e
        puts "#{test_label}#{lib_label} : #{e.inspect}"
      end
    end
  end
end


HELLO_ITERS = 2_000_000

run_test("Hello World Decode", :decode, 'trivial_helloworld', iters: HELLO_ITERS)
run_test("Hello World Encode", :encode, 'trivial_helloworld', iters: HELLO_ITERS)

REALISTIC_ITERS = 100

realistic_tests = TESTCASES.keys.reject { |k| k.start_with?("torture_") || k.start_with?("trivial_") }

run_test("Realistic Decode Tests", :decode, realistic_tests, iters: REALISTIC_ITERS, unit: 'ms', show_mbps: true)
run_test("Realistic Encode Tests", :encode, realistic_tests, iters: REALISTIC_ITERS, unit: 'ms', show_mbps: true)

torture_tests = TESTCASES.keys.select { |k| k.start_with?("torture_") }

run_test("Decode Torture Tests", :decode, torture_tests, unit: 'ms', show_mbps: true)
