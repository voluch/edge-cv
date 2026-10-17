#pragma once
#include <vector>

namespace ecv {

struct LatencyStats {
  double p50 = 0, p95 = 0, p99 = 0, mean = 0, max = 0;
};

// Percentiles use linear interpolation (same as numpy's default). Throws on empty input.
LatencyStats latency_stats(std::vector<double> latencies_ms);

}  // namespace ecv
