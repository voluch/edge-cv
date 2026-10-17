#include "ecv/common/bench.hpp"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <stdexcept>

namespace ecv {
namespace {

double percentile(const std::vector<double>& sorted, double p) {
  const double pos = p / 100.0 * static_cast<double>(sorted.size() - 1);
  const auto lo = static_cast<std::size_t>(std::floor(pos));
  const auto hi = static_cast<std::size_t>(std::ceil(pos));
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - static_cast<double>(lo));
}

}  // namespace

LatencyStats latency_stats(std::vector<double> v) {
  if (v.empty()) throw std::invalid_argument("no latencies given");
  std::sort(v.begin(), v.end());
  LatencyStats s;
  s.p50 = percentile(v, 50);
  s.p95 = percentile(v, 95);
  s.p99 = percentile(v, 99);
  s.mean = std::accumulate(v.begin(), v.end(), 0.0) / static_cast<double>(v.size());
  s.max = v.back();
  return s;
}

}  // namespace ecv
