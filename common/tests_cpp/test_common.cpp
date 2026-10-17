#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <numeric>
#include <string>
#include <vector>

#include "ecv/common/bench.hpp"
#include "ecv/common/geometry.hpp"
#include "ecv/common/types.hpp"

#define CHECK(cond)                                                        \
  do {                                                                     \
    if (!(cond)) {                                                         \
      std::fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond); \
      std::exit(1);                                                        \
    }                                                                      \
  } while (0)

int main() {
  // JSON line matches the Python writer for the documented example
  ecv::FrameRecord r;
  r.frame = 1234;
  r.t_ns = 1739000000123456789LL;
  r.dets.push_back({"car", 0.91f, {412, 233, 520, 301}});
  ecv::Track t;
  t.id = 17;
  t.cls = "car";
  t.xyxy = {410, 231, 519, 300};
  t.ground_xy_m = std::array<double, 2>{12.4, 3.1};
  t.speed_kmh = 34.2;
  r.tracks.push_back(t);
  const std::string expect =
      "{\"frame\":1234,\"t_ns\":1739000000123456789,\"dets\":[{\"cls\":\"car\",\"score\":0.91,"
      "\"xyxy\":[412,233,520,301]}],\"tracks\":[{\"id\":17,\"cls\":\"car\","
      "\"xyxy\":[410,231,519,300],\"ground_xy_m\":[12.4,3.1],\"speed_kmh\":34.2}]}";
  CHECK(ecv::to_json_line(r) == expect);

  // Homography round trip
  ecv::Homography h;
  h.h = {0.02, 0.001, -3.0, 0.0005, 0.03, -5.0, 1e-5, 2e-4, 1.0};
  auto g = h.pixel_to_ground(640, 360);
  auto p = h.ground_to_pixel(g[0], g[1]);
  CHECK(std::fabs(p[0] - 640) < 1e-6 && std::fabs(p[1] - 360) < 1e-6);

  // Latency stats match numpy for 1..100
  std::vector<double> v(100);
  std::iota(v.begin(), v.end(), 1.0);
  auto s = ecv::latency_stats(v);
  CHECK(std::fabs(s.p50 - 50.5) < 1e-9 && std::fabs(s.p99 - 99.01) < 1e-9 && s.max == 100);

  std::puts("ok");
  return 0;
}
